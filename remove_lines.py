import numpy as np
import cv2

src = cv2.imread('twinkle1.png')
gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
bw = cv2.adaptiveThreshold(~gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, -2)

horizontal = bw.copy()
vertical = bw.copy()

horizontalsize = horizontal.shape[1] / 40

horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontalsize, 1))

horizontal = cv2.erode(horizontal, horizontalStructure, (-1, -1))
horizontal = cv2.dilate(horizontal, horizontalStructure, (-1, -1))

verticalsize = vertical.shape[0] / 40

verticalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, verticalsize))

vertical = cv2.erode(vertical, verticalStructure, (-1, -1))
vertical = cv2.dilate(vertical, verticalStructure, (-1, -1))

vertical = ~vertical

edges = cv2.adaptiveThreshold(vertical, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 3, -2)

kernel = np.ones((2, 2), np.uint8)
edges = cv2.dilate(edges, kernel)

smooth = np.copy(vertical)
smooth = cv2.blur(smooth, (2, 2))

vertical = np.ma.masked_array(smooth, edges)

cv2.imshow('smooth', vertical)
cv2.waitKey(0)
cv2.destroyAllWindows()
