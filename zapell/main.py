"""
main.py for HW3.

feel free to include libraries needed
"""
import numpy as np
from matplotlib import pyplot as plt
from common import read_img, save_img
import cv2
import os
import random

def homography_transform(X, H):
    # Perform homography transformation on a set of points X
    # using homography matrix H
    #
    # Input - a set of 2D points in an array with size (N,2)
    #         a 3*3 homography matrix
    # Output - a set of 2D points in an array with size (N,2)
    ones = np.ones((len(X), 1))
    X = np.hstack((X, ones))
    #print(X)
    Y = np.matmul(H, X.T).T
    #print(Y)

    return Y[:,:2]/Y[:,2:3]
    #.reshape((3,1))


def fit_homography(XY):
    # Given two set of points X, Y in one array,
    # fit a homography matrix from X to Y
    #
    # Input - an array with size(N,4), each row contains two
    #         points in the form[x^T_i,y^T_i]1×4
    # Output - a 3*3 homography matrix
    X = XY[:,:2]
    Y = XY[:, 2:]
    n = len(XY)
    A = np.ones((2*n,9))
    for i in range(0,2*n, 2):
        arr1 = np.array([0,0,0,-X[i//2,0],-X[i//2,1],-1, Y[i//2,1]*X[i//2,0], Y[i//2,1]*X[i//2,1], Y[i//2,1]])
        A[i] = arr1
        arr2 = np.array([X[i//2,0],X[i//2,1],1,0,0,0, -Y[i//2,0]*X[i//2,0], -Y[i//2,0]*X[i//2,1], -Y[i//2,0]])
        A[i+1] = arr2
    w,v = np.linalg.eig(np.matmul(A.T, A))
    mi = np.argmin(w)
    #print(v)
    H = v[:,mi].reshape((3,3))
    H = H/H[2,2]
    return H


def p1():
    # code for Q1.2.3 - Q1.2.5
    # 1. load points X from p1/transform.npy
    X = np.load('./p1/transform.npy')
    # 2. fit a transformation y=Sx+t
    n = len(X)
    Y = X[:, 2:]
    X = X[:,:2]
    A = np.ones((2*n,6))
    b = np.ones((2*n, 1))
    for i in range(0,2*n, 2):
        arr = np.array([X[i//2,0], X[i//2,1], 0, 0, 1, 0])
        A[i] = arr
        arr1 = np.array([0,0,X[i//2,0], X[i//2,1], 0, 1])
        A[i+1] = arr1

        b[i] = Y[i//2,0]
        b[i+1] = Y[i//2,1]

    v = np.matmul(np.linalg.inv(np.matmul(A.T, A)), np.matmul(A.T, b))
    t = v[-2:]
    s = v[:4].reshape((2,2))
    print('s: ' , s,'t :', t)
    
    # 3. transform the points
    y_hat = np.matmul(s,X.T) + t

    # 4. plot the original points and transformed points
    plt.scatter(X[:,0],X[:,1], c="blue")
    plt.scatter(Y[:,0], Y[:,1], c='red')
    plt.scatter(y_hat.T[:,0], y_hat.T[:,1], c='green')
    plt.savefig('./1.2.4_plot.png')
    plt.close()


    # code for Q1.2.6 - Q1.2.8
    case = 8  # you will encounter 8 different transformations
    for i in range(case):
        XY = np.load('p1/points_case_'+str(i)+'.npy')
        # 1. generate your Homography matrix H using X and Y
        #
        #    specifically: fill function fit_homography()
        #    such that H = fit_homography(XY)
        H = fit_homography(XY)
        #print(i, H)
        # 2. Report H in your report
        #print(H)
        # 3. Transform the points using H
        #
        #    specifically: fill function homography_transform
        #    such that Y_H = homography_transform(X, H)
        Y_H = homography_transform(XY[:, :2], H)
        # 4. Visualize points as three images in one figure
        # the following code plot figure for you
        plt.scatter(XY[:, 1], XY[:, 0], c="red")  # X
        plt.scatter(XY[:, 3], XY[:, 2], c="green")  # Y
        plt.scatter(Y_H[:, 1], Y_H[:, 0], c="blue")  # Y_hat
        plt.savefig('./case_'+str(i))
        plt.close()


def euclidean_dist(X, Y):
    """
    Inputs:
    - X: A numpy array of shape (N, F)
    - Y: A numpy array of shape (M, F)

    Returns:
    A numpy array D of shape (N, M) where D[i, j] is the Euclidean distance
    between X[i] and Y[i].
    """
    nrm = np.linalg.norm(X, axis=1, keepdims=True)
    D = nrm**2 + np.linalg.norm(Y, axis=1, keepdims=True).T**2 - 2* np.dot(X, Y.T)
    D = np.sqrt(np.clip(D,0,None))
    return D


def stitchimage(imgleft, imgright):
    left = cv2.cvtColor(imgleft,cv2.COLOR_BGR2GRAY)
    right = cv2.cvtColor(imgright,cv2.COLOR_BGR2GRAY)
    # 1. extract descriptors from images
    #    you may use SIFT/SURF of opencv
    sift = cv2.xfeatures2d.SIFT_create()
    kp_l, des_l = sift.detectAndCompute(left,None)
    kp_r, des_r = sift.detectAndCompute(right,None)

    # input data
    X = np.array([(int(round(k.pt[0])), int(round(k.pt[1]))) for k in kp_l])
    # transformed data
    Y = np.array([(int(round(k.pt[0])), int(round(k.pt[1]))) for k in kp_r])

    des_dist = euclidean_dist(des_l/ np.linalg.norm(des_l), des_r/ np.linalg.norm(des_r))

    matches = []
    for i in range(0, len(des_dist)):
        y = np.argpartition(des_dist[i], 2)
        if (y[0]/y[1]) > .7:
            matches.append([i, np.argmin(des_dist[i])])

    d_m = []
    idx_left = [m[0] for m in matches]
    idx_right = [m[1] for m in matches]
    
    for i in range(0,len(matches)):
        dm = cv2.DMatch(idx_left[i], idx_right[i], des_dist[int(idx_left[i]), int(idx_right[i])])
        d_m.append(dm)

    x_pts = [X[i] for i in idx_left]
    y_pts = [Y[i] for i in idx_right]
    XY = np.hstack((x_pts,y_pts))
    # 2. select paired descriptors
    # 3. run RANSAC to find a transformation
    #    matrix which has most innerliers
    res = ransac(XY, .5, 10000)
    print(res)
    out = np.ones((left.shape[1] + 400, left.shape[0]+70))
    print('out', out.shape)
    # 4. warp one image by your transformation
    #    matrix
    #
    #    Hint:
    #    a. you can use function of opencv to warp image
    #    b. Be careful about final image size
    # bbb 180, 70
    # uttower 800, 300
    trans = np.array([[1,0,180],
    [0,1,70],
    [0,0,1]], dtype=np.float32)

    im = cv2.warpPerspective(imgleft.astype(np.float),trans@res[0],out.shape)
    bl = [0,0,1]
    br = [0,568,1]
    tl = [599,0,1]
    tr = [599,568,1]
    nbl = res[0]@bl
    nbr = res[0]@br
    ntl = res[0]@tl
    ntr = res[0]@tr

    trans2 = np.array([[1,0,180],
    [0,1,70]], dtype=np.float32)
    im_right = cv2.warpAffine(imgright.astype(np.float), trans2, out.shape)

    print(nbl, nbr, ntl, ntr)
    # 5. combine two images, use average of them
    #    in the overlap area
    
    left_vals = im > 0
    right_vals = im_right > 0
    for j in range(im.shape[1]):
        for i in range(im.shape[0]):
            for k in range(im.shape[2]):

                if left_vals[i,j][k] and right_vals[i,j][k]:
                    im[i,j][k] = (im[i,j][k] + im_right[i,j][k])/2
                if not left_vals[i,j][k] and right_vals[i,j][k]:
                    im[i,j][k] = im_right[i,j][k]


    return im


def ransac(pts, threshold, Ntrials):
    X, Y = np.array(pts[:,:2]), np.array(pts[:,2:])

    best, bestCount, bestAvgResid = None, -1, -1
    for i in range(Ntrials):
        subset = pts[np.random.choice(X.shape[0], 4, replace=False), :]
        h = fit_homography(subset)

        y_hat = homography_transform(X, h)
        d = np.linalg.norm(Y - y_hat, axis=1)
        avgResid = np.mean(d[d<threshold])
        num_inliers = np.count_nonzero(d < threshold)

        if num_inliers > bestCount:
            bestCount = num_inliers
            best = h
            bestAvgResid = avgResid
    print(bestAvgResid, bestCount)

    return best, bestCount





def p2(p1, p2, savename):
    # read left and right images
    imgleft = read_img(p1)
    imgright = read_img(p2)
    # stitch image
    output = stitchimage(imgleft, imgright)
    # save stitched image
    save_img(output, './{}.jpg'.format(savename))


if __name__ == "__main__":
    # Problem 1
    p1()

    # Problem 2
    # 2.1
    # switch in uttower/bbb
    
    left = cv2.imread('./p2/bbb_left.jpg')
    left = cv2.cvtColor(left, cv2.COLOR_BGR2GRAY)
    plt.imsave("grey_bbb_left.jpg", left, cmap='gray')

    right = cv2.imread('./p2/bbb_right.jpg')
    right = cv2.cvtColor(right, cv2.COLOR_BGR2GRAY)
    plt.imsave("grey_bbb_right.jpg", right, cmap='gray')
    
    # 2.2
    sift = cv2.xfeatures2d.SIFT_create()
    # left keypoint detection
    kpleft = sift.detect(left,None)
    left_kp_img = cv2.drawKeypoints(left,kpleft,np.array([]),flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    cv2.imwrite('sift_keypoints_left_bbb.jpg', left_kp_img)

    # right keypoint detection
    kpright = sift.detect(right, None)
    right_kp_img = cv2.drawKeypoints(right, kpright, np.array([]), flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    cv2.imwrite('sift_keypoints_right_bbb.jpg', right_kp_img)

   
    sift = cv2.xfeatures2d.SIFT_create()

    kp_l, des_l = sift.detectAndCompute(left,None)
    kp_r, des_r = sift.detectAndCompute(right,None)

    des_dist = euclidean_dist(des_l/ np.linalg.norm(des_l), des_r/ np.linalg.norm(des_r))
    matches = []
    print(des_dist.shape)
    for i in range(0, len(des_dist)):
        y = np.argpartition(des_dist[i], 2)
        if (y[0]/y[1]) > .7:
            matches.append([i, np.argmin(des_dist[i])])

    d_m = []
    idx_left = [m[0] for m in matches]
    idx_right = [m[1] for m in matches]
    
    for i in range(0,len(matches)):
        dm = cv2.DMatch(idx_left[i], idx_right[i], des_dist[int(idx_left[i]), int(idx_right[i])])
        d_m.append(dm)
    
    mtc = cv2.drawMatches(left, kp_l, right, kp_r, d_m[:50], np.array([]))
    cv2.imwrite('./bbb_matches.png', mtc)
"""
    #p2('p2/uttower_left.jpg', 'p2/uttower_right.jpg', 'uttower')
    #p2('p2/bbb_left.jpg', 'p2/bbb_right.jpg', 'bbb')

    # Problem 3
    # add your code for implementing Problem 3
    #
    # Hint:
    # you can reuse functions in Problem 2

    # p3
    
    orig = read_img('./front_view.jpg')
    orig_g = cv2.cvtColor(orig,cv2.COLOR_BGR2GRAY)
    #plt.imshow(orig_g, cmap='gray')
    #plt.show()

    patt = read_img('./block_m.jpeg')
    patt_g = cv2.cvtColor(patt,cv2.COLOR_BGR2GRAY)

    sift = cv2.xfeatures2d.SIFT_create()
    kp_l, des_l = sift.detectAndCompute(orig_g,None)
    kp_r, des_r = sift.detectAndCompute(patt_g,None)

    # input data
    X = np.array([(int(round(k.pt[0])), int(round(k.pt[1]))) for k in kp_l])
    # transformed data
    Y = np.array([(int(round(k.pt[0])), int(round(k.pt[1]))) for k in kp_r])

    des_dist = euclidean_dist(des_l/ np.linalg.norm(des_l), des_r/ np.linalg.norm(des_r))

    matches = []
    for i in range(0, len(des_dist)):
        y = np.argpartition(des_dist[i], 2)
        if (y[0]/y[1]) > .7:
            matches.append([i, np.argmin(des_dist[i])])

    d_m = []
    idx_left = [m[0] for m in matches]
    idx_right = [m[1] for m in matches]
    
    for i in range(0,len(matches)):
        dm = cv2.DMatch(idx_left[i], idx_right[i], des_dist[int(idx_left[i]), int(idx_right[i])])
        d_m.append(dm)

    x_pts = [X[i] for i in idx_left]
    y_pts = [Y[i] for i in idx_right]
    XY = np.hstack((x_pts,y_pts))
   
    # 4. warp one image by your transformation
    #    matrix
    
    scale = np.array([[.5,0],
    [0,.5]], dtype=np.float32)

    trans2 = np.array([[1,0,620],
    [0,1,1000]], dtype=np.float32)


    im = cv2.warpAffine(patt.astype(np.float), scale@trans2, orig_g.shape)
    print(im.shape)
    # 5. combine two images, use average of them
    #    in the overlap area
    
    left_vals = im > 0
    right_vals = orig > 0
    for j in range(im.shape[1]):
        for i in range(im.shape[0]):
            for k in range(im.shape[2]):

                if left_vals[i,j][k] and right_vals[i,j][k]:
                    im[i,j][k] = (im[i,j][k] + orig[i,j][k])/2
                if not left_vals[i,j][k] and right_vals[i,j][k]:
                    im[i,j][k] = orig[i,j][k]


    plt.imshow(im)
    plt.show()
    """