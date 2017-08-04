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
    cursor.excute('select * from flight_info')
    flightinfos = cursor.fetchall()

    flightDict = None
    for flight in flightinfos:
        flightDict[flight['']]
    conn.close
    return flightinfos
