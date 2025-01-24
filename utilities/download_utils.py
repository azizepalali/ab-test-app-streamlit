import io
import base64

def get_excel_download_link(df, filename="A_B_Test_Results.xlsx"):
    """
    Creates a downloadable link for a Pandas DataFrame as an Excel file.

    Parameters:
        df (pd.DataFrame): DataFrame to be downloaded.
        filename (str): Name of the downloaded file.

    Returns:
        str: HTML link for downloading the file.
    """
    # Ensure DataFrame is valid
    if df is None or df.empty:
        raise ValueError("The DataFrame is empty or invalid.")

    # Write DataFrame to an Excel file in memory
    towrite = io.BytesIO()
    df.to_excel(towrite, engine="openpyxl", index=False, header=True)
    towrite.seek(0)

    # Encode file for download
    b64 = base64.b64encode(towrite.read()).decode()
    return f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}">Download {filename}</a>'
