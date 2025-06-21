import pandas as pd
import numpy as np
import pickle

with open("random_forest_model.pkl", "rb") as f:
    model = pickle.load(f)


description = pd.read_csv("description (version 1).csv")
precautions = pd.read_csv("precautions_df (version 1).csv")
diets = pd.read_csv("diets (version 1).csv")
workout = pd.read_csv("workout_df (version 1).csv")
medications = pd.read_csv("medications (version 1).csv")
training = pd.read_csv("Training (version 1).csv")

# Use the same symptoms list as healthcare-app.py
symptoms_list = training.columns[:-1].tolist()  # All columns except the last one (prognosis)
disease_names = sorted(training["prognosis"].unique())

def predict_disease(symptoms_selected):
    input_vector = [1 if symptom in symptoms_selected else 0 for symptom in symptoms_list]
    prediction = model.predict(np.array(input_vector).reshape(1, -1))[0]
    if isinstance(prediction, (int, np.integer)):
        prediction = disease_names[prediction]
    return prediction

def get_symptoms_list():
    return symptoms_list

def get_recommendations(symptoms_selected):
    predicted = predict_disease(symptoms_selected)
    desc_row = description[description['Disease'] == predicted]
    desc = desc_row['Description'].values[0] if not desc_row.empty else "No description found."
    pre_row = precautions[precautions['Disease'] == predicted]
    pre = pre_row.iloc[:, 1:].dropna(axis=1).values.flatten() if not pre_row.empty else ["No precautions found."]
    diet_row = diets[diets['Disease'] == predicted]
    diet = diet_row['Diet'].values[0] if not diet_row.empty else "No diet recommendations found."
    work_row = workout[workout['disease'] == predicted]
    work = work_row['workout'].values if not work_row.empty else ["No workouts found."]
    med_row = medications[medications['Disease'] == predicted]
    med = med_row['Medication'].values[0] if not med_row.empty else "No medications found."
    return {
        'disease': predicted,
        'desc': desc,
        'precautions': pre,
        'diet': diet,
        'workouts': work,
        'medications': med
    } 

