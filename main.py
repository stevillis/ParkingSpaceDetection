"""
Created on Wed Jan 03 11:19:25 2018

@author: Stévillis and Valdinilson
title: Smart Parking System

"""

import cv2
import numpy as np

import yaml
import markPolygons

# Path references
fn_yaml = r'datasets/parkinglot.yml'
change_pos = 0.0
config = {'parking_overlay': True,
          'parking_detection': True,
          'min_area_motion_contour': 200,  # area given to detect motion
          'show_ids': True,  # shows id on each region
          'park_laplacian_th': 1.8,
          'park_sec_to_wait': 1,  # 4 wait time for changing the status of a region
          'start_frame': 0}  # 35000 # begin frame from specific frame number

# Set capture device
cap = cv2.VideoCapture(0)
video_info = {'fps': cap.get(cv2.CAP_PROP_FPS),
              'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
              'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
              'fourcc': cap.get(cv2.CAP_PROP_FOURCC),
              'num_of_frames': int(cap.get(cv2.CAP_PROP_FRAME_COUNT))}

cap.set(cv2.CAP_PROP_POS_FRAMES, config['start_frame'])  # jump to frame

# Read YAML data (parking space polygons)
with open(fn_yaml, 'r') as stream:
    parking_data = yaml.load(stream)
parking_contours = []
parking_bounding_rects = []
parking_mask = []

if parking_data != None:
    for park in parking_data:
        points = np.array(park['points'])
        print(points)

        rect = cv2.boundingRect(points)
        print(rect)

        points_shifted = points.copy()
        points_shifted[:, 0] = points[:, 0] - rect[0]  # shift contour to region of interest
        points_shifted[:, 1] = points[:, 1] - rect[1]
        parking_contours.append(points)
        parking_bounding_rects.append(rect)
        mask = cv2.drawContours(np.zeros((rect[3], rect[2]), dtype=np.uint8), [points_shifted],
                                contourIdx=-1, color=255, thickness=-1, lineType=cv2.LINE_8)
        mask = mask == 255
        parking_mask.append(mask)
else:
    # Initialize the parking spaces marking
    markPolygons.start(cap)

kernel_erode = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))  # morphological kernel
kernel_dilate = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 19))
if parking_data != None:
    parking_status = [False] * len(parking_data)
    parking_buffer = [None] * len(parking_data)


def print_parkIDs(park, coor_points, frame_rev):
    moments = cv2.moments(coor_points)
    centroid = (int(moments['m10'] / moments['m00']) - 3, int(moments['m01'] / moments['m00']) + 3)
    # putting numbers on marked regions
    cv2.putText(frame_rev, str(park['id']), (centroid[0] + 1, centroid[1] + 1), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(frame_rev, str(park['id']), (centroid[0] - 1, centroid[1] - 1), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(frame_rev, str(park['id']), (centroid[0] + 1, centroid[1] + 1), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(frame_rev, str(park['id']), (centroid[0] - 1, centroid[1] - 1), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (255, 255, 255), 1, cv2.LINE_AA)

    cv2.putText(frame_rev, str(park['id']), centroid, cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (0, 0, 0), 1, cv2.LINE_AA)


while (cap.isOpened()):
    # Read frame-by-frame
    video_cur_pos = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0  # Current position of the video file in seconds
    video_cur_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)  # Index of the frame to be decoded/captured next
    ret, frame = cap.read()

    if ret == False:
        print('Capture Error')
        break

    # Background Subtraction
    frame_blur = cv2.GaussianBlur(frame.copy(), (5, 5), 3)
    frame_gray = cv2.cvtColor(frame_blur, cv2.COLOR_BGR2GRAY)
    frame_out = frame.copy()

    # detecting cars and vacant spaces
    if config['parking_detection']:
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
                parking_buffer[ind] = video_cur_pos
                change_pos = video_cur_pos

            # If status is still different than the one saved and counter is open
            elif status != parking_status[ind] and parking_buffer[ind] != None:
                if video_cur_pos - parking_buffer[ind] > config['park_sec_to_wait']:
                    parking_status[ind] = status
                    parking_buffer[ind] = None
            # If status is still same and counter is open
            elif status == parking_status[ind] and parking_buffer[ind] != None:
                parking_buffer[ind] = None

    # Changing the color on the basis on status change occured in the aboce section and putting numbers on areas
    if config['parking_overlay']:
        for ind, park in enumerate(parking_data):
            points = np.array(park['points'])
            if parking_status[ind]:
                color = (0, 255, 0)
            else:
                color = (0, 0, 255)
            cv2.drawContours(frame_out, [points], contourIdx=-1, color=color, thickness=2, lineType=cv2.LINE_8)
            if config['show_ids']:
                print_parkIDs(park, points, frame_out)

    # Display video
    cv2.imshow('frame', frame_out)
    k = cv2.waitKey(1)
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
