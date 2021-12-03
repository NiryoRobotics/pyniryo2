# Imports
from pyniryo2 import *
import pyniryo.vision as vision

# Connecting to robot
ws_name = "gazebo_1"
robot_ip = "127.0.0.1"

niryo_robot = NiryoRobot(robot_ip)  # =< Replace by robot ip address

# Calibrating Robot
niryo_robot.arm.calibrate_auto()
# Updating tool
niryo_robot.tool.update_tool()

# Looping Forever
nb_errors = 0
while nb_errors < 5:
    # Moving to observation pause
    niryo_robot.arm.move_pose([0.16, 0.0, 0.35, 0.0, 1.57, 0.0])

    # -- 1 -- ##
    img_compressed = niryo_robot.vision.get_img_compressed()
    img = vision.uncompress_image(img_compressed)
    vision.show_img_and_check_close("Image", img)
    # // 1 // ##
    # -- 2 -- ##
    im_work = vision.extract_img_workspace(img, workspace_ratio=1.0)

    if im_work is None:
        print("Unable to find markers")
        nb_errors += 1
        continue
    vision.show_img("Image Work", im_work, wait_ms=100)
    # // 2 // ##

    # -- 3 -- ##
    low_thresh_list, high_thresh_list = [90, 115, 75], [115, 255, 255]
    img_thresh = vision.threshold_hsv(im_work, low_thresh_list, high_thresh_list)
    vision.show_img("Thresh", img_thresh, wait_ms=100)

    # // 3 // ##

    # -- 4 & 5 -- ##
    im_morpho = vision.morphological_transformations(img_thresh, morpho_type=vision.MorphoType.OPEN,
                                                      kernel_shape=(5, 5), kernel_type=vision.KernelType.ELLIPSE)
    vision.show_img("Morpho", im_morpho, wait_ms=100)
    # // 4 & 5 // ##

    # -- 6 -- #
    best_contour = vision.biggest_contour_finder(im_morpho)
    if len(best_contour) == 0:
        print("No blob found")
        nb_errors += 1
        continue
    vision.show_img("Biggest Contour", vision.draw_contours(im_morpho, [best_contour]), wait_ms=100)
    # // 6 // #
    # -- 7 & 8 -- #
    cx, cy = vision.get_contour_barycenter(best_contour)
    height, width = img_thresh.shape
    x_rel = float(cx) / width
    y_rel = float(cy) / height
    angle = vision.get_contour_angle(best_contour)
    # // 7 & 8// #
    # -- 9 -- #
    height_offset = 0.0
    obj_pose = niryo_robot.vision.get_target_pose_from_rel(ws_name, height_offset,
                                                           x_rel, y_rel, angle)
    # // 9 // #

    # -- 10 -- #
    place_pose = PoseObject(
        x=0.0, y=0.20, z=0.3,
        roll=0.0, pitch=1.57, yaw=1.57
    )

    # Picking the object
    niryo_robot.pick_place.pick_from_pose(obj_pose)

    # Placing the object
    niryo_robot.pick_place.place_from_pose(place_pose)
    # // 10 // #

niryo_robot.arm.go_to_sleep()
niryo_robot.end()
