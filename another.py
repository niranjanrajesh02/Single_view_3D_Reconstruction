import cv2
import numpy as np

img_path = 'box..jpg'
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
        cv2.circle(param[0], (x, y), 4, param[1], -1)
        corX.append(x)
        corY.append(y)


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
            if k == 27 or corX.__len__() == 4:
                cv2.imshow('select_edges', img)
                cv2.waitKey(20)
                break
            if k == ord("q"):
                exit(1)
                break

        cv2.line(img, (corX[0], corY[0]), (corX[1], corY[1]), color, 4)
        cv2.line(img, (corX[2], corY[2]), (corX[3], corY[3]), color, 4)
        cv2.line(img, (corX[2], corY[2]), (corX[3], corY[3]), color, 4)
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
        del corX[:]
        del corY[:]


# mark the axes and input the distance from origin
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
        if i != 0:
            print ("please mention the distance from origin for "), colrgb[i-1], " axis"
            real_distance[i] = input(": ")


# main program

def main():
    global corX
    global corY
    global vanishing_points

    image = cv2.imread(img_path)
    img = image.copy()
    mark_edges(img)

    print

    img = image.copy()
    mark_axes(img)

    origin = [corX[0], corY[0], 1]
    # transpose
    O = np.array([origin]).T

    ref1 = np.array([[corX[1], corY[1], 1]]).T
    ref2 = np.array([[corX[2], corY[2], 1]]).T
    ref3 = np.array([[corX[3], corY[3], 1]]).T

    print ("Vanishing points:")
    print (vanishing_points)

    # transpose
    Vx = np.array([list(vanishing_points[0])]).T
    Vy = np.array([list(vanishing_points[1])]).T
    Vz = np.array([list(vanishing_points[2])]).T

    # scaling factor
    ax = (np.linalg.lstsq(Vx, ref1 - O)[0]) / real_distance[1]
    by = (np.linalg.lstsq(Vy, ref2 - O)[0]) / real_distance[2]
    cz = (np.linalg.lstsq(Vz, ref3 - O)[0]) / real_distance[3]

    # scaled
    Vxs = (Vx * ax[0][0]).flatten()
    Vys = (Vy * by[0][0]).flatten()
    Vzs = (Vz * cz[0][0]).flatten()

    # Projective matrix
    P = np.array([Vxs, Vys, Vzs, origin]).T

    print
    print ("Projection matrix: \n", P)

    img = image.copy()

    # xy img plane
    Hxy = P[:, [0, 1, 3]]
    pxy = cv2.warpPerspective(img, Hxy, (1000, 1000), flags=cv2.WARP_INVERSE_MAP)
    cv2.imshow('img_xy', pxy)
    cv2.imwrite('planexy.png', pxy)

    # xz img plane
    Hxz = P[:, [0, 2, 3]]
    pxz = cv2.warpPerspective(img, Hxz, (1000, 1000), flags=cv2.WARP_INVERSE_MAP)
    cv2.imshow('img_xz', pxz)
    cv2.imwrite('planexz.png', pxz)

    # yz img plane
    Hyz = P[:, [1, 2, 3]]
    pyz = cv2.warpPerspective(img, Hyz, (1000, 1000), flags=cv2.WARP_INVERSE_MAP)
    cv2.imshow('img_yz', pyz)
    cv2.imwrite('planeyz.png', pyz)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()