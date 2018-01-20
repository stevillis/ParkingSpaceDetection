"""
Created on Wed Jan 03 11:19:25 2018

@author: Stévillis and Valdinilson
title: Smart Parking System

"""

import cv2
import numpy as np
import time
import yaml

import markpolygons

from webparking import webserver


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
            # cv2.imshow('Mask', mask)
            # cv2.waitKey(0)
            mask = mask == 255

            parking_mask.append(mask)
    else:
        # Initialize the parking spaces marking
        markpolygons.start(cap)


def detect_cars_and_vacant_spaces(frame_blur):
    """ Detect cars and vacant spaces in parking. """

    # Dictionary of parking spaces status informations.
    parking_dict = {}
    # detecting cars and vacant spaces
    for ind, park in enumerate(parking_data):

        points = np.array(park['points'])
        rect = parking_bounding_rects[ind]
        # roi_gray = frame_gray[rect[1]:(rect[1] + rect[3]),
        # rect[0]:(rect[0] + rect[2])]  # crop roi for faster calculation
        roi_gray = frame_blur[rect[1]:(rect[1] + rect[3]),
                   rect[0]:(rect[0] + rect[2])]  # crop roi for faster calculation
        laplacian = cv2.Laplacian(roi_gray, cv2.CV_64F)
        points[:, 0] = points[:, 0] - rect[0]  # shift contour to roi
        points[:, 1] = points[:, 1] - rect[1]

        delta = np.mean(np.abs(laplacian * parking_mask[ind]))
        status = delta < config['park_laplacian_th']

        # While parking spaces isn't in the end, add parking index and status to the parking_dict
        print(ind, len(parking_data))
        if ind < len(parking_data):
            parking_dict[str(ind + 1)] = parking_status[ind]  # ind starts in 0
        if ind == 1:  # When all the parking spaces were done, send the dict to webserver
            print('Before:', webserver.parking_spaces)
            webserver.update_parking_spaces(dict(parking_dict))
            print('After:', webserver.parking_spaces)
            parking_dict.clear()

        if parking_status[ind]:
            pass
            # print('Vaga {} está vazia!'.format(str(int(park['id']) + 1)))
        else:
            pass
            # print('Vaga {} está ocupada!'.format(str(int(park['id']) + 1)))

        # If detected a change in parking status, save the current time
        if status != parking_status[ind] and parking_buffer[ind] is None:
            parking_buffer[ind] = time.time() - time_video

        # If status is still different than the one saved and counter is open
        elif status != parking_status[ind] and parking_buffer[ind] is not None:
            if time_video - parking_buffer[ind] > config['park_sec_to_wait']:
                parking_status[ind] = status
                parking_buffer[ind] = None


        # If status is still same and counter is open
        elif status == parking_status[ind] and parking_buffer[ind] is not None:
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
    config = {'park_laplacian_th': 2.1,
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

    # Draw parking masks
    draw_masks(parking_data)

    if parking_data is not None:
        parking_status = [False] * len(parking_data)
        parking_buffer = [None] * len(parking_data)

        # list_time_of_while_execution = []
        # While takes about 0.037 seconds for each loop
        # 1 second ~ 27 while iterations
        counter_of_while_executions = 0

        while cap.isOpened():

            # time_execution = time.time()

            # Read frame-by-frame
            ret, frame = cap.read()

            # Counting time of video in seconds
            time_video = time.time()

            if not ret:
                print('Capture Error')
                break

            # Background Subtraction
            # frame_blur = cv2.GaussianBlur(frame.copy(), (5, 5), 3)
            # frame_gray = cv2.cvtColor(frame_blur, cv2.COLOR_BGR2GRAY)

            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            frame_his = clahe.apply(frame_gray)
            __, frame_thr = cv2.threshold(frame_his, 40, 255, cv2.THRESH_BINARY);
            frame_blur = cv2.GaussianBlur(frame_thr, (5, 5), 3)

            # detect_cars_and_vacant_spaces(frame_gray)
            # detect_cars_and_vacant_spaces(frame_blur)

            if counter_of_while_executions == 27:
                detect_cars_and_vacant_spaces(frame_blur)
                counter_of_while_executions = 0

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
            elif k & 0xFF == ord('d'):
                with open(fn_yaml, 'w') as stream:
                    pass
                break

            """time_execution2 = time.time() - time_execution
            list_time_of_while_execution.append(time_execution2)
            print('Tempo de execução', time_execution2)
            if len(list_time_of_while_execution) > 100:
                print('Mean of time execution:', sum(list_time_of_while_execution)/len(list_time_of_while_execution))
                break
            """
            counter_of_while_executions += 1
            # print(counter_of_while_executions)
        # time.sleep(1)

        cap.release()
        cv2.destroyAllWindows()
