# PyMOL script to load a receptor and the top docking poses for ligands.
#
# Corrected version with a Python function to handle loops and indentation.
#
from pymol import cmd
import sys
import os

def visualize_poses(receptor_pdb, results_dir, image_dir):
    """
    Loads receptor, iterates through ligand poses, and saves images.
    """
    # Create the output directory if it doesn't exist
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    # Load the receptor
    cmd.load(receptor_pdb, "receptor")
    cmd.color("gray80", "receptor")
    cmd.show("surface", "receptor")
    cmd.set("surface_color", "white")
    
    # Corrected transparency command
    cmd.set("transparency", 0.3, "receptor") 

    # Find all ligand result files in the results directory
    for filename in sorted(os.listdir(results_dir)):
        if filename.endswith("_out.pdbqt"):
            ligand_name = filename.replace("_out.pdbqt", "")
            ligand_path = os.path.join(results_dir, filename)

            # Load the ligand poses and name the object
            cmd.load(ligand_path, ligand_name)
            
            # Style the ligand
            cmd.show("sticks", f"({ligand_name})")
            cmd.util.cbag(f"(organic and {ligand_name})") # Color heteroatoms
            cmd.set("stick_radius", 0.15, ligand_name)

            # Center and zoom on the ligand
            cmd.center(ligand_name, animate=-1)
            cmd.zoom("center", 8)
            cmd.bg_color("white") # Set a white background for nice images

            # Save a high-quality image
            image_path = os.path.join(image_dir, f"{ligand_name}_pose.png")
            cmd.png(image_path, width=1200, height=900, dpi=300, ray=1)

            # Hide the current ligand so the next one can be shown
            cmd.disable(ligand_name)

    # Show the receptor clearly for a final view
    cmd.center("receptor")
    print("Image generation complete.")

# --- Script Execution Starts Here ---

# Get arguments from the command line
receptor_file = sys.argv[-3]
results_directory = sys.argv[-2]
image_directory = sys.argv[-1]

# Run the main function
visualize_poses(receptor_file, results_directory, image_directory)

# Quit PyMOL
cmd.quit()