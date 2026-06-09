import pandas as pd
from rest_framework.response import Response
from rest_framework import status

#Responds for uploading files from selected folder
def upload_service(*args):
    if len(args) < 2:
        return Response({"error": "Not enought files uploaded"}, status=status.HTTP_204_NO_CONTENT)
    else:
        excel_files = [file for file in args if file.name.endswith((".xlsx", ".xls"))]

        if not excel_files:
            return Response({"error": "No excel files found"}, status=status.HTTP_400_BAD_REQUEST)

        #Returns only excel files from folder
        return Response({
            "passed": "All good",
            "fisiere": [file.name for file in excel_files]
        }, status=status.HTTP_200_OK)


#Responds for extracting the columns from primary file
def get_columns_service(file, sheet_name):
    try:
        df = pd.read_excel(file, sheet_name=sheet_name, nrows=0)  # nrows=0 reads only haders

        return Response({"columns": list(df.columns)}, status=status.HTTP_200_OK)
    except Exception as ex:
        return Response({"error": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def compare_strings_service(str1, str2):
    """
    Compares two column names to determine if they refer to the same column.
    Handles case differences (Name vs NAme) and minor typos.
    
    Returns str1 if strings are considered equal, None otherwise.
    """
    # exact match
    if str1 == str2:
        return str1

    # case-insensitive match (Name == NAme == NAME)
    if str1.lower() == str2.lower():
        return str1

    # if lenght is too diferent 
    if abs(len(str1) - len(str2)) > 2:
        return None

    # one char difference — handles typos (Nmae vs Name)
    differences = sum(1 for a, b in zip(str1.lower(), str2.lower()) if a != b)
    differences += abs(len(str1) - len(str2))  # diferenta de lungime conteaza ca diferente

    if differences <= 1:
        return str1

    return None


#Responds for merging files and writing final dataframe to excel file in selected sheet
def merge_service(sheet_name, selected_columns, primary_file_name, output_file, *args):
    import json
    import io
    from django.http import HttpResponse

    excel_files = [file for file in args if file.name.endswith((".xlsx", ".xls"))] #reads excel files

    try:
        columns = json.loads(selected_columns) #extracts selected columns

        primary_file = next((file for file in excel_files if file.name == primary_file_name), None)
        other_files = [file for file in excel_files if file.name != primary_file_name]

        # reads primary file and deletes unselected columns
        main_frame = pd.read_excel(primary_file, sheet_name=sheet_name, header=[0]).fillna(" ")
        columns_to_drop = [col for col in main_frame.columns.tolist() if col not in columns]
        main_frame = main_frame.drop(columns=columns_to_drop)


    except Exception as ex:
        return Response({"error": f"Error reading primary file: {ex}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    try:
        frames = [pd.read_excel(file, sheet_name=sheet_name, header=[0]).fillna(" ") for file in other_files]
    except Exception as ex:
        return Response({"error": f"Error in one of selected files: {ex}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    try:
        for frame in frames:
            # deletes unselected columns from every frame
            to_drop = []
            for drop_col in columns_to_drop:
                for frame_col in frame.columns.tolist():
                    col = compare_strings_service(frame_col, drop_col)
                    if col:
                        to_drop.append(col)
                        break
            frame = frame.drop(columns=to_drop)

            # If a column from current frame is not found in selected_columns
            # then append this column to dataframe with value=" " by default
            for col in frame.columns.tolist():
                if col not in columns:
                    main_frame[col] = " "

            #merge dataframes
            main_frame = pd.concat([main_frame, frame], ignore_index=True).fillna(" ")

        # deletes empty rows
        #main_frame = main_frame.replace(r'^\s*$', pd.NA, regex=True).dropna(how='all')

    except Exception as ex:
        return Response({"error": f"Error during merge: {ex}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    #Writing output file
    try:
        # Reads output file and saves existing sheets
        output_workbook = pd.ExcelFile(output_file)
        existing_sheets = output_workbook.sheet_names

        if sheet_name in existing_sheets:
            return Response({"error": f"Sheet '{sheet_name}' already exists in output file."}, status=status.HTTP_400_BAD_REQUEST)

        output_buffer = io.BytesIO()
        with pd.ExcelWriter(output_buffer, engine='openpyxl') as writer:
            for s in existing_sheets:
                df_existing = pd.read_excel(output_file, sheet_name=s)
                df_existing.to_excel(writer, sheet_name=s, index=False)

            # Writes result into sheet
            main_frame.to_excel(writer, sheet_name=sheet_name, index=False)

        output_buffer.seek(0) # Points to buffer start (otherwise nothing will be writen)

        response = HttpResponse(
            output_buffer.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="{output_file.name}"'
        return response

    except Exception as ex:
        return Response({"error": f"Error writing output file: {ex}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)