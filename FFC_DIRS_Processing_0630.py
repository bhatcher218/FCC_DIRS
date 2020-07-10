# buffer_clipv2.py (soft-coded version)
# Purpose: Buffer a zone and use it to clip another file
# Usage: workspace output_directory file_to_buffer buffer_dist. file_to_clip
# Input example: C:/gispy/data/ch07/ C:/gispy/scratch/ special_regions.shp "1 mile" park.shp

import os
import datetime
import arcpy
from arcpy import env
import sys






Outputs = sys.argv[1]
CountyData = sys.argv[2]
DIRS_Data = sys.argv[3]
EventName = sys.argv[4]
DIRS_Date = sys.argv[5]

'''arcpy.env.workspace = "C:/FCC_DIRS/DIRS_Cell_Outage.gdb"


#variable to set

CountyData = "C:/FCC_DIRS/DIRS_Inputs.gdb/counties_2020"
DIRS_Data = "C:/FCC_DIRS/DIRS_CellOutage_620.csv"
EventName = "Dorian"
DIRS_Date = "06/27/2019" '''

arcpy.env.workspace = Outputs
arcpy.env.overwriteOutput = True
arcpy.env.qualifiedFieldNames = False
#variable for arcgis tool




#pull name of csv fles for field manipulations

CsvName = os.path.basename(DIRS_Data)
CsvName2 = os.path.splitext(CsvName)[0]


#date Name Variable
DateSplit = DIRS_Date.split('/')
DateName = ("".join(DateSplit))
Year = DateName[4:9]

Table = arcpy.conversion.TableToTable(DIRS_Data, Outputs, "DIRS_Table" + DateName)
# Create the Initiral DIRS File and update with current date 
SourceFile = "C:/FCC_DIRS/DIRS_Cell_Outage.gdb/" + EventName + "_Main_DIRS_Outage_" + Year

if arcpy.Exists(EventName + "_Main_DIRS_Outage_" + Year):
    DIRS_join2 = arcpy.management.AddJoin(CountyData, "CountyCaps", Table, "Affected_Counties", "KEEP_ALL")
    SecondaryFile = arcpy.CopyFeatures_management(DIRS_join2, EventName + "_" + DateName + Year)
    arcpy.management.Append(SecondaryFile, SourceFile , "TEST")
    SQL = "counties_2020_Date IS NULL"

    with arcpy.da.UpdateCursor(in_table= SourceFile, field_names= EventName + "_Main_DIRS_Outage_" + Year + '.Date',  where_clause = SQL ) as cursor:
        for row in cursor:
            row[0]=  DIRS_Date
            cursor.updateRow(row)
else:
    print ('no')

    
    DIRS_join = arcpy.management.AddJoin(CountyData, "CountyCaps", Table, "Affected_Counties", "KEEP_ALL")

    MainFile = arcpy.CopyFeatures_management(DIRS_join, EventName + "_Main_DIRS_Outage_" + Year)

    arcpy.management.CalculateField(MainFile, "Date","'" + DIRS_Date + "'", "Python 3", '')





#populate the date field

### arcpy.management.CalculateField("Dorian_DIRS_Outage_2019", "counties_2020_Date", '"06-18-2010"', "PYTHON3", '')








