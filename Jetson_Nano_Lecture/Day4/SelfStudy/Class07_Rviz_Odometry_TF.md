# Class 07: Rviz, Odometry, TF 실습

## 1. Rviz (ROS Visualization)

### 1.1 Rviz 개념

Rviz는 ROS용 3D 시각화 도구입니다. 센서 데이터, 로봇 모델, 맵 등을 실시간으로 시각화합니다.

### 1.2 Rviz 주요 Displays

```
Rviz Displays:
┌─────────────────────────────────────┐
│ Displays                            │
│ ├─ Global Options                   │
│ │   ├─ Fixed Frame: base_footprint │
│ │   └─ Background Color            │
│ ├─ RobotModel                       │
│ ├─ TF                               │
│ ├─ Grid                             │
│ ├─ LaserScan                        │
│ ├─ PointCloud                       │
│ ├─ Image                            │
│ ├─ Map                              │
│ ├─ Path                             │
│ ├─ Odometry                         │
│ └─ PoseArray                        │
└─────────────────────────────────────┘
```

### 1.3 Rviz 설정 저장

```xml
<!-- ~/.rviz/default.rviz -->
<rviz config version="0.1">
  <Tools>
    - Class: rviz/Interact
    - Class: rviz/MoveCamera
    - Class: rviz/Select
  </Tools>

  <Displays>
    - Class: rviz/Grid
      Reference Frame: base_footprint
      Name: Grid

    - Class: rviz/RobotModel
      Name: Robot Model
      Robot Description: robot_description

    - Class: rviz/TF
      Name: TF
      Frame Timeout: 15
  </Displays>
</rviz>
```

### 1.4 Rvizlaunch 파일

```xml
<!-- launch/rviz.launch -->
<launch>
  <node name="rviz" pkg="rviz" type="rviz" args="-d $(find my_robot)/config/robot.rviz"/>
</launch>
```

## 2. Odometry (里程计)

### 2.1 Odometry 개념

Odometry는-wheel 인코더 데이터를 기반으로 로봇의 위치와 방향을 추정합니다.

### 2.2 Odometry 메시지

```msg
# nav_msgs/Odometry
std_msgs/Header header
string child_frame_id
geometry_msgs/PoseWithCovariance pose
  geometry_msgs/Pose pose
    geometry_msgs/Point position
      float64 x
      float64 y
      float64 z
    geometry_msgs/Quaternion orientation
      float64 x
      float64 y
      float64 z
      float64 w
  float64[36] covariance
geometry_msgs/TwistWithCovariance twist
  geometry_msgs/Twist twist
  float64[36] covariance
```

### 2.3 Odometry 계산

```python
#!/usr/bin/env python3
import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import TransformStamped
import tf.transformations as transformations
import math

class OdometryCalculator:
    def __init__(self):
        rospy.init_node('odometry_calculator')

        # 초기 위치
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0

        # 이전encodervalues
        self.prev_left_enc = 0
        self.prev_right_enc = 0

        # 파라미터
        self.wheel_radius = rospy.get_param('~wheel_radius', 0.05)
        self.wheel_separation = rospy.get_param('~wheel_separation', 0.2)

        # Publisher
        self.odom_pub = rospy.Publisher('/odom', Odometry, queue_size=10)

        # TF Broadcaster
        self.tf_broadcaster = tf.TransformBroadcaster()

        self.rate = rospy.Rate(30)

    def calculate_odometry(self, left_enc, right_enc):
        """Encodervalues에서 Odometry 계산"""
        # 차분 계산
        d_left = left_enc - self.prev_left_enc
        d_right = right_enc - self.prev_right_enc

        # 이동 거리
        d_center = (d_left + d_right) / 2.0 * self.wheel_radius

        # 회전 각도
        d_theta = (d_right - d_left) * self.wheel_radius / self.wheel_separation

        # 위치 업데이트
        self.x += d_center * math.cos(self.theta + d_theta / 2.0)
        self.y += d_center * math.sin(self.theta + d_theta / 2.0)
        self.theta += d_theta

        # 이전 encodervalues 업데이트
        self.prev_left_enc = left_enc
        self.prev_right_enc = right_enc

        return self.x, self.y, self.theta

    def publish_odometry(self, x, y, theta):
        """Odometry 메시지 Publishing"""
        # Quaternion 생성
        q = transformations.quaternion_from_euler(0, 0, theta)

        # Odometry 메시지
        odom = Odometry()
        odom.header.stamp = rospy.Time.now()
        odom.header.frame_id = 'odom'
        odom.child_frame_id = 'base_link'

        odom.pose.pose.position.x = x
        odom.pose.pose.position.y = y
        odom.pose.pose.position.z = 0.0
        odom.pose.pose.orientation.x = q[0]
        odom.pose.pose.orientation.y = q[1]
        odom.pose.pose.orientation.z = q[2]
        odom.pose.pose.orientation.w = q[3]

        # Publishing
        self.odom_pub.publish(odom)

        # TF Publishing
        t = TransformStamped()
        t.header.stamp = rospy.Time.now()
        t.header.frame_id = 'odom'
        t.child_frame_id = 'base_link'
        t.transform.translation.x = x
        t.transform.translation.y = y
        t.transform.translation.z = 0.0
        t.transform.rotation.x = q[0]
        t.transform.rotation.y = q[1]
        t.transform.rotation.z = q[2]
        t.transform.rotation.w = q[3]

        self.tf_broadcaster.sendTransform(t)

    def run(self):
        while not rospy.is_shutdown():
            # 실제 구현에서는 encoder 데이터Subscribe 필요
            # 예시 데이터
            left_enc = 0
            right_enc = 0

            x, y, theta = self.calculate_odometry(left_enc, right_enc)
            self.publish_odometry(x, y, theta)

            self.rate.sleep()

if __name__ == '__main__':
    try:
        calc = OdometryCalculator()
        calc.run()
    except rospy.ROSInterruptException:
        pass
```

