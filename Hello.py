import json
from werkzeug.exceptions import BadRequest
from flask import Flask, jsonify, request
from BodyComp import BodyComp
from Db_connection import Db_connection
from Dietitian import Dietitian
from HealthHist import HealthHist
from LifeStyle import LifeStyle
from Patient import Patient
from Anthropometry import Anthropometry
from MealPrep import MealPrep
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello world!'
    
#DIETITIAN CLASS
@app.get('/dietitian/login')
def getDietitian():
    try:
        data = request.get_json()
        return Dietitian.fetchDietitian(data['dietitian_email'],data['dietitian_pwd']);
    except:
        raise BadRequest('Something went wrong, please contact the system provider');
    
@app.get('/dietitian/patients')
def fetDietitianPatients():
    try:
        data = request.get_json()
        return Dietitian.fetchDietitianPatients(data['dietitian_ID']);
    except:
        raise BadRequest('Something went wrong, please contact the system provider');


@app.post('/dietitian/createPatient')
def setPatient():
    data = request.get_json()
    return Dietitian.createPatient(json.dumps(data))

@app.post('/dietitian/deactivatePatient')
def deactivatePatient():
    data = request.get_json()
    return Dietitian.deactivatePatient(data['patient_ID']);

@app.post('/dietitian/activatePatient')
def activatePatient():
    data = request.get_json()
    return Dietitian.activatePatient(data['patient_ID']);

#END OF DIETITIAN CLASS.


#PATIENT CLASS
@app.get('/patient/login')
def getPatient():
    try:
        data = request.get_json()
        return Patient.fetchPatient(data['patient_email'],data['patient_pwd']);
    except:
        raise BadRequest('Something went wrong, please contact the system provider');

@app.get('/patient/staticInfo')
def getPatientStaticInfo():
    try:
        data = request.get_json()
        return Patient.fetchPatientStaticInfo(data['patient_ID']);
    except:
        raise BadRequest('Something went wrong, please contact the system provider');


@app.get('/patient/LastAnthropometry')
def getPatientLastAnthropometry():
    #try:
        data = request.get_json()
        return Anthropometry.fetchPatientLastAnth(data['patient_ID']);
  #  except:
   #     raise BadRequest('Something went wrong, please contact the system provider');


@app.get('/patient/AnthropometryHistory')
def getPatientAnthropometryHist():
    #try:
        data = request.get_json()
        return Anthropometry.fetchPatientAnthHist(data['patient_ID']);
  #  except:
   #     raise BadRequest('Something went wrong, please contact the system provider');

@app.get('/patient/LastBodyComp')
def getPatientLastBodyComp():
    #try:
        data = request.get_json()
        return BodyComp.fetchPatientLastBC(data['patient_ID']);
  #  except:
   #     raise BadRequest('Something went wrong, please contact the system provider');


@app.get('/patient/BodyCompHistory')
def getPatientBodyCompHist():
    #try:
        data = request.get_json()
        return BodyComp.fetchPatientBCHist(data['patient_ID']);
  #  except:
   #     raise BadRequest('Something went wrong, please contact the system provider');

@app.get('/patient/LastHealthHistory')
def getPatientLastHealthHistory():
    #try:
        data = request.get_json()
        return HealthHist.fetchPatientLastBC(data['patient_ID']);
  #  except:
   #     raise BadRequest('Something went wrong, please contact the system provider');


@app.get('/patient/allHealthHistory')
def getPatientAllHealthHistory():
    #try:
        data = request.get_json()
        return HealthHist.fetchPatientAllHealthHist(data['patient_ID']);
  #  except:
   #     raise BadRequest('Something went wrong, please contact the system provider');

@app.get('/patient/LastLifeStyle')
def getPatientLastLifeStyle():
    #try:
        data = request.get_json()
        return LifeStyle.fetchPatientLastLifeStyle(data['patient_ID']);
  #  except:
   #     raise BadRequest('Something went wrong, please contact the system provider');


@app.get('/patient/LifeStyleHistory')
def getPatientLifeStyleHistory():
    #try:
        data = request.get_json()
        return LifeStyle.fetchPatientLifeStyleHist(data['patient_ID']);
  #  except:
   #     raise BadRequest('Something went wrong, please contact the system provider');


@app.get('/patient/allInfo')
def getPatientAllInfo():
    #try:
        data = request.get_json()
        return Patient.fetchPatientAllInfo(data['patient_ID']);
  #  except:
   #     raise BadRequest('Something went wrong, please contact the system provider');


@app.delete('/patient/deletePatient')
def deletePatient():
    data = request.get_json()
    return Patient.deleteAccount(data['patient_ID']);

@app.put('/patient/updateStaticInfo')
def updatePatientStatic():
    data = request.get_json()
    return Patient.updatePatientStatInfo(json.dumps(data))

@app.post('/patient/addAnthropometry')
def addAnthropometry():
    data = request.get_json()
    return Anthropometry.addAnthropometry(json.dumps(data))

@app.post('/patient/addBodyComp')
def addBodyComp():
    data = request.get_json()
    return BodyComp.addBodyComp(json.dumps(data))


@app.post('/patient/addHealthHistory')
def addHealthHistory():
    data = request.get_json()
    return HealthHist.addHealthHistory(json.dumps(data))

@app.post('/patient/addLifeStyle')
def addLifeStyle():
    data = request.get_json()
    return LifeStyle.addLifeStyle(json.dumps(data))

#END OF PATIENT CLASS





@app.get('/recepies')
def getPatients():
    conn = Db_connection.getConnection()
    cur = conn.cursor()
    cur.execute('select r."Name" as recipee ,i."name" as ingredient, ri.grammes ,ri.litters, ri.cup ,ri.tbsp ,ri.small ,ri.medium ,ri."Large" from recipeingredients ri,recipee r, ingredient i where  r.recipee_id =ri.recipee_id and ri.ingredient_id = i.ingredient_id;')
    recepies = cur.fetchall()
    #print(recepies);
    # recepies = json.dumps(recepies)
    # print("_____________________________________________________");
    # print("______________________________________________________");
    # print(recepies);
    recepies = jsonify(recepies)
    # print("_____________________________________________________");
    # print("______________________________________________________");
    # print(recepies);
    # recepies = json.dumps(recepies);
    cur.close()
    return recepies;




############################################################## JREIJ'S CODE

# @app.post('/mealprep/add')
# def addMealPrep():
#     data = request.get_json()
#     return MealPrep.addMealPrep(json.dumps(data))


# Generate Meal Plan
@app.post('/MealPrep/generateMealPlanBestCombination')
def generate_meal_plan_one_combinationt():
    data = request.get_json()
    return MealPrep.generate_meal_plan_LSM_best_combination(data['dietitian_ID'],  data['protein_goal'], data['carbs_goal'], data['fat_goal'])

@app.post('/dietitian/generateMealPlanLSMSevenCombinations')
def generate_meal_plan_LSM_seven_best_combinations():
    data = request.get_json()
    return MealPrep.generate_meal_plan_LSM_seven_best_combinations(data['dietitian_ID'], data['protein_goal'], data['carbs_goal'], data['fat_goal'])

@app.post('/MealPrep/generateShoppingList')
def generate_shopping_list_endpoint():
    data = request.get_json()
    return MealPrep.generate_shopping_list(data['dietitian_ID'], data['recipee_id'])
    


app.run()