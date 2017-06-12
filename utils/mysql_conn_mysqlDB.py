import MySQLdb as mdb

def get_mysqldb_con():
    "get skyboundeduser database connection and return the cursor"
    try:
        con = mdb.connect(host='bloomsky.cb2tvmnyo0zz.us-west-1.rds.amazonaws.com', port=3306,
                          user='Yang', passwd='12345678', db='mysql',
                          charset='utf8', connect_timeout=30)
        print 'SUCCESSFUL'
    except mdb.Error, e:
        print "Exception Error %d: %s" % (e.args[0], e.args[1])
        con = None
    return con
