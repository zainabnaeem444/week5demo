import os

class Config:
    MYSQL_HOST = 'mysql-container'  # Host machine's address (localhost)
    MYSQL_PORT = 3306  # The port mapped to MySQL in the container
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'admin'
    MYSQL_DB = 'sakila'
    SECRET_KEY = 'your-secret-key-here-change-this-in-production'
