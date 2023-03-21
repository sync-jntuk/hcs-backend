from .validate import is_valid
from models.db_connection import fetch_one, insert


class NurseModule:
    def details(params):
        if not is_valid(params):
            return {"errno": 403}
        required = [
            'nurse_health_id'
        ]
        for i in required:
            if i not in params:
                return {"errno": 403}
        query = f"""
            select * from nurse_master
            where nurse_health_id = '{params['nurse_health_id']}'
        """
        data = fetch_one(query)
        if 'nurse_id' not in data:
            return {"message": 404}
        return data

    def create(params):
        if not is_valid(params):
            return {"errno": 403}
        required = [
            'nurse_first_name', 'nurse_last_name', 'nurse_middle_name',
            'nurse_address', 'nurse_health_id'
        ]
        for i in required:
            if i not in params:
                return {"errno": 403}
        query = f"""
            insert into nurse_master set
        """
        for key in required:
            query += f"{key} = '{params[key]}', "
        query = query[:-2]
        data = insert(query)
        return data
