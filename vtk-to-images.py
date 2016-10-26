from vtk import *
from PIL import Image
import numpy as np
import math
import os

dx = 0.01

# open vtk file
file_name = "testcase2_800.vtk"

reader = vtkUnstructuredGridReader()
reader.SetFileName(file_name)
Data = reader.GetOutput()
reader.Update()
bounds = Data.GetBounds()

xmin, xmax, ymin, ymax, zmin, zmax = bounds

print bounds

npx = int(math.floor((xmax - xmin)/dx))
npy = int(math.floor((ymax - ymin)/dx))
npz = int(math.floor((zmax - zmin)/dx))

print "Points in x: " + str(npx) + " in y: " + str(npy) + " in z: " + str(npz)

locator = vtkCellLocator()
locator.SetDataSet(Data)
locator.BuildLocator()

cellid = locator.FindCell([0.5,2.8,0.5])
cell = Data.GetCell(cellid)

celldata = Data.GetCellData()
celldata.Update()

densityarray = celldata.GetArray(5)

mindensity, maxdensity = densityarray.GetValueRange()
prefactor = 254./(maxdensity - mindensity)


for k in range(npz):
    imagedata = []
    for i in range(npx):
        for j in range(npy):
            cellid = locator.FindCell([xmin+dx*i,ymin+dx*j,zmin+dx*k])
            if cellid == -1:
                value = 0.0;
            else:
                value = prefactor*(densityarray.GetValue(cellid) - mindensity)
            imagedata.append(value)
    smalldata = np.array(imagedata,dtype="uint8")
    print "Saving image: " + str(k) 
    theimage = Image.frombytes('L',(npy,npx),smalldata)
    theimage.save('image' + '%04d' % k + '.png', 'PNG')
