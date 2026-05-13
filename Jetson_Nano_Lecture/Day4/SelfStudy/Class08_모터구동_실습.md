# Class 08: 모터 구동 실습

## 1. 모터 드라이버 basics

### 1.1 모터 드라이버 유형

```
모터 드라이버:
┌─────────────────────────────────────┐
│           DC 모터                   │
│  - L298N (H-Bridge)                │
│  - L293D                           │
│  - DRV8833                         │
│  - BTS7960 (고전력)                │
├─────────────────────────────────────┤
│           Servo 모터                │
│  - PWM 제어                        │
│  - 각도 지정                       │
├─────────────────────────────────────┤
│           BLDC 모터                 │
│  - Electronic Speed Controller     │
│  - 다상 PWM                        │
└─────────────────────────────────────┘
```

### 1.2 Jetson GPIO

```python
import RPi.GPIO as GPIO

# GPIO 번호 설정
GPIO.setmode(GPIO.BOARD)  # 물리 핀 번호
# 또는
GPIO.setmode(GPIO.BCM)    # Broadcom 번호

# 핀 설정
GPIO.setup(11, GPIO.OUT)  # 출력
GPIO.setup(12, GPIO.IN)   # 입력
```

## 2. Differential Drive 모델

### 2.1 Kinematics

```
Differential Drive Kinematics:
┌─────────────────────────────────────┐
│ v = (v_right + v_left) / 2         │
│ ω = (v_right - v_left) / L         │
│                                     │
│ v_right = v + ω * L / 2            │
│ v_left = v - ω * L / 2             │
└─────────────────────────────────────┘

L: 바퀴 간 거리
v: 선속도
ω: 각속도
```

### 2.2 속도 계산

```python
def diff_drive_inverse(v, omega, L):
    """선속도/각속도에서 개별 바퀴 속도 계산"""
    v_right = v + omega * L / 2
    v_left = v - omega * L / 2
    return v_left, v_right

def diff_drive_forward(v_left, v_right, L):
    """개별 바퀴 속도에서 선속도/각속도 계산"""
    v = (v_right + v_left) / 2
    omega = (v_right - v_left) / L
    return v, omega
```

## 3. 모터 제어 노드

### 3.1 기본 Motor Driver

```python
#!/usr/bin/env python3
# motor_driver.py
import rospy
import RPi.GPIO as GPIO
from geometry_msgs.msg import Twist

class MotorDriver:
    def __init__(self):
        rospy.init_node('motor_driver')

        # GPIO 핀 설정
        self.PIN_LEFT_EN = 12
        self.PIN_LEFT_IN1 = 11
        self.PIN_LEFT_IN2 = 13

        self.PIN_RIGHT_EN = 18
        self.PIN_RIGHT_IN1 = 16
        self.PIN_RIGHT_IN2 = 15

        # GPIO 초기화
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup([self.PIN_LEFT_EN, self.PIN_LEFT_IN1, self.PIN_LEFT_IN2,
                    self.PIN_RIGHT_EN, self.PIN_RIGHT_IN1, self.PIN_RIGHT_IN2],
                   GPIO.OUT)

        # PWM 초기화
        self.left_pwm = GPIO.PWM(self.PIN_LEFT_EN, 1000)
        self.right_pwm = GPIO.PWM(self.PIN_RIGHT_EN, 1000)
        self.left_pwm.start(0)
        self.right_pwm.start(0)

        # 파라미터
        self.wheel_separation = rospy.get_param('~wheel_separation', 0.2)
        self.wheel_radius = rospy.get_param('~wheel_radius', 0.05)
        self.max_speed = rospy.get_param('~max_speed', 1.0)

        # Subscriber
        rospy.Subscriber('/cmd_vel', Twist, self.cmd_callback)

        rospy.loginfo("Motor driver initialized")

    def cmd_callback(self, msg):
        """cmd_vel 메시지 처리"""
        linear = msg.linear.x
        angular = msg.angular.z

        # 속도 제한
        linear = max(-self.max_speed, min(self.max_speed, linear))
        angular = max(-self.max_speed, min(self.max_speed, angular))

        # Differential Drive 계산
        v_right = (linear + angular * self.wheel_separation / 2) / self.wheel_radius
        v_left = (linear - angular * self.wheel_separation / 2) / self.wheel_radius

        # PWM로 속도 제어
        self.set_motor_speed(v_left, v_right)

    def set_motor_speed(self, v_left, v_right):
        """모터 속도 설정"""
        # 왼쪽 모터
        if v_left > 0:
            GPIO.output(self.PIN_LEFT_IN1, True)
            GPIO.output(self.PIN_LEFT_IN2, False)
        else:
            GPIO.output(self.PIN_LEFT_IN1, False)
            GPIO.output(self.PIN_LEFT_IN2, True)

        self.left_pwm.ChangeDutyCycle(min(100, abs(v_left) * 100))

        # 오른쪽 모터
        if v_right > 0:
            GPIO.output(self.PIN_RIGHT_IN1, True)
            GPIO.output(self.PIN_RIGHT_IN2, False)
        else:
            GPIO.output(self.PIN_RIGHT_IN1, False)
            GPIO.output(self.PIN_RIGHT_IN2, True)

        self.right_pwm.ChangeDutyCycle(min(100, abs(v_right) * 100))

    def stop(self):
        """모터 정지"""
        self.left_pwm.ChangeDutyCycle(0)
        self.right_pwm.ChangeDutyCycle(0)

    def cleanup(self):
        """정리"""
        self.stop()
        self.left_pwm.stop()
        self.right_pwm.stop()
        GPIO.cleanup()

    def run(self):
        rospy.spin()

if __name__ == '__main__':
    try:
        driver = MotorDriver()
        driver.run()
    except rospy.ROSInterruptException:
        pass
    finally:
        driver.cleanup()
```

