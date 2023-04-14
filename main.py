import os
import requests
from datetime import datetime

GENDER = "male"
WEIGHT_KG = 70
HEIGHT_CM = 180
AGE = 26
APP_ID = os.environ.get("APP_ID")
API_KEY = os.environ.get("API_KEY")
NUTRIENTS_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"
SHEETY_AUTH = os.environ.get("SHEETY_AUTH")
SHEETY_ENDPOINT = os.environ.get("SHEETY_ENDPOINT")

user_input = input("What did you do today?: ")
headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

data = {
    "query": user_input,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE,
}
#------------------------GETTING THE CALLORIES BURNED THROUGH NUTRIENT API--------------------------#
nutrient_request = requests.post(NUTRIENTS_ENDPOINT, json=data, headers=headers)

nutrient_request.raise_for_status()

result = nutrient_request.json()
duration = result["exercises"][0]["duration_min"]
calories = result["exercises"][0]["nf_calories"]
exercise_name = result["exercises"][0]["name"]


sheety_headers = {
    "Authorization": SHEETY_AUTH
}

date = datetime.now().strftime("%Y/%m/%d")
time = datetime.now().strftime("%H:%M:%S")

add_workout = {
    "workout": {
        "date": date,
        "time": time,
        "exercise": exercise_name.title(),
        "duration": duration,
        "calories": calories,
    }
}
#------------------------------POSTING DATA THROUGH SHEETY API---------------------------------#
post_data = requests.post(SHEETY_ENDPOINT, json=add_workout, headers=sheety_headers)
post_data.raise_for_status()
print(post_data.text)