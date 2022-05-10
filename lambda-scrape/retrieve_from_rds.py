import sys
import logging
import secrets
import pymysql
rds_host  = secrets.rds_endpoint
name = secrets.db_username
password = secrets.db_password
db_name = secrets.db_name

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    conn = pymysql.connect(host=rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
except pymysql.MySQLError as e:
    logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
    logger.error(e)
    sys.exit()

logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")

def retrieve_config():
    config = {
        "webhooks": {},
        "keywords": {}
    }

    with conn.cursor() as cur:
        cur.execute("select Keyword, ChannelID")
        for row in cur:
            logger.info(row)
            print(row)
    conn.commit()

    return config