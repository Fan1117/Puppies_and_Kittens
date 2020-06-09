# OpenBCI Experiment: ExternalTriggerCreator
# A python script to customize video components and external trigger for EEG experiments

# Date: 06/09/2020
# Author: Fan Li

import cv2
import glob
import argparse
import json
import random
import copy
import os

random.seed(30)


def create_video(image_base_path, fps, flick_times, screen_size, time_range_per_image, video_output, label_output, trigger_position):
    size = tuple(screen_size)
    img_array = []
    frames_array = []
    label_array = []
    label_index = []
    filename_array = []
    class_list = os.listdir(image_base_path + 'Image_Class')
    print("class_list: ", class_list)
    # class frames
    for i in range(len(class_list)):
        class_item = class_list[i]

        for filename in glob.glob(image_base_path + 'Image_Class/' + class_item + '/*.jpg'):
            print(filename)
            img = cv2.imread(filename)
            img = cv2.resize(img, size)
            random_number = random.randint(int(time_range_per_image[0] * 10), int(time_range_per_image[1] * 10))
            frame_numbers = int(random_number * fps / 10)
            frames, label = create_frames(img, frame_numbers, class_item, fps, trigger_position)
            frames_array.append(frames)
            label_array.append(label)
            label_index.append(i)
            filename_array.append(filename)

    print("length of z", len(frames_array))
    # random
    z = list(zip(frames_array, label_array, label_index, filename_array))

    random.shuffle(z)
    new_frame_array, new_label_array, new_label_index_array, new_filename_array = zip(*z)
    for frames in new_frame_array:
        for image in frames:
            img_array.append(image)

    with open(label_output, 'w') as handle:
        for i in range(len(new_label_array)):
            handle.write("%s," % new_label_index_array[i])
            handle.write("%s," % new_label_array[i])
            local_file_name = new_filename_array[i].split("\\")[-1]
            handle.write("%s," % local_file_name)
            handle.write("\n")

    # Welcome frames
    welcome_array = []

    img = cv2.imread(image_base_path + 'Welcome/welcome2OpenBCI.jpg')
    img_black = cv2.imread(image_base_path + 'Welcome/welcome2OpenBCI.jpg')
    img_white = cv2.imread(image_base_path + 'Welcome/welcome2OpenBCI.jpg')

    img = cv2.resize(img, size)

    img_black = cv2.resize(img_black, size)
    img_white = cv2.resize(img_white, size)

    cv2.rectangle(img_black, (trigger_position[0], trigger_position[1]), (trigger_position[2], trigger_position[3]), (0, 0, 0), -1)
    cv2.rectangle(img_white, (trigger_position[0], trigger_position[1]), (trigger_position[2], trigger_position[3]), (255, 255, 255), -1)

    for i in range(3 * fps):
        welcome_array.append(img)
    for j in range(flick_times):
        for i in range(int(0.1 * fps)):
            welcome_array.append(img_black)
        for i in range(int(0.1 * fps)):
            welcome_array.append(img_white)
    print(len(img_array))

    # ending frames
    ending_array = []
    for j in range(flick_times):
        for i in range(int(0.1 * fps)):
            ending_array.append(img_black)
        for i in range(int(0.1 * fps)):
            ending_array.append(img_white)

    img_array = welcome_array + img_array + ending_array
    print(len(welcome_array), len(img_array))

    out = cv2.VideoWriter(video_output, cv2.VideoWriter_fourcc(*'FMP4'), fps, size)
    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()


def create_frames(img, frame_num, label, fps, trigger_position):
    img_white = copy.deepcopy(img)
    img_black = copy.deepcopy(img)

    # white
    cv2.rectangle(img_white,
                  (trigger_position[0], trigger_position[1]), (trigger_position[2], trigger_position[3]),
                  (255, 255, 255),
                  -1)
    # black
    cv2.rectangle(img_black,
                  (trigger_position[0], trigger_position[1]), (trigger_position[2], trigger_position[3]),
                  (0, 0, 0),
                  -1)
    frame_array = []
    for i in range(int(0.1 * fps)):
        frame_array.append(img_black)
    for i in range(frame_num):
        frame_array.append(img_black)
    for i in range(int(0.1 * fps)):
        frame_array.append(img_white)
    return frame_array, label


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--load_json", help="load json to parse args")
    args = parser.parse_args()
    if args.load_json:
        with open(args.load_json, 'rt') as f:
            t_args = argparse.Namespace()
            t_args.__dict__.update(json.load(f))
            args = parser.parse_args(namespace=t_args)
    create_video(args.image_base_path,
                 args.fps,
                 args.flick_times,
                 args.screen_size,
                 args.time_range_per_image,
                 args.video_output,
                 args.label_output,
                 args.trigger_position)
