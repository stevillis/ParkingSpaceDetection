"""
Created on Wed Jan 03 11:19:25 2018

@author: Stévillis and Valdinilson
title: Smart Parking System

"""

import cv2
import numpy as np

import yaml
import markpolygons

import time


def draw_masks(parking_data):
    """ Draw masks in parking_data points. """
    if parking_data is not None:
        for park in parking_data:
            points = np.array(park['points'])
            rect = cv2.boundingRect(points)
            points_shifted = points.copy()
            points_shifted[:, 0] = points[:, 0] - rect[0]  # shift contour to region of interest
            points_shifted[:, 1] = points[:, 1] - rect[1]
            parking_contours.append(points)
            parking_bounding_rects.append(rect)
            mask = cv2.drawContours(np.zeros((rect[3], rect[2]), dtype=np.uint8), [points_shifted],
                                    contourIdx=-1, color=255, thickness=-1, lineType=cv2.LINE_8)
            cv2.imshow('Mask', mask)
            cv2.waitKey(0)
            mask = mask == 255
            parking_mask.append(mask)
    else:
        # Initialize the parking spaces marking
        markpolygons.start(cap)


def detect_cars_and_vacant_spaces(frame_gray):
    """ Detect cars and vacant spaces in parking. """
    global parking_space_empty
    # detecting cars and vacant spaces
    for ind, park in enumerate(parking_data):
        points = np.array(park['points'])
        rect = parking_bounding_rects[ind]
        roi_gray = frame_gray[rect[1]:(rect[1] + rect[3]),
                   rect[0]:(rect[0] + rect[2])]  # crop roi for faster calculation
        laplacian = cv2.Laplacian(roi_gray, cv2.CV_64F)

        points[:, 0] = points[:, 0] - rect[0]  # shift contour to roi
        points[:, 1] = points[:, 1] - rect[1]
        delta = np.mean(np.abs(laplacian * parking_mask[ind]))
        status = delta < config['park_laplacian_th']

        # If detected a change in parking status, save the current time
        if status != parking_status[ind] and parking_buffer[ind] == None:
            parking_buffer[ind] = time.time() - time_video

        # If status is still different than the one saved and counter is open
        elif status != parking_status[ind] and parking_buffer[ind] != None:
            if time_video - parking_buffer[ind] > config['park_sec_to_wait']:
                parking_status[ind] = status
                parking_buffer[ind] = None
                parking_space_empty = not parking_space_empty

                if parking_space_empty:
                    print('Vaga {} está vazia!'.format(str(int(park['id']) + 1)))
                else:
                    print('Vaga {} está ocupada!'.format(str(int(park['id']) + 1)))

        # If status is still same and counter is open
        elif status == parking_status[ind] and parking_buffer[ind] != None:
            parking_buffer[ind] = None


def print_parkIDs(park, coor_points, frame_rev):
    """ Print Park IDs in parking spaces. """
    moments = cv2.moments(coor_points)
    centroid = (int(moments['m10'] / moments['m00']) - 3, int(moments['m01'] / moments['m00']) + 3)
    cv2.putText(frame_rev, str(int(park['id']) + 1), centroid, cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (255, 0, 0), 1, cv2.LINE_AA)


if __name__ == '__main__':

    # Path references
    fn_yaml = r'datasets/parkinglot.yml'
    config = {'park_laplacian_th': 1.8,
              'park_sec_to_wait': 2000,  # 4 wait time for changing the status of a region
              'start_frame': 0}  # 35000 # begin frame from specific frame number

    # Set capture device
    cap = cv2.VideoCapture(1)

    cap.set(cv2.CAP_PROP_POS_FRAMES, config['start_frame'])  # jump to frame

    # Read YAML data (parking space polygons)
    with open(fn_yaml, 'r') as stream:
        parking_data = yaml.load(stream)
    parking_contours = []
    parking_bounding_rects = []
    parking_mask = []
    parking_space_empty = True
    first_loop = True

    # Draw parking masks
    draw_masks(parking_data)

    if parking_data is not None:
        parking_status = [False] * len(parking_data)
        parking_buffer = [None] * len(parking_data)

    while cap.isOpened():
        # Read frame-by-frame
        ret, frame = cap.read()

        # Conting time of video in seconds
        time_video = time.time()

        if not ret:
            print('Capture Error')
            break

        # Background Subtraction
        frame_blur = cv2.GaussianBlur(frame.copy(), (5, 5), 3)
        frame_gray = cv2.cvtColor(frame_blur, cv2.COLOR_BGR2GRAY)

        detect_cars_and_vacant_spaces(frame_gray)

        # Changing the color on the basis on status change occured in the aboce section and putting numbers on areas
        frame_out = frame.copy()
        for ind, park in enumerate(parking_data):
            points = np.array(park['points'])
            if parking_status[ind]:
                color = (0, 255, 0)
            else:
                color = (0, 0, 255)

            cv2.drawContours(frame_out, [points], contourIdx=-1, color=color, thickness=2, lineType=cv2.LINE_8)
            print_parkIDs(park, points, frame_out)

        # Display video
        cv2.imshow('frame', frame_out)
        k = cv2.waitKey(1)
        if k == 27:
            break

    # time.sleep(1)

    cap.release()
    cv2.destroyAllWindows()
