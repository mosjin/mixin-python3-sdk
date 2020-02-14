# -*- coding: utf-8 -*-

# robot ids:
client_ids_robots = {
    "JinLab": { "name": "JinLab.com", "id": "b5b127c2-72b6-4e92-a7c7-c414d2fa49d0" },
}

def get_robot_list():
    return client_ids_robots

def get_robot_info( name ):
    robots = client_ids_robots
    if name in robots:
        return robots.get( name )

    return ""

def get_robot_id( name ):
    info = get_robot_info( name )
    if info:
        return info[ "id" ]

    return ""

def get_robot_name( name ):
    info = get_robot_info( name )
    if info:
        return info[ "name" ]

    return ""

# print( get_robot_id( "MsgFavorite") )