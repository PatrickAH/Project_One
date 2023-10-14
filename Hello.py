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
from Ingredient import Ingredient
from Diet import Diet
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

#END OF DIETITIAN CLASS


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


########################## Generate Meal Plan

# should it be get??
@app.get('/MealPrep/generateMealPlan')
def generate_meal_plan_LSM():
    data = request.get_json()
    meal_plan = MealPrep.generate_meal_plan_LSM(data['dietitian_ID'], data['protein_goal'], data['carbs_goal'], data['fat_goal'], data['nbr_days'])
    return meal_plan
# should it be get??
@app.get('/MealPrep/generateMealPlanFixedLunch')
def generate_meal_plan_fixed_lunch():
    data = request.get_json()
    meal_plan = MealPrep.generate_meal_plan_with_fixed_lunch(data['dietitian_ID'], data['protein_goal'], data['carbs_goal'], data['fat_goal'], data['nbr_days'], data['fixed_lunch_id'])
    return meal_plan

@app.get('/MealPrep/generateShoppingList')
def generate_shopping_list():
    data = request.get_json()
    return MealPrep.generate_shopping_list(data['dietitian_ID'], data['recipee_id'])
    
@app.get('/MealPrep/getPatientMealPlanHistory')
def get_patient_meal_plan_history():
    # this funciton was not tested due to lack of data in the meal_prep table 
    data = request.get_json()
    return MealPrep.get_patient_meal_plan_history(data['patient_id'], data['dietitian_id'])



########################## Ingredient Class
@app.get('/Ingredient/details')
def getIngredientDetails():
    data = request.get_json()
    return Ingredient.fetchIngredientDetails(data['ingredient_id'])

@app.post('/Ingredient/addIngredient')
def addIngredient():
    data = request.get_json()
    return Ingredient.addIngredient(json.dumps(data))    
           
@app.put('/Ingredient/updateIngredient')
def updateIngredient():
    try:
        data = request.get_json()
        ingredient_id = data.get('ingredient_id')

        if not ingredient_id:
            return jsonify({'status': 'failed', 'message': 'Ingredient ID is required'}), 400

        result = Ingredient.updateIngredient(ingredient_id, data)
        return jsonify({'status': 'success', 'message': result}), 200

    except ValueError as ve:
        return jsonify({'status': 'failed', 'message': str(ve)}), 400
    except Exception as e:
        app.logger.error(f"Exception occurred: {e}")
        return jsonify({'status': 'failed', 'message': 'Something went wrong'}), 500    


########################## Diet Class

@app.post('/Diet/createDiet')
def createDiet():
    data = request.get_json()
    return Diet.createDiet(json.dumps(data))
  

@app.put('/Diet/udpateDiet')
def updateDiet():
    try:
        data = request.get_json()
        diet_id = data.get('diet_id')

        if not diet_id:
            return jsonify({'status': 'failed', 'message': 'Diet ID is required'}), 400

        result = Diet.updateDiet(diet_id, data)
        return jsonify({'status': 'success', 'message': result}), 200

    except ValueError as ve:
        return jsonify({'status': 'failed', 'message': str(ve)}), 400
    except Exception as e:
        app.logger.error(f"Exception occurred: {e}")
        return jsonify({'status': 'failed', 'message': 'Something went wrong'}), 500     

@app.delete('/Diet/deleteDiet')
def deleteDiet():
    try:
        data = request.get_json()
        diet_id = data.get('diet_id')

        if not diet_id:
            return jsonify({'status': 'failed', 'message': 'Diet ID is required'}), 400

        result = Diet.deleteDiet(diet_id)
        return jsonify({'status': 'success', 'message': result}), 200

    except ValueError as ve:
        return jsonify({'status': 'failed', 'message': str(ve)}), 400
    except Exception as e:
        app.logger.error(f"Exception occurred: {e}")
        return jsonify({'status': 'failed', 'message': 'Something went wrong'}), 500  

@app.get('/Diet/getDietHistory')
def getDietHistory():
    try:
        data = request.get_json()
        patient_id = data.get('patient_id')

        if not patient_id:
            return jsonify({'status': 'failed', 'message': 'Patient ID is required'}), 400

        diets = Diet.getDietHistory(patient_id)
        return jsonify({'status': 'success', 'data': diets}), 200

    except ValueError as ve:
        return jsonify({'status': 'failed', 'message': str(ve)}), 400
    except Exception as e:
        app.logger.error(f"Exception occurred: {e}")
        return jsonify({'status': 'failed', 'message': 'Something went wrong'}), 500

@app.get('/Diet/getLastDiet')
def getLastDiet():
    try:
        data = request.get_json()
        patient_id = data.get('patient_id')

        if not patient_id:
            return jsonify({'status': 'failed', 'message': 'Patient ID is required'}), 400

        diet = Diet.getLastDiet(patient_id)
        
        if diet is None:
            return jsonify({'status': 'success', 'message': 'No diets found for the given patient ID'}), 200

        return jsonify({'status': 'success', 'data': diet}), 200

    except ValueError as ve:
        return jsonify({'status': 'failed', 'message': str(ve)}), 400
    except Exception as e:
        app.logger.error(f"Exception occurred: {e}")
        return jsonify({'status': 'failed', 'message': 'Something went wrong'}), 500





        


app.run()