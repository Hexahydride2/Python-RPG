import os

# Set your target folder path
folder_path = R"C:\Users\papic\Documents\Second_term\Python_Essentials\group1-dragonquest\timefantasy_characters\timefantasy_characters\frames\chara\chara8_3"  # Change this to your folder path

# Define the new names in order
new_filenames = [
    "down_walk(1).png", "left_walk(1).png", "right_walk(1).png", "up_walk(1).png",
    "down_stand.png", "left_stand.png", "right_stand.png", "up_stand.png",
    "down_walk(2).png", "left_walk(2).png", "right_walk(2).png", "up_walk(2).png"
]

# Get all files in the folder and sort them by name
files = sorted(os.listdir(folder_path))

# Filter only PNG files (optional, to avoid renaming unwanted files)
files = [f for f in files if f.endswith(".png")]

# Ensure the file count matches
if len(files) != len(new_filenames):
    print("Error: Number of files does not match expected count!")
else:
    # Rename each file
    for old_name, new_name in zip(files, new_filenames):
        old_path = os.path.join(folder_path, old_name)
        new_path = os.path.join(folder_path, new_name)
        os.rename(old_path, new_path)
        print(f"Renamed: {old_name} -> {new_name}")

print("Renaming complete!")
