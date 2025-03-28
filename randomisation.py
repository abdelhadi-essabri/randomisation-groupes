import pandas as pd
import streamlit as st
import os
import tempfile

def assign_group(sexe, age, assigned_participants):
    """
    Assigne un participant à un groupe (A ou B) de manière équilibrée en fonction du sexe et de la tranche d'âge.
    """
    tranche_age = '18-35' if age <= 35 else '36-65'
    
    # Clé pour identifier la catégorie
    category_key = (sexe, tranche_age)
    
    # Initialiser la répartition si elle n'existe pas encore
    if category_key not in assigned_participants:
        assigned_participants[category_key] = {'A': 0, 'B': 0}
    
    # Assigner au groupe le moins rempli dans la catégorie
    if assigned_participants[category_key]['A'] <= assigned_participants[category_key]['B']:
        assigned_participants[category_key]['A'] += 1
        return "A"
    else:
        assigned_participants[category_key]['B'] += 1
        return "B"

def load_data(filename):
    """Charge le fichier Excel s'il existe, sinon crée un DataFrame vide."""
    if os.path.exists(filename):
        return pd.read_excel(filename)
    else:
        return pd.DataFrame(columns=["ID", "Sexe", "Age", "Tranche_Age", "Groupe"])

def save_data(df, filename):
    """Sauvegarde les données dans un fichier Excel."""
    df.to_excel(filename, index=False)

# Interface Streamlit
st.title("Assignation aléatoire des participants")

# Création d'un fichier temporaire pour Streamlit Cloud
with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp_file:
    data_file = tmp_file.name  # Créer un fichier temporaire pour stocker le fichier Excel
    # Vérification si le fichier existe déjà et création d'un DataFrame vide si nécessaire
    if not os.path.exists(data_file):
        df = pd.DataFrame(columns=["ID", "Sexe", "Age", "Tranche_Age", "Groupe"])
        save_data(df, data_file)  # Sauvegarder ce fichier vide si c'est la première fois

df = load_data(data_file)

# Initialisation des participants assignés
group_counts = {}
for _, row in df.iterrows():
    key = (row["Sexe"], row["Tranche_Age"])
    if key not in group_counts:
        group_counts[key] = {"A": 0, "B": 0}
    group_counts[key][row["Groupe"]] += 1

# Entrée utilisateur
sexe = st.radio("Sexe", ["H", "F"], index=0)
age = st.number_input("Âge", min_value=18, max_value=65, step=1)

if st.button("Assigner le participant"):
    groupe = assign_group(sexe, age, group_counts)
    tranche_age = '18-35' if age <= 35 else '36-65'
    new_id = df["ID"].max() + 1 if not df.empty else 1
    new_participant = pd.DataFrame([[new_id, sexe, age, tranche_age, groupe]], columns=df.columns)
    df = pd.concat([df, new_participant], ignore_index=True)
    save_data(df, data_file)
    st.success(f"Le participant (ID: {new_id}, Sexe: {sexe}, Âge: {age}) a été assigné au groupe {groupe}.")

# Affichage des données
st.write("### Liste des participants")
st.dataframe(df)
# ####
# Bouton pour télécharger le fichier Excel
st.download_button(
    label="Télécharger le fichier Excel",
    data=df.to_excel(index=False),  # Convertir le DataFrame en bytes
    file_name="participants_assignes.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
