from vtk import *
from PIL import Image
import numpy as np
import math
import os

# distance between the streamlines (x, y axes)
dx = 0.2

file_name = "/tmp/testcase2/VTK/testcase2_2000.vtk"

reader = vtkUnstructuredGridReader()
reader.SetFileName(file_name)
Data = reader.GetOutput()
reader.Update()
bounds = Data.GetBounds()

xmin, xmax, ymin, ymax, zmin, zmax = bounds
xmin = xmin + 0.3
xmax = xmax - 0.3
ymin = ymin + 0.3
ymax = ymax - 0.3
zmin = zmin + 0.3
zmax = zmax - 0.3

top_z = 9.5
low_z = zmin
low_x = -3.7
top_x = 3.7

npx = int(math.floor(math.fabs((top_x - low_x))/dx))
npz = int(math.floor(math.fabs((top_z - low_z))/dx))

locator = vtkCellLocator()
locator.SetDataSet(Data)
locator.BuildLocator()

cellid = locator.FindCell([0.5,2.8,0.5])
cell = Data.GetCell(cellid)

celldata = Data.GetCellData()
celldata.Update()

velocityarray = celldata.GetArray(8)

def generate_streamline(pointx, pointy, pointz,
                        xmax_, xmin_, ymax_, ymin_, zmax_, zmin_,
                        delta, points_max, outputfile):

    # points counter and stop condition
    
    n_points = 0
    stop = False

    while (stop != True):
        pointid = locator.FindCell([pointx, pointy, pointz])
        # stop if no point can be found
        if pointid == -1:
            stop = True
            norm = vx = vy = vz = vx_n = vy_n = vz_n = 0.0
        # get the velocity data at current point
        else:
            vx, vy, vz = velocityarray.GetTuple(pointid)
            norm = math.sqrt(vx*vx+vy*vy+vz*vz)
            
        # write current point plus the speed of the current point
        outputfile.write(str(pointx) + " " + 
                         str(pointy) + " " + 
                         str(pointz) + " " +
                         str(norm) + "\n")

        # further avoid a lockup if the velocity might become zero
        # and check weather we are not out of bounds
        
        if (((vx == 0.) and (vy == 0.) and (vz == 0.)) 
            or (n_points > points_max) or
            ( pointx > xmax_ ) or (pointx < xmin_) or
            ( pointy > ymax_ ) or (pointy < ymin_) or
            ( pointz > zmax_ ) or (pointz < zmin_)):
            stop = True

        # otherwise calculate the next position from the current position
        else:
            vx_n = vx/norm
            vy_n = vy/norm
            vz_n = vz/norm
            
            pointx = pointx + vx_n*delta
            pointy = pointy + vy_n*delta
            pointz = pointz + vz_n*delta 
            n_points = n_points + 1

k = 0
for i in range (npx):
    for j in range (npz):
        f = open("sline"+ str(k), 'w+')
        generate_streamline(low_x+dx*i, -10, low_z+dx*j,
                            xmax + 0.3, xmin - 0.3,
                            ymax + 0.3, ymin - 0.3,
                            zmax + 0.3, zmin - 0.3, 0.01, 10000, f)
        k = k+1
        f.close()
