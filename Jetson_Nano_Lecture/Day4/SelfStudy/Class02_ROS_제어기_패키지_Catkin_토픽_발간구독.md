# Class 02: ROS 제어기 패키지 및 Catkin 토픽 발간구독

## 1. ROS 서비스 (Services)

### 1.1 서비스 개념

Service는 동기식 요청-응답 통신 방식입니다. Client가 Request를 보내면 Server가 Response를 반환합니다.

```
Service Communication:
┌─────────┐    Request     ┌─────────┐
│ Client  │ ──────────────▶│ Server  │
│         │◀────────────── │         │
│         │    Response    │         │
└─────────┘                └─────────┘
```

### 1.2 표준 서비스

```bash
# 표준 서비스 예시
/clear                 # 로그清除
/get_loggers          # 로거 설정 조회
/set_logger_level     # 로거 설정 변경
/rostopic list        # 토픽 목록
```

### 1.3 서비스 정의

```srv
# ~/catkin_ws/src/my_package/srv/AddTwoInts.srv
int64 a
int64 b
---
int64 sum
```

### 1.4 서비스 서버/클라이언트

```python
# Service Server
import rospy
from my_package.srv import AddTwoInts, AddTwoIntsResponse

def add_two_ints_callback(req):
    print(f"Received: a={req.a}, b={req.b}")
    return AddTwoIntsResponse(req.a + req.b)

rospy.init_node('add_two_ints_server')
service = rospy.Service('add_two_ints', AddTwoInts, add_two_ints_callback)
rospy.spin()

# Service Client
import rospy
from my_package.srv import AddTwoInts

rospy.init_node('add_two_ints_client')
service = rospy.ServiceProxy('add_two_ints', AddTwoInts)
response = service(3, 5)
print(f"Result: {response.sum}")
```

## 2. ROS 액션 (Actions)

### 2.1 액션 개념

Action은 비동기式的 목표-결과 통신입니다. 장기 실행 작업에 적합하며, 피드백을 포함합니다.

```
Action Communication:
┌─────────┐    Goal     ┌─────────┐
│ Client  │ ──────────▶│ Server  │
│         │◀─────────── │         │
│         │   Feedback  │         │
│         │◀─────────── │         │
│         │    Result   │         │
└─────────┘             └─────────┘
```

### 2.2 액션 정의

```action
# ~/catkin_ws/src/my_package/action/MyAction.action
# Goal
geometry_msgs/Pose target_pose
---
# Result
nav_msgs/Path path
---
# Feedback
float32 distance_remaining
```

## 3. Catkin 패키지 구조

### 3.1 기본 구조

```
my_robot_package/
├── CMakeLists.txt
├── package.xml
├── src/
│   ├── __init__.py
│   ├── publisher_node.py
│   └── subscriber_node.py
├── scripts/
│   ├── launch_script.py
│   └── config_script.py
├── launch/
│   ├── robot.launch
│   └── simulation.launch
├── msg/
│   ├── CustomMessage.msg
│   └── AnotherMessage.msg
├── srv/
│   ├── AddTwoInts.srv
│   └── SetMotor.srv
├── action/
│   └── MoveRobot.action
├── config/
│   ├── params.yaml
│   └── config.yaml
└── urdf/
    ├── robot.urdf
    └── robot.gazebo
```

### 3.2 package.xml

```xml
<?xml version="1.0"?>
<package format="2">
  <name>my_robot_package</name>
  <version>1.0.0</version>
  <description>My robot package</description>

  <maintainer email="user@example.com">User Name</maintainer>
  <license>MIT</license>

  <buildtool_depend>catkin</buildtool_depend>

  <build_depend>rospy</build_depend>
  <build_depend>roscpp</build_depend>
  <build_depend>std_msgs</build_depend>
  <build_depend>geometry_msgs</build_depend>
  <build_depend>nav_msgs</build_depend>
  <build_depend>sensor_msgs</build_depend>
  <build_depend>message_generation</build_depend>

  <exec_depend>rospy</exec_depend>
  <exec_depend>roscpp</exec_depend>
  <exec_depend>std_msgs</exec_depend>
  <exec_depend>geometry_msgs</exec_depend>
  <exec_depend>nav_msgs</exec_depend>
  <exec_depend>sensor_msgs</exec_depend>
  <exec_depend>message_runtime</exec_depend>

  <export>
  </export>
</package>
```

