#!/usr/bin/env python
import os, h5py, sys, random
import numpy as np 
# from draw import Draw
from mad import MAD


DEBUG = True
TIME_WINDOW_SIZE = 30

script_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(script_dir, 'data')
train_data_dir = os.path.join(data_dir, 'train_data')
validation_data_dir = os.path.join(data_dir, 'validation_data')
test_data_dir = os.path.join(data_dir, 'test_data')

def log(str):
    if DEBUG:
        print(str)

def preprocess_data(actions):
    for a, action in enumerate(actions):
        for f, frame in enumerate(action):
            if not np.any(frame):
                actions[a][f] = action[f - 1]
    return actions

def get_time_windows(actions, classes):
    windows_list = []
    labels_list = []
    for a_idx, action in enumerate(actions):
        no_frames = action.shape[0]
        no_joints = action.shape[2]
        no_windows = no_frames - TIME_WINDOW_SIZE + 1
        windows = np.empty((no_windows, 3, TIME_WINDOW_SIZE, no_joints))
        labels = np.full((no_windows), classes[a_idx], dtype=np.uint8)        
        for w_idx in range(no_windows):
            window = np.empty((3, TIME_WINDOW_SIZE, no_joints))
            for delta_t in range(TIME_WINDOW_SIZE):
                frame = action[w_idx + delta_t]
                window[0][delta_t] = frame[0]
                window[1][delta_t] = frame[1]
                window[2][delta_t] = frame[2]
            windows[w_idx] = window
        windows_list.append(windows)
        labels_list.append(labels)
    return np.concatenate(windows_list), np.concatenate(labels_list)

def over_sample(data, classes):
    classes_count = {}
    data_grouped = [] # TODO grupuj klasy zeby potem wybrac dla kazdej klasy dodatkowe samples
    for c_idx, c in enumerate(classes):
        if c in classes_count:
            classes_count[c] += 1
        else:
            classes_count[c] = 1
    max_samples = 0
    for c, num_samples in classes_count:
        if num_samples > max_samples:
            max_samples = num_samples
    for 

    print classes_count
    return data, classes

def save_data(data, labels, dir):
    with h5py.File(os.path.join(dir, 'data.h5'), 'w') as f:
        f.create_dataset('data', data=data)
        f.create_dataset('label', data=labels)
    with open(os.path.join(dir, 'index.txt'), 'w') as f:
        f.write(os.path.join(dir, 'data.h5'))

def count_samples(classes):
    totals = {0:0, 1:0, 2:0, 3:0}
    for class_idx in classes:
        totals[class_idx] += 1
    labeled = {
        'walking' : totals[0],
        'punch' : totals[1],
        'swing' : totals[2],
        'arm swipe' : totals[3]
        }
    return labeled

mad = MAD()

log('Reading raw data')
train_actions_raw, train_classes = mad.get_actions_of_subjects(1, 1)
validation_actions_raw, validation_classes = mad.get_actions_of_subjects(11, 11)
test_actions_raw, test_classes = mad.get_actions_of_subjects(16, 16)

log('Preprocessing data')
train_actions = preprocess_data(train_actions_raw)
validation_actions = preprocess_data(validation_actions_raw)
test_actions = preprocess_data(test_actions_raw)

log('Adding flipped data')
train_actions, train_classes = mad.add_flipped_actions(train_actions, train_classes)
validation_actions, validation_classes = mad.add_flipped_actions(validation_actions, validation_classes)
test_actions, test_classes = mad.add_flipped_actions(test_actions, test_classes)

log('Computing NROs')
train_actions_nro = mad.actions_to_nro(train_actions)
validation_actions_nro = mad.actions_to_nro(validation_actions)
test_actions_nro = mad.actions_to_nro(test_actions)

log('Constructing time windows')
train_data, train_labels = get_time_windows(train_actions_nro, train_classes)
validation_data, validation_labels = get_time_windows(validation_actions_nro, validation_classes)
test_data, test_labels = get_time_windows(test_actions_nro, test_classes)

log('Over-sampling data')
train_data, train_labels = over_sample(train_data, train_labels)

log('Saving data')
save_data(train_data, train_labels, train_data_dir)
save_data(validation_data, validation_labels, validation_data_dir)
save_data(test_data, test_labels, test_data_dir)

train_samples = count_samples(train_labels)
validation_samples = count_samples(validation_labels)
test_samples = count_samples(test_labels)

print 'Train data samples: ' + str(train_samples)
print 'Validation data samples: ' + str(validation_samples)
print 'Test data samples: ' + str(test_samples)
print 'Train data shape: ' + str(train_data.shape)
print 'Validation data shape: ' + str(validation_data.shape)
print 'Test data shape: ' + str(test_data.shape)


### animate skeleton in frames x-y
# mad = MAD()
# draw = Draw()
# skeleton_file = h5py.File(os.path.join(mad_data_dir, 'sub01', 'seq01_sk.mat'), 'r')
# frames = mad.get_skeleton_at_frames(skeleton_file, 465, 578)
# draw.animate_skeleton(frames)

### draw skeleton at frame x
# mad = MAD()
# draw = Draw()
# skeleton_file = h5py.File(os.path.join(mad_data_dir, 'sub01', 'seq01_sk.mat'), 'r')
# frame = mad.get_skeleton_at_frame(skeleton_file, 465)
# draw.draw_skeleton(frame)