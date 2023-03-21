from mysql.connector import connect


mydb = connect(
    user='root',
    host='localhost',
    password='sandyblaze',
    database='hcs',
    auth_plugin='mysql_native_password'
)


def fetch_one(query):
    db_cursor = mydb.cursor()
    try:
        db_cursor.execute(query)
        keys = db_cursor.column_names
        vals = db_cursor.fetchone()
        if not vals:
            return {"errno": 404}
        data = dict(zip(keys, vals))
    except Exception as e:
        data = {"message": str(e)}
    finally:
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
    except Exception as e:
        data = {"message": str(e)}
    finally:
        db_cursor.close()
    return data


def insert(query):
    data = {"message": 200}
    db_cursor = mydb.cursor()
    try:
        db_cursor.execute(query)
        mydb.commit()
    except Exception as e:
        data = {"message": str(e)}
    finally:
        db_cursor.close()
    return data


def insert_many(queries):
    data = {"message": 200}
    db_cursor = mydb.cursor()
    try:
        for query in queries:
            db_cursor.execute(query)
        mydb.commit()
    except Exception as e:
        data = {"message": str(e)}
    finally:
        db_cursor.close()
    return data
