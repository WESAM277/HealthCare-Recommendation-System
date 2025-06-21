from flask import Flask, render_template, request
from healthcare_core import get_symptoms_list, get_recommendations

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    recommendations = None
    selected_symptoms = []
    symptoms_list = get_symptoms_list()
    print(f"Symptoms list: {symptoms_list}")  # Debug print
    if request.method == 'POST':
        selected_symptoms = request.form.getlist('symptoms')
        print(f"Selected symptoms: {selected_symptoms}")  # Debug print
        if selected_symptoms:
            recommendations = get_recommendations(selected_symptoms)
            print(f"Recommendations: {recommendations}")  # Debug print
    return render_template('index.html', symptoms_list=symptoms_list, recommendations=recommendations, selected_symptoms=selected_symptoms)

@app.route('/developers')
def developers():
    return render_template('developers.html')

if __name__ == '__main__':
    app.run(debug=True)


    #cd "C:\Users\user\Desktop\ah-healthcare"
