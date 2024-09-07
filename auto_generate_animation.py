import subprocess
import os
import bpy 
import sys
import random
import colorsys
import argparse

#Generating that auto-increment file name based on the names of the files in the directory
def get_incremented_filename(directory, base_name, extension):
    existing_files = [
        f for f in os.listdir(directory)
        if f.startswith(base_name) and f.endswith(extension)
    ]
    
    existing_numbers = []
    for f in existing_files:
        name, ext = os.path.splitext(f)
        try:
            number = int(name[len(base_name):])
            existing_numbers.append(number)
        except ValueError:
            pass
    
    next_number = max(existing_numbers, default=0) + 1
    return f"{base_name}{next_number}{extension}"
    

# Used for debugging purposes    
def _debug(material_name, hex_color):
    # Debug: Print available materials
    print("Available materials:")
    for mat in bpy.data.materials:
        print(mat.name)
    print("Hex color to change to: ")
    print(hex_color);
    
    # Debug: Print all objects and their materials
    print("\nObjects and their materials:")
    for obj in bpy.data.objects:
        if obj.type == 'MESH':  # Only process objects of type 'MESH'
            if obj.material_slots:
                print(f"Object: {obj.name}")
                for mat_slot in obj.material_slots:
                    if mat_slot.material:
                        print(f"  Material: {mat_slot.material.name}")
    
    # Debug: Print nodes in materials
    print("\nMaterial nodes:")
    for mat in bpy.data.materials:
        print(f"Material: {mat.name}")
        if mat.use_nodes:
            for node in mat.node_tree.nodes:
                print(f"  Node: {node.name} ({node.type})")


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))
    
    
def generate_random_color():
    #h,s,l = random.random(), 0.5 + random.random()/2.0, 2.0 #0.4 + random.random()/5.0
    #r,g,b = [int(256*i) for i in colorsys.hls_to_rgb(h,l,s)]
    #return tuple(int(256*i) for i in colorsys.hls_to_rgb(h,l,s))
    rand = lambda: random.randint(0, 255)
    return hex_to_rgb('#%02X%02X%02X' % (rand(), rand(), rand()))


# If material is Principled BSDF
def set_material_color(material_name, hex_color):
    material = bpy.data.materials.get(material_name)
    if material:
        material.use_nodes = True
        bsdf = material.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            if hex_color:
                rgb_color = hex_to_rgb(hex_color)
            else:
                rgb_color = generate_random_color()
                print("Material color not set. Using random.")
            print(f"Setting the BSDF color to '{rgb_color}'.")
            bsdf.inputs['Base Color'].default_value = (*rgb_color, 1.0)  # Add alpha as 1.0
        else:
            print(f"BSDF node not found in material '{material_name}'.")
    else:
        print(f"Material '{material_name}' not found.")
        
        
def set_all_material_colors():
    print("\nMaterial nodes:")
    for material in bpy.data.materials:
        print(f"Material: {material.name}")
        if material:
            material.use_nodes = True
            bsdf = material.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                rgb_color = generate_random_color()
                print(f"Setting the BSDF color to '{rgb_color}'.")
                bsdf.inputs['Base Color'].default_value = (*rgb_color, 1.0)  # Add alpha as 1.0
                

#If material is Emission            
def set_emission_color(material_name, hex_color):
    
    # Retrieve the material by name
    material = bpy.data.materials.get(material_name)
    if material:
        material.use_nodes = True
        # Get the "Emission" shader node
        emission_node = material.node_tree.nodes.get("Emission")
        if emission_node:
            #rgb_color = hex_to_rgb(hex_color)
            rgb_color = generate_random_color()
            # Set the emission color
            print(f"Setting the emission color to '{rgb_color}'.")
            emission_node.inputs['Color'].default_value = (*rgb_color, 1.0)
        else:
            print(f"Emission node not found in material '{material_name}'.")
    else:
        print(f"Material '{material_name}' not found.")
        
