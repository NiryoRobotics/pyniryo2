import roslibpy

# from pyniryo2.utils import pose_quat_dict_to_list, pose_quat_list_to_dict

from .enums import AnimationMode


class LedRingServices(object):

    def __init__(self, client):
        self.__client = client

        self.set_led_ring_service = roslibpy.Service(self.__client,
                                                        '/niryo_robot_led_ring/user_service',
                                                        'niryo_robot_led_ring/LedUser')


    def set_led_ring_request(self, animation_nb, color = [0, 0, 0], color_list = [[0, 0, 0]], frequency = 0, iterations = 0, speed = 0, wait = False):
        animation_mode = {'animation': animation_nb}
        color_rgb = self.color_to_color_rgba(color)
        color_list_rgb = [self.color_to_color_rgba(color) for color in color_list]
        return roslibpy.ServiceRequest({"animation_mode": animation_mode, 
                                        "color": color_rgb,
                                        "colors_list": color_list_rgb,
                                        "frequency": frequency,
                                        "iterations": iterations,
                                        "speed_ms": speed,
                                        "wait_answer": wait })
   
    @staticmethod
    def color_to_color_rgba(color):
        return {'r': color[0], 'g' : color[1], 'b': color[2], 'a': 0} 

