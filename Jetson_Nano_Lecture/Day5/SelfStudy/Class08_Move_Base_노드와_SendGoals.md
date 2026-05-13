# Class 08: Move_Base 노드와 SendGoals 실습

## 1. Move_Base 노드 이해

### 1.1 Move_Base 아키텍처

```
Move_Base Architecture:
┌───────────────────────────────────────────┐
│              Move Base                    │
│  ┌─────────────────────────────────────┐ │
│  │     Global Planner                  │ │
│  │     (전역 경로 계획)                 │ │
│  └─────────────────────────────────────┘ │
│                    ↓                      │
│  ┌─────────────────────────────────────┐ │
│  │     Local Planner                   │ │
│  │     (지역 충돌 회피)                 │ │
│  └─────────────────────────────────────┘ │
│                    ↓                      │
│  ┌─────────────────────────────────────┐ │
│  │     Costmap 2D                      │ │
│  │     (비용 맵)                        │ │
│  └─────────────────────────────────────┘ │
│                    ↓                      │
│  ┌─────────────────────────────────────┐ │
│  │     Base Controller                 │ │
│  │     (모터 제어)                      │ │
│  └─────────────────────────────────────┘ │
└───────────────────────────────────────────┘
         ↓                         ↓
    /cmd_vel              /move_base/result
```

### 1.2 Move_Base 인터페이스

```msg
# 입력 토픽
/move_base_simple/goal     # PoseStamped
/move_base/goal             # MoveBaseAction (Action)

# 출력 토픽
/move_base/status           # GoalStatusArray
/move_base/feedback         # MoveBaseFeedback
/move_base/result           # MoveBaseResult

# 서비스
/move_base/make_plan        # GetPlan
/move_base/clear_costmaps   # Empty
```

### 1.3 Action 인터페이스

```action
# MoveBaseAction
# Goal
geometry_msgs/PoseStamped target_pose
---
# Result
---
# Feedback
geometry_msgs/PoseStamped base_position
std_msgs/Float32 distance_remaining
```

## 2. Goal 전송 방법

### 2.1命令行에서 Goal 전송

```bash
# simple goal (rostopic)
rostopic pub /move_base_simple/goal geometry_msgs/PoseStamped \
  "{header: {stamp: now, frame_id: 'map'}, \
    pose: {position: {x: 2.0, y: 1.0, z: 0.0}, \
           orientation: {x: 0.0, y: 0.0, z: 0.707, w: 0.707}}}"
```

### 2.2 Python 클라이언트

```python
#!/usr/bin/env python3
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

def send_goal(x, y, theta):
    # Action Client 생성
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    rospy.loginfo("Waiting for move_base server...")
    client.wait_for_server()

    # Goal 생성
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()

    goal.target_pose.pose.position.x = x
    goal.target_pose.pose.position.y = y
    goal.target_pose.pose.position.z = 0.0

    #Quaternion from angle
    import math
    goal.target_pose.pose.orientation.z = math.sin(theta / 2)
    goal.target_pose.pose.orientation.w = math.cos(theta / 2)

    # Goal 전송
    rospy.loginfo(f"Sending goal: x={x}, y={y}, theta={theta}")
    client.send_goal(goal)

    # 결과 대기
    client.wait_for_result(rospy.Duration(60))

    # 결과 반환
    result = client.get_result()
    if result:
        rospy.loginfo("Goal reached!")
    else:
        rospy.loginfo("Goal failed!")

    return client.get_result()

if __name__ == '__main__':
    rospy.init_node('send_goal_client')
    send_goal(2.0, 0.0, 0.0)
```

### 2.3 서비스로 Goal 전송

```python
#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import PoseStamped
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib

def send_goal_service(x, y, theta):
    """목표 위치로 이동하는 서비스 노드"""
    pub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=1)

    rate = rospy.Rate(10)
    while pub.get_num_connections() < 1:
        rate.sleep()

    msg = PoseStamped()
    msg.header.frame_id = 'map'
    msg.header.stamp = rospy.Time.now()
    msg.pose.position.x = x
    msg.pose.position.y = y
    msg.pose.position.z = 0.0

    import math
    msg.pose.orientation.z = math.sin(theta / 2)
    msg.pose.orientation.w = math.cos(theta / 2)

    pub.publish(msg)
    rospy.loginfo(f"Goal sent: ({x}, {y}, {theta})")

if __name__ == '__main__':
    rospy.init_node('goal_service')
    send_goal_service(1.0, 0.0, 0.0)
```

## 3. 다중 목표 순회

### 3.1 Waypoint 순회

