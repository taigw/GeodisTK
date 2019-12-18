import GeodisTK
import numpy as np
import time
from PIL import Image
import matplotlib.pyplot as plt


def geodesic_distance_2d(I, S, lamb, iter):
    '''
    get 2d geodesic disntance by raser scanning.
    I: input image
    S: binary image where non-zero pixels are used as seeds
    lamb: weighting betwween 0.0 and 1.0
          if lamb==0.0, return spatial euclidean distance without considering gradient
          if lamb==1.0, the distance is based on gradient only without using spatial distance
    iter: number of iteration for raster scanning.
    '''
    return GeodisTK.geodesic2d_raster_scan(I, S, lamb, iter)

def test_geodesic_distance2d(img, seed_pos):
    I = np.asanyarray(img, np.float32)
    S = np.zeros((I.shape[0], I.shape[1]), np.uint8)
    S[seed_pos[0]][seed_pos[1]] = 1
    t0 = time.time()
    D1 = GeodisTK.geodesic2d_fast_marching(I,S)
    t1 = time.time()
    D2 = geodesic_distance_2d(I, S, 1.0, 2)
    dt1 = t1 - t0
    dt2 = time.time() - t1
    D3 = geodesic_distance_2d(I, S, 0.0, 2)
    D4 = geodesic_distance_2d(I, S, 0.5, 2)
    print("runtime(s) of fast marching {0:}".format(dt1))
    print("runtime(s) of raster  scan  {0:}".format(dt2))

    plt.figure(figsize=(15,5))
    plt.subplot(1,5,1); plt.imshow(img)
    plt.autoscale(False);  plt.plot([seed_pos[0]], [seed_pos[1]], 'ro')
    plt.axis('off'); plt.title('(a) input image \n with a seed point')
    
    plt.subplot(1,5,2); plt.imshow(D1)
    plt.axis('off'); plt.title('(b) Geodesic distance \n based on fast marching')
    
    plt.subplot(1,5,3); plt.imshow(D2)
    plt.axis('off'); plt.title('(c) Geodesic distance \n based on ranster scan')

    plt.subplot(1,5,4); plt.imshow(D3)
    plt.axis('off'); plt.title('(d) Euclidean distance')

    plt.subplot(1,5,5); plt.imshow(D4)
    plt.axis('off'); plt.title('(e) Mexture of Geodesic \n and Euclidean distance')
    plt.show()

def test_geodesic_distance2d_gray_scale_image():
    img = Image.open('data/img2d.png').convert('L')
    seed_position = [100, 100]
    test_geodesic_distance2d(img, seed_position)

def test_geodesic_distance2d_RGB_image():
    img = Image.open('data/ISIC_546.jpg')
    seed_position = [128, 128]
    test_geodesic_distance2d(img, seed_position)

if __name__ == '__main__':
    test_geodesic_distance2d_gray_scale_image()
    # test_geodesic_distance2d_RGB_image()