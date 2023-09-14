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
    def generate_meal_plan_LSM_best_combination(dietitian_ID, protein_goal, carbs_goal, fat_goal):
        cur = Db_connection.getConnection().cursor()
        if dietitian_ID == '':
            cur.close()
            return 'Dietitian ID is missing'
        
        # Fetch all meals
        cur.execute("SELECT recipee_id, protein, carbs, fat, meal_type FROM recipee")
        meals = cur.fetchall()
        
        breakfasts = [meal for meal in meals if meal[4] == 'Breakfast']
        lunches = [meal for meal in meals if meal[4] == 'Lunch']
        dinners = [meal for meal in meals if meal[4] == 'Dinner']
        
        # Generate all possible combinations of meals for breakfast, lunch, and dinner
        meal_combinations = list(itertools.product(breakfasts, lunches, dinners))
        
        best_score = float('inf')
        best_combination = None
        
        for combo in meal_combinations:
            protein_meals = sum(meal[1] for meal in combo)
            carbs_meals = sum(meal[2] for meal in combo)
            fat_meals = sum(meal[3] for meal in combo)
            
            # Calculate LSM score
            score = ((protein_goal - protein_meals)**2 + 
                     (carbs_goal - carbs_meals)**2 + 
                     (fat_goal - fat_meals)**2)
            
            if score < best_score:
                best_score = score
                best_combination = [meal[0] for meal in combo]  # Assuming meal[0] is the recipee_id
        
        cur.close()
        return json.dumps({"best_combination": best_combination, "best_score": best_score}, default=handle_decimal)
    
    
    @staticmethod
    def generate_meal_plan_LSM_seven_best_combinations(dietitian_ID, protein_goal, carbs_goal, fat_goal):
        cur = Db_connection.getConnection().cursor()
        if dietitian_ID == '':
            cur.close()
            return 'Dietitian ID is missing'
        
        # Fetch meals by type
        cur.execute("SELECT recipee_id, protein, carbs, fat, meal_type FROM recipee")
        meals = cur.fetchall()
        
        breakfasts = [meal for meal in meals if meal[4] == 'Breakfast']
        lunches = [meal for meal in meals if meal[4] == 'Lunch']
        dinners = [meal for meal in meals if meal[4] == 'Dinner']
        
        # Generate all possible combinations of meals for breakfast, lunch, and dinner
        meal_combinations = list(itertools.product(breakfasts, lunches, dinners))
        
        
        # Use a heap to keep track of the top 7 combinations
        top_combinations = []
        
        for combo in meal_combinations:
            protein_meals = sum(meal[1] for meal in combo)
            carbs_meals = sum(meal[2] for meal in combo)
            fat_meals = sum(meal[3] for meal in combo)
            
            # Calculate LSM score
            score = ((protein_goal - protein_meals)**2 + 
                      (carbs_goal - carbs_meals)**2 + 
                      (fat_goal - fat_meals)**2)
            
            # Add the combination and its score to the heap
            heapq.heappush(top_combinations, (score, [meal[0] for meal in combo]))
            
            # Keep only the top 7 combinations in the heap
            if len(top_combinations) > 7:
                heapq.heappop(top_combinations)
        
        # Extract the best combinations from the heap
        print (top_combinations)
        best_combinations = [heapq.heappop(top_combinations) for _ in range(len(top_combinations))]
        best_combinations.reverse()  # Reverse to have the lowest (best) scores first
        # print (best_combinations)
        cur.close()
        return json.dumps({"best_combinations": best_combinations}, default=handle_decimal)