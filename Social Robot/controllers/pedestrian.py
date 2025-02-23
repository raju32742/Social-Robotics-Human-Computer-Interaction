# Copyright 1996-2023 Cyberbotics Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Pedestrian class container."""
from controller import Supervisor, Keyboard

import optparse
import math


class Pedestrian (Supervisor):
    """Control a Pedestrian PROTO."""

    def __init__(self):
        """Constructor: initialize constants."""
        self.BODY_PARTS_NUMBER = 13
        self.WALK_SEQUENCES_NUMBER = 8
        self.ROOT_HEIGHT = 1.27
        self.CYCLE_TO_DISTANCE_RATIO = 0.22
        self.speed = 1.15
        self.current_height_offset = 0
        self.joints_position_field = []
        self.joint_names = [
            "leftArmAngle", "leftLowerArmAngle", "leftHandAngle",
            "rightArmAngle", "rightLowerArmAngle", "rightHandAngle",
            "leftLegAngle", "leftLowerLegAngle", "leftFootAngle",
            "rightLegAngle", "rightLowerLegAngle", "rightFootAngle",
            "headAngle"
        ]
        self.height_offsets = [  # those coefficients are empirical coefficients which result in a realistic walking gait
            -0.02, 0.04, 0.08, -0.03, -0.02, 0.04, 0.08, -0.03
        ]
        self.angles = [  # those coefficients are empirical coefficients which result in a realistic walking gait
            [-0.52, -0.15, 0.58, 0.7, 0.52, 0.17, -0.36, -0.74],  # left arm
            [0.0, -0.16, -0.7, -0.38, -0.47, -0.3, -0.58, -0.21],  # left lower arm
            [0.12, 0.0, 0.12, 0.2, 0.0, -0.17, -0.25, 0.0],  # left hand
            [0.52, 0.17, -0.36, -0.74, -0.52, -0.15, 0.58, 0.7],  # right arm
            [-0.47, -0.3, -0.58, -0.21, 0.0, -0.16, -0.7, -0.38],  # right lower arm
            [0.0, -0.17, -0.25, 0.0, 0.12, 0.0, 0.12, 0.2],  # right hand
            [-0.55, -0.85, -1.14, -0.7, -0.56, 0.12, 0.24, 0.4],  # left leg
            [1.4, 1.58, 1.71, 0.49, 0.84, 0.0, 0.14, 0.26],  # left lower leg
            [0.07, 0.07, -0.07, -0.36, 0.0, 0.0, 0.32, -0.07],  # left foot
            [-0.56, 0.12, 0.24, 0.4, -0.55, -0.85, -1.14, -0.7],  # right leg
            [0.84, 0.0, 0.14, 0.26, 1.4, 1.58, 1.71, 0.49],  # right lower leg
            [0.0, 0.0, 0.42, -0.07, 0.07, 0.07, -0.07, -0.36],  # right foot
            [0.18, 0.09, 0.0, 0.09, 0.18, 0.09, 0.0, 0.09]  # head
        ]
        Supervisor.__init__(self)
            # initialize keyboard for controlling the robot
        self.keyboard = Keyboard()
        self.keyboard.enable(self.time_step)

    def run(self):
        """Set the Pedestrian pose and position."""
        opt_parser = optparse.OptionParser()
        opt_parser.add_option("--trajectory", default="", help="Specify the trajectory in the format [x1 y1, x2 y2, ...]")
        opt_parser.add_option("--speed", type=float, default=0.5, help="Specify walking speed in [m/s]")
        opt_parser.add_option("--step", type=int, help="Specify time step (otherwise world time step is used)")
        options, args = opt_parser.parse_args()
        if not options.trajectory or len(options.trajectory.split(',')) < 2:
            print("You should specify the trajectory using the '--trajectory' option.")
            print("The trajectory should have at least 2 points.")
            return
        if options.speed and options.speed > 0:
            self.speed = options.speed
        if options.step and options.step > 0:
            self.time_step = options.step
        else:
            self.time_step = int(self.getBasicTimeStep())
        point_list = options.trajectory.split(',')
        self.number_of_waypoints = len(point_list)
        self.waypoints = []
        for i in range(0, self.number_of_waypoints):
            self.waypoints.append([])
            self.waypoints[i].append(float(point_list[i].split()[0]))
            self.waypoints[i].append(float(point_list[i].split()[1]))
        self.root_node_ref = self.getSelf()
        self.root_translation_field = self.root_node_ref.getField("translation")
        self.root_rotation_field = self.root_node_ref.getField("rotation")
        for i in range(0, self.BODY_PARTS_NUMBER):
            self.joints_position_field.append(self.root_node_ref.getField(self.joint_names[i]))

        # compute waypoints distance
        self.waypoints_distance = []
        for i in range(0, self.number_of_waypoints):
            x = self.waypoints[i][0] - self.waypoints[(i + 1) % self.number_of_waypoints][0]
            y = self.waypoints[i][1] - self.waypoints[(i + 1) % self.number_of_waypoints][1]
            if i == 0:
                self.waypoints_distance.append(math.sqrt(x * x + y * y))
            else:
                self.waypoints_distance.append(self.waypoints_distance[i - 1] + math.sqrt(x * x + y * y))
       
        while self.step(self.time_step) != -1:
            key = self.keyboard.getKey()
            if key == ord('0'):  # press 'S' to sit down
                # Assuming 'leftLegAngle', 'leftLowerLegAngle', and 'leftFootAngle' control the sitting action
                self.getMotor('leftLegAngle').setPosition(-0.5)  # sitdown_position
                self.getMotor('leftLowerLegAngle').setPosition(1.0)  # sitdown_position
                self.getMotor('leftFootAngle').setPosition(0.5)  # sitdown_position
                # Do the same for the right leg
                self.getMotor('rightLegAngle').setPosition(-0.5)  # sitdown_position
                self.getMotor('rightLowerLegAngle').setPosition(1.0)  # sitdown_position
                self.getMotor('rightFootAngle').setPosition(0.5)  # sitdown_position
            elif key == ord('1'):  # press 'H' for handshake
                # Assuming 'leftArmAngle' controls the handshake action
                self.getMotor('leftArmAngle').setPosition(0.7)  # handshake_position
            elif key == ord('2'):  # press 'U' to stand up
                # Assuming 'leftLegAngle', 'leftLowerLegAngle', and 'leftFootAngle' control the standing action
                self.getMotor('leftLegAngle').setPosition(0.0)  # standup_position
                self.getMotor('leftLowerLegAngle').setPosition(0.0)  # standup_position
                self.getMotor('leftFootAngle').setPosition(0.0)  # standup_position
                # Do the same for the right leg
                self.getMotor('rightLegAngle').setPosition(0.0)  # standup_position
                self.getMotor('rightLowerLegAngle').setPosition(0.0)  # standup_position
                self.getMotor('rightFootAngle').setPosition(0.0)  # standup_position


controller = Pedestrian()
controller.run()
