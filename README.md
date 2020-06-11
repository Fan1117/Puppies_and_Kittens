# Puppies_and_Kittens
This is a repo for customizing video components and external triggers for OpenBCI EEG experiments.

# Quick Start
1. Install OpenCV packages by ```pip install opencv-python```
2. Find the folder ```./Images/Image_Class/Cat```. Put the kitten images in this folder.
3. Find the folder ```./Images/Image_Class/Dog```. Put the puppie images in this folder.
4. In the terminal, change directory to the current folder or type ```cd /Puppies_and_Kittens/```. Then type ```python ExternalTriggerCreator.py -l settings.json```. The experiment video ```project_video.mp4``` and the corresponding labels ```label.txt``` will be output in the folder ```./```

# Arguments in json file with default values
1. "image_base_path": "./Images/", directory that stores all the images including welcome page and classification image pages.
2. "image_types": ["Cat", "Dog"], 
3. "video_time": 3000, default time for each image to appear (ms)
4. "trigger_interval": 100, time for the trigger to flick one time (ms)
5. "flick_times": 5, times for the trigger to flick at the begining and ending of the video (ms)
6. "fps": 20, 
7. "screen_size": [500, 400], 
8. "time_range_per_image": [3.5, 6.5], 
9. "video_output": "project_video.mp4",
10. "label_output": "labels.txt",
11. "trigger_position": [0, 300, 100, 400], [x_start, y_start, x_end, y_end]
