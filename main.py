import cv2
import numpy as np

img_path = 'b2.jpg'
corX = []
corY = []
vanishing_points = []
real_distance = [0, 0, 0, 0]
colrgb = ['blue', 'green', 'red']

print ("Please Select the points of the Edges:")


def mark_points(event, x, y, flags, param):
    global corX
    global corY
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(param[0], (int(x), int(y)), 4, param[1], -1)
        corX.append(x)
        corY.append(y)


#return vanishing points for x,y and z directions respectively.
def mark_edges(img):
    global corX
    global corY
    global vanishing_points
    for i in range(0, 3):
        print ("Mark 2 Points for ", colrgb[i],  " edge: ")
        color = [0, 0, 0]
        color[i] = 255
        color = tuple(color)
        cv2.namedWindow('select_edges')
        cv2.setMouseCallback('select_edges', mark_points, (img, color))
        while 1:
            cv2.imshow('select_edges', img)
            k = cv2.waitKey(20) & 0xFF
            if k == 27 or corX.__len__() == 6:
                cv2.imshow('select_edges', img)
                cv2.waitKey(20)
                break
            if k == ord("q"):
                exit(1)
                break

        cv2.line(img, (corX[0], corY[0]), (corX[1], corY[1]), color, 4)
        cv2.line(img, (corX[2], corY[2]), (corX[3], corY[3]), color, 4)
        cv2.line(img, (corX[4], corY[4]), (corX[5], corY[5]), color, 4)
        cv2.imshow('select_edges', img)
        cv2.waitKey(20)

        # Store the end-points
        e1 = [corX[0], corY[0], 1]
        e2 = [corX[1], corY[1], 1]
        e3 = [corX[2], corY[2], 1]
        e4 = [corX[3], corY[3], 1]

        # Parameters of lines
        L1 = np.cross(e1, e2)
        L2 = np.cross(e3, e4)

        # Intersection points = cross product of two lines
        V_homogenious = np.cross(L1, L2)

        # making the last coordinte 1 (homogenious co-ordinates)
        if V_homogenious[2] != 0:
            Vh = np.divide(V_homogenious, V_homogenious[2])
        vanishing_points.append(Vh)

        # for next side delete previous ones
        # print(corX)
        # print(corY)
        if i == 0:
            X_0 = corX
            Y_0 = corY
        elif i == 1:
            X_1 = corX
            Y_1 = corY
        else:
            X_2 = corX
            Y_2 = corY

        del corX[:]
        del corY[:]


    Vx = vanishing_points[0]
    Vy = vanishing_points[1]
    Vz = vanishing_points[2]
    print(Vx)
    print(Vy)
    print(Vz)
    return Vx,Vy,Vz


## Marking axes return worl coordinates and references points for axes
def mark_axes(img):
    global corX
    global corY
    print ("click on the origin and then the endpoints of the axes in the same order as you did previously")
    print ("also enter the distance from origin")
    for i in range(0, 4):
        color = [0, 0, 0]
        if i > 0:
            color[(i - 1) % 3] = 255
            color = tuple(color)
        cv2.namedWindow('select_axes')
        cv2.setMouseCallback('select_axes', mark_points, color)
        while 1:
            cv2.imshow('select_axes', img)
            k = cv2.waitKey(20) & 0xFF
            if k == 27 or corX.__len__() == (i + 1) :
                cv2.circle(img, (corX[i], corY[i]), 4, color, -1)
                if i != 0:
                    cv2.line(img, (corX[0], corY[0]), (corX[i], corY[i]), color, 4)
                cv2.imshow('select_axes', img)
                cv2.waitKey(20)
                break
            if k == ord("q"):
                exit(1)
                break

    return corX,corY  #corX[0] = wc, corX[1] = x direction ref point and similar for y and z

mark_edges(cv2.imread('box..jpg'))
mark_axes(cv2.imread('box..jpg'))