### 3.3 CMakeLists.txt

```cmake
cmake_minimum_required(VERSION 3.0.2)
project(my_robot_package)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  geometry_msgs
  nav_msgs
  sensor_msgs
  message_generation
)

## Custom Message
add_message_files(
  FILES
  CustomMessage.msg
)

## Custom Service
add_service_files(
  FILES
  SetMotor.srv
)

## Custom Action
add_action_files(
  FILES
  MoveRobot.action
)

generate_messages(
  DEPENDENCIES
  std_msgs
  geometry_msgs
  nav_msgs
  sensor_msgs
)

catkin_package(
  CATKIN_DEPENDS
    roscpp
    rospy
    std_msgs
    geometry_msgs
    nav_msgs
    sensor_msgs
    message_runtime
)

## Build Python scripts
catkin_install_python(PROGRAMS
  scripts/my_script.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

## Build executables
add_executable(publisher_node src/publisher_node.cpp)
add_dependencies(publisher_node ${${PROJECT}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})
target_link_libraries(publisher_node ${catkin_LIBRARIES})

add_executable(subscriber_node src/subscriber_node.cpp)
add_dependencies(subscriber_node ${${PROJECT}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})
target_link_libraries(subscriber_node ${catkin_LIBRARIES})
```

## 4. Catkin 토픽 발간구독实战

### 4.1 패키지 생성

```bash
cd ~/catkin_ws/src
catkin_create_pkg robot_control roscpp rospy std_msgs geometry_msgs nav_msgs sensor_msgs

cd ~/catkin_ws
catkin build
source devel/setup.bash
```

### 4.2 토픽 Publisher 노드

```python
#!/usr/bin/env python3
# ~/catkin_ws/src/robot_control/src/cmd_vel_publisher.py

import rospy
from geometry_msgs.msg import Twist, Pose
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan

class RobotController:
    def __init__(self):
        # Publisher
        self.cmd_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.pose_pub = rospy.Publisher('/robot_pose', Pose, queue_size=10)

        # Subscriber
        self.odom_sub = rospy.Subscriber('/odom', Odometry, self.odom_callback)
        self.scan_sub = rospy.Subscriber('/scan', LaserScan, self.scan_callback)

        rospy.init_node('robot_controller', anonymous=True)
        self.rate = rospy.Rate(10)  # 10Hz

        # 상태 변수
        self.current_pose = None
        self.current_scan = None

    def odom_callback(self, msg):
        """Odometry 콜백"""
        self.current_pose = msg.pose.pose
        rospy.loginfo(f"Position: ({self.current_pose.position.x:.2f}, {self.current_pose.position.y:.2f})")

    def scan_callback(self, msg):
        """LaserScan 콜백"""
        self.current_scan = msg
        min_dist = min(msg.ranges)
        rospy.loginfo(f"Min distance: {min_dist:.2f}m")

    def move_forward(self, speed=0.5, duration=2):
        """전진 이동"""
        msg = Twist()
        msg.linear.x = speed

        start_time = rospy.Time.now()
        while (rospy.Time.now() - start_time).to_sec() < duration:
            self.cmd_pub.publish(msg)
            self.rate.sleep()

        # 정지
        msg.linear.x = 0
        self.cmd_pub.publish(msg)

    def rotate(self, angular_speed=1.0, angle=3.14159):
        """회전"""
        msg = Twist()
        msg.angular.z = angular_speed

        start_time = rospy.Time.now()
        while (rospy.Time.now() - start_time).to_sec() < angle:
            self.cmd_pub.publish(msg)
            self.rate.sleep()

        msg.angular.z = 0
        self.cmd_pub.publish(msg)

    def run(self):
        """메인 실행 루프"""
        rospy.loginfo("Robot controller started")

        while not rospy.is_shutdown():
            # 전진 2초
            self.move_forward(0.5, 2)

            # 회전 180도
            self.rotate(1.0, 3.14159)

            rospy.sleep(1)

if __name__ == '__main__':
    try:
        controller = RobotController()
        controller.run()
    except rospy.ROSInterruptException:
        pass
```

