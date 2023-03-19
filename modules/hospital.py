from .validate import is_valid
from models.db_connection import fetch_one


class HospitalModule:
    def details(params):
        if not is_valid(params):
            return {"errno": 403}
        required = [
            'hospital_id'
        ]
        for i in required:
            if i not in params:
                return {"errno": 403}
        query = f"""
            select * from hospital_master
            where hospital_id = '{params['hospital_id']}'
        """
        data = fetch_one(query)
        if 'hospital_id' not in data:
            return {"message": 404}
        del data['hospital_record_creation_time']
        data = {k: (v or "xxxx") for k, v in data.items()}
        return data
