from vtk import *
from PIL import Image
import numpy as np
import math
import os

dx = 0.01

# open vtk file
file_name = "/home/haschka/Downloads/VTK/three_tube_U+V+W+T.vtk"

reader = vtkRectilinearGridReader()
reader.SetFileName(file_name)
Data = reader.GetOutput()
reader.Update()
bounds = Data.GetBounds()

xmin, xmax, ymin, ymax, zmin, zmax = bounds

print bounds

npz = int(math.floor((zmax - zmin)/dx))

# print "Points in x: " + str(npx) + " in y: " + str(npy) + " in z: " + str(npz)

locator = vtkPointLocator()
locator.SetDataSet(Data)
locator.BuildLocator()

pointid = locator.FindClosestPoint([0.,0.,6.])
point = Data.GetPoint(pointid)

pointdata = Data.GetPointData()
pointdata.Update()

densityarray = pointdata.GetArray(1)

mindensity, maxdensity = densityarray.GetValueRange()
prefactor = 254./(maxdensity - mindensity)

print ("Minimum : " + str(mindensity))
print ("Maximum : " + str(maxdensity))
print ("Conversion Factor : " + str(prefactor))

r = 0.07
npt = int(math.floor(2.*math.pi/dx))

print npt

imagedata = []
for k in range(npz):
    for i in range(npt):
        pointid = locator.FindClosestPoint([r*math.cos(dx*i),
                                            r*math.sin(dx*i),
                                            zmin+dx*k])
        if pointid == -1:
            value = 0.0;
        else:
            value = prefactor*(densityarray.GetValue(pointid) - mindensity)
        imagedata.append(value)
smalldata = np.array(imagedata,dtype="uint8")
#print "Saving image: " + str(k) 
theimage = Image.frombytes('L',(npt,npz),smalldata)
theimage.save('cylinder.png', 'PNG')
