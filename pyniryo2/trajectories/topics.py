from pyniryo2.niryo_topic import NiryoTopic
# from pyniryo2.arm.objects import HardwareStatusObject, JointStateObject
from pyniryo2.objects import PoseObject


class TrajectoryTopics(object):

    def __init__(self, client):
        self.__client = client

