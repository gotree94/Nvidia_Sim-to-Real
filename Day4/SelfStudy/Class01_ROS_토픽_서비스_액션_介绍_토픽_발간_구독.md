# Class 01: ROS 토픽 서비스 액션 소개 및 토픽 발간 구독 실습

## 1. ROS 통신 유형 개요

### 1.1 통신 방식 비교

```
ROS Communication Types:
┌─────────────────────────────────────┐
│            Topics                   │
│    - 비동기, 연속 데이터 스트림     │
│    - Publisher/Subscriber 모델     │
│    - 다대다 통신                   │
├─────────────────────────────────────┤
│            Services                 │
│    - 동기식, 요청-응답 모델         │
│    - RPC 스타일                    │
│    - 일대일 통신                   │
├─────────────────────────────────────┤
│            Actions                  │
│    - 비동기, 목표-결과 모델         │
│    - 피드백 포함                   │
│    - 긴 작업에 적합                │
└─────────────────────────────────────┘
```

### 1.2 Topic vs Service vs Action

| 구분 | Topic | Service | Action |
|------|-------|---------|--------|
| 통신방식 | 비동기 | 동기 | 비동기 |
| 응답 | 없음 | 단일 응답 | 피드백+결과 |
| 사용예 | 센서 데이터 | 설정 변경 | 이동 명령 |
|频率 | 높음 | 낮음 | 중간 |

## 2. ROS Topics

### 2.1 Topic 개념

Topics는 연속적인 데이터 흐름에 사용됩니다. Publisher가 데이터를 보내면 Subscriber가 받는 구조입니다.

### 2.2 표준 토픽

```bash
# 주요 표준 토픽
/cmd_vel          # 속도 명령 (geometry_msgs/Twist)
/odom             #里程计 (nav_msgs/Odometry)
/scan             # 라이다 스캔 (sensor_msgs/LaserScan)
/image_raw        # 카메라 이미지 (sensor_msgs/Image)
/battery_state    # 배터리 상태 (sensor_msgs/BatteryState)
/tf               # 좌표계 변환 (tf2_msgs/TFMessage)
```

### 2.3 토픽 메시지 유형

```msg
# geometry_msgs/Twist
geometry_msgs/Vector3 linear
geometry_msgs/Vector3 angular

# sensor_msgs/LaserScan
std_msgs/Header header
float32 angle_min
float32 angle_max
float32 angle_increment
float32 time_increment
float32 scan_time
float32 range_min
float32 range_max
float32[] ranges
float32[] intensities

# nav_msgs/Odometry
std_msgs/Header header
geometry_msgs/PoseWithCovariance pose
geometry_msgs/TwistWithCovariance twist
```

## 3. 토픽 발간 (Publisher)

### 3.1 Python Publisher

```python
#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import String

class SimplePublisher:
    def __init__(self):
        # 토픽Publisher 초기화
        self.cmd_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.string_pub = rospy.Publisher('/chatter', String, queue_size=10)

        # 노드 초기화
        rospy.init_node('simple_publisher', anonymous=True)
        self.rate = rospy.Rate(10)  # 10Hz

    def publish_twist(self, linear_x=0, angular_z=0):
        """Twist 메시지 발간"""
        msg = Twist()
        msg.linear.x = linear_x
        msg.linear.y = 0.0
        msg.linear.z = 0.0
        msg.angular.x = 0.0
        msg.angular.y = 0.0
        msg.angular.z = angular_z

        self.cmd_pub.publish(msg)
        rospy.loginfo(f"Published: linear={linear_x}, angular={angular_z}")

    def publish_string(self, message):
        """String 메시지 발간"""
        msg = String()
        msg.data = message
        self.string_pub.publish(msg)
        rospy.loginfo(f"Published: {message}")

    def run(self):
        """실행 루프"""
        while not rospy.is_shutdown():
            self.publish_twist(0.5, 0.0)  # 0.5m/s 전진
            self.publish_string(f"Time: {rospy.get_time()}")
            self.rate.sleep()

if __name__ == '__main__':
    try:
        publisher = SimplePublisher()
        publisher.run()
    except rospy.ROSInterruptException:
        pass
```

### 3.2 C++ Publisher

```cpp
#include <ros/ros.h>
#include <geometry_msgs/Twist.h>

int main(int argc, char **argv) {
    ros::init(argc, argv, "cpp_publisher");
    ros::NodeHandle nh;

    ros::Publisher cmd_pub = nh.advertise<geometry_msgs::Twist>("/cmd_vel", 10);
    ros::Rate loop_rate(10);

    geometry_msgs::Twist msg;

    while (ros::ok()) {
        msg.linear.x = 0.5;
        msg.angular.z = 0.0;

        cmd_pub.publish(msg);
        ROS_INFO("Published: linear=%f, angular=%f", msg.linear.x, msg.angular.z);

        ros::spinOnce();
        loop_rate.sleep();
    }

    return 0;
}
```

