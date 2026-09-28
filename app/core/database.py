from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
import logging
logger=logging.getLogger(__name__)
Base =declarative_base()

server=r'DESKTOP-HN5RUV9\SQLEXPRESS'
database='EMP_DB'
driver='ODBC driver 17 for SQL Server'

def get_connection():
        connection_string=(
            f"mssql+pyodbc://@{server}/{database}"
            f"?driver={driver.replace(" ","+")}&trusted_connection=yes"
        )
        return create_engine(connection_string)
engine=get_connection()
#print("database connected succesfully")
logger.info("database connected succesfully")