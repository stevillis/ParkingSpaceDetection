# -*- coding: utf-8 -*-

"""
Created on Wed Jan 03 11:19:25 2018

@author: Stévillis and Valdinilson
title: Smart Parking System
"""

import cv2
import numpy as np
import yaml
import time
import markpolygons


def draw_masks(parking_data):
    """
    Draw masks in parking_data points.
    :param parking_data: points of parking spaces
    :return: None
    """

    if parking_data is not None:  # If there are points of parking spaces in the parkinglot.yml file
        for park in parking_data:
            points = np.array(park['points'])  # Convert the parkinglot.yml data to a numpy array
            rect = cv2.boundingRect(points)  # Return the points of the rectangle around the parking space (x, y, w, h)

            points_shifted = points.copy()  # Just a faster copy of points (better than slices)
            # Shift contour to region of interest
            # Subtract x (from x, y, w, h) value from the original x points
            points_shifted[:, 0] = points[:, 0] - rect[0]
            # Subtract y (from x, y, w, h) value from the original y points
            points_shifted[:, 1] = points[:, 1] - rect[1]

            parking_bounding_rects.append(rect)  # Store the region of each parking space for analysis

            """
            Paremeters of drawContours:
                image - An array of zeros with dimensions h and w
                contours - All the input contours 
                countourIdx - Parameter indicating a contour to draw. If it is negative, all the contours are drawn.
                color - Color of the contours. color=255 menas color=(255,255,255)
                thickness - Thickness of lines the contours are drawn with. If it is negative , the contour interiors 
                are drawn.                 
            """
            mask = cv2.drawContours(np.zeros((rect[3], rect[2]), dtype=np.uint8), [points_shifted],
                                    contourIdx=-1, color=255, thickness=-1, lineType=cv2.LINE_8)
            print(mask)
            mask = mask == 255  # Compare all the mask points. Zero becomes False and 255 becomes True

            parking_mask.append(mask)  # Store the region of each parking space drawn for analysis
    else:  # Initialize the parking spaces marking
        markpolygons.start(cap)


def detect_vacant_spaces(frame_blur):
    """
    Detect cars and vacant spaces in parking.
    :param frame_blur: frame_blur
    :return: None
    """
    parking_dict = {}  # Store the status of each parking space

    # Detecting vacant spaces
    for ind, park in enumerate(parking_data):

        points = np.array(park['points'])
        rect = parking_bounding_rects[ind]
        # roi_gray = frame_gray[rect[1]:(rect[1] + rect[3]),
        # rect[0]:(rect[0] + rect[2])]  # crop roi for faster calculation
        roi_gray = frame_blur[rect[1]:(rect[1] + rect[3]),
                   rect[0]:(rect[0] + rect[2])]  # Crop roi for faster calculation

        laplacian = cv2.Laplacian(roi_gray, cv2.CV_64F)  # Apply Laplacian filter to detect edges

        points[:, 0] = points[:, 0] - rect[0]  # Shift contour to roi
        points[:, 1] = points[:, 1] - rect[1]
        # Compute the arithmetic mean along the specified axis and returns a new array containing the mean values
        delta = np.mean(np.abs(laplacian * parking_mask[ind]))
        status = delta < config['park_laplacian_th']

        # While parking spaces isn't in the end, add parking index and status to the parking_dict
        if ind < len(parking_data):
            parking_dict[str(ind + 1)] = parking_status[ind]  # ind starts in 0
        if ind == len(parking_data) - 1:  # When all the parking spaces were done
            # Write the parking_dict in a temp_file to be read after
            f = open('file_temp.txt', 'w')
            f.write(str(parking_dict))
            f.close()

            parking_dict.clear()  # Clear the dict to restart the process

        if parking_status[ind]:
            print('Vaga {} está vazia!'.format(int(park['id']) + 1))
        else:
            print('Vaga {} está ocupada!'.format(int(park['id']) + 1))

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


def print_parkIDs(park, coor_points, frame):
    """
    Print Park IDs in parking spaces.
    :param park: Each parking space
    :param coor_points: Coordinates of parking space
    :param frame: Frame to put the text indice
    :return: None
    """
    moments = cv2.moments(coor_points)  # Calculate the center of mass of the object
    centroid = (int(moments['m10'] / moments['m00']) - 3, int(moments['m01'] / moments['m00']) + 3)
    cv2.putText(frame, str(int(park['id']) + 1), centroid, cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (255, 0, 0), 1, cv2.LINE_AA)


if __name__ == '__main__':

    # Path references
    fn_yaml = r'datasets/parkinglot.yml'
    config = {'park_laplacian_th': 2.1,
              'park_sec_to_wait': 2000  # 4 wait time for changing the status of a region
              }

    # Set capture device
    cap = cv2.VideoCapture(0)

    # Read YAML data (parking space polygons)
    with open(fn_yaml, 'r') as stream:
        parking_data = yaml.load(stream)

    parking_bounding_rects = []  # Points of parking spaces
    parking_mask = []  # bool points of parking spaces

    # Draw parking masks
    draw_masks(parking_data)

    if parking_data is not None:  # If there are points of parking spaces in the parkinglot.yml file
        parking_status = [False] * len(parking_data)  # A list of len(parking_data) False items
        parking_buffer = [None] * len(parking_data)  # # A list of len(parking_data) None items

        # While takes about 0.037 seconds for each loop
        # 1 second ~ 27 while iterations
        while_executions_counter = 0

        while cap.isOpened():
            # Read frame-by-frame
            ret, frame = cap.read()

            # Counting time of video in seconds
            time_video = time.time()

            if not ret:  # Camera is not running
                print('Capture Error')
                break

            # Background Subtraction
            # frame_blur = cv2.GaussianBlur(frame.copy(), (5, 5), 3)
            # frame_gray = cv2.cvtColor(frame_blur, cv2.COLOR_BGR2GRAY)
            # detect_vacant_spaces(frame_gray)
            # detect_vacant_spaces(frame_blur)

            if while_executions_counter == 27:  # After 1 second, check if the parking spaces status has changed
                frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # Base class for Contrast Limited Adaptive Histogram Equalization
                clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))

                # Create implementation for CLAHE: Equalizes the histogram of a grayscale image using Contrast Limited
                # Adaptive Histogram Equalization.
                frame_his = clahe.apply(frame_gray)

                __, frame_thr = cv2.threshold(frame_his, 40, 255, cv2.THRESH_BINARY)  # Get a binary image
                frame_blur = cv2.GaussianBlur(frame_thr, (5, 5), 3)  # Apply a GaussianBlur filter to reduce noise

                detect_vacant_spaces(frame_blur)  # Call the function to detect vacant spaces

                while_executions_counter = 0

            # Changing the color on the basis on status change occured in the above section and putting numbers on areas
            frame_out = frame.copy()
            for ind, park in enumerate(parking_data):
                points = np.array(park['points'])  # Points of parking spaces
                if parking_status[ind]:
                    color = (0, 255, 0)
                else:
                    color = (0, 0, 255)

                cv2.drawContours(frame_out, [points], contourIdx=-1, color=color, thickness=2, lineType=cv2.LINE_8)
                print_parkIDs(park, points, frame_out)  # Put a number on each parking space

            # Display video
            cv2.imshow('frame', frame_out)
            k = cv2.waitKey(1)
            if k == 27:
                break
            elif k & 0xFF == ord('d'):  # Delete all the parking spaces points
                with open(fn_yaml, 'w') as stream:
                    pass
                break
            while_executions_counter += 1

    cap.release()  # Close capturing device
    cv2.destroyAllWindows()
