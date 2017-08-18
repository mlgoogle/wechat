import MySQLdb
import config


def readDataFromSQL():
    conn = MySQLdb.connect(host = config.SQL_HOST,
                           user = config.SQL_USER,
                           db = config.SQL_DBNAME,
                           passwd = config.SQL_PASSWD,
                           port = config.SQL_PORT,
                           charset = config.SQL_CHARSET)

    cursor = conn.cursor()
    cursor.execute('select * from flight_info')
    flightinfos = cursor.fetchall()

    flightDict = None
    for flight in flightinfos:
        flightDict[flight['']]
    cursor.close()
    conn.close()
    return flightinfos

def modfyStatus():

    conn = MySQLdb.connect(host = config.SQL_HOST,
                           user = config.SQL_USER,
                           db = config.SQL_DBNAME,
                           passwd = config.SQL_PASSWD,
                           port = config.SQL_PORT,
                           charset = config.SQL_CHARSET)

    cursor = conn.cursor()
    sql_str = 'select * from flight_info'
    try:
        cursor.execute(sql_str)
    except:
        conn.rollback()
    conn.close


