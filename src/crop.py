import cv2 as cv

img = cv.imread('frames/frame_8.png')
cropped_img = img[0:100, 750:]
cv.imshow('cropped', cropped_img)
cv.waitKey(0)
# cropped_img.imwrite('cropped.png')
