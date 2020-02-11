"""
Starter code for EECS 442 W20 HW1
"""
from util import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import imageio as im
import skimage.transform
matplotlib.use('TkAgg')


def rotX(theta):
    # TODO: Return the rotation matrix for angle theta around X axis
    R = np.array([[1, 0,0],
    [0, np.cos(theta), -np.sin(theta)],
    [0, np.sin(theta), np.cos(theta)]])
    return R


def rotY(theta):
    # TODO: Return the rotation matrix for angle theta around Y axis
    R = np.array([[np.cos(theta), 0, np.sin(theta)],
    [0,1,0],
    [-np.sin(theta), 0, np.cos(theta)]])
    return R

# done
def part1():
    # a
    N = 30
    R = [rotY(theta) for theta in np.linspace(0, 2*np.pi, N)]
    generate_gif(R)
    # b
    rot1 = rotX(np.pi/4)@ rotY(np.pi/4)
    rot2 = rotY(np.pi/4)@ rotX(np.pi/4)
    renderCube(R = rot1, file_name='rot_b1')
    renderCube(R = rot2, file_name='rot_b2')
    # c
    renderCube(R=(rotX(np.arctan(1/np.sqrt(2)))@rotY(np.pi/4)), file_name='diag_c')
    # d
    renderCube(f=np.inf,R=(rotX(np.arctan(1/np.sqrt(2)))@rotY(np.pi/4)), file_name='diag_d')


# how do we do this func for all pics
def split_triptych(trip, folder="gorskii"):
    # TODO: Split a triptych into thirds and return three channels in numpy arrays
    #ind_h = np.floor(trip.shape[0]/3).astype(int)
    #image = trip[10:-10,:]
    if folder=="tableau":
        n = int(trip.shape[0]/3)
        b,g,r = trip[0:n,20:-20], trip[n:2*n,20:-20], trip[2*n:3*n,20:-20]

    if folder=="gorskii":
        b, g, r = trip[9:336, 9:375], trip[ 347:674,9:375], trip[ 685:1012, 9:375]
    img = np.stack([r,g,b], axis=-1)
    image_mean = np.mean(img, axis = (0,1))
    image_std = np.std(img, axis=(0,1)) 
    img = ((img-image_mean)/image_std)
    return img

def alt_metric(ch1, ch2):
    return np.sum(ch1 * ch2)

def normalized_cross_correlation(ch1, ch2):
    # TODO: Implement the default similarity metric
    return np.sum(ch1/np.linalg.norm(ch1) * (ch2/np.linalg.norm(ch2)))

# np.roll?
def best_offset(ch1, ch2, metric, Xrange=np.arange(-15, 16), Yrange=np.arange(-15, 16)):
    # TODO: Use metric to align ch2 to ch1 and return optimal offsets
    # matrix to hold alignment scores
    scores = np.zeros( (len(Xrange), len(Yrange)))

    # initialize scores
    best_offset = None
    best_score = -np.inf # set this to -np.inf if you're maximizing

     # loop through values
    for i, x in enumerate(Xrange):
        for j, y in enumerate(Yrange):
      
            offset = np.array([x, y])
            # get full matrix of scores?
            x_off = np.roll(ch2,x, axis=0)
            _off = np.roll(x_off, y, axis=1)
            scores[i, j] = metric(ch1, _off)
            if scores[i, j] > best_score:
                best_score = scores[i, j]
                best_offset = offset
    #print(scores)
    print(best_offset, best_score)
    return best_offset


def align_and_combine(R, G, B, metric):
    # TODO: Use metric to align three channels and return the combined RGB image
    r_offset = best_offset(G, R, metric)
    b_offset = best_offset(G, B, metric)
    r_shift = np.roll(R, r_offset[0], axis=0)
    r_shift = np.roll(r_shift, r_offset[1], axis=1)
    b_shift = np.roll(B, b_offset[0], axis=0)
    b_shift = np.roll(b_shift, b_offset[1], axis=1)
    alig = np.stack([r_shift, G, b_shift], axis=-1)
    print("offset 1: {}, offset 2: {}".format(r_offset, b_offset))
    return alig



