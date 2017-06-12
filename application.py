import logging
import json

import flask
from flask import request, Response

# from utils.s3_connection import connect_to_s3

from utils.cassandra_conn import setup_connection
from utils.cassandra_conn_log import setup_log_connection
from utils.mysql_conn_bloomskyDB import get_bloomskydb_con
from utils.mysql_conn_mysqlDB import get_mysqldb_con

from utils.email_cron_job import send_alarm_email_to_staff, server_disk_alert
from utils.countActiveDevices import get_active_sky_devices, get_active_storm_devices
from utils.cassandra_slow_log import get_cassandra_slow_log
from utils.mysql_slow_log import get_mysql_slow_log
from utils.datastax_alert_notification import notification
from utils.checkAbnormalData import check_abnormal_sky_devices, check_abnormal_storm_devices

from utils.misc import readable_time_without_hms
import time
import datetime


# Create and configure the Flask app
application = flask.Flask(__name__)
application.config.from_object('default_config')
application.debug = application.config['FLASK_DEBUG'] in ['true', 'True']

# cur, con = get_mysqldb_con()
cassandra_session = setup_connection()
cassandra_log_session = setup_log_connection()

@application.route('/test-monitor', methods=['POST'])
def system_monitor():

    response = None

    if request.json is None:
        # Expect application/json request
        response = Response("", status=415)
    else:
        message = dict()
        try:
            # If the message has an SNS envelope, extract the inner message
            if request.json.has_key('TopicArn') and request.json.has_key('Message'):
                message = json.loads(request.json['Message'])
            else:
                message = request.json

            # message_content = message['Message']
            send_alarm_email_to_staff(message)

            response = Response("", status=200)
        except Exception as ex:
            logging.exception('Error processing message: %s' % request.json)
            response = Response(ex.message, status=500)

    return response

@application.route('/server_status_email', methods=['POST'])
def send_server_disk_status_email():
    response = None
    try:
        status = server_disk_alert()
        response = Response("", status=status)
    except Exception as e:
        print e

    return response

@application.route('/count_active_sky_devices', methods=['POST'])
def get_active_sky_devices_per_hour():

    cur,con = get_bloomskydb_con()

    date = readable_time_without_hms(time.time())
    # date = datetime.datetime.now().strftime("%Y-%m-%d")
    ts = int(time.time())

    response = None
    try:
        status = get_active_sky_devices(cur, cassandra_session, date, ts)
        response = Response("", status=200)
    except Exception as e:
        print e

    cur.close()
    con.close()

    return response

@application.route('/count_active_storm_devices', methods=['POST'])
def get_active_storm_devices_per_hour():

    cur,con = get_bloomskydb_con()

    date = readable_time_without_hms(time.time())
    # date = datetime.datetime.now().strftime("%Y-%m-%d")
    ts = int(time.time())

    response = None

    try:
        status = get_active_storm_devices(cur, cassandra_session, date, ts)
        response = Response("", status=200)
    except Exception as e:
        print e

    cur.close()
    con.close()
    return response

@application.route('/cassandra_slow_log', methods=['GET'])
def get_cassandra_slow_log_per_hour():

    response = None
    try:
        status = get_cassandra_slow_log(cassandra_log_session)
        response = Response("", status=status)
    except Exception as e:
        print e
    return response

@application.route('/mysql_slow_log', methods=['GET'])
def get_mysql_slow_log_per_hour():

    cur,con = get_mysqldb_con()

    date = readable_time_without_hms(time.time())
    # date = datetime.datetime.now().strftime("%Y-%m-%d")
    ts = int(time.time())

    response = None

    status = get_mysql_slow_log(cur)

    response = Response("", status=status)

    cur.close()
    con.close()

    return response

# @application.route('/datastax_alert', methods=['POST'])
# def get_datastax_alert_per_hour():
#     response = None
#     status = notification()
#     response = Response("", status=status)
#     print "datastax warning...."
#     return response

@application.route('/check_abnormal_sky_data', methods=['POST'])
def check_abnormal_sky_devices_per_hour():

    cur, con = get_bloomskydb_con()

    date = readable_time_without_hms(time.time())
    # date = datetime.datetime.now().strftime("%Y-%m-%d")
    ts = int(time.time())

    response = None
    try:
        status = check_abnormal_sky_devices(cur,cassandra_session, date, ts)
        response = Response("", status=status)
    except Exception as e:
        print e

    cur.close()
    con.close()

    return response

@application.route('/check_abnormal_storm_data', methods=['POST'])
def check_abnormal_storm_devices_per_hour():

    cur, con = get_bloomskydb_con()

    date = readable_time_without_hms(time.time())
    # date = datetime.datetime.now().strftime("%Y-%m-%d")
    ts = int(time.time())

    response = None
    try:
        status = check_abnormal_storm_devices(cur,cassandra_session, date, ts)
        response = Response("", status=status)
    except Exception as e:
        print e

    cur.close()
    con.close()

    return response

if __name__ == '__main__':
    application.run(host='0.0.0.0')
