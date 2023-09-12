import pandas as pd
import json
import numpy as np
import plotly.graph_objs as go
import sys
import matplotlib



def euler_to_rotation_matrix(yaw, pitch, roll):
    # Convert degrees to radians
    yaw = np.deg2rad(yaw)
    pitch = np.deg2rad(pitch)
    roll = np.deg2rad(roll)

    # Create rotation matrix
    R_x = np.array([[1, 0, 0],
                    [0, np.cos(roll), -np.sin(roll)],
                    [0, np.sin(roll), np.cos(roll)]])
    
    R_y = np.array([[np.cos(pitch), 0, np.sin(pitch)],
                    [0, 1, 0],
                    [-np.sin(pitch), 0, np.cos(pitch)]])
    
    R_z = np.array([[np.cos(yaw), -np.sin(yaw), 0],
                    [np.sin(yaw), np.cos(yaw), 0],
                    [0, 0, 1]])

    R = np.dot(R_z, np.dot(R_y, R_x))

    return R

def rgba_to_hex(rgba):
    r, g, b, _ = rgba
    return '#{:02x}{:02x}{:02x}'.format(int(r*255), int(g*255), int(b*255))

def visualize_data(csv_file, json_file):
    # load csv
    df = pd.read_csv(csv_file)

    # load json
    with open(json_file) as f:
        data = json.load(f)

    # Create a cone for each pose in the CSV data
    trace_cones = []
    cmap = matplotlib.colormaps.get_cmap('Purples')
    for i in range(0, len(df), 5):
        x, y, z = df.loc[i, ['X', 'Y', 'Z']]
        yaw, pitch, roll = df.loc[i, ['Yaw', 'Pitch', 'Roll']]
        R = euler_to_rotation_matrix(yaw, pitch, roll)
        u, v, w = R[:, 0]
        
        rgba = cmap(i / len(df))
        color = rgba_to_hex(rgba)
        
        trace_cones.append(
            go.Cone(
                x=[x], y=[y], z=[z],
                u=[-u], v=[-v], w=[-w],
                sizemode="absolute",
                sizeref=10,  
                anchor="tail",
                colorscale=[[0, color], [1, color]],
                opacity = 0.3,
                showscale=False,
                name=f'Pose {i}'
            )
        )
    
    # Define colors for each group
    group_colors = {
        "Group0": 'red',
        "Group1": 'green',
        "Group2": 'blue',
        "Group3": 'yellow'
    }

    # Create a cone and a label for each camera in the JSON data
    cones = []
    labels = []
    for i, camera in enumerate(data['cameras']): 
        if camera['Name'] == 'viewport':
            continue 
        x, y, z = camera['Position']
        yaw, pitch, roll = camera['Rotation']
        R = euler_to_rotation_matrix(yaw, pitch, roll)
        u, v, w = R[:, 0]

        # Determine the color of the cone based on the group
        color = 'grey'  # default color if camera is not in any group
        for group, cameras in group_colors.items():
            if camera['Name'] in data[group]:
                color = group_colors[group]
                break

        cones.append(
            go.Cone(
                x=[x], y=[y], z=[z],
                u=[-u], v=[-v], w=[-w],
                sizemode="absolute",
                sizeref=10,  
                anchor="tail",
                colorscale=[[0, color], [1, color]],
                opacity = 0.3,
                showscale=False,
                name=camera['Name']
            )
        )
        labels.append(
            go.Scatter3d(
                x=[x], y=[y-1.0e-2], z=[z],
                mode='text',
                text=[camera['Name']],
                textposition="top center",
                textfont=dict(size=10, color='black')  
            )
        )
    
    layout = go.Layout(
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0
        ),
        showlegend=False,
        scene=dict(
            camera=dict(
                eye=dict(x=1.5, y=-1.5, z=1)
            ),
            #xaxis=dict(range=[0, 2.5]) 
        )
    )
    
    fig = go.Figure(data=trace_cones + cones + labels, layout=layout)
    fig.show()

if __name__ == "__main__":
    csv_file = sys.argv[1] 
    json_file = sys.argv[2]
    visualize_data(csv_file, json_file)