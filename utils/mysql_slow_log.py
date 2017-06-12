
def get_mysql_slow_log(cur):

    cur.execute("SELECT * FROM slow_log")
    rows = cur.fetchall()

    if len(rows) > 0:
        for item in rows:
            print item['start_time'], item["user_host"], item['query_time'], \
                  item['lock_time'], item['rows_sent'], item['rows_examined'],\
                  item['db'], item['insert_id'], item['server_id'],item['thread_id']
    else:
        print 'No Slow Log Exists'
