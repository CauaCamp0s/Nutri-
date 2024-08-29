from flask import Flask, render_template, request
import requests
from googletrans import Translator

app = Flask(__name__)

# Chaves da API Edamam (substitua pelos valores reais)
EDAMAM_APP_ID = '9cb04da1'
EDAMAM_API_KEY = '479e57a53f395251946987b4a9a810b6'

# Inicializa o tradutor
translator = Translator()

# Função para buscar informações na Edamam API
def get_nutrition_data(food_item):
    url = "https://api.edamam.com/api/nutrition-data"
    params = {
        "app_id": EDAMAM_APP_ID,
        "app_key": EDAMAM_API_KEY,
        "ingr": food_item
    }
    response = requests.get(url, params=params)
    return response.json()

# Função para traduzir texto com googletrans
def translate_text(text, target_lang='pt'):
    translated = translator.translate(text, dest=target_lang)
    return translated.text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    food_item = request.form['food']
    nutrition_data = get_nutrition_data(food_item)

    # Extraindo e traduzindo informações relevantes
    translated_info = {}
    if 'totalNutrients' in nutrition_data:
        nutrients = nutrition_data['totalNutrients']
        name = translate_text(food_item)
        calories = nutrients.get('ENERC_KCAL', {}).get('quantity', 'N/A')
        protein = nutrients.get('PROCNT', {}).get('quantity', 'N/A')
        carbs = nutrients.get('CHOCDF', {}).get('quantity', 'N/A')
        fats = nutrients.get('FAT', {}).get('quantity', 'N/A')

        translated_info[name] = {
            'calories': calories,
            'protein': protein,
            'carbs': carbs,
            'fats': fats
        }

    return render_template('results.html', data=translated_info)

if __name__ == '__main__':
    app.run(debug=True)
