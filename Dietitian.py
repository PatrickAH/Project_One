from flask import jsonify
import flask
from werkzeug.exceptions import BadRequest
import json
from Db_connection import Db_connection
from Patient import Patient


class Dietitian:

    # raise_amount = 1.04 -- this will appear in all classes 
    # in the self.raise_amount or Class.raise_amount but can be overridable

    def __init__(self,dietitianID,Fname,Lname,DOB,phone,email):
        self.dietitianID=dietitianID
        self.Fname=Fname
        self.Lname=Lname
        self.DOB=DOB
        self.phone=phone
        self.email=email
        # Dietitian.num_of_emps +=1 This will create a variable in all the instances

    def dietitian_json(self):
        print('json dietitian______')
        jsonDietitian = json.dumps(vars(self));
        print(jsonDietitian)
        return jsonDietitian;



# STATIC METHODS TO BE USED
    @staticmethod
    def fetchDietitian(d_email,d_pwd):
        cur = Db_connection.getConnection().cursor()
        if d_email == '' or d_pwd == '':
            return('Please enter an Email and Password');
        cur.execute("select d.dietitian_id, d.first_name , d.family_name , d.email , d.phone_number, to_char(d.date_of_birth, 'DD/MM/YYYY') from dietitian d where d.email = %s and d.pwd = %s",(d_email,d_pwd))
        dietitian = cur.fetchall()
        if cur.rowcount == 1 :
            print(cur.rowcount)
            dietitianR = Dietitian(dietitian[0][0],dietitian[0][1],dietitian[0][2],dietitian[0][3],dietitian[0][4],dietitian[0][5])
            cur.close;
            return dietitianR.dietitian_json();
        else :
            cur.close;
            return('The email or password is incorrect');


    @staticmethod
    def fetchDietitianPatients(dietitian_ID):
        cur = Db_connection.getConnection().cursor()
        if dietitian_ID == '':
            cur.close
            return('dietitian_ID is missing');
        cur.execute("select p.patient_id ,p.first_name ,p.last_name ,p.gender ,to_char(p.date_of_birth, 'DD/MM/YYYY'),p.phone ,p.email ,p.address ,p.dietitian_id ,p.status  from patient_static_info p where p.dietitian_id = %s",(dietitian_ID))
        patients = cur.fetchall()
        #patientsArray = [];
        jsonPatientsArray = [];
        for patient in patients:
            patientObject = Patient(patient[0],patient[1],patient[2],patient[3],patient[4],patient[5],patient[6],patient[7],patient[8],patient[9])
            #patientsArray.append(patientObject)
            jsonPatientsArray.append(patientObject.Patient_json())
        cur.close;
        return jsonPatientsArray;


#insert methods
    @staticmethod
    def createPatient(patientJSON):
        patientData = json.loads(patientJSON)
        if patientData['dietitian_id'] == '' :
            return 'Dietitian ID is missing'
        if patientData['pwd'] =='' :
            return 'please set a temporary password for the client'
        cur = Db_connection.getConnection().cursor()
        cur.execute("INSERT INTO public.patient_static_info (first_name, last_name, gender, date_of_birth, phone, email, address, dietitian_id, pwd, status) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING patient_id"
                    ,(patientData['first_name'], patientData['last_name'], patientData['gender'], patientData['date_of_birth'], 
                      patientData['phone'], patientData['email'], patientData['address'], patientData['dietitian_id']
                      , patientData['pwd'], 'ACTIVE'));
        patient_ID = cur.fetchone()[0]
        print('patient ID is ',patient_ID)
        Db_connection.commit();
        patientData['patient_id'] = str(patient_ID)
        return json.dumps(patientData)
    
    @staticmethod
    def deactivatePatient(patient_ID):
        if patient_ID == '' :
            return 'Patient ID is missing'
        cur = Db_connection.getConnection().cursor()
        cur.execute("UPDATE patient_static_info SET status= %s WHERE patient_id= %s",("UNACTIVE",patient_ID));
        Db_connection.commit();
        return patient_ID

    @staticmethod
    def activatePatient(patient_ID):
        if patient_ID == '' :
            return 'Patient ID is missing'
        cur = Db_connection.getConnection().cursor()
        cur.execute("UPDATE patient_static_info SET status= %s WHERE patient_id= %s",("ACTIVE",patient_ID));
        Db_connection.commit();
        return patient_ID
