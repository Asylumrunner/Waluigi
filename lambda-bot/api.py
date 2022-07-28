from flask import Flask, request, jsonify
from secrets import rds_host, name, password, db_name
import pymysql
import logging
from sys import exit

app = Flask(__name__)
app.config['DEBUG'] = True
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# TODO: Zappa only supports up to Python 3.9, downgrade venv from 3.10

try:
    conn = pymysql.connect(host=rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
except pymysql.MySQLError as e:
    logger.error("ERROR: Could not connect to MySQL instance")
    logger.error(e)
    exit()

@app.route('/register', methods=['POST'])
def register_webhook():
    content_type = request.headers.get('Content-Type')
    if (content_type != 'application/json'):
        response = jsonify('Invalid content type')
        response.status_code = 400
    else:
        register_request = request.get_json()
        try:
            with conn.cursor() as cur:
                cur.execute("insert into webhooks (id, webhook_url, server, channel) values(NULL, \"{0}\", \"{1}\", \"{2}\")".format(register_request['webhook_url'], register_request['server'], register_request['channel']))
                conn.commit()
            response = jsonify("Registration successful")
        except pymysql.MySQLError as e:
            response = jsonify("Insertion into database failed: {}".format(e))
            response.status_code = 500
    return response

@app.route('/addterm', methods=['POST'])
def add_scrape_term():
    content_type = request.headers.get('Content-Type')
    if (content_type != 'application/json'):
        response = jsonify('Invalid content type')
        response.status_code = 400
    else:
        term_request = request.get_json()
        try:
            with conn.cursor() as cur:
                cur.execute("insert into search_terms (id, term, server, channel) values(NULL, \"{0}\", \"{1}\", \"{2}\")".format(term_request['term'], term_request['server'], term_request['channel']))
                conn.commit()
            response = jsonify("Registration successful")
        except pymysql.MySQLError as e:
            response = jsonify("Insertion into database failed: {}".format(e))
            response.status_code = 500
    return response


@app.route('/removeterm', methods=['POST'])
def remove_scrape_term():
    content_type = request.headers.get('Content-Type')
    if (content_type != 'application/json'):
        response = jsonify('Invalid content type')
        response.status_code = 400
    else:
        term_request = request.get_json()
        try:
            with conn.cursor() as cur:
                cur.execute("delete from search_terms where term='{}' and server='{}' and channel='{}'".format(term_request['term'], term_request['server'], term_request['channel']))
                conn.commit()
            response = jsonify("Deletion successful")
        except pymysql.MySQLError as e:
            response = jsonify("Insertion into database failed: {}".format(e))
            response.status_code = 500
    return response


@app.route('/deregister', methods=['POST'])
def deregister_webhook():
    content_type = request.headers.get('Content-Type')
    if (content_type != 'application/json'):
        response = jsonify('Invalid content type')
        response.status_code = 400
    else:
        deregistration_request = request.get_json()
        try:
            with conn.cursor() as cur:
                cur.execute("delete from webhooks where server='{}' and channel='{}'".format(deregistration_request['server'], deregistration_request['channel']))
                cur.execute("delete from search_terms where server='{}' and channel='{}'".format(deregistration_request['server'], deregistration_request['channel']))
                conn.commit()
            response = jsonify("Deletion successful")
        except pymysql.MySQLError as e:
            response = jsonify("Insertion into database failed: {}".format(e))
            response.status_code = 500
    return response


