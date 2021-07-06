#!/usr/bin/env python
# coding=utf-8

import numpy as np


class PoseObject:
    """
    Pose object which stores x, y, z, roll, pitch & yaw parameters
    """

    def __init__(self, x, y, z, roll, pitch, yaw):
        # X (meter)
        self.x = float(x)
        # Y (meter)
        self.y = float(y)
        # Z (meter)
        self.z = float(z)
        # Roll (radian)
        self.roll = float(roll)
        # Pitch (radian)
        self.pitch = float(pitch)
        # Yaw (radian)
        self.yaw = float(yaw)

    def __str__(self):
        position = "x = {:.4f}, y = {:.4f}, z = {:.4f}".format(self.x, self.y, self.z)
        orientation = "roll = {:.3f}, pitch = {:.3f}, yaw = {:.3f}".format(self.roll, self.pitch, self.yaw)
        return position + "\n" + orientation

    def __repr__(self):
        return self.__str__()

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        z = self.z + other.z
        roll = self.roll + other.roll
        pitch = self.pitch + other.pitch
        yaw = self.yaw + other.yaw
        return PoseObject(x, y, z, roll, pitch, yaw)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        z = self.z - other.z
        roll = self.roll - other.roll
        pitch = self.pitch - other.pitch
        yaw = self.yaw - other.yaw
        return PoseObject(x, y, z, roll, pitch, yaw)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z \
               and self.roll == other.roll and self.pitch == other.pitch and self.yaw == other.yaw

    def copy_with_offsets(self, x_offset=0., y_offset=0., z_offset=0., roll_offset=0., pitch_offset=0., yaw_offset=0.):
        """
        Create a new pose from copying from copying actual pose with offsets

        :rtype: PoseObject
        """
        return PoseObject(self.x + x_offset,
                          self.y + y_offset,
                          self.z + z_offset,
                          self.roll + roll_offset,
                          self.pitch + pitch_offset,
                          self.yaw + yaw_offset)

    def to_list(self):
        """
        Return a list [x, y, z, roll, pitch, yaw] corresponding to the pose's parameters

        :rtype: list[float]
        """
        list_pos = [self.x, self.y, self.z, self.roll, self.pitch, self.yaw]
        return list(map(float, list_pos))

    @property
    def quaternion(self):
        return self.euler_to_quaternion(self.roll, self.pitch, self.yaw)

    @property
    def quaternion_pose(self):
        return [self.x, self.y, self.z] + list(self.euler_to_quaternion(self.roll, self.pitch, self.yaw))

    @staticmethod
    def euler_to_quaternion(roll, pitch, yaw):
        qx = np.sin(roll / 2) * np.cos(pitch / 2) * np.cos(yaw / 2) - np.cos(roll / 2) * np.sin(pitch / 2) * np.sin(
            yaw / 2)
        qy = np.cos(roll / 2) * np.sin(pitch / 2) * np.cos(yaw / 2) + np.sin(roll / 2) * np.cos(pitch / 2) * np.sin(
            yaw / 2)
        qz = np.cos(roll / 2) * np.cos(pitch / 2) * np.sin(yaw / 2) - np.sin(roll / 2) * np.sin(pitch / 2) * np.cos(
            yaw / 2)
        qw = np.cos(roll / 2) * np.cos(pitch / 2) * np.cos(yaw / 2) + np.sin(roll / 2) * np.sin(pitch / 2) * np.sin(
            yaw / 2)

        return [qx, qy, qz, qw]

    @staticmethod
    def quaternion_to_euler_angle(x, y, z, w):
        ysqr = y * y

        t0 = +2.0 * (w * x + y * z)
        t1 = +1.0 - 2.0 * (x * x + ysqr)
        x_value = np.arctan2(t0, t1)

        t2 = +2.0 * (w * y - z * x)

        t2 = np.clip(t2, a_min=-1.0, a_max=1.0)
        y_value = np.arcsin(t2)

        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (ysqr + z * z)
        z_value = np.arctan2(t3, t4)

        return x_value, y_value, z_value
