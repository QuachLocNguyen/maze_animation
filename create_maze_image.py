import numpy as np
import cv2

# Define the map
MAP = """
##############################
#         #              #   #
# ####    ########       #   #
#    #    #              #   #
#    ###     #####  ######   #
#      #   ###   #           #
#      #     #   #  #  #   ###
#     #####    #    #  #     #
#              #       #     #
##############################
"""

# Convert map to a list
MAP = [list(x) for x in MAP.split("\n") if x]
M = 10
N = 30
W = 21
mau_xanh  = np.zeros((W,W,3), np.uint8) + (np.uint8(255), np.uint8(0), np.uint8(0))
mau_trang = np.zeros((W,W,3), np.uint8) + (np.uint8(255), np.uint8(255), np.uint8(255))
image = np.ones((M*W, N*W, 3), np.uint8)*255

for x in range(0, M):
    for y in range(0, N):
        if MAP[x][y] == '#':
            image[x*W:(x+1)*W, y*W:(y+1)*W] = mau_xanh
        elif MAP[x][y] == ' ':
            image[x*W:(x+1)*W, y*W:(y+1)*W] = mau_trang

cv2.imwrite('maze.bmp', image)
