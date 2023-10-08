from database import MySQLDatabaseManager, MySQLDatabaseConnection
import os

mysql_config = {
    'host': os.environ.get('MYSQL_HOST'),
    'user': os.environ.get('MYSQL_USER'),
    'port': os.environ.get('MYSQL_PORT'),
    'password': os.environ.get('MYSQL_PASSWORD'),
    'database': os.environ.get('MYSQL_DB'),
}

db_connection = MySQLDatabaseConnection(**mysql_config)
db_manager = MySQLDatabaseManager(db_connection)