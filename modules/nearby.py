from .validate import is_valid
from models.db_connection import fetch_all, upsert


class MapsModule:
    def getNearByItems(params):
        required = ['lat', 'long', 'range', 'role_name']
        for i in required:
            if i not in params:
                return {"errno": 403}
        if not is_valid(params):
            return {"errno": 403}
        lat, long, range = params['lat'], params['long'], params['range']
        degree_width, limit = 111, int(int(range) / 2 + 0.5)
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
        return data

    def insertNewItem(params):
        required = ['lat', 'long', 'id', 'role_name']
        for i in required:
            if i not in params:
                return {"errno": 403}
        if not is_valid(params):
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
