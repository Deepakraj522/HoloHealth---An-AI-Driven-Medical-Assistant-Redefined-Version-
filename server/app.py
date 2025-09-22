from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import pickle
import pandas as pd
import openai
import os
import json
import requests

# Initialize Flask app
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Try to load models, but continue if they fail
outcome_model = None
disease_model = None

try:
    with open('assets/outcome_model.pkl', 'rb') as f:
        outcome_model = pickle.load(f)
    print("Outcome model loaded successfully")
except Exception as e:
    print(f"Could not load outcome model: {e}")

try:
    with open('assets/disease_model.pkl', 'rb') as f:
        disease_model = pickle.load(f)
    print("Disease model loaded successfully")
except Exception as e:
    print(f"Could not load disease model: {e}") 

# Welcome GET Request API
@app.route('/', methods=['GET'])
@cross_origin()
def status():
    return jsonify({'service': 'diagnoze-api', 'status': 'active'}), 200

@app.route('/predict', methods=['POST'])
@cross_origin()
def predict():
    try:
        data = request.json
        print(f"Prediction request: {data}")
        
        # Handle both old format (from SymptomAnalysis) and new format (from other components)
        if 'symptoms' in data:
            # New format: {"symptoms": ["fever", "cough", "fatigue"]}
            symptoms = data['symptoms']
            
            # Convert symptoms to our prediction logic
            prediction_result = predict_from_symptoms(symptoms)
            return jsonify(prediction_result)
        
        else:
            # Old format: {"fever": "Yes", "cough": "Yes", ...}
            input_data = pd.DataFrame({
                "Fever": [1 if data.get("fever", "No") == "Yes" else 0],
                "Cough": [1 if data.get("cough", "No") == "Yes" else 0],
                "Fatigue": [1 if data.get("fatigue", "No") == "Yes" else 0],
                "Difficulty Breathing": [1 if data.get("difficulty_breathing", "No") == "Yes" else 0],
                "Age": [data.get("age", 25)],
                "Gender": [1 if data.get("gender", "Male") == "Male" else 0],
                "Blood Pressure": [0 if data.get("blood_pressure", "Normal") == "Low" else 1 if data.get("blood_pressure", "Normal") == "Normal" else 2],
                "Cholesterol Level": [0 if data.get("cholesterol", "Normal") == "Normal" else 1]
            })
            
            try:
                if outcome_model is not None and disease_model is not None:
                    outcome_prediction = outcome_model.predict(input_data)[0]
                    
                    if outcome_prediction != "Positive":
                        return jsonify({'status': False, 'disease': None, 'confidence': 0})
                        
                    disease_prediction = disease_model.predict(input_data)[0]
                    return jsonify({'status': True, 'disease': disease_prediction, 'confidence': 85})
                else:
                    raise Exception("Models not available")
            except Exception as model_error:
                print(f"Model prediction error: {str(model_error)}")
                # Fallback to symptom-based prediction
                symptoms = []
                if data.get("fever") == "Yes":
                    symptoms.append("fever")
                if data.get("cough") == "Yes":
                    symptoms.append("cough")
                if data.get("fatigue") == "Yes":
                    symptoms.append("fatigue")
                if data.get("difficulty_breathing") == "Yes":
                    symptoms.append("difficulty_breathing")
                
                prediction_result = predict_from_symptoms(symptoms)
                return jsonify({
                    'status': True if prediction_result.get('prediction') != 'No significant symptoms detected' else False,
                    'disease': prediction_result.get('prediction'),
                    'confidence': prediction_result.get('confidence', 50)
                })
                
    except Exception as e:
        print(f"Prediction error: {str(e)}")
        return jsonify({'error': 'Prediction failed', 'details': str(e)}), 500

