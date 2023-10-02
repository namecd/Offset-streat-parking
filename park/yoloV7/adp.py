import cv2
import os
import cv2
import base64


import utils.IOF


img = cv2.imread('first_frame.jpg')


def first_frame(mp4_loc=r'1.mp4'):
    first_frame_loc = "pict/1.jpg"
    videoCapture = cv2.VideoCapture(mp4_loc)
    success, frame = videoCapture.read()
    if success:
        cv2.imwrite(first_frame_loc, frame)
        cv2.imwrite('first_frame.jpg', frame)



def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        xy = "%d,%d" % (x, y)
        utils.IOF.addpt(x, y)
        print(x, y)
        cv2.circle(img, (x, y), 2, (0, 0, 255))
        cv2.putText(img, xy, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 0, 255))
        cv2.imshow("image", img)


def addpoint():
    global img

    img = cv2.imread('first_frame.jpg')
    cv2.namedWindow("image", 0)
    # cv2.resizeWindow('Img_1', (10240, 7680))
    cv2.setMouseCallback("image", on_EVENT_LBUTTONDOWN)
    while 1:
        cv2.imshow("image", img)
        key = cv2.waitKey(5) & 0xFF
        if key == ord('q'):
            utils.IOF.init()
            break
    cv2.destroyAllWindows()
