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
    db_cursor.execute(query)
    keys = db_cursor.column_names
    vals = db_cursor.fetchone()
    if not vals:
        return {"errno": 404}
    data = dict(zip(keys, vals))
    return data


def fetch_all(query):
    db_cursor.execute(query)
    keys = db_cursor.column_names
    vals = db_cursor.fetchall()
    data = []
    for row in vals:
        data.append(dict(zip(keys, row)))
    return data
