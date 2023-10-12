# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 21:52:42 2023

@author: gjreij-ext
"""

# Model for MealPrep
from Db_connection import Db_connection
import json
import itertools
import heapq
from decimal import Decimal

def handle_decimal(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError
    
    
class MealPrep:

    def __init__(self, diet_id, recipee_id, date,meal_id,patient_id,diet_start_date):
        self.diet_id = diet_id
        self.recipee_id = recipee_id  
        self.date = date  
        self.meal_id = meal_id  
        self.patient_id = patient_id
        self.diet_start_date = diet_start_date  

    def MealPrep_json(self):
        return json.dumps(vars(self), default=str)
    
    
        
    @staticmethod
    def generate_shopping_list(dietitian_ID, recipee_id):
        cur = Db_connection.getConnection().cursor()
        if dietitian_ID == '':
            cur.close()
            return 'Dietitian ID is missing'
        
        query = f"""SELECT ingredient_id, grammes, litters, cup, tbsp, tsp, small, medium, "Large" 
                    FROM recipeingredients WHERE recipee_id = {recipee_id}"""
        cur.execute(query)
        
        ingredients = cur.fetchall()
        shopping_list = [ingredient[0] for ingredient in ingredients]  
        
        cur.close()
        return json.dumps({"shopping_list": shopping_list})
    
    
    
    @staticmethod
    def generate_meal_plan_LSM(dietitian_ID, protein_goal, carbs_goal, fat_goal, nbr_days):
        cur = Db_connection.getConnection().cursor()
        if dietitian_ID == '':
            cur.close()
            return 'Dietitian ID is missing'
        
        # Fetch all meals
        cur.execute("SELECT recipee_id, protein, carbs, fat, meal_type, servings FROM recipee")
        meals = cur.fetchall()
        
        breakfasts = [meal for meal in meals if meal[4] == 'Breakfast']
        lunches = [meal for meal in meals if meal[4] == 'Lunch']
        dinners = [meal for meal in meals if meal[4] == 'Dinner']
        # Use a heap to keep track of the top 7 combinations
        all_combinations = []
        
        # Generate all possible combinations of meals for breakfast, lunch, and dinner
        for breakfast in breakfasts:
            for lunch in lunches:
                for dinner in dinners:
                    for breakfast_servings in range(1, int(breakfast[5]) + 1):  # Assuming servings is an integer
                        for lunch_servings in range(1, int(lunch[5]) + 1):
                            for dinner_servings in range(1, int(dinner[5]) + 1):
                                protein_meals = (breakfast[1] * breakfast_servings + 
                                                 lunch[1] * lunch_servings + 
                                                 dinner[1] * dinner_servings)
                                carbs_meals = (breakfast[2] * breakfast_servings + 
                                               lunch[2] * lunch_servings + 
                                               dinner[2] * dinner_servings)
                                fat_meals = (breakfast[3] * breakfast_servings + 
                                             lunch[3] * lunch_servings + 
                                             dinner[3] * dinner_servings)
                                
                                # Calculate LSM score
                                score = (4*(protein_goal - protein_meals)**2 + 
                                         (carbs_goal - carbs_meals)**2 + 
                                         (fat_goal - fat_meals)**2)
                                
                                # Add the combination and its score to the heap
                                combination = {
                                    "breakfast": breakfast[0:4],
                                    "lunch": lunch[0:4],
                                    "dinner": dinner[0:4],
                                    "breakfast_servings": breakfast_servings,
                                    "lunch_servings": lunch_servings,
                                    "dinner_servings": dinner_servings,
                                    "score": score,
                                }
                                
                                all_combinations.append(combination)
        
        # Sort the combinations based on LSM score in ascending order
        all_combinations.sort(key=lambda x: x["score"])
        best_combinations = all_combinations[:nbr_days]
        cur.close()
        

        return json.dumps({"best_combinations": best_combinations}, default=lambda x: float(x) if isinstance(x, Decimal) else x)
    
    
    def generate_meal_plan_with_fixed_lunch(dietitian_ID, protein_goal, carbs_goal, fat_goal, nbr_days, fixed_lunch_id):
        cur = Db_connection.getConnection().cursor()
        if dietitian_ID == '':
            cur.close()
            return 'Dietitian ID is missing'
        
        # Fetch all meals
        cur.execute("SELECT recipee_id, protein, carbs, fat, meal_type, servings FROM recipee")
        meals = cur.fetchall()
        
        breakfasts = [meal for meal in meals if meal[4] == 'Breakfast']
        lunches = [meal for meal in meals if meal[4] == 'Lunch' and meal[0] == fixed_lunch_id]
        dinners = [meal for meal in meals if meal[4] == 'Dinner']
        
        # Use a list to keep track of the top combinations
        all_combinations = []
        
        # Fetch the fixed lunch
        fixed_lunch = lunches[0] if lunches else None
        if not fixed_lunch:
            return 'Invalid fixed lunch ID'
        
        # Generate all possible combinations of meals for breakfast and dinner with the fixed lunch
        for breakfast in breakfasts:
            for dinner in dinners:
                for breakfast_servings in range(1, int(breakfast[5]) + 1):
                    for dinner_servings in range(1, int(dinner[5]) + 1):
                        for lunch_servings in range(1, int(fixed_lunch[5]) + 1):
                            protein_meals = (breakfast[1] * breakfast_servings + 
                                             fixed_lunch[1] * lunch_servings + 
                                             dinner[1] * dinner_servings)
                            carbs_meals = (breakfast[2] * breakfast_servings + 
                                           fixed_lunch[2] * lunch_servings + 
                                           dinner[2] * dinner_servings)
                            fat_meals = (breakfast[3] * breakfast_servings + 
                                         fixed_lunch[3] * lunch_servings + 
                                         dinner[3] * dinner_servings)
                            
                            # Calculate LSM score
                            score = (4*(protein_goal - protein_meals)**2 + 
                                     (carbs_goal - carbs_meals)**2 + 
                                     (fat_goal - fat_meals)**2)
                            
                            # Add the combination and its score to the list
                            combination = {
                                "breakfast": breakfast[0:4],
                                "lunch": fixed_lunch[0:4],
                                "dinner": dinner[0:4],
                                "breakfast_servings": breakfast_servings,
                                "lunch_servings": lunch_servings,
                                "dinner_servings": dinner_servings,
                                "score": score,
                            }
                            
                            all_combinations.append(combination)
        
        # Sort the combinations based on LSM score in ascending order
        all_combinations.sort(key=lambda x: x["score"])
        best_combinations = all_combinations[:nbr_days]
        cur.close()
        
        return json.dumps({"best_combinations": best_combinations}, default=lambda x: float(x) if isinstance(x, Decimal) else x)

    @staticmethod
    def get_patient_meal_plan_history(patient_id, dietitian_id):
        cur = Db_connection.getConnection().cursor()
        
        if not patient_id or not dietitian_id:
            cur.close()
            return 'Patient ID or Dietitian ID is missing'
        
        # Query to fetch all meal plans for the given patient_id and dietitian_id
        cur.execute("SELECT * FROM meal_prep WHERE patient_id = %s AND dietitian_id = %s", (patient_id, dietitian_id))
        
        meal_plans = cur.fetchall()
        
        # Convert the result to a list of dictionaries for easier JSON serialization
        meal_plans_list = []
        for meal_plan in meal_plans:
            meal_plan_dict = {
                'diet_id': meal_plan[0],
                'recipee_id': meal_plan[1],
                'Date': meal_plan[2],
                'meal_id': meal_plan[3],
                'quantity': meal_plan[4],
                'patient_id': meal_plan[5],
                'diet_start_date': meal_plan[6]
            }
            meal_plans_list.append(meal_plan_dict)
        
        cur.close()
        
        return json.dumps({"meal_plans": meal_plans_list})
        