## 4. 토픽 구독 (Subscriber)

### 4.1 Python Subscriber

```python
#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import String

class SimpleSubscriber:
    def __init__(self):
        # 토픽 Subscriber 초기화
        rospy.Subscriber('/cmd_vel', Twist, self.cmd_callback)
        rospy.Subscriber('/chatter', String, self.string_callback)

        rospy.init_node('simple_subscriber', anonymous=True)
        rospy.loginfo("Subscriber started")

    def cmd_callback(self, msg):
        """cmd_vel 토픽 수신 콜백"""
        rospy.loginfo(f"Received cmd_vel: linear.x={msg.linear.x}, angular.z={msg.angular.z}")

    def string_callback(self, msg):
        """String 토픽 수신 콜백"""
        rospy.loginfo(f"Received: {msg.data}")

    def run(self):
        """스핀 (이벤트 루프)"""
        rospy.spin()

if __name__ == '__main__':
    try:
        subscriber = SimpleSubscriber()
        subscriber.run()
    except rospy.ROSInterruptException:
        pass
```

### 4.2 C++ Subscriber

```cpp
#include <ros/ros.h>
#include <geometry_msgs/Twist.h>

void cmdCallback(const geometry_msgs::Twist::ConstPtr& msg) {
    ROS_INFO("Received: linear.x=%f, angular.z=%f",
             msg->linear.x, msg->angular.z);
}

int main(int argc, char **argv) {
    ros::init(argc, argv, "cpp_subscriber");
    ros::NodeHandle nh;

    ros::Subscriber sub = nh.subscribe("/cmd_vel", 10, cmdCallback);

    ros::spin();

    return 0;
}
```

## 5. 실습: 토픽 테스트

### 5.1 Publishing 노드

```bash
# 실습용 Publishing 노드 실행
rosrun beginner_tutorials talker.py
```

### 5.2 Subscribing 노드

```bash
# 실습용 Subscribing 노드 실행
rosrun beginner_tutorials listener.py
```

### 5.3命令行 테스트

```bash
# 토픽 목록 확인
rostopic list

# 특정 토픽 정보
rostopic info /cmd_vel

# 토픽 타입 확인
rostopic type /cmd_vel

# 메시지 필드 확인
rostopic show /cmd_vel

# 실시간 데이터 보기
rostopic echo /cmd_vel

# 토픽 전송 (명령행에서)
rostopic pub /cmd_vel geometry_msgs/Twist "{linear: {x: 0.5, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"

# 주기적 전송
rostopic pub /cmd_vel geometry_msgs/Twist "{linear: {x: 0.5, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}" -r 10
```

### 5.4 토픽 빈도 측정

```bash
# 토픽 Hz 확인
rostopic hz /cmd_vel

# 대역폭 확인
rostopic bw /cmd_vel
```

## 6. 커스텀 메시지

### 6.1 메시지 정의

```msg
# ~/catkin_ws/src/my_package/msg/MyMessage.msg
string name
int32 age
float32[] data
```

### 6.2 package.xml 수정

```xml
<build_depend>message_generation</build_depend>
<exec_depend>message_runtime</exec_depend>
```

### 6.3 CMakeLists.txt 수정

```cmake
find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  message_generation
)

add_message_files(
  FILES
  MyMessage.msg
)

generate_messages(
  DEPENDENCIES
  std_msgs
)

catkin_package(
  CATKIN_DEPENDS roscpp rospy message_runtime
)
```

### 6.4 커스텀 메시지 사용

```python
import rospy
from my_package.msg import MyMessage

pub = rospy.Publisher('my_topic', MyMessage, queue_size=10)

msg = MyMessage()
msg.name = "Robot"
msg.age = 1
msg.data = [1.0, 2.0, 3.0]

pub.publish(msg)
```

## 7. 실습 과제

1. `/cmd_vel` 토픽을 Publish하는 노드를 작성하세요.
2. `/scan` 토픽을 Subscribe하여 라이다 데이터를 출력하는 노드를 작성하세요.
3.命令行에서 토픽을 Publish하고 Subscribe 노드에서 확인하세요.
4. 커스텀 메시지를 정의하고 사용하는 노드를 작성하세요.

## 8. 다음 실습 예고

다음 클래스에서는 ROS 서비스와 제어기 패키지에 대해 학습합니다.