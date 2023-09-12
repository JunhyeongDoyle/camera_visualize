import pandas as pd
import json
import numpy as np

# Load the JSON data
with open('S_Group3.json', 'r') as file:
    data = json.load(file)

# Given sequence of camera views
camera_sequence = ["v04","v05", "v06", "v07", "v08", "v09", "v10", "v11", 
                   "v10", "v09", "v08", "v09", "v10", "v11", "v12", 
                   "v13", "v14", "v15", "v16", "v17", "v18", "v19", 
                   "v20", "v21", "v20", "v19", "v18", "v19", "v20", 
                   "v21", "v22", "v23", "v24", "v25"]

# Extract the selected poses based on the given sequence
direct_selected_poses = []
for cam in camera_sequence:
    for camera in data["cameras"]:
        if camera["Name"] == cam:
            position = camera["Position"]
            rotation = camera["Rotation"]
            yaw, pitch, roll = rotation[0], rotation[1], rotation[2]
            direct_selected_poses.append({
                "X": position[0],
                "Y": position[1],
                "Z": position[2],
                "Yaw": yaw,
                "Pitch": pitch,
                "Roll": roll
            })

# Convert the directly selected poses to a DataFrame
df_direct_sequence = pd.DataFrame(direct_selected_poses)


def interpolate_pose(start, end, num_points):
    """Linearly interpolate between two poses."""
    t_values = np.linspace(0, 1, num_points)
    interpolated_poses = []

    for t in t_values:
        interpolated_pose = {
            "X": (1-t)*start["X"] + t*end["X"],
            "Y": (1-t)*start["Y"] + t*end["Y"],
            "Z": (1-t)*start["Z"] + t*end["Z"],
            "Yaw": (1-t)*start["Yaw"] + t*end["Yaw"],
            "Pitch": (1-t)*start["Pitch"] + t*end["Pitch"],
            "Roll": (1-t)*start["Roll"] + t*end["Roll"]
        }
        interpolated_poses.append(interpolated_pose)

    return interpolated_poses

# Interpolate the poses with 9 interpolated points between each segment
num_points_per_interval = 10  # 9 interpolated points + 1 endpoint
interpolated_poses_300 = []

for i in range(len(camera_sequence) - 1):
    start_pose = direct_selected_poses[i]
    end_pose = direct_selected_poses[i + 1]
    interpolated_segment = interpolate_pose(start_pose, end_pose, num_points_per_interval)[:-1]
    interpolated_poses_300.extend(interpolated_segment)

# Remove the first pose to get exactly 300 poses
# interpolated_poses_300 = interpolated_poses_300[1:]

interpolated_poses_300.append(direct_selected_poses[-1])

# Convert the interpolated poses to a DataFrame and save to a CSV file
df_interpolated_exact_300 = pd.DataFrame(interpolated_poses_300)
df_interpolated_exact_300.to_csv('interpolated_camera_poses.csv', index=False)