def build_pyramid(image):
    img = split_triptych(image, "tableau")
    #img = img[10:,10:-20,:]
    
    top_img = skimage.transform.resize(img, (int(img.shape[0]/16), int(img.shape[1]/16)))
    #print(top_img.shape)
    r_top, g_top, b_top = top_img[:,:,0], top_img[:,:,1], top_img[:,:,2]
    #top_alig = align_and_combine(r_top, g_top, b_top, normalized_cross_correlation)
    g_top_offset = best_offset(r_top, g_top, normalized_cross_correlation,np.arange(-10,10),np.arange(-10,10))
    
    b_top_offset = best_offset(r_top, b_top, normalized_cross_correlation,np.arange(-10,10),np.arange(-10,10))
    print("g top offset: {}".format(g_top_offset))
    print("b top offset: {}".format(b_top_offset))
    top_offset = np.array([g_top_offset, b_top_offset])
    #print(top_offset)
    #im.imwrite('top-pyr.jpg', top_alig)

    # mid level processing
    mid_img = skimage.transform.resize(img, (int(img.shape[0]/4), int(img.shape[1]/4)))
    # offset here
    #im.imwrite('preoffset-mid-pyr.jpg', mid_img)
    
    #print(mid_img.shape)
    r_mid, g_mid, b_mid = mid_img[:,:,0], mid_img[:,:,1], mid_img[:,:,2]
    # offset by 4 times top level offset
    g_shift_mid = np.roll(g_mid, 4*g_top_offset[0], axis=0)
    g_shift_mid = np.roll(g_shift_mid, 4*g_top_offset[1], axis=1)
    b_shift_mid = np.roll(b_mid, 4*b_top_offset[0], axis=0)
    b_shift_mid = np.roll(b_shift_mid, 4*b_top_offset[1], axis=1)
    
    mid_img = np.stack([r_mid, g_shift_mid, b_shift_mid], axis=-1)
    r_mid, g_mid, b_mid = mid_img[:,:,0], mid_img[:,:,1], mid_img[:,:,2]
    #im.imwrite('postoffset-mid-pyr.jpg', mid_img)
    #mid_alig = align_and_combine(r_mid, g_mid, b_mid,normalized_cross_correlation)

    g_mid_offset = best_offset(r_mid, g_mid, normalized_cross_correlation,np.arange(-10,10),np.arange(-10,10))
    b_mid_offset = best_offset(r_mid, b_mid, normalized_cross_correlation,np.arange(-10,10),np.arange(-10,10))
    print("g mid offset: {}".format(g_mid_offset))
    print("b mid offset: {}".format(b_mid_offset))
    mid_offset = np.array([g_mid_offset, b_mid_offset])

    r,g,b = img[:,:,0], img[:,:,1], img[:,:,2]

    g_shift_bot = np.roll(g, 4*g_mid_offset[0] + 16*g_top_offset[0], axis=0)
    g_shift_bot = np.roll(g_shift_bot, 4*g_mid_offset[1]+ 16*g_top_offset[1], axis=1)
    b_shift_bot = np.roll(b, 4*b_mid_offset[0]+ 16*b_top_offset[0], axis=0)
    b_shift_bot = np.roll(b_shift_bot, 4*b_mid_offset[1]+ 16*b_top_offset[1], axis=1)
    
    #bot_alig = align_and_combine(r, g_shift_bot, b_shift_bot, normalized_cross_correlation)

    bot_img = np.stack([r, g_shift_bot, b_shift_bot], axis=-1)
    r,g,b = bot_img[:,:,0], bot_img[:,:,1], bot_img[:,:,2]
    g_bot_offset = best_offset(r, g, normalized_cross_correlation,np.arange(-10,10),np.arange(-10,10))
    b_bot_offset = best_offset(r, b, normalized_cross_correlation,np.arange(-10,10),np.arange(-10,10))
    print("g bot offset: {}".format(g_bot_offset))
    print("b bot offset: {}".format(b_bot_offset))
    bot_offset = np.array([g_bot_offset, b_bot_offset])
    
    final_offset = 16*top_offset + 4*mid_offset + bot_offset
    print("g final offset: {}".format(final_offset[0]))
    print("b final offset: {}".format(final_offset[1]))
    #print(final_offset)
    g_shift = np.roll(g, final_offset[0][0], axis=0)
    g_shift = np.roll(g_shift, final_offset[0][1], axis=1)
    b_shift = np.roll(b, final_offset[1][0], axis=0)
    b_shift = np.roll(b_shift, final_offset[1][1], axis=1)
    
    alig = np.stack([r, g_shift, b_shift], axis=-1)
    return alig, final_offset

