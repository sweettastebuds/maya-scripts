"""
    Disable Segment Scale Compensate for the selected joint(s).
    
    Can be used to turn off Segment Scale Compensate for multiple joints at once.
    If no joint is selected, a message will be printed in the Script Editor.
    
    Usage:
        Select a joint and run the script.
        
    SSC is used to compensate for non-uniform scaling of parent joints.
    This can cause issues when exporting to game engines.
"""

import maya.cmds as cmds

# Get the currently selected joint
selected_joint = cmds.ls(selection=True, type='joint')

if selected_joint:
    # Check if the selected item is a joint
    joint_name = selected_joint[0]

    # Disable Segment Scale Compensate for the selected joint
    cmds.setAttr(joint_name + '.segmentScaleCompensate', 0)

    print(f"Segment Scale Offset turned off for {joint_name}.")
else:
    print("Please select a joint.")