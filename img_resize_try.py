import cv2

img = cv2.imread(r"C:\Users\user\Desktop\New folder\IMG_7682.JPG")
scale = 40

width = int(img.shape[1] * scale/100)
height = int(img.shape[0] * scale/100)

dim = (width,height)

im = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

cv2.imwrite(r"C:\Users\user\Desktop\New folder\New folder\hello1.jpg",im)
