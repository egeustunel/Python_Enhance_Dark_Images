from builtins import print
from scipy import ndimage
import numpy as np
from skimage import io, color
from math import pi, sqrt, exp
import matplotlib.pyplot as plt
import cv2
import os
from PIL import  Image


def part1(flashed, flashedBW, nonflashed, nonflashedBW):
    flashedFloat = flashed.astype(float)

    # Obtaining color layer

    flashedFloat[:, :, 0] = flashedFloat[:, :, 0] / flashedBW.astype(float)
    flashedFloat[:, :, 1] = flashedFloat[:, :, 1] / flashedBW.astype(float)
    flashedFloat[:, :, 2] = flashedFloat[:, :, 2] / flashedBW.astype(float)

    # Applying bilateral filter on both bw images

    nonflashedBWLargeScale = cv2.bilateralFilter(nonflashedBW, 5, 10, 10)
    flashedBWLargeScale = cv2.bilateralFilter(flashedBW, 5, 10, 10)

    cv2.imwrite("part1/nonflashedBWLargeScale.jpg", nonflashedBWLargeScale)
    cv2.imwrite("part1/flashedBWLargeScale.jpg", flashedBWLargeScale)

    # Obtaining edge sharpness details

    sharpnessInfo = flashedBW.astype(float) / flashedBWLargeScale.astype(float)


    details = sharpnessInfo * nonflashedBWLargeScale
    flashedFloat[:, :, 0] = flashedFloat[:, :, 0] * details
    flashedFloat[:, :, 1] = flashedFloat[:, :, 1] * details
    flashedFloat[:, :, 2] = flashedFloat[:, :, 2] * details

    enhanced = flashedFloat.astype('uint8')

    return enhanced


def part2(flashed, flashedBW, nonflashed, nonflashedBW):
    # This function simply converts the image to BW with intensity-color decoupling method in the appendix

    flashedFloat = flashed.astype(float)

    flashedBWDecoupled = ((flashedFloat[:, :, 0] * flashedFloat[:, :, 0]) / (
            flashedFloat[:, :, 0] + flashedFloat[:, :, 1] + flashedFloat[:, :, 2])) + (
                                 (flashedFloat[:, :, 1] * flashedFloat[:, :, 1]) / (
                                 flashedFloat[:, :, 0] + flashedFloat[:, :, 1] + flashedFloat[:, :, 2])) + (
                                 (flashedFloat[:, :, 2] * flashedFloat[:, :, 2]) / (
                                 flashedFloat[:, :, 0] + flashedFloat[:, :, 1] + flashedFloat[:, :, 2]))
    flashedBWDecoupled = flashedBWDecoupled.astype('uint8')

    # Once we got the BW version of the flashed image, the rest of the operation is the same
    enhanced = part1(flashed, flashedBWDecoupled, nonflashed, nonflashedBW)

    return enhanced


def bonus(flashed, flashedBW, nonflashed, nonflashedBW):

    return


def main():
    try:
        if not os.path.exists("part1/"):
            os.makedirs("part1/")
    except OSError:
        print('Error: Creating directory. ')

    # Reading the images
    flashed = cv2.imread("images/flash.jpg")
    flashedBW = cv2.imread("images/flash.jpg", 0)

    nonflashed = cv2.imread("images/no-flash.jpg")
    nonflashedBW = cv2.imread("images/no-flash.jpg", 0)

    enhanced = part1(flashed, flashedBW, nonflashed, nonflashedBW)
    enhancedDecoupled = part2(flashed, flashedBW, nonflashed, nonflashedBW)
    #bonus(flashed, flashedBW, nonflashed, nonflashedBW)

    # show/save result images
    # cv2.imshow('im', nonflashed)
    cv2.imwrite("part1/nonflashed.jpg", nonflashed)
    #cv2.waitKey()
    # cv2.imshow('im', flashed)
    cv2.imwrite("part1/flashed.jpg", flashed)
    #cv2.waitKey()
    # cv2.imshow('im', enhanced)
    cv2.imwrite("part1/enhanced.jpg", enhanced)
    #cv2.waitKey()
    # cv2.imshow('im', enhancedDecoupled)
    cv2.imwrite("part1/enhancedDecoupled.jpg", enhancedDecoupled)
    #cv2.waitKey()

    return


main()
