import cv2
import numpy as np
from Site.models import ConvertedImage

def detectPlane(filename, hfov, vfov, width, height):
    print(filename)
    # Read the image
    filename = "./static/" + filename
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
    final_image = cv2.drawContours(img, [largest_rectangle], 0, (0, 255, 0), 2)
    path = "convertedImage/" + filename.split('/')[-1].split('.')[0] + "_detected." + filename.split('.')[-1]
    output_filename = "./static/convertedImage/" + filename.split('/')[-1].split('.')[0] + "_detected." + filename.split('.')[-1]
    largest_rectangle.flatten().reshape(-1, 2).tolist()
    cv2.imwrite(output_filename, final_image)
    print(output_filename)

    from django.core.files import File

    corner1_x, corner1_y = largest_rectangle[0]
    corner2_x, corner2_y = largest_rectangle[1]
    corner3_x, corner3_y = largest_rectangle[2]
    corner4_x, corner4_y = largest_rectangle[3]

    with open(output_filename, 'rb') as image_file:
        converted_image = ConvertedImage(
            image=path,
            corner1_x=corner1_x, corner1_y=corner1_y,
            corner2_x=corner2_x, corner2_y=corner2_y,
            corner3_x=corner3_x, corner3_y=corner3_y,
            corner4_x=corner4_x, corner4_y=corner4_y,
            hfov=hfov, vfov=vfov, width=width, height=height
        )
    return converted_image



# REFERENCES FOR TESTING
# corners = detectPlane("test1.jpg")
# print(corners)
# from PaintCalculations import calculateSideLengths, calculateRealArea, getImageDimensions
# side_lengths = calculateSideLengths(corners)

# distance_to_rectangle = 20 # Distance in feet
# hfov = 70 # Horizontal field of view in degrees
# dfov = 77 # Diagonal field of view in degrees

# file_path = "./staticfiles/testImages/test1.jpg"

# image_width, image_height = getImageDimensions(file_path)

# area_feet, area_inches = calculateRealArea(side_lengths, distance_to_rectangle, hfov, vfov, image_width, image_height)
# print(f"Area in square feet: {area_feet}")
# print(f"Area in square inches: {area_inches}")