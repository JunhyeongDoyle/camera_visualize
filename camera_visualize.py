import pandas as pd
import json
import numpy as np
import plotly.graph_objs as go
import sys

def visualize_data(csv_file, json_file, config_file):
    # load csv
    df = pd.read_csv(csv_file)

    # load json
    with open(json_file) as f:
        data = json.load(f)
        
    # load config
    with open(config_file) as f:
        config = json.load(f)

    # Create a trace for the CSV data
    trace1 = go.Scatter3d(
        x=df['X'],
        y=df['Y'],
        z=df['Z'],
        mode='lines',
        line=dict(
            color='green',
            width=config["pose_size"]
        ),
        name='Pose Trace'
    )

    # List of main cameras
    main_cameras = config["main_camera"]  

    # Create a cone and a label for each camera in the JSON data
    cones = []
    labels = []
    for i, camera in enumerate(data['cameras'][config["v00_index"]:]):  # v00부터 추출
        x, y, z = camera['Position']
        rx, ry, rz = camera['Rotation']

        color = 'blue' if camera['Name'] in main_cameras else 'red'

        cones.append(
            go.Cone(
                x=[x], y=[y], z=[z],
                u=[rx], v=[ry], w=[rz],
                sizemode="absolute",
                sizeref=config["cone_size"],  
                anchor="tail",
                colorscale=[[0, color], [1, color]],
                opacity = 0.3,
                showscale=False,
                name=camera['Name']
            )
        )
        labels.append(
            go.Scatter3d(
                x=[x], y=[y], z=[z],
                mode='text',
                text=[camera['Name']],
                textposition="bottom center",
                textfont=dict(size=config["text_size"], color='black')  
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
            #zaxis=dict(range=[0, 2.5])  Set graph range (optional)
        )
    )
    
    fig = go.Figure(data=[trace1] + cones + labels, layout=layout)
    fig.show()

if __name__ == "__main__":
    csv_file = sys.argv[1] 
    json_file = sys.argv[2]
    config_file = sys.argv[3]
    visualize_data(csv_file, json_file, config_file)
