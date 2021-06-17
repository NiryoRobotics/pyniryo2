from collections import namedtuple
import numpy as np

from pyniryo2.niryo_topic import NiryoTopic


class VisionTopics(object):

    def __init__(self, client):
        self.__client = client

        self.compressed_video_stream_topic = NiryoTopic(self.__client,
                                                        '/niryo_robot_vision/compressed_video_stream',
                                                        'sensor_msgs/CompressedImage',
                                                        compressed_video_stream_topic_conversion)

        self.camera_info_topic = NiryoTopic(self.__client,
                                            '/niryo_robot_vision/camera_intrinsics',
                                            'sensor_msgs/CameraInfo',
                                            camera_info_topic_conversion)


def compressed_video_stream_topic_conversion(msg):
    return msg['data']


def camera_info_topic_conversion(msg):
    CameraInfo = namedtuple("CameraInfo", ['intrinsics', 'distortion'])

    mtx = np.reshape(msg['K'], (3, 3))
    dist = np.expand_dims(msg['D'], axis=0)

    return CameraInfo(intrinsics=mtx, distortion=dist)
