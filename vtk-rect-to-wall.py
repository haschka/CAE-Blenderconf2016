from vtk import *
from PIL import Image
import numpy as np
import math
import os

dx = 0.01

# open vtk file
file_name = "testcase.vtk"

reader = vtkRectilinearGridReader()
reader.SetFileName(file_name)
Data = reader.GetOutput()
reader.Update()
bounds = Data.GetBounds()

xmin, xmax, ymin, ymax, zmin, zmax = bounds

print bounds

npx = int(math.floor((xmax - zmin)/dx))
npy = int(math.floor((ymax - ymin)/dx))
npz = int(math.floor((zmax - zmin)/dx))

# print "Points in x: " + str(npx) + " in y: " + str(npy) + " in z: " + str(npz)

locator = vtkPointLocator()
locator.SetDataSet(Data)
locator.BuildLocator()

pointid = locator.FindClosestPoint([0.,0.,6.])
point = Data.GetPoint(pointid)

pointdata = Data.GetPointData()
pointdata.Update()

densityarray = pointdata.GetArray(0)

mindensity, maxdensity = densityarray.GetValueRange()
prefactor = 254./(maxdensity - mindensity)

print ("Minimum : " + str(mindensity))
print ("Maximum : " + str(maxdensity))
print ("Conversion Factor : " + str(prefactor))

imagedata = []
for k in range(npz):
    for i in range(npx):
        pointid = locator.FindClosestPoint([xmin+dx*i,
                                            ymin+3,
                                            zmin+dx*k])
        if pointid == -1:
            value = 0.0
        else:
            value = prefactor*(densityarray.GetValue(pointid) - mindensity)
        imagedata.append(value)
smalldata = np.array(imagedata,dtype="uint8")
theimage = Image.frombytes('L',(npx,npz),smalldata)
print("Saving Wall")
theimage.save('Wallxz_ymin.png', 'PNG')

imagedata = []
for k in range(npz):
    for i in range(npx):
        pointid = locator.FindClosestPoint([xmin+dx*i,
                                            ymax-3,
                                            zmin+dx*k])
        if pointid == -1:
            value = 0.0
        else:
            value = prefactor*(densityarray.GetValue(pointid) - mindensity)
        imagedata.append(value)
smalldata = np.array(imagedata,dtype="uint8")
theimage = Image.frombytes('L',(npx,npz),smalldata)
print("Saving Wall")
theimage.save('Wallxz_ymax.png', 'PNG')

imagedata = []
for k in range(npz):
    for i in range(npy):
        pointid = locator.FindClosestPoint([xmin+3,
                                            ymin+dx*i,
                                            zmin+dx*k])
        if pointid == -1:
            value = 0.0
        else:
            value = prefactor*(densityarray.GetValue(pointid) - mindensity)
        imagedata.append(value)
smalldata = np.array(imagedata,dtype="uint8")
theimage = Image.frombytes('L',(npy,npz),smalldata)
print("Saving Wall")
theimage.save('Wallyz_xmin.png', 'PNG')

imagedata = []
for k in range(npz):
    for i in range(npy):
        pointid = locator.FindClosestPoint([xmax-3,
                                            ymin+dx*i,
                                            zmin+dx*k])
        if pointid == -1:
            value = 0.0
        else:
            value = prefactor*(densityarray.GetValue(pointid) - mindensity)
        imagedata.append(value)
smalldata = np.array(imagedata,dtype="uint8")
theimage = Image.frombytes('L',(npy,npz),smalldata)
print("Saving Wall")
theimage.save('Wallyz_xmax.png', 'PNG')

imagedata = []
for k in range(npy):
    for i in range(npx):
        pointid = locator.FindClosestPoint([xmax+dx*i,
                                            ymin+dx*k,
                                            zmin+3])
        if pointid == -1:
            value = 0.0
        else:
            value = prefactor*(densityarray.GetValue(pointid) - mindensity)
        imagedata.append(value)
smalldata = np.array(imagedata,dtype="uint8")
theimage = Image.frombytes('L',(npx,npy),smalldata)
print("Saving Wall")
theimage.save('Wallxy_zmin.png', 'PNG')

imagedata = []
for k in range(npy):
    for i in range(npx):
        pointid = locator.FindClosestPoint([xmax+dx*i,
                                            ymin+dx*k,
                                            zmax-3])
        if pointid == -1:
            value = 0.0
        else:
            value = prefactor*(densityarray.GetValue(pointid) - mindensity)
        imagedata.append(value)
smalldata = np.array(imagedata,dtype="uint8")
theimage = Image.frombytes('L',(npx,npy),smalldata)
print("Saving Wall")
theimage.save('Wallxy_zmax.png', 'PNG')
