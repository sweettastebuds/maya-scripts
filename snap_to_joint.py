import maya.cmds as cmds

# pylint: disable=no-member
def snap_to_joint(axis=("x", "y", "z")):
    """
    Snaps the first selected joint to the pivot position of the second selected joint.
    """
    # Get the selected joints
    selected_joints = cmds.ls(selection=True, type='joint')

    # Check if two joints are selected
    if len(selected_joints) != 2:
        cmds.warning('Please select two joints.')
        return

    # Get the pivot position of the second joint
    source_position = cmds.xform(selected_joints[1], query=True, worldSpace=True, translation=True)
    target_position = cmds.xform(selected_joints[0], query=True, worldSpace=True, translation=True)
    snapto_position = []

    snapto_position = [source_position[0]] if "x" in axis else [target_position[0]]
    snapto_position.append(source_position[1] if "y" in axis else target_position[1])
    snapto_position.append(source_position[2] if "z" in axis else target_position[2])

    # Snap the first joint to the snapto position
    cmds.xform(selected_joints[0], worldSpace=True, translation=snapto_position)

snap_to_joint()
