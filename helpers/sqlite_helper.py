import configparser
import sqlite3
import subprocess
import csv

class SQLiteHelper:
    def __init__(self, oldFileKey: str, newFileKey: str) -> None:
        self.oldTableKey = oldFileKey
        self.newTableKey = newFileKey
        self.parser = configparser.ConfigParser()
        self.parser.read('config.ini')
        self.databaseName = self.parser.defaults().get('databasename')
        self.oldTableName = self.parser.defaults().get('oldtable')
        self.newTableName = self.parser.defaults().get('newtable')
        self.rowsDeletedTableName = self.parser.defaults().get('rowsdeletedtablename')
        self.rowsInsertedTableName = self.parser.defaults().get('rowsinsertedtablename')
        self.rowsUpdatedTableName = self.parser.defaults().get('rowsupdatedtablename')
    
    def connect(self) -> None:
        self.conn = sqlite3.connect(self.databaseName)
        self.cursor = self.conn.cursor()
    
    def cleanup(self) -> None:
        self.cursor.execute(f'DROP TABLE IF EXISTS {self.oldTableName}')
        self.cursor.execute(f'DROP TABLE IF EXISTS {self.newTableName}')
        self.cursor.execute(f'DROP TABLE IF EXISTS {self.rowsDeletedTableName}')
        self.cursor.execute(f'DROP TABLE IF EXISTS {self.rowsInsertedTableName}')
        self.cursor.execute(f'DROP TABLE IF EXISTS {self.rowsUpdatedTableName}')
    
    def createTableFromSchemaFile(self, schemaFilePath: str) -> None:
        subprocess.run(['sqlite3', f'{self.databaseName}', f'.read {schemaFilePath}'], capture_output=True)
    
    def importCSVFile(self, csvFilePath: str, tableName: str) -> None:
        subprocess.run(['sqlite3', f'{self.databaseName}', f'.import --csv --skip 1 {csvFilePath} {tableName}'])

    def getNumberOfColumns(self, tableName: str) -> int:
        return self.cursor.execute(f"SELECT COUNT(*) FROM pragma_table_info('{tableName}')").fetchone()[0]
    
    def getColumnNames(self, tableName: str) -> list:
        result = self.cursor.execute(f'SELECT * FROM {tableName}')
        colNames = [description[0] for description in result.description]
        return colNames
    
    def getOldTableColumnNames(self) -> list:
        return self.getColumnNames(self.oldTableName)

    def getNewTableColumnNames(self) -> list:
        return self.getColumnNames(self.newTableName)

    def writeResultToFile(self, result: sqlite3.Cursor, fileName: str) -> None:
        with open(fileName, 'w') as fout:
            csvOut = csv.writer(fout)
            for row in result:
                csvOut.writerow(row)
    
    def getDeletedRows(self) -> None:
        self.cursor.execute(f'CREATE TABLE {self.rowsDeletedTableName} AS SELECT * FROM {self.oldTableName} WHERE "{self.oldTableKey}" NOT IN (SELECT "{self.newTableKey}" FROM {self.newTableName})')
    
    def getNewInsertedRows(self) -> None:
        self.cursor.execute(f'CREATE TABLE {self.rowsInsertedTableName} AS SELECT * FROM {self.newTableName} WHERE "{self.newTableKey}" NOT IN (SELECT "{self.oldTableKey}" FROM {self.oldTableName})')
    
    def getUpdatedRows(self) -> None:
        self.cursor.execute(f'CREATE TABLE {self.rowsUpdatedTableName} AS SELECT * FROM {self.oldTableName} INNER JOIN {self.newTableName} ON {self.oldTableName}."{self.oldTableKey}" = {self.newTableName}."{self.newTableKey}" WHERE {self.oldTableName}."{self.oldTableKey}" NOT IN (SELECT "{self.oldTableKey}" FROM {self.oldTableName} NATURAL JOIN {self.newTableName});')
    
    def getDataFromTable(self, tableName: str, limit: int, offset: int) -> list:
        result = self.cursor.execute(f'SELECT * FROM {tableName} LIMIT {limit} OFFSET {offset}')
        return result.fetchall()