### 4.3 토픽 Subscriber 노드

```python
#!/usr/bin/env python3
# ~/catkin_ws/src/robot_control/src/sensor_subscriber.py

import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan, Image
from std_msgs.msg import String

class SensorSubscriber:
    def __init__(self):
        # Multiple Subscribers
        rospy.Subscriber('/cmd_vel', Twist, self.cmd_vel_callback)
        rospy.Subscriber('/odom', Odometry, self.odom_callback)
        rospy.Subscriber('/scan', LaserScan, self.scan_callback)
        rospy.Subscriber('/battery_state', String, self.battery_callback)

        rospy.init_node('sensor_subscriber', anonymous=True)
        rospy.loginfo("Sensor subscriber started")

        # 데이터 저장을 위한 변수
        self.latest_odom = None
        self.latest_scan = None
        self.latest_cmd = None

    def cmd_vel_callback(self, msg):
        self.latest_cmd = msg
        rospy.logdebug(f"Cmd: v={msg.linear.x}, w={msg.angular.z}")

    def odom_callback(self, msg):
        self.latest_odom = msg
        # Odometry 데이터 처리

    def scan_callback(self, msg):
        self.latest_scan = msg
        # LaserScan 데이터 처리
        # 예:正面 장애물 감지
        if len(msg.ranges) > 0:
            front_idx = len(msg.ranges) // 2
            front_dist = msg.ranges[front_idx]
            if front_dist < 0.5:
                rospy.logwarn(f"Obstacle ahead: {front_dist:.2f}m")

    def battery_callback(self, msg):
        rospy.loginfo(f"Battery: {msg.data}")

    def get_latest_data(self):
        """최신 데이터 반환"""
        return {
            'odom': self.latest_odom,
            'scan': self.latest_scan,
            'cmd': self.latest_cmd
        }

    def run(self):
        rospy.spin()

if __name__ == '__main__':
    try:
        subscriber = SensorSubscriber()
        subscriber.run()
    except rospy.ROSInterruptException:
        pass
```

## 5. Launch 파일

### 5.1 기본 Launch

```xml
<!-- ~/catkin_ws/src/robot_control/launch/robot_control.launch -->
<launch>
  <!-- 노드 파라미터 -->
  <param name="robot_name" value="my_robot"/>
  <param name="max_speed" value="1.0"/>

  <!-- Publisher 노드 -->
  <node name="robot_controller" pkg="robot_control" type="cmd_vel_publisher.py" output="screen"/>

  <!-- Subscriber 노드 -->
  <node name="sensor_subscriber" pkg="robot_control" type="sensor_subscriber.py" output="screen"/>

  <!-- RViz -->
  <node name="rviz" pkg="rviz" type="rviz" args="-d $(find robot_control)/config/robot.rviz"/>
</launch>
```

### 5.2 Launch 실행

```bash
# Launch 파일 실행
roslaunch robot_control robot_control.launch

# 특정 노드만 실행
roslaunch robot_control robot_control.launch only_sensor:=true
```

## 6. 실습 과제

1. Robot Controller 패키지를 생성하세요.
2. `/cmd_vel`에 Twist 메시지를 Publish하는 노드를 작성하세요.
3. `/odom`과 `/scan`을 Subscribe하여 데이터를 출력하는 노드를 작성하세요.
4. Launch 파일로 여러 노드를 동시에 실행하세요.

## 7. 다음 실습 예고

다음 클래스에서는 ROS 주요 도구와 로봇 Catkin 패키지에 대해 학습합니다.