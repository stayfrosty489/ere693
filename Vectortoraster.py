import numpy,arcpy,os,sys
from arcpy import env
from arcpy.sa import *
arcpy.env.overwriteOutput = True
lie=arcpy.CheckOutExtension ('Spatial')
print lie
shapefiles=[]
stormfolder=1
#r'//hd.ad.syr.edu/02/04e4df/Documents/Desktop/GISModeling/Lab8/
while stormfolder<=4:
    print 'checking folder',stormfolder
    shapefiles=[]
    for root, dirs, files in os.walk('storm'+str(stormfolder)):
        for file in files:
            if file.endswith('.shp'):
                    shapefiles.append('storm'+str(stormfolder)+'/'+file)
    print 'done creating an array of the shapefiles'
    print 'converting to rasters'
    rasters=[]
    for x in range(len(shapefiles)):
        print 'converting',shapefiles[x]
        raster=arcpy.PolygonToRaster_conversion(shapefiles[x], 'value', 'storm'+str(stormfolder)+'/raster'+str(x), 'CELL_CENTER', 'NONE',0.00012196015)
        rasters.append(raster)
    print 'completed raster conversion'
    print 'calculating cell statistics'
    maxreflect=CellStatistics (rasters, 'MAXIMUM', 'DATA')
    maxreflect.save('storm'+str(stormfolder)+'/reflect'+str(stormfolder)+'.tif')
    lowerLeft = arcpy.Point(maxreflect.extent.XMin,maxreflect.extent.YMin)
    cellSize = maxreflect.meanCellWidth
    reflectence=arcpy.RasterToNumPyArray(maxreflect)
    rows=len(reflectence)
    cols=len(reflectence[0])
    rainfallraster=numpy.zeros((rows,cols))
    for row in range(rows):
        for col in range(cols):
            if reflectence[row][col]<0:
                rainfallraster[row][col]=0
            rainfallraster[row][col]=(reflectence[row][col]/300)**(1/1.4)
    where_are_NaNs = numpy.isnan(rainfallraster)
    rainfallraster[where_are_NaNs]=0
    newraster=arcpy.NumPyArrayToRaster(rainfallraster,lowerLeft,cellSize)
    newraster.save('storm'+str(stormfolder)+'/rainfall'+str(stormfolder)+'.tif')
    stormfolder=stormfolder+1
    print 'completed rainfall calc'
    print 'complete with folder',stormfolder
print 'finished making max reflectance rasters'
