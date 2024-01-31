import maya.cmds as cmds
import maya.mel as mel
import os

# pylint: disable=no-member
def export_animations_for_unreal(file_path, start_frame, end_frame):
    """
    Export animations for Unreal Engine.

    Args:
        file_path (str): The file path to export the animations to.
        start_frame (int): The start frame for baking the complex animation.
        end_frame (int): The end frame for baking the complex animation.
    """
    # Set the animation export options for FBX
    mel.eval('FBXResetExport')  # Reset to default settings
    mel.eval('FBXExportInAscii -v true')  # Export in ASCII format (optional)
    mel.eval('FBXExportUpAxis Y')  # Set the Up Axis to Y
    mel.eval('FBXExportApplyConstantKeyReducer -v false')  # Disable constant key reducer
    mel.eval('FBXExportBakeComplexAnimation -v true')  # Enable complex animation baking
    mel.eval(f'FBXExportBakeComplexStart -v {start_frame}')  # Start frame for baking
    mel.eval(f'FBXExportBakeComplexEnd -v {end_frame}')  # End frame for baking
    mel.eval('FBXExportBakeComplexStep -v true')  # Step value
    mel.eval('FBXExportBakeResampleAnimation -v true')  # Enable resampling
    mel.eval('FBXExportQuaternion -v euler')  # Use Euler angles for rotation
    mel.eval('FBXExportUseSceneName -v true') # Use the scene name for the exported file

    # Export the selected animations to an FBX file
    mel.eval(f'FBXExport -f "{file_path}" -s')

def get_timeline_range():
    """
    Get the start and end frame of the timeline.

    Returns:
        tuple: A tuple containing the start frame and end frame of the timeline.
    """
    # Get the start frame of the timeline
    start_frame = cmds.playbackOptions(query=True, minTime=True)

    # Get the end frame of the timeline
    end_frame = cmds.playbackOptions(query=True, maxTime=True)

    return start_frame, end_frame

def select_all_joints():
    """
    Select all joints in the scene.
    """
    cmds.select(clear=True)
    joints = cmds.ls(type="joint")
    cmds.select(joints, add=True)

def select_object_by_name(name):
    """
    Select an object in the scene by its name.

    Args:
        name (str): The name of the object to select.
    """
    cmds.select(clear=True)
    cmds.select(name)

def delete_unrecognized_nodes():
    """
    Delete unrecognized nodes from the scene.
    """
    unrecognized_nodes = ['vraySettings']
    
    # Check if the unrecognized nodes exist in the scene
    for node in unrecognized_nodes:
        if cmds.objExists(node):
            cmds.delete(node)
            print(f"Deleted unrecognized node: {node}")
        else:
            print(f"No unrecognized node found: {node}")

def main():
    scene_name = cmds.file(query=True, sceneName=True, shortName=True).split(".")[0]
    export_path = f"A:/projects-gamedev/UE5_Blank/Import/{scene_name}.fbx"
    delete_unrecognized_nodes()

    start_frame, end_frame = get_timeline_range()
    select_all_joints()
    export_animations_for_unreal(export_path, start_frame, end_frame)


if __name__ == "__main__":
    files_dir = "D:/michael/Sync/projects/stretchminder/Female01/Female01_retargeting_delivery_ramon/SOURCE/female_retarget"
    files = [f for f in os.listdir(files_dir) if f.endswith(".mb") or f.endswith(".ma")]
    try:
        import maya.standalone
        maya.standalone.initialize()
    except:
        pass

    for mfile in files:
        print(f"Exporting file: {mfile}")
        file_path = os.path.join(files_dir, mfile)
        cmds.file(file_path, open=True, force=True)
        main()

    try:
        maya.standalone.uninitialize()
    except:
        pass