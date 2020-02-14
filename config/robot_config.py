# -*- coding: utf-8 -*-
"""
Mixin Config
get below config from https://developers.mixin.one/dashboard

Website: jinLab.com
mixin: 1051676
update: 2020-02-14
"""

from config import robot_lists
from common_functions import load_robot_info_by_file, get_admin_mixin_id

# robot admins:
mosjin_mixin_id = get_admin_mixin_id()

robot_id = 7000102145
robot_name = "MyRobot"
robot_json_file = 'keystore-7000102145.json'

robot_info = load_robot_info_by_file( robot_json_file )
client_ids_robots = robot_lists.get_robot_list()


# robot: 7000102145
##################################################### online #####################################################
client_id=  robot_info[ 'client_id']
client_secret = "839d7b5577188fd7e5291b23c3abc27cb57b7b0c1172ac73b4854d376c732fe0"
pay_pin = robot_info[ 'pin']
pay_session_id = robot_info[ 'session_id']
pin_token =  robot_info[ 'pin_token']
private_key = robot_info[ 'private_key']