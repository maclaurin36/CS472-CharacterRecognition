import numpy as np
import cv2
import json
import pandas as pd

def combineRectangles(rectangle1, rectangle2):
    veryLeftX = rectangle1.leftX if rectangle1.leftX < rectangle2.leftX else rectangle2.leftX
    veryRightX = rectangle1.rightX if rectangle1.rightX > rectangle2.rightX else rectangle2.rightX
    veryUpperY = rectangle1.upperY if rectangle1.upperY < rectangle2.upperY else rectangle2.upperY
    veryLowerY = rectangle1.lowerY if rectangle1.lowerY > rectangle2.lowerY else rectangle2.lowerY
    newRectangle = boundingRectangle()
    newRectangle.leftX = veryLeftX
    newRectangle.rightX = veryRightX
    newRectangle.upperY = veryUpperY
    newRectangle.lowerY = veryLowerY
    newRectangle.width = veryRightX - veryLeftX
    newRectangle.height = veryLowerY - veryUpperY
    return newRectangle

def createRectangleWithTuple(tuple):
    newRectangle = boundingRectangle()
    newRectangle.leftX = tuple[0]
    newRectangle.upperY = tuple[1]
    newRectangle.rightX = tuple[0] + tuple[2]
    newRectangle.lowerY = tuple[1] + tuple[3]
    newRectangle.width = tuple[2]
    newRectangle.height = tuple[3]
    return newRectangle


def getCharacterBoundingBoxes(boundingRectangles):
    # Get the characters (assign columns to same character
    allRectangles = []
    for i in range(len(boundingRectangles)):
        allRectangles.append(createRectangleWithTuple(boundingRectangles[i]))

    allRectangles.sort(key=lambda rectangle: rectangle.leftX)
    finalRectangles = []
    curRectangle = None
    for i, rectangle in enumerate(allRectangles):
        if curRectangle is None:
            curRectangle = rectangle
        if i + 1 == len(allRectangles):
            finalRectangles.append(curRectangle)
            break
        if curRectangle.get_overlaps(allRectangles[i + 1]):
            curRectangle = combineRectangles(curRectangle, allRectangles[i + 1])
        else:
            finalRectangles.append(curRectangle)
            curRectangle = None
    return finalRectangles


def getCroppedImages(finalRectangles, img):
    all_cropped = []
    for rectangle in finalRectangles:
        crop_img = img[int(rectangle.upperY):int(rectangle.lowerY), int(rectangle.leftX):int(rectangle.rightX)]
        (thresh, blackAndWhiteImage) = cv2.threshold(crop_img, 127, 255, cv2.THRESH_BINARY)
        rows, cols, _ = blackAndWhiteImage.shape
        newArray = np.zeros((rows, cols))
        for i in range(rows):
            for j in range(cols):
                if blackAndWhiteImage[i][j][0] == 255:
                    newArray[i][j] = 1
                else:
                    newArray[i][j] = 0
        all_cropped.append(newArray)
    return all_cropped

class boundingRectangle():
    def __init__(self):
        self.leftX = 0
        self.rightX = 0
        self.upperY = 0
        self.lowerY = 0
        self.width = 0
        self.height = 0

    def get_overlaps(self, otherRectangle):
        if otherRectangle.leftX < self.leftX < otherRectangle.rightX:
            return True
        if otherRectangle.leftX < self.rightX < otherRectangle.rightX:
            return True
        if otherRectangle.leftX < self.leftX and otherRectangle.rightX > self.rightX:
            return True
        if self.leftX < otherRectangle.leftX and self.rightX > otherRectangle.rightX:
            return True
        return False

def createFlatCharObjectFromJson(myJson):
    myObject = json.loads(myJson)
    return FlatCharacterObject(np.array(pd.read_json(myObject['dfString'])), myObject['label'])

class FlatCharacterObject:

    def __init__(self, array, label):
        self.dfString = pd.DataFrame(array).to_json()
        self.label = label

    def to_json(self):
        return json.dumps({"dfString":self.dfString, "label":self.label})

    def get_array(self):
        return pd.read_json(self.dfString)


def main2():
    # Read in the image
    img = cv2.imread(r'C:\Users\jesse.clark_awardco\Desktop\All.PNG')

    # Convert the image to grayscale in order to find edges
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find Canny edges
    edged = cv2.Canny(gray, 30, 200)

    cv2.imshow("bla", edged)
    # Get the contours from the image that has been edged
    contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    contours_poly = [None] * len(contours)
    # The Bounding Rectangles will be stored here:
    boundRect = []

    # Alright, just look for the outer bounding boxes:
    for i, c in enumerate(contours):

        # Smooth the shape into a polygon then get the bounding rectangle
        contours_poly[i] = cv2.approxPolyDP(c, 3, True)
        boundRect.append(cv2.boundingRect(contours_poly[i]))

    # Get the characters (assign columns to same character
    finalRectangles = getCharacterBoundingBoxes(boundRect)

    cropped_images = getCroppedImages(finalRectangles, img)
    flatCharacterObject = FlatCharacterObject(cropped_images[8], "3")
    str = flatCharacterObject.to_json()
    flatCharObject2 = createFlatCharObjectFromJson(str)
    for curRectangle in finalRectangles:
        cv2.rectangle(img, (curRectangle.leftX, curRectangle.upperY),
                      (curRectangle.rightX, curRectangle.lowerY), (0, 255, 0), 2)

    # Show the bounded image
    cv2.imshow('Bounded', img)
    cv2.waitKey(0)

    # Show the first cropped bounded image
    crop_img = img[int(boundRect[0][1]):int(boundRect[0][1] + boundRect[0][3]), int(boundRect[0][0]):int(boundRect[0][0] + boundRect[0][2])]
    cv2.imshow("cropped", crop_img)
    print(crop_img)
    cv2.waitKey(0)

    cv2.destroyAllWindows()

if __name__ == '__main__':
    main2()
