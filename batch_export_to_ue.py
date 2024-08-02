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
    # mel.eval('FBXExportInAscii -v true')  # Export in ASCII format (optional)
    mel.eval('FBXExportUpAxis Y')  # Set the Up Axis to Y
    mel.eval('FBXExportApplyConstantKeyReducer -v false')  # Disable constant key reducer
    mel.eval('FBXExportBakeComplexAnimation -v true')  # Enable complex animation baking
    mel.eval(f'FBXExportBakeComplexStart -v {start_frame}')  # Start frame for baking
    mel.eval(f'FBXExportBakeComplexEnd -v {end_frame}')  # End frame for baking
    mel.eval('FBXExportBakeComplexStep -v false')  # Step value
    mel.eval('FBXExportBakeResampleAnimation -v true')  # Enable resampling
    mel.eval('FBXExportQuaternion -v euler')  # Use Euler angles for rotation
    mel.eval('FBXExportUseSceneName -v true') # Use the scene name for the exported file
    mel.eval("FBXProperty Export|IncludeGrp|Geometry|BlindData -v false")

    # Export the selected animations to an FBX file
    # mel.eval(f'FBXExport -f "{file_path}" -s')
    cmds.FBXExport('-file', file_path)
    
def export_animation(export_path, export_animation=False, animation_only=False, bake_animation=True):
    import pymel.core as pm
    pm.mel.FBXResetExport()
    pm.mel.eval(f"FBXProperty Export|IncludeGrp|Animation -v {int(export_animation)};") #We cast because the bool in MEL is all lowercase
    pm.mel.FBXExportCameras(v=False)
    pm.mel.FBXExportConstraints(v=False)
    pm.mel.FBXExportEmbeddedTextures(v=False)
    pm.mel.FBXExportFileVersion(v='FBX202000')
    pm.mel.FBXExportIncludeChildren(v=True)
    pm.mel.FBXExportInputConnections(v=False)
    pm.mel.FBXExportLights(v=False)
    pm.mel.FBXExportReferencedAssetsContent(v=True)
    pm.mel.FBXExportShapes(v=True)
    pm.mel.FBXExportSkins(v=True)
    pm.mel.FBXExportSmoothingGroups(v=True)
    pm.mel.FBXExportSmoothMesh(v=True)
    pm.mel.FBXExportTangents(v=True)
    pm.mel.FBXExportTriangulate(v=False)
    pm.mel.FBXExportUseSceneName(v=False)
    pm.mel.FBXExportInAscii(v=False)
    
    pm.mel.FBXExportAnimationOnly(v=animation_only)
    pm.mel.FBXExportBakeComplexAnimation(v=bake_animation)
    pm.mel.FBXExportBakeComplexStart(v=pm.playbackOptions(q=True, minTime=True))
    pm.mel.FBXExportBakeComplexEnd(v=pm.playbackOptions(q=True, maxTime=True))
    
    pm.mel.FBXExport(s=True, f=export_path)

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

def select_all_joints(root_joint):
    """
    Select all joints in the scene under the root joint.
    """
    cmds.select(clear=True)
    cmds.select(root_joint, hierarchy=True)

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
    unrecognized_nodes = ['vraySettings','ngSkinToolsData_skinCluster1']
    
    # Check if the unrecognized nodes exist in the scene
    for node in unrecognized_nodes:
        if cmds.objExists(node):
            cmds.delete(node)
            print(f"Deleted unrecognized node: {node}")
        else:
            print(f"No unrecognized node found: {node}")

def main(export_path):
    scene_name = cmds.file(query=True, sceneName=True, shortName=True).split(".")[0]
    
    #export_path =r"A:/projects/3d-move-avatars/UE5_Retargeting/Import/Male3/%s.fbx" % scene_name
    export_path = export_path + "/" + f"{scene_name}.fbx"
    print(f"Exporting file to: {export_path}")
    
    if not os.path.exists(os.path.dirname(export_path)):
        os.mkdir(os.path.dirname(export_path))
    
    delete_unrecognized_nodes()

    start_frame, end_frame = get_timeline_range()
    select_all_joints("Root_M")
    # export_animations_for_unreal(export_path, start_frame, end_frame)
    export_animation(export_path, export_animation=True, animation_only=True, bake_animation=True)


if __name__ == "__main__":
    root_dir = r"D:/michael/Sync/projects/stretchminder/3d-move-avatars"
    # avatar_dir = "Female/V1/Working Files/Animations"
    avatar_dir = "Male/V1/Working Files/Animations"
    files_dir = root_dir + "/" + avatar_dir
    print(f"Files dir: {files_dir}")
    
    export_path = root_dir + "/" + "Male/V1/Animations/FBX"
    print(f"Exporting to: {export_path}")
    
    anims_list = [
        "SeatedCatCow2",
        "SeatedPelvicTilt",
    ]
        
    files = [f for f in os.listdir(files_dir) if f.endswith(".mb") or f.endswith(".ma")]
    
    if len(anims_list) > 0:
        files = [f for f in files if f.split(".")[0] in anims_list]


    try:
        import maya.standalone
        maya.standalone.initialize()
    except:
        pass

    for mfile in files:
        print(f"Exporting file: {mfile}")
        file_path = os.path.join(files_dir, mfile)
        cmds.file(file_path, open=True, force=True)
        main(export_path)

    try:
        maya.standalone.uninitialize()
    except:
        pass