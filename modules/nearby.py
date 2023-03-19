from .validate import is_valid
from models.db_connection import fetch_all, upsert
from .doctor import DoctorModule
from .hospital import HospitalModule


class MapsModule:
    def getNearByItems(params):
        required = ['lat', 'long', 'range', 'role_name']
        for i in required:
            if i not in params:
                return {"errno": 403}
        if not is_valid(params):
            return {"errno": 403}
        roles = ['doctor', 'physiotherapist', 'nurse', 'hospital']
        if params['role_name'] not in roles:
            return {"errno": 403}
        lat, long, kmrange = params['lat'], params['long'], params['range']
        degree_width, limit = 111, int(int(kmrange) / 2 + 0.5)
        k_lat = int(float(lat) * degree_width / 2)
        k_long = int(float(long) * degree_width / 2)
        query = f"""
            select * from coordinates
            where {k_lat - limit} <= k_latitude
            and k_latitude <= {k_lat + limit}
            and {k_long - limit} <= k_longitude
            and k_longitude <= {k_long + limit}
            and role_name = '{params['role_name']}'
        """
        data = fetch_all(query)
        if params['role_name'] == 'doctor':
            for row in data:
                row['doctor_details'] = DoctorModule.details(
                    {'doctor_id': str(row['id'])})
                row['hospital_details'] = HospitalModule.details(
                    {'hospital_id': str(row['doctor_details'].get('doctor_hospital_id', "-1"))})
        return data

    def insertNewItem(params):
        required = ['lat', 'long', 'id', 'role_name']
        for i in required:
            if i not in params:
                return {"errno": 403}
        if not is_valid(params):
            return {"errno": 403}
        roles = ['doctor', 'physiotherapist', 'nurse', 'hospital']
        if params['role_name'] not in roles:
            return {"errno": 403}
        degree_width = 111
        lat, long = params['lat'], params['long']
        _id, role_name = params['id'], params['role_name']
        k_lat = int(float(lat) * degree_width / 2)
        k_long = int(float(long) * degree_width / 2)
        query = f"""
            insert into coordinates
            set k_latitude = {k_lat}, k_longitude = {k_long},
            latitude = {lat}, longitude = {long}, id = {_id},
            role_name = '{role_name}'
        """
        data = upsert(query)
        return data
