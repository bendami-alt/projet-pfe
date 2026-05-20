from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
import os

def create_report():
    doc = Document()
    
    # Define styles to be plain
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Arial'
    font.size = Pt(11)
    
    # Title
    title = doc.add_heading('PARTIE 4 : RÉALISATION (APPLICATION)', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # 14. Conception du système
    doc.add_heading('14. Conception du système', level=1)
    
    doc.add_heading('Schéma global', level=2)
    doc.add_paragraph(
        "L'application EduPredict fonctionne comme une passerelle interactive entre les utilisateurs finaux et les "
        "modèles prédictifs d'Intelligence Artificielle. Le système global repose sur une interaction client-serveur "
        "classique où le navigateur web (Frontend) communique avec un serveur web Django (Backend). Ce serveur interroge "
        "une base de données PostgreSQL pour la persistance des données et fait appel à un module d'Intelligence Artificielle "
        "(pipeline SVM sérialisé via Joblib) pour générer des prédictions en temps réel sur la performance académique."
    )
    
    doc.add_heading('Architecture simple', level=2)
    doc.add_paragraph(
        "EduPredict utilise l'architecture MVT (Model-View-Template) propre à Django :\n"
        "- Modèle (Model) : Gère le schéma de données (tables Utilisateurs, Étudiants, Professeurs) via l'ORM Django, "
        "et intègre la logique de déclenchement du pipeline ML lors de la sauvegarde d'un profil.\n"
        "- Vue (View) : Traite les requêtes HTTP, orchestre la logique métier (validation des formulaires, exécution de l'IA), "
        "et interagit avec la base de données PostgreSQL.\n"
        "- Gabarit (Template) : Fichiers HTML5/CSS3 utilisant Bootstrap 5 pour un affichage adaptatif (responsive) et dynamique des données."
    )
    
    doc.add_heading('Planification du projet (PERT et GANTT)', level=2)
    doc.add_paragraph(
        "[INSTRUCTION : Insérez ici vos diagrammes de GANTT et PERT illustrant la planification des tâches (Conception, "
        "Analyse de données, Développement Web, Tests) et l'allocation des ressources pour ce projet.]"
    )
    
    doc.add_heading('Modélisation UML', level=2)
    doc.add_paragraph(
        "Diagramme de cas d'utilisation :\n"
        "- Administrateur : Gère les comptes utilisateurs (CRUD complet), consulte les statistiques globales.\n"
        "- Professeur : Ajoute, modifie et suit les étudiants qui lui sont assignés, génère des rapports PDF.\n"
        "- Étudiant : Consulte son profil personnel, voit sa note prédite et l'historique de ses performances.\n\n"
        "Diagramme de séquence (Processus de Prédiction) :\n"
        "1. Le professeur soumet les données d'un étudiant via le formulaire.\n"
        "2. Le système valide les données et appelle le script ml/utils.py.\n"
        "3. Le système charge model_final.pkl et scaler.pkl.\n"
        "4. Les données sont normalisées, et le SVM génère la prédiction (ex: 'A').\n"
        "5. La prédiction et l'historique sont sauvegardés dans PostgreSQL.\n\n"
        "[INSTRUCTION : Insérez ici vos schémas visuels UML correspondants.]"
    )
    
    # 15. Implémentation
    doc.add_heading('15. Implémentation', level=1)
    
    doc.add_heading("Description de l'application", level=2)
    doc.add_paragraph(
        "L'application est divisée en plusieurs modules interconnectés :\n"
        "- Module d'Authentification : Contrôle d'accès basé sur les rôles (RBAC) pour isoler les espaces Admin, Professeur et Étudiant.\n"
        "- Module de Gestion (CRUD) : Interfaces permettant la manipulation des données académiques avec des mesures de sécurité (protection CSRF).\n"
        "- Module de Prédiction : Moteur d'inférence en arrière-plan traduisant les entrées utilisateurs en notes prédictives via un modèle SVM.\n"
        "- Module de Suivi (Historique) : Conservation d'une trace chronologique des prédictions pour évaluer l'évolution des étudiants.\n"
        "- Module de Reporting : Génération automatisée de documents PDF (via xhtml2pdf) consolidant les résultats de l'étudiant."
    )
    
    doc.add_heading('Interfaces (captures d’écran)', level=2)
    doc.add_paragraph(
        "[INSTRUCTION : Insérez ici les captures d'écran des interfaces clés : 1) Page de connexion, 2) Tableau de bord Professeur, "
        "3) Formulaire d'ajout d'étudiant, 4) Profil de l'étudiant avec l'historique des prédictions.]"
    )
    
    # 16. Tests et validation
    doc.add_heading('16. Tests et validation', level=1)
    
    doc.add_heading('Cas de test', level=2)
    doc.add_paragraph(
        "Plusieurs scénarios de test ont été exécutés pour garantir la robustesse du système :\n"
        "- Test d'intégrité : Tentative d'insertion de valeurs textuelles dans des champs numériques (rejeté par les formulaires Django).\n"
        "- Test ML : Saisie de données extrêmes (ex: 0% d'assiduité, 0h d'étude) pour vérifier si le modèle retourne bien la classe 'D'.\n"
        "- Test d'accès : Tentative de modification du profil d'un étudiant par un professeur non assigné (accès refusé grâce aux décorateurs)."
    )
    
    doc.add_heading('Résultats obtenus', level=2)
    doc.add_paragraph(
        "Les tests ont validé le pipeline complet : l'intégration entre le modèle pré-entraîné (Data Science) et "
        "le framework Django (Web) s'effectue en temps quasi-réel (moins de 2 secondes). Le stockage de l'historique "
        "fonctionne correctement sans tronquer les données."
    )
    
    # Conclusion générale
    doc.add_heading('Conclusion générale', level=1)
    
    doc.add_heading('A- Récapitulatif du travail', level=2)
    
    doc.add_paragraph(
        "Réponse à la problématique :\n"
        "Le projet EduPredict répond efficacement à la problématique du suivi réactif en proposant un outil proactif. "
        "Au lieu de constater l'échec après l'examen, la plateforme permet d'anticiper la note finale dès la mi-semestre "
        "en se basant sur des indicateurs fiables (score intermédiaire, présence, motivation, etc.).\n\n"
        
        "Analyse des résultats et limites du travail :\n"
        "Le système montre une grande efficacité dans la transmission des données entre l'interface et le modèle. "
        "Cependant, la précision des prédictions reste intrinsèquement liée à la qualité des données initiales d'entraînement.\n\n"
        
        "Interprétation globale et Apport du projet :\n"
        "Le projet apporte une numérisation intelligente à la gestion académique. En automatisant les prédictions et "
        "l'historique, il offre un véritable outil d'aide à la décision (Decision Support System) pour le corps enseignant.\n\n"
        
        "Limites (Données et Modèles) :\n"
        "Les modèles actuels (SVM, Decision Tree) sont simples et dépendent d'un jeu de données statique potentiellement "
        "limité en diversité. L'application web traite ces données parfaitement, mais un volume de données en temps réel "
        "plus massif serait nécessaire pour affiner les algorithmes."
    )
    
    doc.add_heading('B- Perspectives du projet', level=2)
    
    doc.add_paragraph(
        "Améliorations possibles :\n"
        "- Implémentation d'un tableau de bord analytique plus riche (Business Intelligence) pour la direction, "
        "avec des graphiques interactifs (ex: Chart.js).\n"
        "- Mise en place d'un système de ré-entraînement automatique (Active Learning) où le modèle ML se met à jour "
        "en fin d'année avec les vraies notes obtenues.\n\n"
        
        "Extensions futures :\n"
        "- Intégration d'un module de messagerie interne pour alerter automatiquement l'étudiant s'il entre dans la zone de risque.\n"
        "- Déploiement complet via conteneurisation Docker sur des serveurs Cloud (Render/AWS) pour une disponibilité continue."
    )
    
    # Bibliographie & Annexes
    doc.add_heading('Bibliographie', level=1)
    doc.add_paragraph(
        "[INSTRUCTION : Citez vos sources ici. Exemples :\n"
        "- Documentation officielle Django (https://docs.djangoproject.com/)\n"
        "- Scikit-Learn: Machine Learning in Python (Pedregosa et al.)\n"
        "- Articles sur l'Educational Data Mining (EDM)]"
    )
    
    doc.add_heading('Annexes', level=1)
    doc.add_paragraph(
        "[INSTRUCTION : Insérez ici des extraits de code pertinents (ex: ml/utils.py), des exemples bruts du "
        "jeu de données, ou des captures d'écran de l'architecture de la base de données (pgAdmin).]"
    )
    
    # Save the document to the user's Desktop
    output_path = r'C:\Users\hp 845\Desktop\Rapport_EduPredict.docx'
    doc.save(output_path)
    print(f"Document saved to {output_path}")

if __name__ == '__main__':
    create_report()
