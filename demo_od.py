import cv2 as cv
import numpy as np

frame_width = 640
frame_height = 480
cap = cv.VideoCapture(0)
cap.set(3, frame_width)
cap.set(4, frame_height)

def empty(a):
    pass

cv.namedWindow("Parameters")
cv.resizeWindow("Parameters", 640, 240)
cv.createTrackbar("Threshold1", "Parameters", 104, 255, empty)
cv.createTrackbar("Threshold2", "Parameters", 20, 255, empty)
cv.createTrackbar("Area", "Parameters", 5000, 30000, empty)


def stackImages(scale, imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv.resize(imgArray[x][y], (0,0), None, scale, scale)
                else:
                    imgArray[x][y] = cv.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: 
                    imgArray[x][y] = cv.cvtColor(imgArray[x][y], cv.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv.resize(imgArray[x], (0,0), None, scale, scale)
            else:
                imgArray[x] = cv.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale, scale)
            if len(imgArray[x].shape) == 2:
                imgArray[x] = cv.cvtColor(imgArray[x], cv.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver


def getContours(img, imgContour):

    contours, hierarchy = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE) # CHAIN_APPROX_SIMPLE

    for cnt in contours:
        area = cv.contourArea(cnt)
        areaMin = cv.getTrackbarPos("Area", "Parameters")
        if area > areaMin:
            cv.drawContours(imgContour, cnt, -1, (225, 0, 255), 7)
            peri = cv.arcLength(cnt, True)
            approx = cv.approxPolyDP(cnt, 0.02*peri, True)
            x, y, w, h = cv.boundingRect(approx)
            cv.rectangle(imgContour, (x, y), (x+w, y+y), (0,255,0), 5)

            cv.putText(imgContour, "Points: " + str(len(approx)), (x + w + 20, y + 20), cv.FONT_HERSHEY_COMPLEX, .7, (0,255,0), 2)
            cv.putText(imgContour, "Area: " + str(int(area)), (x + w + 20, y + 45), cv.FONT_HERSHEY_COMPLEX, .7, (0,255,0), 2)




while True:
    success, img = cap.read()
    imgContour = img.copy()

    imgBlur = cv.GaussianBlur(img, (7, 7), 1)
    imgGray = cv.cvtColor(imgBlur, cv.COLOR_BGR2GRAY)


    threshold1 = cv.getTrackbarPos("Threshold1", "Parameters")
    threshold2 = cv.getTrackbarPos("Threshold2", "Parameters")
    imgCanny = cv.Canny(imgGray, threshold1, threshold2)
    kernel = np.ones((5, 5))
    imgDil = cv.dilate(imgCanny, kernel, iterations=1)

    getContours(imgDil, imgContour)

    imgStack = stackImages(0.8, ([img, imgGray, imgCanny], [imgDil, imgContour, imgContour]))

    cv.imshow("Results", imgStack)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break


