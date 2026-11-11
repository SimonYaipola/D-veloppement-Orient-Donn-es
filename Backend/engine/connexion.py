import urllib.parse

from sqlalchemy import create_engine

from .config_local import SERVER, DATABASE, USERNAME, PASSWORD


params = urllib.parse.quote_plus(
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    f"UID={USERNAME};"
    f"PWD={PASSWORD};"
)

engine = create_engine(
    f"mssql+pyodbc:///?odbc_connect={params}",
    use_setinputsizes=False,
)