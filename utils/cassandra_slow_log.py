import time
from cassandra_conn_log import setup_log_connection

def get_cassandra_slow_log(session):

    slow_logs = session.execute("SELECT * FROM node_slow_log")

    for item in slow_logs:
        print item['username'], item["node_ip"], item['date'], item['start_time'], item['commands'], item['duration'], item['parameters'], item['table_names'], item['source_ip']
