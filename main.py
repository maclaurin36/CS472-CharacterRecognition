import numpy as np
import cv2

def main2():
    img = cv2.imread(r'C:\Users\jesse.clark_awardco\Downloads\Drawing.sketchpad.png')
    cv2.waitKey(0)

    # Grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find Canny edges
    edged = cv2.Canny(gray, 30, 200)
    cv2.waitKey(0)

    contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    contours_poly = [None] * len(contours)
    # The Bounding Rectangles will be stored here:
    boundRect = []

    # Alright, just look for the outer bounding boxes:
    for i, c in enumerate(contours):

        if hierarchy[0][i][3] == -1:
            contours_poly[i] = cv2.approxPolyDP(c, 3, True)
            boundRect.append(cv2.boundingRect(contours_poly[i]))

    # Draw the bounding boxes on the (copied) input image:
    for i in range(len(boundRect)):
        color = (0, 255, 0)
        cv2.rectangle(img, (int(boundRect[i][0]), int(boundRect[i][1])),
                      (int(boundRect[i][0] + boundRect[i][2]), int(boundRect[i][1] + boundRect[i][3])), color, 2)

    cv2.imshow('some image', gray)
    cv2.imshow('Canny Edges After Contouring', edged)
    cv2.waitKey(0)

    print("Number of Contours found = " + str(len(contours)))

    # Draw all contours
    # -1 signifies drawing all contours
    # cv2.drawContours(img, contours, -1, (0, 255, 0), 3)

    cv2.imshow('Contours', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def main():
    im = cv2.imread(r'C:\Users\jesse.clark_awardco\Downloads\Drawing.sketchpad.png')
    im[im == 255] = 1
    im[im == 0] = 255
    im[im == 1] = 0
    im2 = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(im2, 127, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for i in range(0, len(contours)):
        if (i % 2 == 0):
            cnt = contours[i]
            # mask = np.zeros(im2.shape,np.uint8)
            # cv2.drawContours(mask,[cnt],0,255,-1)
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.imshow('Features', im)
            cv2.imwrite(str(i) + '.png', im)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main2()
