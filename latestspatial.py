import arcpy

def spatial_join_and_add_field(target_fc, join_fc, target_field, join_field):
   
    arcpy.env.workspace = r"C:\path\to\your\geodatabase.gdb"


    arcpy.SpatialJoin_analysis(target_fc, join_fc, "temp_join", "JOIN_ONE_TO_ONE", "KEEP_ALL")


    field_names = [field.name for field in arcpy.ListFields(join_fc)]
    if target_field not in field_names:
        arcpy.AddField_management(join_fc, target_field, "TEXT")


    target_fields = {}

 
    with arcpy.da.SearchCursor("temp_join", [join_field, target_field]) as cursor:
        for row in cursor:
            join_value = row[0]
            target_value = row[1]
            target_fields[join_value] = target_value

 
    with arcpy.da.UpdateCursor(join_fc, [join_field, target_field]) as cursor:
        for row in cursor:
            join_value = row[0]
            if join_value in target_fields:
                row[1] = target_fields[join_value]
                cursor.updateRow(row)

    print("Spatial join completed. Field added to the join feature class.")


    arcpy.Delete_management("temp_join")


def main_menu():
    print("Spatial Join Tool")
    print("-----------------\n")
    print("1. Perform Spatial Join and Add Field")
    print("2. Quit\n")

    choice = input("Enter your choice (1-2): ")

    if choice == "1":
        target_fc = input("Enter the target feature class name: ")
        join_fc = input("Enter the join feature class name: ")
        target_field = input("Enter the target field name to add: ")
        join_field = input("Enter the join field name: ")

        spatial_join_and_add_field(target_fc, join_fc, target_field, join_field)
    elif choice == "2":
        print("Exiting the program...")
        return
    else:
        print("Invalid choice. Please try again.\n")

    print("\n")
    main_menu()


main_menu()
