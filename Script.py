#Created by Tyler Pitts
# Lab 9
import numpy,arcpy,os,sys
from arcpy import env
from arcpy.sa import *

arcpy.env.overwriteOutput = True
lie=arcpy.CheckOutExtension ('Spatial')
print lie
print 'importing files'
existinglanduse='Lab06Data.gdb/LanduseExisting'
futurelanduse='Lab06Data.gdb/LanduseFuture'
imprev='Lab06Data.gdb/Impervious'
lakes='Lab06Data.gdb/Lakes'
soils='Lab06Data.gdb/Soils'
DEM='Lab06Data.gdb/DEM'
Mask='Lab06Data.gdb/AnalysisMask'
BMPs='Lab06Data.gdb/BMPs'
StreamPoints='Lab06Data.gdb/StreamInvPts'
print 'completed inmporting files'
landuses=[existinglanduse,futurelanduse]
print 'creating flow direction'
filledDEM=Fill(DEM, "")
filledDEM.save('Lab06Data.gdb/filledDEM')
flowdirect=FlowDirection(filledDEM)
flowdirect.save('Lab06Data.gdb/flowdirect')
count=0
flowarray1=[]
flowarray2=[]
while count<2:
    
    count=count+1
    print count
    
    print 'creating union'
    in_features=[landuses[count-1],imprev,lakes]
    arcpy.Union_analysis(in_features, 'Lab06Data.gdb/Unionexisiting'+str(count))
    Unionfeature='Lab06Data.gdb/Unionexisiting'+str(count)
    print 'Union complete'
    
    fields=['total_N','total_P','Cu','Zn','Sediment','FecalColiform']
    for value in range(len(fields)):
        print 'adding', fields[value],'field'
        arcpy.AddField_management (Unionfeature, fields[value], 'DOUBLE')
        
    Unioncursor=arcpy.UpdateCursor('Lab06Data.gdb/Unionexisiting'+str(count),['Reclassify','total_N','total_P','Cu','Zn','Sediment','FecalColiform'])

    check=True
    print 'fields added'
    print 'populating fields'
    while check==True:
        for row in Unioncursor:
            classification=row.getValue('Reclassify')
    ##        print 'assigning', classification, 'values'
            if classification=='Low Density Residential':
                row.setValue('total_N',float(6.4))
                row.setValue('total_P',float(0.7))
                row.setValue('Cu',float(0))
                row.setValue('Zn',float(0))
                row.setValue('Sediment',float(150))
                row.setValue('FecalColiform',float(16.2))
            if classification=='Medium Density Residential':
                row.setValue('total_N',float(11.2))
                row.setValue('total_P',float(1.6))
                row.setValue('Cu',float(0))
                row.setValue('Zn',float(0))
                row.setValue('Sediment',float(242.5))
                row.setValue('FecalColiform',float(130.2))
            if classification=='Industrial':
                row.setValue('total_N',float(10.4))
                row.setValue('total_P',float(1.9))
                row.setValue('Cu',float(0.2))
                row.setValue('Zn',float(0.1))
                row.setValue('Sediment',float(372.5))
                row.setValue('FecalColiform',float(8.4))
            if classification=='Commercial':
                row.setValue('total_N',float(14))
                row.setValue('total_P',float(2.7))
                row.setValue('Cu',float(0))
                row.setValue('Zn',float(0))
                row.setValue('Sediment',float(400))
                row.setValue('FecalColiform',float(8.4))        
            if classification=='Agricultural':
                row.setValue('total_N',float(2.3))
                row.setValue('total_P',float(0.1))
                row.setValue('Cu',float(0))
                row.setValue('Zn',float(0))
                row.setValue('Sediment',float(10))
                row.setValue('FecalColiform',float(12))        
            if classification=='Very Low Density Residential':
                row.setValue('total_N',float(6.4))
                row.setValue('total_P',float(0.7))
                row.setValue('Cu',float(0))
                row.setValue('Zn',float(0))
                row.setValue('Sediment',float(150))
                row.setValue('FecalColiform',float(16.2))
            if classification=='Roadways':
                row.setValue('total_N',float(12.2))
                row.setValue('total_P',float(1.8))
                row.setValue('Cu',float(0))
                row.setValue('Zn',float(0.1))
                row.setValue('Sediment',float(405))
                row.setValue('FecalColiform',float(2.8))
            if classification=='Parks and Open Space':
                row.setValue('total_N',float(2.3))
                row.setValue('total_P',float(0.1))
                row.setValue('Cu',float(0))
                row.setValue('Zn',float(0))
                row.setValue('Sediment',float(10))
                row.setValue('FecalColiform',float(12))
            if classification=='Research Triangle Park':
                row.setValue('total_N',float(9.4))
                row.setValue('total_P',float(0.7))
                row.setValue('Cu',float(0))
                row.setValue('Zn',float(0.1))
                row.setValue('Sediment',float(50))
                row.setValue('FecalColiform',float(14.8))
            if classification=='High Density Residential':
                row.setValue('total_N',float(11.2))
                row.setValue('total_P',float(1.6))
                row.setValue('Cu',float(0))
                row.setValue('Zn',float(0))
                row.setValue('Sediment',float(242.5))
                row.setValue('FecalColiform',float(30.2))
            else:
                check=False
            Unioncursor.updateRow(row)
    print 'done populating values'
    DEM1=Raster(DEM)
    cell_size=DEM1.meanCellWidth
    rasters=[]
    #===================================================================================
    for i in range(len(fields)):
        print 'creating raster for',fields[i]
        fieldraster=arcpy.PolygonToRaster_conversion(Unionfeature, fields[i], 'Lab06Data.gdb/r'+fields[i]+str(count),"CELL_CENTER","NONE",cell_size)
        rasters.append(fieldraster)
    for values in range(len(rasters)):
        print 'calculating flow using',rasters[values] 
        flowrasters=FlowAccumulation (flowdirect, rasters[values])
        flowrasters.save('Lab06Data.gdb/FA'+fields[values]+str(count)+'.tif')
        if count<2:
            flowarray1.append(flowrasters)
        if count==2:
            flowarray2.append(flowrasters)
    if count==2:
        BMPrasterarray=[]
        print 'converting BMPs to rasters'
        BMPfields=['TN_Eff_ex','TP_Eff_ex','CU_Eff_Ex','Zn_Eff_Ex','Sed_Eff_Ex','FC_Eff_Ex']
        for ii in range(len(BMPfields)):
            BMPrasters=arcpy.PointToRaster_conversion(BMPs,BMPfields[ii] , 'Lab06Data.gdb/BMP'+BMPfields[ii]++'.tif',"MAXIMUM","NONE",cell_size)
            print 'creating BMP accumulated flow'
            BMPflowrasters=FlowAccumulation (flowdirect, BMPrasters)
            BMPflowrasters.save('Lab06Data.gdb/FABMP'+BMPfields[ii]+'.tif')
            BMPrasterarray.append(BMPflowrasters)
        print 'future bmp accu complete'
            

