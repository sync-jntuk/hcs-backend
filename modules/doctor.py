from .validate import is_valid
from models.db_connection import fetch_one


class DoctorModule:
    def details(params):
        if not is_valid(params):
            return {"errno": 403}
        required = [
            'doctor_id'
        ]
        for i in required:
            if i not in params:
                return {"errno": 403}
        query = f"""
            select * from doctor_master
            where doctor_id = '{params['doctor_id']}'
        """
        data = fetch_one(query)
        if 'doctor_id' not in data:
            return {"message": 404}
        del data['doctor_record_creation_time']
        del data['doctor_dob']
        return data
