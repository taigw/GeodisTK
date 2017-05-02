import geodesic_distance
import numpy as np
import time
from PIL import Image
import matplotlib.pyplot as plt
import vtk
from vtk.util.numpy_support import vtk_to_numpy, numpy_to_vtk
from vtk.vtkIOImagePython import vtkNIFTIImageWriter

def load_vtk_data(imgName):
    if(imgName.endswith('nii')):
        reader=vtk.vtkNIFTIImageReader()
    elif(imgName.endswith('mha')):
        reader = vtk.vtkMetaImageReader()
    else:
        raise ValueError('could not open file {0:}'.format(imgName))
    reader.SetFileName(imgName)
    reader.Update()

    img=reader.GetOutput()
    shape=img.GetDimensions()
    sc = img.GetPointData().GetScalars()
    a = vtk_to_numpy(sc).reshape([shape[2],shape[1],shape[0]])
    return a

def save_vtk_data(data, imgName):
    shape = data.shape
    data = data.reshape([shape[2],shape[1],shape[0]])
    vtk_array = numpy_to_vtk(num_array=data.ravel(), deep=True, array_type=vtk.VTK_UNSIGNED_CHAR)
    # Convert the VTK array to vtkImageData
    img_vtk = vtk.vtkImageData()
    img_vtk.SetDimensions(data.shape)
    img_vtk.SetSpacing([1.0, 1.0, 1.0])
    img_vtk.GetPointData().SetScalars(vtk_array)
    
    writer = vtk.vtkNIFTIImageWriter()
    writer.SetInputData(img_vtk)
    writer.SetFileName(imgName)
    writer.Write()

def test_geodesic_distance3d():
    
    I = load_vtk_data("../data/img3d.nii")
    I = np.asarray(I, np.float32)
    I = I[0:40, 100:150, 100:150]
    S = np.zeros_like(I, np.uint8)
    S[25][25][25] = 1
    t0 = time.time()
    D1 = geodesic_distance.geodesic3d_fast_marching(I,S)
    t1 = time.time()
    D2 = geodesic_distance.geodesic3d_raster_scan(I,S)
    dt1 = t1 - t0
    dt2 = time.time() - t1
    print "runtime(s) fast marching {0:}".format(dt1)
    print "runtime(s) raster scan   {0:}".format(dt2)
    diff = D1 - D2
    print "itensity difference of two methods (mean, std):", diff.mean(), diff.std()
    max_iten = D1.max()
    D1 = D1*255/max_iten
    D1 = np.asarray(D1, np.uint8)
    save_vtk_data(D1, "../data/image3d_dis1.nii")

    max_iten = D2.max()
    D2 = D2*255/max_iten
    D2 = np.asarray(D2, np.uint8)
    save_vtk_data(D2, "../data/image3d_dis2.nii")
    
    
    I = I*255/I.max()
    I = np.asarray(I, np.uint8)
    save_vtk_data(I, "../data/image3d_sub.nii")

if __name__ == '__main__':
    test_geodesic_distance3d()
