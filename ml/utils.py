import os
import joblib
import pandas as pd

from django.conf import settings


BASE_DIR = settings.BASE_DIR


# Chargement des fichiers ML
model_path = os.path.join(BASE_DIR, 'ml', 'models', 'model_final.pkl')
scaler_path = os.path.join(BASE_DIR, 'ml', 'models', 'scaler.pkl')
le_style_path = os.path.join(BASE_DIR, 'ml', 'models', 'le_style.pkl')
le_motivation_path = os.path.join(BASE_DIR, 'ml', 'models', 'le_motivation.pkl')
le_parental_path = os.path.join(BASE_DIR, 'ml', 'models', 'le_parental_support.pkl')
le_note_path = os.path.join(BASE_DIR, 'ml', 'models', 'le_note.pkl')
le_target_path = os.path.join(BASE_DIR, 'ml', 'models', 'le_target.pkl')


# Chargement du modèle et outils
model = joblib.load(model_path)
scaler = joblib.load(scaler_path)
le_style = joblib.load(le_style_path)
le_motivation = joblib.load(le_motivation_path)
le_parental_support = joblib.load(le_parental_path)
le_note = joblib.load(le_note_path)
le_target = joblib.load(le_target_path)


def predict_student(student):
    """
    Retourne la prédiction finale :
    A / B / C / D
    """

    try:
        # Encodage style apprentissage
        try:
            encoded_style = le_style.transform([student.learning_style])[0]
        except:
            encoded_style = 0

        # Nouveaux encodages demandés
        encoded_motivation = le_motivation.transform([student.motivation])[0]
        encoded_parental = le_parental_support.transform([student.parental_support])[0]
        encoded_previous_grade = le_note.transform([student.previous_grade])[0]

        # Construction des données avec l'ordre strict
        data = pd.DataFrame([{
            'Score_MiParcours': student.midterm_score,
            'Completion_Devoirs': student.assignment_completion,
            'Taux_Presence': student.attendance_rate,
            'Heures_Etude': student.study_hours,
            'Motivation': encoded_motivation,
            'Soutien_Parental': encoded_parental,
            'Note_Precedente': encoded_previous_grade,
            'Style_Apprentissage': encoded_style
        }])

        # Forcer l'ordre des colonnes explicitement
        column_order = [
            'Score_MiParcours', 'Completion_Devoirs', 'Taux_Presence', 
            'Heures_Etude', 'Motivation', 'Soutien_Parental', 
            'Note_Precedente', 'Style_Apprentissage'
        ]
        data = data[column_order]

        # Normalisation
        data_scaled = scaler.transform(data)

        # Prédiction
        prediction = model.predict(data_scaled)

        # Décodage avec le_target
        final_prediction = le_target.inverse_transform(prediction)[0]

        print("PREDICTION =", final_prediction)
        
        return final_prediction

    except Exception as e:
        print("Erreur prédiction :", e)
        return 'N/A'
        
