import numpy as np
import cv2
import json
import pandas as pd
from FlatCharacterObject import *
import DataExtraction.SlantTransformer

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


def getRawArrays(finalRectangles, img):
    all_cropped = []
    for rectangle in finalRectangles:
        crop_img = img[int(rectangle.upperY):int(rectangle.lowerY), int(rectangle.leftX):int(rectangle.rightX)]
        (thresh, blackAndWhiteImage) = cv2.threshold(crop_img, 127, 255, cv2.THRESH_BINARY)
        rows, cols, _ = blackAndWhiteImage.shape
        newArray = np.zeros((rows, cols))
        for i in range(rows):
            for j in range(cols):
                if blackAndWhiteImage[i][j][0] == 255:
                    newArray[i][j] = 0
                else:
                    newArray[i][j] = 1
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


def writeFile(filePath, label, outPath, clear=False):
    # Read in the image
    img = cv2.imread(filePath)

    # Convert the image to grayscale in order to find edges
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find Canny edges
    edged = cv2.Canny(gray, 30, 200)

    # Get the contours from the image that has been edged
    contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    contours_poly = [None] * len(contours)
    # The Bounding Rectangles will be stored here:
    cv2_bounding_rectangles = []

    # Alright, just look for the outer bounding boxes:
    for i, c in enumerate(contours):
        # Smooth the shape into a polygon then get the bounding rectangle
        contours_poly[i] = cv2.approxPolyDP(c, 3, True)
        cv2_bounding_rectangles.append(cv2.boundingRect(contours_poly[i]))

    # Get the characters (assign columns to same character
    final_rectangles = getCharacterBoundingBoxes(cv2_bounding_rectangles)

    raw_arrays = getRawArrays(final_rectangles, img)

    if clear:
        labelFile = open(outPath, "w")
        labelFile.write("")
        labelFile.close()


    slantTransformer = DataExtraction.SlantTransformer.SlantTransformer()
    labelFile = open(outPath, "a")
    for image_array in raw_arrays:
        currentCharacterObject = FlatCharacterObject(image_array, label)
        slightLeftSlantedCharacterObject = FlatCharacterObject(slantTransformer.getSlantedMatrix(image_array, -0.1), label)
        slightRightSlantedCharacterObject = FlatCharacterObject(slantTransformer.getSlantedMatrix(image_array, 0.1), label)
        majorLeftSlantedCharacterObject = FlatCharacterObject(slantTransformer.getSlantedMatrix(image_array, -1), label)
        majorRightSlantedCharacterObject = FlatCharacterObject(slantTransformer.getSlantedMatrix(image_array, 1), label)
        labelFile.write(currentCharacterObject.to_json())
        labelFile.write('\n')
        labelFile.write(slightLeftSlantedCharacterObject.to_json())
        labelFile.write('\n')
        labelFile.write(slightRightSlantedCharacterObject.to_json())
        labelFile.write('\n')
        labelFile.write(majorLeftSlantedCharacterObject.to_json())
        labelFile.write('\n')
        labelFile.write(majorRightSlantedCharacterObject.to_json())
        labelFile.write('\n')
    labelFile.close()


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

    cropped_images = getRawArrays(finalRectangles, img)
    flatCharacterObject = FlatCharacterObject(cropped_images[8], "3")
    str = flatCharacterObject.to_json()
    flatCharObject2 = createFlatCharObjectFromJson(str)
    arr = flatCharObject2.get_array()
    print(flatCharObject2.dfString)
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
    # main2()
    writeFile(r"C:\Users\jesse.clark_awardco\Desktop\FancyDivides.PNG", "fancyDivide", "characters.txt", True)
    writeFile(r"C:\Users\jesse.clark_awardco\Desktop\DotMultiplies.PNG", "dotMultiply", "characters.txt", False)
    writeFile(r"C:\Users\jesse.clark_awardco\Desktop\AsteriskMultiplies.PNG", "asteriskMultiply", "characters.txt", False)
    writeFile(r"C:\Users\jesse.clark_awardco\Desktop\SlashDivides.PNG", "slashDivide", "characters.txt", False)
    writeFile(r"C:\Users\jesse.clark_awardco\Desktop\XMultiplis.PNG", "XMultiply", "characters.txt", False)
    writeFile(r"C:\Users\jesse.clark_awardco\Desktop\equals.PNG", "equal", "characters.txt", False)
    writeFile(r"C:\Users\jesse.clark_awardco\Desktop\RightParenthesis.PNG", "rightParen", "characters.txt", False)
    writeFile(r"C:\Users\jesse.clark_awardco\Desktop\LeftParenthesis.PNG", "leftParen", "characters.txt", False)
    writeFile(r"C:\Users\jesse.clark_awardco\Desktop\Pluses.PNG", "plus", "characters.txt", False)
    writeFile(r"C:\Users\jesse.clark_awardco\Desktop\Zeros.PNG", "zero", "characters.txt", False)
    writeFile(r"C:\Users\jesse.clark_awardco\Desktop\Nines.PNG", "nine", "characters.txt", False)
    writeFile(r"C:\Users\jesse.clark_awardco\Desktop\Eights.PNG", "eight", "characters.txt", False)
    writeFile(r"C:\Users\jesse.clark_awardco\Desktop\SevensWithCross.PNG", "sevenWithCross", "characters.txt", False)
    writeFile(r"C:\Users\jesse.clark_awardco\Desktop\Sevens.PNG", "seven", "characters.txt", False)
    writeFile(r"C:\Users\jesse.clark_awardco\Desktop\Sixes.PNG", "six", "characters.txt", False)
    writeFile(r"C:\Users\jesse.clark_awardco\Desktop\Fives.PNG", "five", "characters.txt", False)
    writeFile(r"C:\Users\jesse.clark_awardco\Desktop\ConnectedFours.PNG", "fourConnected", "characters.txt", False)
    writeFile(r"C:\Users\jesse.clark_awardco\Desktop\Fours.PNG", "four", "characters.txt", False)
    writeFile(r"C:\Users\jesse.clark_awardco\Desktop\Threes.PNG", "three", "characters.txt", False)
    writeFile(r"C:\Users\jesse.clark_awardco\Desktop\CurvyTwos.PNG", "twoCurvy", "characters.txt", False)
    writeFile(r"C:\Users\jesse.clark_awardco\Desktop\normalTwos.PNG", "two", "characters.txt", False)
    writeFile(r"C:\Users\jesse.clark_awardco\Desktop\FunkyOnes.PNG", "oneFancy", "characters.txt", False)
    writeFile(r"C:\Users\jesse.clark_awardco\Desktop\StraightOnes.PNG", "one", "characters.txt", False)
    # myObjs = readFile("../characters.txt")
    print("done")
