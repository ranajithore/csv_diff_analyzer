import os

class CSVUtil:
    @staticmethod
    def createTableFromCSV(filePath: str, tableName: str) -> str:
        fileName, _ = os.path.splitext(os.path.basename(filePath))
        schemaFile = f'{fileName}-schema.sql'
        os.system(f'head -n 10 {filePath} | csvsql -i sqlite --tables {tableName} > {schemaFile}')
        return schemaFile
    
    @staticmethod
    def removeFile(fileName: str) -> None:
        os.remove(fileName)