weightedarray=[]
for xx in range(len(BMPfields)):
    print xx
    maxvalue=arcpy.GetRasterProperties_management(BMPrasterarray[xx],'MAXIMUM','')  
    maxvalue=float(maxvalue.getOutput(0))
    weightedFutureAccum=((maxvalue-BMPrasterarray[xx])/maxvalue)*flowarray2[xx]
    weightedFutureAccum.save('Lab06Data.gdb/WeightedFF'+fields[xx]+'.tif')
    weightedarray.append(weightedFutureAccum)
            
# getting values for stream points
differencearray=[]
differencearray1=[]
myrange=RemapRange([[0,0.05,'NoData'],[0.05000001,.1,1],[.100001,.25,2],[.25000001,.5,3],[.500001,1000000000000,4]])
for index in range(len(weightedarray)):
    print fields[index]
    differenceraster=weightedarray[index]/flowarray1[index]
    streamoutput=ExtractValuesToPoints (StreamPoints, differenceraster,'Lab06Data.gdb/streampts'+fields[index])    
    differenceraster1=Reclassify (differenceraster, 'Value', myrange)
    differenceraster.save('Lab06Data.gdb/difference'+fields[index]+'.tif')
    differenceraster1.save('Lab06Data.gdb/pdifference'+fields[index]+'.tif')
    differencearray.append(differenceraster)
    differencearray1.append(differenceraster1)
    StreamToFeature(differenceraster1,flowdirect, 'Lab06Data.gdb/stream'+fields[index])
    










