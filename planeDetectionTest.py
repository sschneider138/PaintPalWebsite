import cv2
import numpy as np

# Read the image
filename = "test5.jpg"
img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)

# Apply Gaussian blur to remove noise
img = cv2.GaussianBlur(img, (5, 5), 0)

# Apply Canny edge detection
edges = cv2.Canny(img, 0, 100)

# Find contours
contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Iterate over the contours and find the largest rectangle (this assumes that the planar surface is a rectangle)
max_area = -1
for contour in contours:
    rect = cv2.minAreaRect(contour)
    box = cv2.boxPoints(rect)
    box = np.intp(box)
    area = cv2.contourArea(box)
    #cv2.drawContours(img, [contour], 0, (0, 0, 255), 2)
    if area > max_area:
        max_area = area
        largest_rectangle = box

# Draw the largest rectangle
img = cv2.imread(filename, cv2.IMREAD_COLOR)
cv2.drawContours(img, [largest_rectangle], 0, (0, 255, 0), 2)

# Display the image
cv2.imshow('Test', img)
cv2.waitKey(0)
cv2.destroyAllWindows()