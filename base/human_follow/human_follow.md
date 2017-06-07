# Return box

x,y,z

# from pixel to camera

PinholeCameraModel

# turtlebot_follower

    cmd->linear.x = (z - goal_z_) * z_scale_;
    cmd->angular.z = -x * x_scale_;
