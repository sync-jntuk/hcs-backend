from mysql.connector import connect


mydb = connect(
    user='root',
    host='localhost',
    password='sandyblaze',
    database='hcs',
    auth_plugin='mysql_native_password'
)

db_cursor = mydb.cursor()

def fetch_one(query):
    data = {}
    db_cursor = mydb.cursor()
    try:
        db_cursor.execute(query)
        keys = db_cursor.column_names
        vals = db_cursor.fetchone()
        if not vals:
            return {"errno": 404}
        data = dict(zip(keys, vals))
        db_cursor.close()
    except:
        db_cursor.close()
    return data


def fetch_all(query):
    data = []
    db_cursor = mydb.cursor()
    try:
        db_cursor.execute(query)
        keys = db_cursor.column_names
        vals = db_cursor.fetchall()
        for row in vals:
            data.append(dict(zip(keys, row)))
        db_cursor.close()
    except:
        db_cursor.close()
    return data