def main():

    parser = argparse.ArgumentParser()
    
    
    

    #-db DATABASE -u USERNAME -p PASSWORD -size 20000
    parser.add_argument("-exe", "--blender_executable", dest = "blender_executable", default = "C:/Program Files/Blender Foundation/Blender 4.0/blender.exe", help="Blender executable")
    parser.add_argument("-i", "--blend_file", dest = "blend_file", default = "C:/Users/Jedi Knight/Documents/GitHub/AnatomyAnimationsVFX/Body/FemaleBody.blend", help="Blender file to run")
    parser.add_argument("-o", "--output_directory", dest ="output_directory", default = "C:/Users/Jedi Knight/Documents/GitHub/AnatomyAnimationsVFX/Body/renders/auto", help="Output folder")
    parser.add_argument("-p", "--base_name",dest = "base_name", default = "auto_rendered_animation_",  help="Output file base name")
    parser.add_argument("-ext", "--extension",dest = "extension", help="Output file extension")
    parser.add_argument("-mat", "--material_name",dest = "material_name", help="Material name")
    parser.add_argument("-hex", "--hex_color",dest = "hex_color", help="Hex color for the material. Random if not set")

    #args = parser.parse_args()
    #args = parser.parse_known_args(sys.argv[sys.argv.index("--")+1:])
    # Handle Blender-specific arguments
    #args, unknown = parser.parse_known_args()
    args = parser.parse_known_args(sys.argv[sys.argv.index("--")+1:])[0]
    
    # Print debug info
    #print(args)
    #print("Unknown arguments:", unknown)
    
    print("Printing args")
    print(args)
    print(args.output_directory)

    # Set the path to the Blender executable
    # blender_executable = "C:/Program Files/Blender Foundation/Blender 4.0/blender.exe"  

    # Set the path to the .blend file
    #if sys.argv[1]:
    #    blend_file = sys.argv[1]
    #else:
    #    blend_file = "C:/Users/Jedi Knight/Documents/GitHub/AnatomyAnimationsVFX/Body/FemaleBody.blend"
    #    print(f"Cannot see .blend input file as argument. Using a default '{blend_file}'")        

    # Set the output directory
    #if sys.argv[2]:
    #    output_directory = sys.argv[2]
    #else:
    #    output_directory = "C:/Users/Jedi Knight/Documents/GitHub/AnatomyAnimationsVFX/Body/renders/auto" 
    #    print(f"Cannot see output directory as argument. Using a default '{output_directory}'")
        
    # Set the output base name 
    #base_name = "auto_rendered_animation_"      # Base name for the output file
    
    # Set the extension
    #extension = ".mkv"                          # Output file extension

    # Accept hex color value as an argument
    #hex_color = sys.argv[-1]

    # Set the material name that you want to change the color of
    #material_name = "Body"  

    # Set the output file name
    output_file = os.path.join(args.output_directory, get_incremented_filename(args.output_directory, args.base_name, args.extension))
    

    # !!!IMPORTANT!!! Ensure the blend file is loaded, otherwise it will try to so this on the default one.
    bpy.ops.wm.open_mainfile(filepath=args.blend_file)

    # Modify the .blend file to update the material color
    #set_material_color(material_name, hex_color)
    set_emission_color(args.material_name, args.hex_color)
    #set_material_color(args.material_name, args.hex_color)
    #set_all_material_colors()

    # !!!IMPORTANT!!! Save the blend file. Otherwise it will render with the default material, not the new one!!!
    bpy.ops.wm.save_mainfile(filepath=args.blend_file)

    # Set the rendering command
    render_command = [
        args.blender_executable, 
        "-b", args.blend_file,    # Run in background mode without UI
        "-o", output_file,   # Specify the output file
        "-a",                     # Render the animation
        #"--", args.hex_color,     # Pass the hex color as an argument
    ]

    # Run the command
    subprocess.run(render_command, check=True)

    print(f"Rendering completed: {output_file}")

if __name__ == '__main__':
  main()