def align_pic(img,g_offset, b_offset):
    r,g,b = img[:,:,0], img[:,:,1], img[:,:,2]
    g_shift = np.roll(g, g_offset[0], axis=0)
    g_shift = np.roll(g_shift, g_offset[1], axis=1)
    b_shift = np.roll(b, b_offset[0], axis=0)
    b_shift = np.roll(b_shift, b_offset[1], axis=1)
    alig = np.stack([r, g_shift, b_shift], axis=-1)
    return alig

def part2():
    # went through pictures one by one to generate
    split_im = im.imread('prokudin-gorskii/00153v.jpg')
    image = split_triptych(split_im)
    im.imwrite('pre-aligned-00153v.jpg', image)
    
    alig = align_and_combine(R=image[:,:,0], G=image[:,:,1], B=image[:,:,2], metric=normalized_cross_correlation)
    im.imwrite('prokudin-gorskii-aligned/00153v.jpg',alig)

    alt_alig = align_and_combine(R=image[:,:,0], G=image[:,:,1], B=image[:,:,2], metric=alt_metric)
    im.imwrite('alt_00153v.jpg', alt_alig)
    
    vanc = im.imread('tableau/vancouver_tableau.jpg')
    vanc_alig = build_pyramid(vanc)
    fullvanc_alig = align_pic(split_triptych(vanc, "tableau"), vanc_alig[1][0], vanc_alig[1][1])
    im.imwrite('vanc_aligned.jpg', fullvanc_alig)

    seoul = im.imread('tableau/seoul_tableau.jpg')
    seo_alig = build_pyramid(seoul)
    fullseoul_alig = align_pic(split_triptych(seoul, "tableau"), seo_alig[1][0], seo_alig[1][1])
    im.imwrite('seoul_aligned.jpg', fullseoul_alig)
    
    pass

def separate_to_channels(img):
    r,g,b = img[:,:,0], img[:,:,1], img[:,:,2]
    lab = skimage.color.rgb2lab(img[:,:,:3])
    l,a,b2 = lab[:,:,0], lab[:,:,1], lab[:,:,2]
    return r,g,b,l,a,b2

def save_channels(arr, dest):
    im.imwrite(dest + "-r.png", arr[0])
    im.imwrite(dest + "-g.png", arr[1])
    im.imwrite(dest + "-b.png", arr[2])
    im.imwrite(dest + "-l.png", arr[3])
    im.imwrite(dest + "-a.png", arr[4])
    im.imwrite(dest + "-b2.png", arr[5])

def part3():
    indoor = im.imread("rubik/indoor.png")
    ind = separate_to_channels(indoor)
    save_channels(ind, "indoor")

    outdoor = im.imread("rubik/outdoor.png")
    out = separate_to_channels(outdoor)
    save_channels(out, "outdoor")

    q3_part3()
    pass

def q3_part3():
    im1 = plt.imread("q3_part3/im1-orig.jpg")
    im1 = im1[504:3528,:,: ]
    im1 = skimage.transform.resize(im1, (256,256))
    im.imwrite("q3_part3/im1.jpg", im1)
    plt.imshow(im1)
    plt.show()
    im2 = plt.imread("q3_part3/im2-orig.jpg")
    im2 = im2[504:3528,:,: ]
    im2 = skimage.transform.resize(im2, (256,256))
    im.imwrite("q3_part3/im2.jpg", im2)
    plt.imshow(im2)
    plt.show()


def main():
    part1()
    part2()
    part3()


if __name__ == "__main__":
    main()
