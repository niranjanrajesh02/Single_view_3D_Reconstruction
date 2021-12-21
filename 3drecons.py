import cv2
import numpy as np

img = cv2.imread('b4.png')

gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,50,150,apertureSize = 3)
######################################################
# lines = cv2.HoughLines(edges,1,np.pi/180,200)
# for rho,theta in lines[0]:
#     a = np.cos(theta)
#     b = np.sin(theta)
#     x0 = a*rho
#     y0 = b*rho
#     x1 = int(x0 + 1000*(-b))
#     y1 = int(y0 + 1000*(a))
#     x2 = int(x0 - 1000*(-b))
#     y2 = int(y0 - 1000*(a))

#     cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)

# cv2.imwrite('houghlines3.jpg',img)
################################################



# As you can see below, the projection of vanishing lines already starts to appear.

# enter image description here

# Now if we play with the parameters for this specific image and skip already-parallel vertical lines, we can get a better set of vanishing lines.

# fine tune parameters
############################################
lines = cv2.HoughLines(edges, 0.7, np.pi/120, 250, min_theta=np.pi/36, max_theta=np.pi-np.pi/36)
for line in lines:
    rho,theta = line[0]
    # skip near-vertical lines
    if abs(theta-np.pi/90) < np.pi/9:
        continue
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 10000*(-b))
    y1 = int(y0 + 10000*(a))
    x2 = int(x0 - 10000*(-b))
    y2 = int(y0 - 10000*(a))
    cv2.line(img,(x1,y1),(x2,y2),(0,0,255),3)

cv2.imwrite('houghlines3.jpg',img)

