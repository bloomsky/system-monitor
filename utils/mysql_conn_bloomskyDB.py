import MySQLdb as mdb

def get_bloomskydb_con():
    "get skyboundeduser database connection and return the cursor"
    try:
        con = mdb.connect(host='bloomsky.cb2tvmnyo0zz.us-west-1.rds.amazonaws.com', port=3306,
                          user='Yang', passwd='12345678', db='bloomsky',
                          charset='utf8', connect_timeout=30)
        cur = con.cursor(mdb.cursors.DictCursor)
        con.set_character_set('utf8')
        cur.execute('SET NAMES utf8;')
        cur.execute('SET CHARACTER SET utf8;')
        cur.execute('SET character_set_connection=utf8;')
        return cur, con
    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        con = None
    return None, con
