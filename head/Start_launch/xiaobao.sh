#!/bin/bash
sleep 2s
gnome-terminal -x bash -c " ./runserver.sh"
sleep 1s
gnome-terminal -x bash -c "echo 'qwertasdfg'|sudo -S /home/daisy/robot/weixin_server/weixinserver" 
sleep 1s
gnome-terminal -x bash -c "source /opt/ros/indigo/setup.bash && source /home/daisy/catkin_ws/devel/setup.bash && roscore"
sleep 1s
gnome-terminal -x bash -c "source /opt/ros/indigo/setup.bash && source /home/daisy/catkin_ws/devel/setup.bash && rosrun sound_loc sound_loc.py"
sleep 10s
gnome-terminal -x bash -c "echo 'qwertasdfg'|sudo chmod 777 /dev/ttyUSB0 && python ~/joey/server.py"
sleep 10s
gnome-terminal -x bash -c "cd ./hark_projs && ./ros_py_ps3_loc.sh"
sleep 1s
gnome-terminal -x bash -c "echo 'qwertasdfg'|sudo -S ./runmc.sh"
sleep 1s
gnome-terminal -x bash -c "source /opt/ros/indigo/setup.bash && source /home/daisy/catkin_ws/devel/setup.bash && roslaunch realsense_camera sr300_nodelet_default.launch"
sleep 1s
gnome-terminal -x bash -c "echo 'qwertasdfg'|sudo -S ./runlin.sh"
sleep 1s
#gnome-terminal -x bash -c "cd ./recognition-test && python recognition.py"
sleep 1s
gnome-terminal -x bash -c "cd ./annual_meeting_demo/server_crosstalk && ./server_crosstalk"
sleep 1s
gnome-terminal -x bash -c "source /opt/ros/indigo/setup.bash && source /home/daisy/catkin_ws/devel/setup.bash && roslaunch xfei_voice face_voice.launch"

