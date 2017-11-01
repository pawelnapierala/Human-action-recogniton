import os, h5py
import numpy as np 


class MAD:

    NO_JOINTS = 20

    # 4  : walking
    # 9  : left arm punch
    # 13 : swing from left
    # 19 : right arm swipe to the right
    ACTIONS = [4, 9, 13, 19]

    ACTIONS_CLASSES_MAP = {
        4 : 0,
        9 : 1,
        13 : 2,
        19 : 3
        }

    CLASSES = {
        0 : 'walking',
        1 : 'punch',
        2 : 'swing',
        3 : 'arm swipe' 
        }

    JOINT_ROTATIONS = {
        2 : 1,
        3 : 2,
        4 : 3,
        5 : 3,
        6 : 5,
        7 : 6,
        8 : 7,
        9 : 3,
        10 : 9,
        11 : 10,
        12 : 11,
        13 : 1,
        14 : 13,
        15 : 14,
        16 : 15,
        17 : 1,
        18 : 17,
        19 : 18,
        20 : 19,
        }

    script_dir = os.path.dirname(os.path.realpath(__file__))
    mad_data_dir = os.path.join('data', 'mad')

    def find_action_frames(self, label_file, action_id):
        labels = label_file['label']
        for row in range(len(labels[0][:])):
            if (labels[0][row] == action_id):
                return int(labels[1][row]), int(labels[2][row])

    def get_skeleton_at_frame(self, skeleton_file, frame):
        return skeleton_file[skeleton_file['skeleton'][frame][0]][:]

    def get_skeleton_at_frames(self, skeleton_file, start_frame, end_frame):
        skeleton = []
        for frame in range(start_frame, end_frame + 1):
            skeleton.append(skeleton_file[skeleton_file['skeleton'][frame][0]][:])
        return skeleton

    def get_nro(self, skeleton):
        nros = np.empty((3, 19))
        for i in range(1, 20):
            p_i = skeleton[:, i]
            p_j = skeleton[:, self.JOINT_ROTATIONS[i + 1] - 1]
            sub = p_i - p_j
            e_dist = np.linalg.norm(sub)
            if e_dist == 0.0:
                raise ValueError('Division by zero, found empty joint coordinates')
            nro = sub / e_dist
            nros[0][i - 1] = nro[0]
            nros[1][i - 1] = nro[1]
            nros[2][i - 1] = nro[2]
        return nros

    def flip_skeleton(self, skeleton):
        flipped = np.copy(skeleton)
        flipped[0,0] = skeleton[0,0] * -1
        flipped[0,1] = skeleton[0,1] * -1
        flipped[0,2] = skeleton[0,2] * -1
        flipped[0,3] = skeleton[0,3] * -1
        flipped[0,4] = skeleton[0,4] * -1
        flipped[0,5] = skeleton[0,5] * -1
        flipped[0,6] = skeleton[0,6] * -1
        flipped[0,7] = skeleton[0,7] * -1
        flipped[0,8] = skeleton[0,8] * -1
        flipped[0,9] = skeleton[0,9] * -1
        flipped[0,10] = skeleton[0,10] * -1
        flipped[0,11] = skeleton[0,11] * -1
        flipped[0,12] = skeleton[0,12] * -1
        flipped[0,13] = skeleton[0,13] * -1
        flipped[0,14] = skeleton[0,14] * -1
        flipped[0,15] = skeleton[0,15] * -1
        flipped[0,16] = skeleton[0,16] * -1
        flipped[0,17] = skeleton[0,17] * -1
        flipped[0,18] = skeleton[0,18] * -1
        flipped[0,19] = skeleton[0,19] * -1
        return flipped

    # actions: list of numpy arrays, each array containing single action sequence
    def actions_to_nro(self, actions):
        nros_list = []
        for action in actions:
            action_nros = np.empty((action.shape[0], 3, 19))
            for f, frame in enumerate(action):
                action_nros[f] = self.get_nro(frame)
            nros_list.append(action_nros)
        return nros_list                

    def get_actions_of_subjects(self, from_subject, to_subject):
        actions = []
        classes = []
        for action_id in self.ACTIONS:
            for subject in range(from_subject, to_subject + 1):
                for sequence in range(2):
                    label_file = h5py.File(os.path.join(self.mad_data_dir, 'sub' + str(subject).zfill(2), 'seq' + str(sequence + 1).zfill(2) + '_label.mat'), 'r')
                    skeleton_file = h5py.File(os.path.join(self.mad_data_dir, 'sub' + str(subject).zfill(2), 'seq' + str(sequence + 1).zfill(2) + '_sk.mat'), 'r')
                    start_frame, end_frame = self.find_action_frames(label_file, action_id)
                    no_frames = end_frame - start_frame
                    action_class = self.ACTIONS_CLASSES_MAP[action_id]
                    action = np.empty((no_frames, 3, self.NO_JOINTS))
                    for i, frame in enumerate(range(start_frame, end_frame)):
                        action[i] = self.get_skeleton_at_frame(skeleton_file, frame)
                        # if not np.any(action[i]): 
                        #     log('Found empty frame: ' + str(frame))
                    actions.append(action)
                    classes.append(self.ACTIONS_CLASSES_MAP[action_id])                    
                    # log('Action ' + self.CLASSES[action_class] + ' | subject ' + str(subject) + ' | sequence ' + str(sequence + 1) + ' | frames ' + str(no_frames) + ' (' + str(start_frame) + '-' + str(end_frame) + ')')
        return actions, classes

    def add_flipped_actions(self, actions, classes):
        flipped_actions = []
        flipped_classes = []
        for a_idx, action in enumerate(actions):
            flipped_action = np.empty((action.shape))
            for f_idx, frame in enumerate(action):
                flipped_skeleton = self.flip_skeleton(frame)
                flipped_action[f_idx] = flipped_skeleton
            flipped_actions.append(flipped_action)
            flipped_classes.append(classes[a_idx])
        return actions + flipped_actions, classes + flipped_classes
