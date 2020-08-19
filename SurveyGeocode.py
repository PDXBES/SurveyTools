import arcpy
import re
import xlrd

egh_public = r"\\oberon\grp117\DAshney\Scripts\connections\egh_public on gisdb1.rose.portland.local.sde"

def create_survey_points_layer(input_excel, excel_sheet, output_gdb):
    output_table = output_gdb + r"\new_survey"
    arcpy.ExcelToTable_conversion(Input_Excel_File= input_excel, Output_Table=output_table, Sheet=excel_sheet)
    return output_gdb + "/new_survey"

def create_survey_points_from_X_Y(input_excel, excel_sheet, output_gdb, feature_class_name):
    output_featureclass_path = output_gdb + "/" + feature_class_name
    output_gdb_in_memory = "in_memory"
    survey = create_survey_points_layer(input_excel, excel_sheet, output_gdb_in_memory)


    geocode_address_table_with_x_y_values(survey, output_featureclass_path)

   # fields_to_keep = [u'OBJECTID', "Address", 'SHAPE@', u'Shape', 'Elevation', 'Basement', 'Notes']
   # delete_all_fields_except_as_specified_and_geometry(output_featureclass_path, fields_to_keep)
   #
   #  arcpy.AddField_management(output_featureclass_path, "Basement", "TEXT", "", "", 10)
   #
   #  arcpy.AddField_management(output_featureclass_path, "RNO", "TEXT", "", "", 20)
   #
   #  arcpy.AddField_management(output_featureclass_path, "NOBSMT", "SHORT")
   #  arcpy.AddField_management(output_featureclass_path, "SURVEYDATE", "DATE")
   #
   #  arcpy.AddField_management(output_featureclass_path, "AREA_ID", "LONG")
   #  arcpy.AddField_management(output_featureclass_path, "AREA_NAME", "TEXT", "", "", 255)
   #  arcpy.AddField_management(output_featureclass_path, "ADDATE", "DATE")

def geocode_address_table_with_x_y_values(input_table, feature_class_path):
    sr = arcpy.SpatialReference("OCRS Portland NAD 1983 CORS96 LCC (Feet Intl)")
    #sr = arcpy.SpatialReference( r"C:\Users\bfreeman\Downloads\OCRS Portland NAD 1983 (2011) LCC (Intl Feet).prj")
    temp_layer = arcpy.MakeXYEventLayer_management(input_table,"Easting", "Northing", "Temp_XY_Layer", sr)
    #filtered_layer = filter_x_y_table_for_ffe(temp_layer)

    arcpy.CopyFeatures_management(temp_layer, feature_class_path)

if __name__ == "__main__":

    input_excel = r"C:\temp\ffe_scratch\surveys\cc_test.xls"
    excel_sheet = "cc_test"
    output_gdb = r"C:\temp\ffe_scratch\FFE_working.gdb"
    fc_name = r"survey2"


    create_survey_points_from_X_Y(input_excel, excel_sheet, output_gdb, fc_name)

