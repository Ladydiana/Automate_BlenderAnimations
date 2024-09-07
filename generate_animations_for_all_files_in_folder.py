import os
import subprocess

def generate_animation_for_blend_files(blender_executable, blend_folder, output_folder):
    # Ensure output directory exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate over all files in the folder
    for filename in os.listdir(blend_folder):
        if filename.endswith(".blend"):
            blend_file = os.path.join(blend_folder, filename)
            output_file = os.path.join(output_folder, os.path.splitext(filename)[0])

            # Construct the command to render the animation for the .blend file
            render_command = [
                blender_executable,
                "--background",         # Run Blender in background mode (without the UI)
                blend_file,             # Path to the .blend file
                "-o", output_file,      # Output file path (Blender will append frame numbers)
                "-a"                    # Render the animation
            ]
            
            # Print the current operation
            print(f"Rendering animation for {filename}...")

            # Execute the command
            subprocess.run(render_command, check=True)

            print(f"Animation rendering completed for {filename}. Output saved to {output_file}.")
    
    print("All animations rendered successfully.")

# Set the paths
blender_executable = r"C:\Program Files\Blender Foundation\Blender 4.0\blender.exe"  # Path to your Blender executable
blend_folder = r"C:\Users\Jedi Knight\Documents\GitHub\SportsAnimations\Football"  # Folder containing .blend files
output_folder = r"C:\Users\Jedi Knight\Documents\GitHub\SportsAnimations\renders"  # Folder where the rendered animations will be saved

# Call the function to generate animations for all .blend files in the folder
generate_animation_for_blend_files(blender_executable, blend_folder, output_folder)
