from helpers.sqlite_helper import SQLiteHelper
from utils.csv_util import CSVUtil
from utils.excel_util import ExcelUtil
from yaspin import yaspin
import os
import shutil
import configparser

def importCSVData(filePath: str, sqliteHelper: SQLiteHelper, tableName: str) -> None:
    schemaFile = CSVUtil.createTableFromCSV(filePath, tableName)
    sqliteHelper.createTableFromSchemaFile(schemaFile)
    CSVUtil.removeFile(schemaFile)
    sqliteHelper.importCSVFile(filePath, tableName)


if __name__ == '__main__':
    parser = configparser.ConfigParser()
    parser.read('config.ini')

    # Read Old CSV File Path and New CSV File Path
    oldFilePath = input('Enter Old File Path: ')
    newFilePath = input('Enter New File Path: ')

    # Read Old CSV File Path and New CSV File Path
    oldFileKey = input('Enter unique column name in Old File: ')
    newFileKey = input('Enter unique column name in New File: ')

    # Clean Output directory
    with yaspin(text=f'Performing cleanup', color='green') as spinner:
        shutil.rmtree(parser.defaults().get('outputdir'), ignore_errors=True)
        os.makedirs(parser.defaults().get('outputdir'), exist_ok=True)
        spinner.ok("✅ ")

    # Create connection to SQLite
    with yaspin(text=f'Creating SQLite connection and cleaning up previous data', color='green') as spinner:
        sqliteHelper = SQLiteHelper(oldFileKey, newFileKey)
        sqliteHelper.connect()
        sqliteHelper.cleanup()
        spinner.ok("✅ ")

    # Import data from both CSV files to SQLite Tables
    with yaspin(text=f'Importing Data from {oldFilePath}', color='green') as spinner:
        importCSVData(oldFilePath, sqliteHelper, parser.defaults().get('oldtable'))
        spinner.ok("✅ ")
    
    with yaspin(text=f'Importing Data from {newFilePath}', color='green') as spinner:
        importCSVData(newFilePath, sqliteHelper, parser.defaults().get('newtable'))
        spinner.ok("✅ ")


    # Get rows which are deleted
    with yaspin(text=f'Checking rows which are deleted', color='green') as spinner:
        sqliteHelper.getDeletedRows()
        spinner.ok("✅ ")

    # Get rows which are added
    with yaspin(text=f'Checking rows which are newly added', color='green') as spinner:
        sqliteHelper.getNewInsertedRows()
        spinner.ok("✅ ")

    # Get rows which are updated
    with yaspin(text=f'Checking rows which are updated', color='green') as spinner:
        sqliteHelper.getUpdatedRows()
        spinner.ok("✅ ")

    # Write data to output files
    with yaspin(text=f'Writing data to output files', color='green') as spinner:
        ExcelUtil.writeDeletedRows(f"{parser.defaults().get('outputdir')}/rows-deleted", 'xlsx')
        ExcelUtil.writeAddedRows(f"{parser.defaults().get('outputdir')}/rows-added", 'xlsx')
        ExcelUtil.writeUpdatedRows(f"{parser.defaults().get('outputdir')}/rows-updated", 'xlsx')
        spinner.ok("✅ ")
