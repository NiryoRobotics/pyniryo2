#!/bin/bash
# file to exec on robot (after chmod +x) when testing led_ring robot status displaying part, starting at the fatal error test
# fatal
rostopic pub /niryo_robot_status/robot_status niryo_robot_status/RobotStatus "robot_status: 0 
robot_message: '' 
logs_status: -3
logs_message: ''" --once 

read -p "Press enter to publish BOOTING"

# booting / update
rostopic pub /niryo_robot_status/robot_status niryo_robot_status/RobotStatus "robot_status: 1
robot_message: ''
logs_status: 0
logs_message: ''" --once 

read -p "Press enter to publish LEARNING MODE ERROR"

# learning error
rostopic pub /niryo_robot_status/robot_status niryo_robot_status/RobotStatus "robot_status: 5
robot_message: ''
logs_status: -2
logs_message: ''" --once 

read -p "Press enter to publish LEARNING MODE WARNING"

# learning warning
rostopic pub /niryo_robot_status/robot_status niryo_robot_status/RobotStatus "robot_status: 5
robot_message: ''
logs_status: -1
logs_message: ''" --once 

read -p "Press enter to publish MOVING ERROR"

# moving error
rostopic pub /niryo_robot_status/robot_status niryo_robot_status/RobotStatus "robot_status: 7
robot_message: ''
logs_status: -2
logs_message: ''" --once 

read -p "Press enter to publish AUTONOMOUS MODE ERROR"

# auto error
rostopic pub /niryo_robot_status/robot_status niryo_robot_status/RobotStatus "robot_status: 8
robot_message: ''
logs_status: -2
logs_message: ''" --once 

read -p "Press enter to publish AUTONOMOUS MODE WARNING"

# auto warning
rostopic pub /niryo_robot_status/robot_status niryo_robot_status/RobotStatus "robot_status: 8
robot_message: ''
logs_status: -1
logs_message: ''" --once 

read -p "Press enter to publish AUTONOMOUS LEARNING MODE"

# auto learning
rostopic pub /niryo_robot_status/robot_status niryo_robot_status/RobotStatus "robot_status: 11
robot_message: ''
logs_status: 0
logs_message: ''" --once 

read -p "Press enter to publish AUTONOMOUS LEARNING MODE WARNING"

# auto learning warning
rostopic pub /niryo_robot_status/robot_status niryo_robot_status/RobotStatus "robot_status: 11
robot_message: ''
logs_status: -1
logs_message: ''" --once 

read -p "Press enter to publish AUTONOMOUS MODE"

# autonomous
rostopic pub /niryo_robot_status/robot_status niryo_robot_status/RobotStatus "robot_status: 8
robot_message: ''
logs_status: 0
logs_message: ''" --once 