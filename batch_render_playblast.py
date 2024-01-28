"""
This module contains functions for rendering Maya animations as GIFs.

The module provides the following functions:
- fix_references(): Fix the file paths of referenced files in the Maya scene.
- create_gif(base_name, file_output_dir, start_frame, end_frame): Create a GIF animation from a sequence of images.
- render_animation_to_gif(maya_file, output_dir): Render a Maya animation as a GIF.
- batch_render_animations_to_gifs(directory, output_dir): Batch render multiple Maya animations as GIFs.
"""

import os
import maya.cmds as cmds
import imageio

try:
    import maya.standalone
    maya.standalone.initialize()
except:
    pass

# Rest of the code...
import os
import maya.cmds as cmds
import imageio

try:
    import maya.standalone
    maya.standalone.initialize()
except:
    pass

def fix_references():
    """
    Fix the file paths of referenced files in the Maya scene.

    This function iterates through all the references in the scene and checks if the reference path contains a specific file name. If it does, the function replaces the reference path with a new path.

    Args:
        None

    Returns:
        None
    """
    # List all references in the scene
    references = cmds.file(query=True, reference=True)
    for ref in references:
        # Get the current path of the reference
        ref_path = cmds.referenceQuery(ref, filename=True)
        ref_filename = os.path.basename(ref_path)
        ref_node = cmds.referenceQuery(ref, referenceNode=True)
        # is reference loaded
        is_loaded = cmds.referenceQuery(ref, isLoaded=True)
        print(f"Reference {ref} is loaded: {is_loaded}")
        # Determine the new path (this is where you'll define your logic to fix the path)
        if "stm_female_rig.0013.mb" in ref_path:
            new_path = r"D:\michael\Sync\projects\stretchminder\Female01\Female01_retargeting_delivery_ramon\SOURCE\stm_female_rig.0013.mb"
            print(f"Changing reference path from {ref_path} to {new_path}")
        # Replace the reference with the new path
        cmds.file(new_path, loadReference=ref_node)

def create_gif(base_name, file_output_dir, start_frame, end_frame):
    """
    Create a GIF animation from a sequence of images.

    This function takes a base name, directory path, start frame, and end frame as input. It reads a sequence of images from the specified directory and creates a GIF animation using the imageio library.

    Args:
        base_name (str): The base name for the GIF file.
        file_output_dir (str): The directory path where the images and GIF file will be saved.
        start_frame (int): The starting frame number of the animation.
        end_frame (int): The ending frame number of the animation.

    Returns:
        None
    """
    gif_filename = os.path.join(file_output_dir, base_name + '.gif')
    with imageio.get_writer(gif_filename, mode='I') as writer:
        for frame_number in range(int(start_frame), int(end_frame) + 1):
            frame_file = os.path.join(file_output_dir, f'{base_name}_playblast.{frame_number:04d}.jpg')
            if os.path.exists(frame_file):
                image = imageio.imread(frame_file)
                writer.append_data(image)

def render_animation_to_gif(maya_file, output_dir):
    """
    Render a Maya animation as a GIF.

    This function opens a Maya file, fixes the references, creates an output directory, renders the animation using playblast, and then creates a GIF from the playblast frames.

    Args:
        maya_file (str): The path to the Maya file.
        output_dir (str): The directory where the GIF will be saved.

    Returns:
        None
    """
    # Load the Maya file
    cmds.file(maya_file, open=True, loadReferenceDepth="none", force=True)
    source_directory = os.path.dirname(maya_file)
    
    fix_references()

    # Create output directory based on Maya file name
    base_name = os.path.splitext(os.path.basename(maya_file))[0]
    file_output_dir = os.path.join(output_dir, base_name)
    if not os.path.exists(file_output_dir):
        os.makedirs(file_output_dir)

    # Render the animation using playblast
    start_frame = cmds.playbackOptions(query=True, minTime=True)
    end_frame = cmds.playbackOptions(query=True, maxTime=True)
    playblast_file = os.path.join(file_output_dir, base_name + '_playblast')
    cmds.playblast(format='image', filename=playblast_file, sequenceTime=0, clearCache=1,
                    viewer=0, showOrnaments=0, fp=4, percent=100, compression='jpg',
                    quality=100, widthHeight=(1920/2, 1080/2), startTime=start_frame, endTime=end_frame, offScreen=True)

    # Create GIF from playblast frames
    # create_gif(base_name, file_output_dir, start_frame, end_frame)
    gif_filename = os.path.join(source_directory, base_name + '.gif')
    frame_duration = 1.0 / 30
    print(f"Creating GIF: {gif_filename}")
    with imageio.get_writer(gif_filename, mode='I', duration=frame_duration) as writer:
        for frame_number in range(int(start_frame), int(end_frame) + 1):
            frame_file = os.path.join(file_output_dir, f'{base_name}_playblast.{frame_number:04d}.jpg')
            if os.path.exists(frame_file):
                # print(f"Appending frame {frame_file}")
                image = imageio.imread(frame_file)
                writer.append_data(image)
        print(f"Created GIF: {gif_filename}")

def batch_render_animations_to_gifs(directory, output_dir):
    """
    Batch render multiple Maya animations as GIFs.

    This function takes a directory path containing multiple Maya files and an output directory path. It iterates through all the files in the directory, renders each animation as a GIF, and saves them in the output directory.

    Args:
        directory (str): The directory path containing the Maya files.
        output_dir (str): The directory where the GIFs will be saved.

    Returns:
        None
    """
    for file in os.listdir(directory):
        if file.endswith('.ma') or file.endswith('.mb'):
            render_animation_to_gif(os.path.join(directory, file), output_dir)

# Example usage
source_directory = r'D:\michael\Sync\projects\stretchminder\Female01\Female01_retargeting_delivery_ramon\SOURCE\female_retarget'
output_directory = r'D:\michael\Sync\projects\stretchminder\Female01\Female01_retargeting_delivery_ramon\SOURCE\female_retarget\Renders'
batch_render_animations_to_gifs(source_directory, output_directory)

try:
    maya.standalone.uninitialize()
except:
    pass