### 3.2 Odometry 포함 버전

```python
#!/usr/bin/env python3
# motor_driver_with_odom.py
import rospy
import RPi.GPIO as GPIO
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import tf.transformations as transformations
import math

class MotorDriverWithOdometry:
    def __init__(self):
        rospy.init_node('motor_driver')

        # GPIO 설정 (이전과 동일)
        # ...

        # Odometry
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        self.prev_left_enc = 0
        self.prev_right_enc = 0

        self.odom_pub = rospy.Publisher('/odom', Odometry, queue_size=10)
        self.tf_broadcaster = tf.TransformBroadcaster()

        rospy.Subscriber('/cmd_vel', Twist, self.cmd_callback)

        self.rate = rospy.Rate(30)

    def cmd_callback(self, msg):
        # 속도 계산 및 모터 제어
        pass

    def update_odometry(self, left_enc, right_enc):
        """Odometry 업데이트"""
        d_left = left_enc - self.prev_left_enc
        d_right = right_enc - self.prev_right_enc

        d_center = (d_left + d_right) / 2 * self.wheel_radius
        d_theta = (d_right - d_left) * self.wheel_radius / self.wheel_separation

        self.x += d_center * math.cos(self.theta + d_theta / 2)
        self.y += d_center * math.sin(self.theta + d_theta / 2)
        self.theta += d_theta

        self.prev_left_enc = left_enc
        self.prev_right_enc = right_enc

    def publish_odometry(self):
        """Odometry Publishing"""
        odom = Odometry()
        odom.header.stamp = rospy.Time.now()
        odom.header.frame_id = 'odom'
        odom.child_frame_id = 'base_link'

        odom.pose.pose.position.x = self.x
        odom.pose.pose.position.y = self.y

        q = transformations.quaternion_from_euler(0, 0, self.theta)
        odom.pose.pose.orientation.x = q[0]
        odom.pose.pose.orientation.y = q[1]
        odom.pose.pose.orientation.z = q[2]
        odom.pose.pose.orientation.w = q[3]

        self.odom_pub.publish(odom)

        # TF Publishing
        t = TransformStamped()
        t.header.stamp = rospy.Time.now()
        t.header.frame_id = 'odom'
        t.child_frame_id = 'base_link'
        t.transform.translation.x = self.x
        t.transform.translation.y = self.y
        t.transform.rotation.x = q[0]
        t.transform.rotation.y = q[1]
        t.transform.rotation.z = q[2]
        t.transform.rotation.w = q[3]

        self.tf_broadcaster.sendTransform(t)

    def run(self):
        while not rospy.is_shutdown():
            self.publish_odometry()
            self.rate.sleep()

if __name__ == '__main__':
    try:
        driver = MotorDriverWithOdometry()
        driver.run()
    except rospy.ROSInterruptException:
        pass
```

## 4. Launch 파일

```xml
<launch>
  <param name="wheel_separation" value="0.2"/>
  <param name="wheel_radius" value="0.05"/>
  <param name="max_speed" value="1.0"/>

  <node name="motor_driver" pkg="my_robot" type="motor_driver.py" output="screen">
    <remap from="/cmd_vel" to="/mobile_base/cmd_vel"/>
  </node>

  <node name="robot_state_publisher" pkg="robot_state_publisher" type="robot_state_publisher"/>

  <node name="rviz" pkg="rviz" type="rviz" args="-d $(find my_robot)/config/motor_test.rviz"/>
</launch>
```

## 5. 테스트

### 5.1命令行 테스트

```bash
# 전진
rostopic pub /cmd_vel geometry_msgs/Twist "{linear: {x: 0.2, y: 0, z: 0}, angular: {x: 0, y: 0, z: 0}}" -r 10

# 회전
rostopic pub /cmd_vel geometry_msgs/Twist "{linear: {x: 0, y: 0, z: 0}, angular: {x: 0, y: 0, z: 0.5}}" -r 10

# 정지
rostopic pub /cmd_vel geometry_msgs/Twist "{linear: {x: 0, y: 0, z: 0}, angular: {x: 0, y: 0, z: 0}}"
```

### 5.2键盘 控制

```bash
# teleop_twist_keyboard 설치
sudo apt install ros-noetic-teleop-twist-keyboard

# 실행
rosrun teleop_twist_keyboard teleop_twist_keyboard.py
```

### 5.3 rqt_plot으로 확인

```bash
# Odometry 확인
rqt_plot /odom/pose/pose/position/x:y
rqt_plot /odom/twist/twist/linear/x
```

## 6. 실습 과제

1. 모터 드라이버 노드를 작성하고 실행하세요.
2. cmd_vel 메시지로 로봇을 이동시켜보세요.
3. Odometry를 Publishing하고 rviz에서 확인하세요.
4. KeyboardTeleop을 사용하여 원격으로 제어하세요.

## 7. 다음 실습 예고

다음 Day5에서는 SLAM과 Navigation에 대해 학습합니다.