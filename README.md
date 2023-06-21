## Pose Visualization Tool
This project contains a Python script that visualizes 3D poses and camera trajectories from provided CSV and JSON files. The visualization is implemented using Plotly, which generates an interactive 3D plot.

The CSV file should contain pose data, and the JSON file should contain camera data including position and rotation. Additionally, the tool allows customization of the visualization through a configuration JSON file. Users can specify main camera identifiers, cone size, text size, and the range of graph axes in the configuration file.

This tool could be useful for individuals working with 3D pose estimation tasks, computer vision, or robotics, where visualizing poses and camera movements is crucial.

**Note:** This project assumes you have the following Python libraries installed: pandas, json, numpy, and plotly.

## Usage
To run the tool, use the command:
```bash
python camera_visualize.py <csv_file> <json_file> <config_file>
```
Replace `<csv_file>`, `<json_file>`, and `<config_file>` with your actual file paths.

Please refer to the sample files in the repository to understand the expected format of the input files.