```python
#!/usr/bin/env python3
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import math

class WaypointNavigator:
    def __init__(self):
        self.client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
        rospy.loginfo("Waiting for move_base server...")
        self.client.wait_for_server()

    def create_goal(self, x, y, theta):
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x = x
        goal.target_pose.pose.position.y = y
        goal.target_pose.pose.orientation.z = math.sin(theta / 2)
        goal.target_pose.pose.orientation.w = math.cos(theta / 2)
        return goal

    def navigate_waypoints(self, waypoints):
        """다중 waypoint 순회"""
        for i, (x, y, theta) in enumerate(waypoints):
            rospy.loginfo(f"Waypoint {i+1}/{len(waypoints)}: ({x}, {y})")

            goal = self.create_goal(x, y, theta)
            self.client.send_goal(goal)

            # 목표 완료 대기
            self.client.wait_for_result(rospy.Duration(60))

            result = self.client.get_result()
            if result:
                rospy.loginfo(f"Waypoint {i+1} reached!")
            else:
                rospy.logwarn(f"Waypoint {i+1} failed!")

            rospy.sleep(1)

        rospy.loginfo("All waypoints completed!")

if __name__ == '__main__':
    rospy.init_node('waypoint_navigator')

    waypoints = [
        (1.0, 0.0, 0.0),
        (2.0, 1.0, 1.57),
        (2.0, 2.0, 3.14),
        (1.0, 1.0, -1.57),
        (0.0, 0.0, 0.0),
    ]

    navigator = WaypointNavigator()
    navigator.navigate_waypoints(waypoints)
```

### 3.2 파일에서 Waypoint 로드

```python
import json

def load_waypoints_from_file(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return [(p['x'], p['y'], p['theta']) for p in data['waypoints']]

# JSON 파일 예시:
# {
#   "waypoints": [
#     {"x": 1.0, "y": 0.0, "theta": 0.0},
#     {"x": 2.0, "y": 1.0, "theta": 1.57}
#   ]
# }
```

## 4. Goal 상태 모니터링

### 4.1 상태 확인

```python
#!/usr/bin/env python3
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

def goal_status_monitor():
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client.wait_for_server()

    goal = MoveBaseGoal()
    # ... goal 설정 ...

    client.send_goal(goal, feedback_cb=feedback_callback)

    while not rospy.is_shutdown():
        state = client.get_state()
        rospy.loginfo(f"Goal state: {state}")

        if state == actionlib.GoalStatus.SUCCEEDED:
            rospy.loginfo("Goal reached!")
            break
        elif state in [actionlib.GoalStatus.PREEMPTED,
                       actionlib.GoalStatus.ABORTED]:
            rospy.logwarn("Goal failed!")
            break

        rospy.sleep(0.5)

def feedback_callback(feedback):
    rospy.loginfo(f"Distance remaining: {feedback.distance_remaining}")

if __name__ == '__main__':
    rospy.init_node('goal_monitor')
    goal_status_monitor()
```

### 4.2 상태常量

```python
# Goal Status Constants
PENDING = 0
ACTIVE = 1
PREEMPTED = 2
SUCCEEDED = 3
ABORTED = 4
REJECTED = 5
PREEMPTING = 6
RECALLING = 7
RECALLED = 8
LOST = 9
```

## 5. 취소 및 재설정

### 5.1 Goal 취소

```python
client.cancel_goal()
```

### 5.2 recovery

```python
def recovery_behavior():
    """문제 발생 시 복구 동작"""
    # 1. 현재 목표 취소
    client.cancel_goal()
    rospy.sleep(1)

    # 2. Costmap 초기화
    rospy.wait_for_service('/move_base/clear_costmaps')
    clear = rospy.ServiceProxy('/move_base/clear_costmaps', Empty)
    clear()

    # 3. Back up
    # ... 후진하는 코드 ...
```

## 6. 실습 과제

1. Python으로 MoveBaseAction 클라이언트를 작성하세요.
2. 다중 waypoint를 순회하는 코드를 작성하세요.
3. Goal 상태를 모니터링하고 피드백을 출력하세요.
4. Goal 취소 및 복구 동작을 구현하세요.

## 7. 마무리

이로써 Day4와 Day5의 모든 클래스가 완성되었습니다.

```
완성된 클래스 요약:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Day 4 (8 Classes)
- ROS Topic/Service/Action
- Catkin 패키지 작성
- ROS 도구 및 원격 개발
- Rviz, Odometry, TF
- 모터 구동

Day 5 (8 Classes)
- SLAM (Gmapping, Cartographer)
- Navigation Stack
- Rviz 시각화
- Move_Base와 Goal 전송
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```