def predict_from_symptoms(symptoms):
    """Predict disease from symptom list"""
    if not symptoms:
        return {'prediction': 'No symptoms provided', 'confidence': 0}
    
    # Disease mapping
    DISEASE_MAPPING = {
        'Psoriasis': 'Dermatologist',
        'Impetigo': 'Dermatologist', 
        'Heart Attack': 'Cardiologist',
        'Hypertension': 'Cardiologist',
        'Diabetes': 'Endocrinologist',
        'Hypothyroidism': 'Endocrinologist',
        'Gastroenteritis': 'Gastroenterologist',
        'Jaundice': 'Gastroenterologist',
        'Osteoarthristis': 'Rheumatologist',
        'Cervical spondylosis': 'Neurologist',
        '(vertigo) Paroymsal  Positional Vertigo': 'Neurologist',
        'Bronchial Asthma': 'Pulmonologist',
        'Common Cold': 'General Practitioner',
        'Flu': 'General Practitioner',
        'Migraine': 'Neurologist',
        'Anxiety': 'Psychiatrist',
        'Depression': 'Psychiatrist'
    }
    
    # Symptom to disease mapping
    SYMPTOM_DISEASE_MAPPING = {
        'fever,cough,fatigue': 'Common Cold',
        'fever,cough,difficulty_breathing': 'Flu', 
        'headache,nausea,sensitivity_to_light': 'Migraine',
        'chest_pain,difficulty_breathing,sweating': 'Heart Attack',
        'joint_pain,swelling,stiffness': 'Osteoarthristis',
        'skin_rash,itching,scaling': 'Psoriasis',
        'abdominal_pain,nausea,vomiting': 'Gastroenteritis',
        'fatigue,weight_gain,cold_intolerance': 'Hypothyroidism',
        'increased_urination,excessive_thirst,fatigue': 'Diabetes',
        'high_bp,headache,chest_pain': 'Hypertension',
        'neck_pain,stiffness,headache': 'Cervical spondylosis',
        'dizziness,loss_of_balance,nausea': '(vertigo) Paroymsal  Positional Vertigo',
        'cough,difficulty_breathing,wheezing': 'Bronchial Asthma',
        'skin_infection,pus,redness': 'Impetigo',
        'yellow_skin,dark_urine,pale_stool': 'Jaundice'
    }
    
    # Normalize symptoms
    normalized_symptoms = [s.lower().replace(' ', '_') for s in symptoms]
    symptom_string = ','.join(sorted(normalized_symptoms))
    
    # Check for direct matches
    prediction = None
    for pattern, disease in SYMPTOM_DISEASE_MAPPING.items():
        pattern_symptoms = set(pattern.split(','))
        user_symptoms = set(normalized_symptoms)
        
        overlap = len(pattern_symptoms.intersection(user_symptoms))
        if overlap >= min(2, len(pattern_symptoms) * 0.6):
            prediction = disease
            break
    
    # Fallback prediction logic
    if not prediction:
        symptom_keywords = normalized_symptoms
        
        if any(keyword in symptom_keywords for keyword in ['fever', 'cough', 'cold']):
            if 'difficulty_breathing' in symptom_keywords:
                prediction = 'Flu'
            else:
                prediction = 'Common Cold'
        elif any(keyword in symptom_keywords for keyword in ['headache', 'head_pain']):
            prediction = 'Migraine'
        elif any(keyword in symptom_keywords for keyword in ['chest_pain', 'heart']):
            prediction = 'Heart Attack'
        elif any(keyword in symptom_keywords for keyword in ['joint_pain', 'knee_pain', 'back_pain']):
            prediction = 'Osteoarthristis'
        elif any(keyword in symptom_keywords for keyword in ['skin', 'rash', 'itching']):
            prediction = 'Psoriasis'
        elif any(keyword in symptom_keywords for keyword in ['abdominal_pain', 'stomach', 'nausea']):
            prediction = 'Gastroenteritis'
        elif any(keyword in symptom_keywords for keyword in ['fatigue', 'tiredness', 'weakness']):
            prediction = 'Hypothyroidism'
        elif any(keyword in symptom_keywords for keyword in ['dizziness', 'vertigo', 'balance']):
            prediction = '(vertigo) Paroymsal  Positional Vertigo'
        else:
            prediction = 'General consultation recommended'
    
    # Calculate confidence
    confidence = min(95, max(60, len(symptoms) * 15 + 30))
    
    return {
        'prediction': prediction,
        'confidence': confidence,
        'recommended_specialist': DISEASE_MAPPING.get(prediction, 'General Practitioner')
    }

@app.route('/chat', methods=['POST'])
@cross_origin()
def chat():
    try:
        data = request.get_json()
        messages = data.get("messages", [])
        provider = data.get("provider", "deepseek")
        
        print(f"Chat request - Provider: {provider}, Messages: {len(messages)}")
        
        # Handle different AI models via OpenRouter
        if provider in ["deepseek", "llama", "gemma"]:
            import requests
            
            # Map provider to actual model names
            model_map = {
                "deepseek": "deepseek/deepseek-r1-0528:free",
                "llama": "meta-llama/llama-3.2-3b-instruct:free",
                "gemma": "google/gemma-2-9b-it:free"
            }
            
            model_name = model_map.get(provider, "deepseek/deepseek-r1-0528:free")
            
            # OpenRouter API call
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": "Bearer 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",
                    "HTTP-Referer": "http://localhost:3000",
                    "X-Title": "HoloHealth",
                    "Content-Type": "application/json"
                },
                json={
                    "model": model_name,
                    "messages": [
                        {"role": "system", "content": "You are a helpful and supportive medical assistant. Provide helpful, caring responses about health and wellness."},
                        *messages
                    ]
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                reply = result["choices"][0]["message"]["content"]
                print(f"AI Response: {reply[:100]}...")
            else:
                print(f"OpenRouter API Error: {response.status_code} - {response.text}")
                reply = "I'm sorry, I'm having trouble connecting to the AI service right now. Please try again later."

        elif provider == "openai":
            try:
                from openai import OpenAI
                client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a helpful and supportive medical assistant."},
                        *messages
                    ]
                )
                reply = response.choices[0].message.content
            except Exception as e:
                print(f"OpenAI Error: {str(e)}")
                reply = "I'm sorry, I'm having trouble with the OpenAI service right now."

        elif provider == "gemini":
            try:
                import google.generativeai as genai
                genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
                model = genai.GenerativeModel('gemini-pro')
                
                # Combine all messages into a single prompt
                prompt = "You are a helpful and supportive medical assistant.\n\n"
                for msg in messages:
                    prompt += f"{msg['role']}: {msg['content']}\n"
                
                response = model.generate_content(prompt)
                reply = response.text
            except Exception as e:
                print(f"Gemini Error: {str(e)}")
                reply = "I'm sorry, I'm having trouble with the Gemini service right now."

        else:
            return jsonify({"error": "Invalid provider specified."}), 400

        return jsonify({"reply": reply})

    except Exception as e:
        print(f"Chat error: {str(e)}")
        return jsonify({"error": f"Chat service error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run()
