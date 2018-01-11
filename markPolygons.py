# press escape to finish doing real time boxing.
# Program marks the polygons in the figure when it gets 4 double clicks
import cv2
import yaml
import numpy as np

refPt = []
numpyList = []
cropping = False
data = []
file_path = 'parkinglot_1_480p.yml'
image = np.zeros((512, 512), np.uint8)

#img = cv2.imread('parkinglot_1_480p.png')

def yaml_loader(file_path):
    with open(file_path, "r") as file_descr:
        data = yaml.load(file_descr)
        return data


def yaml_dump(file_path, data):
    with open(file_path, "a") as file_descr:
        yaml.dump(data, file_descr)


def yaml_dump_write(file_path, data):
    with open(file_path, "w") as file_descr:
        yaml.dump(data, file_descr)


def click_and_crop(event, x, y, flags, param):
    current_pt = {'id': 0, 'points': []}
    # grab references to the global variables
    global refPt, cropping, image
    if event == cv2.EVENT_LBUTTONDBLCLK:
        refPt.append((x, y))
        cropping = False
    if len(refPt) == 4:
        if data == []:
            if yaml_loader(file_path) != None:
                data_already = len(yaml_loader(file_path))
            else:
                data_already = 0
        else:
            if yaml_loader(file_path) != None:
                data_already = len(data) + len(yaml_loader(file_path))
            else:
                data_already = len(data) 
        
        cv2.line(image, refPt[0], refPt[1], (0, 255, 0), 1)
        cv2.line(image, refPt[1], refPt[2], (0, 255, 0), 1)
        cv2.line(image, refPt[2], refPt[3], (0, 255, 0), 1)
        cv2.line(image, refPt[3], refPt[0], (0, 255, 0), 1)

        temp_lst1 = list(refPt[2])
        temp_lst2 = list(refPt[3])
        temp_lst3 = list(refPt[0])
        temp_lst4 = list(refPt[1])
        
        current_pt['points'] = [temp_lst1, temp_lst2, temp_lst3, temp_lst4]
        current_pt['id'] = data_already
        data.append(current_pt)
        # data_already+=1
        refPt = []
        numpyList = []

def start(cap):
    # data list into yaml file    
    if data == []:
        global image
        
        print('Selecione as vagas e pressione Esc quando terminar.')
        
        _, frame = cap.read()
        image = frame.copy()
        
        cv2.namedWindow("Double click to mark points")
        cv2.imshow("Double click to mark points", image)
        cv2.setMouseCallback("Double click to mark points", click_and_crop)

        while True:
            # display the image and wait for a keypress
            cv2.imshow("Double click to mark points", image)
            key = cv2.waitKey(1) & 0xFF
            if cv2.waitKey(33) == 27:
                break

        print('Salvando marcações de vagas...')
        yaml_dump(file_path, data)               
        cv2.destroyAllWindows() #important to prevent window from becoming inresponsive
