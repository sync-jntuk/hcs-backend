from .validate import is_valid
from models.db_connection import fetch_one, insert, fetch_all, insert_many


class UserModule:
    def create(params):
        if not is_valid(params):
            return {"errno": 403}
        required = [
            'patient_first_name', 'patient_middle_name', 'patient_last_name', 'patient_dob', 'patient_gender',
            'patient_blood_group', 'patient_aadhar', 'patient_pan_number', 'patient_voter_id', 'patient_occupation',
            'patient_primary_address', 'patient_mail', 'bank_name', 'branch_name', 'ifsc_code',
            'bank_account_number', 'patient_phone_number'
        ]
        for i in required:
            if i not in params:
                return {"errno": 403}
        patient_id = fetch_one("select * from master_count where master_name = 'patients'")
        if 'master_count' not in patient_id:
            return {"errno": 403}
        patient_id = '23' + str(int(patient_id['master_count']) + 1).rjust(6, '0')
        query = f"""
            insert into patient_master set patient_id = '{patient_id}',
        """
        for key, value in params.items():
            query += f"{key} = '{value}', "
        query = query[:-2]
        data = insert_many(
            [query, "update master_count set master_count = master_count + 1 where master_name = 'patients'"])
        return data


    def login(params):
        if not is_valid(params):
            return {"errno": 403}
        required = [
            'UserName', 'PassWord'
        ]
        for i in required:
            if i not in params:
                return {"errno": 403}
        query = f"""
            select * from patient_auth
            where (
                patient_id = '{params['UserName']}'
                or patient_mail = '{params['UserName']}'
                or phone_no = '{params['UserName']}'
            )
            and password = '{params['PassWord']}'
        """
        data = fetch_one(query)
        if 'patient_id' not in data:
            return {"errno": 404}
        patient_id = data['patient_id']
        field_maps = {
            "Patient Id": "patient_id",
            "First Name": "patient_first_name",
            "Middle Name": "patient_middle_name",
            "Last Name": "patient_last_name",
            "Date Of Birth": "patient_dob",
            "Gender": "patient_gender",
            "Blood Group": "patient_blood_group",
            "Aadhaar Number": "patient_aadhar",
            "Pan Card Number": "patient_pan_number",
            "Voter Card Number": "patient_voter_id",
            "Occupation": "patient_occupation",
            "Primary Address": "patient_primary_address",
            "Primary Email": "patient_primary_email",
            "Bank Name": "bank_name",
            "Branch Name": "branch_name",
            "IFSC Code": "ifsc_code",
            "Bank Account Number": "bank_account_number",
            "Phone Number": "patient_phone_number",
            "Alternative Phone Number": "patient_phone_number",
            "Nominee Name": "nominee_name",
            "Nominee Phone Number": "nominee_phone_number",
            "Nominee Relation": "nominee_relation",
            "Nominee Email": "nominee_mail",
            "Nominee Address": "nominee_address"
        }
        query = f"""
            select * from patient_master
            where patient_id = {patient_id}
        """
        rdata = fetch_one(query)
        rdata['patient_dob'] = str(rdata['patient_dob'])
        data = {k: (rdata.get(v, "xxxx") or "xxxx")
                for k, v in field_maps.items()}
        return data

    def bookAppointment(params):
        if not is_valid(params):
            return {"errno": 403}
        required = [
            'doctor_id', 'patient_id', 'appointment_date', 'appointment_time'
        ]
        for i in required:
            if i not in params:
                return {"errno": 403}
        params['appointment_date'] = '-'.join(
            params['appointment_date'].split('-')[::-1])
        query = f"""
            insert into appointments set
            doctor_id = '{params['doctor_id']}',
            patient_id = '{params['patient_id']}',
            appointment_date = '{params['appointment_date']}',
            appointment_time = '{params['appointment_time']}'
        """
        data = insert(query)
        return data

    def getAppointment(params):
        if not is_valid(params):
            return {"errno": 403}
        required = [
            'patient_id'
        ]
        for i in required:
            if i not in params:
                return {"errno": 403}
        query = f"""
            select * from appointments
            where patient_id = '{params['patient_id']}'
        """
        data = fetch_all(query)
        for row in data:
            row['appointment_date'] = str(row['appointment_date'])
            row['appointment_time'] = str(row['appointment_time'])
        return data
