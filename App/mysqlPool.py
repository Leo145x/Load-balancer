from mysql.connector import pooling
import os
from dotenv import load_dotenv

class Mysql():
    def __init__(self) -> None:
        load_dotenv()
        self.mysql_host = os.getenv("MYSQL_HOST")
        self.mysql_user = os.getenv("MYSQL_USER")
        self.mysql_password = os.getenv("MYSQL_PASSWORD")
        self.mysql_database = os.getenv("MYSQL_DATABASE")
        self.mysql_pool = None

    def mysql_info(self):
        info = {
            "user": self.mysql_user,
            "password": self.mysql_password,
            "host": self.mysql_host,
            "database": self.mysql_database
        }
        return info

    def create_connect_pool(self):
        self.mysql_pool = pooling.MySQLConnectionPool(pool_name="tenpool", pool_size=2, **self.mysql_info())
        return self.mysql_pool



# if __name__ != "__main__":
#     mysql_istance = Mysql()
#     mysql_istance.create_connect_pool()
