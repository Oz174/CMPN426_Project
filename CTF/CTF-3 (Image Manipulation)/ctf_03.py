import cv2

img1 = cv2.imread('first.png')

img2 = cv2.imread('second.png')

cv2.imwrite('result.png', img1+img2)

cv2.imshow('some', img2+img1)
cv2.waitKey()
cv2.destroyWindow('some')
