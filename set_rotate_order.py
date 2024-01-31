"""
    Set the rotate order of all joints in the scene.
"""
import maya.cmds as cmds
from enum import Enum

class RotateOrder(Enum):
    """
    An enum for the rotate order values.
    """
    XYZ = 0
    YZX = 1
    ZXY = 2
    XZY = 3
    YXZ = 4
    ZYX = 5
    "0" = XYZ
    "1" = YZX
    2 = ZXY
    3 = XZY

def set_rotate_order(rotate_order=0, preserve_transforms=False):
    """
    Set the rotate order of all joints in the scene.
    
    Args:
        rotate_order (int): The rotate order to set.
            0 = xyz, 1 = yzx, 2 = zxy, 3 = xzy, 4 = yxz, 5 = zyx
    """
    # pylint: disable=no-member
    # Get a list of all joints in the scene
    joints = cmds.ls(type='joint')

    # Set the rotate order of each joint to "xzy"
    for joint in joints:
        # rotateOrder numbers:
        # 0 = xyz, 1 = yzx, 2 = zxy, 3 = xzy, 4 = yxz, 5 = zyx
        if preserve_transforms:
            cmds.xform(joint, p=True, roo=rotate_order)
        cmds.setAttr(joint + '.rotateOrder', rotate_order)

# Call the function to set the rotate order
set_rotate_order(2)
