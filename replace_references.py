"""
This script provides functions to fix the file paths of referenced files in a
Maya scene and run the script as a batch process on a directory of Maya files.

Usage:
    - fix_references(search_string, replace_path): Fix the file paths of referenced files in the Maya scene.
    - run_as_batch(dir_to_files, search_string, replace_path): Run the script as a batch process on a directory of Maya files.
    
Example:
    fix_references("search_path", "new_path")
    run_as_batch("directory_path", "old_path", "new_path")
"""

import os
import maya.cmds as cmds

# pylint: disable=no-member
def fix_references(search_string, replace_path):
    """
    Fix the file paths of referenced files in the Maya scene.

    This function iterates through all the references in the scene and checks if the reference path contains a specific file name. If it does, the function replaces the reference path with a new path.

    Args:
        search_string (str): The string to search for in the reference path.
        replace_path (str): The new path to replace the reference path with.

    Returns:
        None
    """
    # List all references in the scene
    references = cmds.file(query=True, reference=True)
    for ref in references:

        ref_path = cmds.referenceQuery(ref, filename=True)
        # ref_filename = os.path.basename(ref_path)
        ref_node = cmds.referenceQuery(ref, referenceNode=True)


        is_loaded = cmds.referenceQuery(ref, isLoaded=True)
        print(f"Reference {ref} is loaded: {is_loaded}")

        if search_string in ref_path:
            print(f"Changing reference path from {ref_path} to {replace_path}")
        
        cmds.file(replace_path, loadReference=ref_node)


def run_as_batch(dir_to_files, search_string, replace_path):
    """
    Run the script as a batch process on a directory of Maya files.

    This function opens each Maya file in the specified directory, fixes the references, and saves the modified file.

    Args:
        dir_to_files (str): The directory path containing the Maya files.
        search_string (str): The string to search for in the reference path.
        replace_path (str): The new path to replace the reference path with.

    Returns:
        None
    """
    # Check if Maya is running in standalone mode
    try:
        import maya.standalone
        maya.standalone.initialize()
    except:
        pass

    for file in os.listdir(dir_to_files):
        if file.endswith(".ma") or file.endswith(".mb"):
            maya_file = os.path.join(dir_to_files, file)
            cmds.file(maya_file, open=True, loadReferenceDepth="none", force=True)

            fix_references(search_string, replace_path)

            cmds.file(save=True, force=True)
            # cmds.file(new=True, force=True)

    try:
        maya.standalone.uninitialize()
    except:
        pass

if __name__ == "__main__":
    search_path = r"D:\michael\Sync\projects\stretchminder\Female01\Female01_retargeting_delivery_ramon\SOURCE\female_retarget"
    replace_path = r"D:\michael\Sync\projects\stretchminder\Female01\Female01_retargeting_delivery_ramon\SOURCE\stm_female_rig.0013.mb"
    run_as_batch(search_path, search_string="stm_female_rig.0013.mb", replace_path=replace_path)