from .validate import is_valid
from models.db_connection import fetch_one


class NurseModule:
    def details(params):
        if not is_valid(params):
            return {"errno": 403}
        required = [
            'nurse_id'
        ]
        for i in required:
            if i not in params:
                return {"errno": 403}
        query = f"""
            select * from nurse_master
            where nurse_id = '{params['nurse_id']}'
        """
        data = fetch_one(query)
        if 'nurse_id' not in data:
            return {"message": 404}
        return data
