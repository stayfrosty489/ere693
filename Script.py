#Tyler Pitts
import numpy,arcpy,os,sys

##Mask = sys.argv[1]
##DEM = sys.argv[2]
Mask = "H:/Desktop/GISModeling/Lab6/Lab06Data.gdb/AnalysisMask"
DEM = arcpy.Raster("H:/Desktop/GISModeling/Lab6/Lab06Data.gdb/DEM")

print "converting feature mask to raster mask..."
Maskraster = arcpy.FeatureToRaster_conversion(Mask, 'OBJECTID', "H:/Desktop/GISModeling/Lab6/Lab06Data.gdb/raster_mask", 40)
print "converting feature mask to raster mask complete"

print "Filling DEM..."
FilledDEM = Fill(arcpy.ExtractByMask (DEM, Maskraster))
print "Filling DEM complete"

print "Calculating Flow Direction..."
Direction = arcpy.FlowDirection(FilledDEM)
print "Calculating Flow Direction complete"

print "Calculating cells..."
Calculated_Raster = arcpy.RasterCalculator(Direction*40*40/43560, "H:/Desktop/GISModeling/Lab6/Lab06Data.gdb/Calculated_Raster")
print "Calculating cells complete"

print "Reclassifying..."
Reclassified_raster = arcpy.Reclassify(Calculated_Raster, "Value", remapTable[[0,590,0][590.00001,99999999,1]], NODATA)
print "Reclassification complete"

print "Saving..."
Reclassified_raster.save("H:/Desktop/GISModeling/Lab5/Lab05Geodatabase.gdb/Reclassified_raster")
print "All Tasks complete"