## 3. TF (Transform)

### 3.1 TF 개념

TF는 좌표계 사이의 변환을 관리합니다. 부모-자식 관계로 구성됩니다.

### 3.2 좌표계 계층

```
TF Tree:
┌─────────────────────────────────────┐
│           map                       │
│        ┌──────┴──────┐             │
│     odom             map            │
│    ┌───┴───┐                     │
│  base_link                      │
│  ┌─┴──┬─┴──┐                  │
│ laser camera                 │
└─────────────────────────────────────┘
```

### 3.3 TF 메시지

```msg
# tf2_msgs/TFMessage
transforms:
  - header:
      stamp:
        sec: 1234567890
        nanosec: 0
      frame_id: "odom"
      child_frame_id: "base_link"
    transform:
      translation:
        x: 0.0
        y: 0.0
        z: 0.0
      rotation:
        x: 0.0
        y: 0.0
        z: 0.0
        w: 1.0
```

### 3.4 TF 사용 예시

```python
#!/usr/bin/env python3
import rospy
import tf
import tf.transformations as transformations
import math

class TFBroadcaster:
    def __init__(self):
        self.tf_broadcaster = tf.TransformBroadcaster()
        self.tf_listener = tf.TransformListener()

    def broadcast_static_transform(self):
        """정적 변환 Broadcasting"""
        # Laser 스캐너 위치
        translation = (0.15, 0.0, 0.1)
        rotation = transformations.quaternion_from_euler(0, 0, 0)

        self.tf_broadcaster.sendTransform(
            translation,
            rotation,
            rospy.Time.now(),
            'laser_link',
            'base_link'
        )

    def lookup_transform(self):
        """변환 조회"""
        try:
            # base_link에서 laser_link로의 변환
            trans, rot = self.tf_listener.lookupTransform(
                '/base_link',
                '/laser_link',
                rospy.Time(0)
            )
            rospy.loginfo(f"Transform: trans={trans}, rot={rot}")
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            pass

    def run(self):
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            self.broadcast_static_transform()
            rate.sleep()

if __name__ == '__main__':
    rospy.init_node('tf_broadcaster_node')
    broadcaster = TFBroadcaster()
    broadcaster.run()
```

## 4. TF 사용实战

### 4.1 URDF에서 TF

```xml
<!-- URDF joint 정의가 자동으로 TF 생성 -->
<joint name="laser_joint" type="fixed">
  <parent link="base_link"/>
  <child link="laser_link"/>
  <origin xyz="0.15 0 0.1" rpy="0 0 0"/>
</joint>
```

### 4.2 Rviz에서 TF 확인

```bash
# Rviz에서 확인
# Displays > TF > Frames에서 확인
# - 모든 프레임 표시 여부
# - frame 속도
```

### 4.3 TF 디버깅

```bash
# TF 트리 확인
rosrun tf tf_echo /base_link /laser_link

# TF 트리 시각화
rosrun tf view_frames

# TF 정보
rosrun tf monitor /base_link /laser_link
```

## 5. Odometry + TF 통합

### 5.1 전체 시스템

```python
class RobotLocalization:
    def __init__(self):
        rospy.init_node('robot_localization')

        # Odometry Publisher
        self.odom_pub = rospy.Publisher('/odom', Odometry, queue_size=10)

        # TF Broadcaster
        self.tf_broadcaster = tf.TransformBroadcaster()

        # 초깃값
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0

        # Subscriber
        rospy.Subscriber('/wheel_encoder', Float64MultiArray, self.encoder_callback)

        self.rate = rospy.Rate(30)

    def encoder_callback(self, msg):
        """Encodervalues 처리"""
        # Odometry 계산
        # TF Publishing
        pass

    def run(self):
        while not rospy.is_shutdown():
            self.rate.sleep()

if __name__ == '__main__':
    RobotLocalization()
```

### 5.2 Launch 파일

```xml
<launch>
  <!-- Odometry 노드 -->
  <node name="odometry_publisher" pkg="my_robot" type="odometry_node.py" output="screen"/>

  <!-- TF 실행 -->
  <node name="robot_state_publisher" pkg="robot_state_publisher" type="robot_state_publisher"/>

  <!-- RViz -->
  <node name="rviz" pkg="rviz" type="rviz" args="-d $(find my_robot)/config/localization.rviz"/>
</launch>
```

## 6. 실습 과제

1. Odometry 메시지를 Publish하는 노드를 작성하세요.
2. TF 변환을 Broadcasting하는 노드를 작성하세요.
3. Rviz에서 Odometry와 TF를 확인하세요.
4. URDF에서 정의된joint를 기반으로 TF가 올바르게 생성되는지 확인하세요.

## 7. 다음 실습 예고

다음 클래스에서는 모터 구동 실습을 진행합니다.