import random
import pandas as pd
import streamlit as st
import os

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

data_file = "participants.xlsx"
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


exit()
import random

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

# Exemple d'utilisation
def main():
    assigned_participants = {}  # Dictionnaire pour suivre la répartition
    
    while True:
        sexe = input("Entrez le sexe du participant (H/F) : ").strip().upper()
        age = int(input("Entrez l'âge du participant : "))
        groupe = assign_group(sexe, age, assigned_participants)
        print(f"Le participant ({sexe}, {age} ans) est assigné au groupe {groupe}.")
        
        cont = input("Voulez-vous ajouter un autre participant ? (O/N) : ").strip().upper()
        if cont != 'O':
            break

if __name__ == "__main__":
    main()

