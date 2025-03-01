import streamlit as st
from random import choice

st.title("Qui va au tableau ? 👀")

# Initialisation des variables de session
if "choices" not in st.session_state:
    st.session_state.choices = []

if "new_option" not in st.session_state:
    st.session_state.new_option = ""

if "draw_mode" not in st.session_state:
    st.session_state.draw_mode = "Avec remise"


def update_choice() -> None:
    """Ajoute un choix à la liste dans la session"""
    new_choice = st.session_state.new_option.strip()
    if new_choice and new_choice not in st.session_state.choices:
        st.session_state.choices.append(new_choice)
    st.session_state.new_option = ""  # Reset du champ après ajout


def delete_choice(option: str) -> None:
    """Supprime un choix de la liste dans la session"""
    if option in st.session_state.choices:
        st.session_state.choices.remove(option)


def get_random_choice() -> str:
    """Tire un choix aléatoire parmi la liste des choix"""
    if st.session_state.choices:
        selected = choice(st.session_state.choices)
        if st.session_state.draw_mode == "Sans remise":
            st.session_state.choices.remove(selected)  # Suppression si sans remise
        return selected
    return None


# Interface utilisateur
with st.expander("⚙️ Gérer les options"):
    st.markdown("Ajoutez, modifiez ou supprimez des options avant de tirer au sort.")

    for option in st.session_state.choices:
        col1, col2 = st.columns([4, 1])
        with col1:
            st.text(option)
        with col2:
            st.button("❌", on_click=lambda opt=option: delete_choice(opt), key=f"del_{option}")

    new_option = st.text_input("Ajouter une nouvelle option :", key="new_option")
    st.button("✅ Ajouter", on_click=update_choice)

st.subheader("📋 Options actuelles")
st.write(", ".join(st.session_state.choices) if st.session_state.choices else "Aucune option disponible.")

# Sélection du mode de tirage
st.subheader("🎲 Mode de tirage")
st.session_state.draw_mode = st.radio(
    "Choisissez un mode de tirage :",
    ["Avec remise", "Sans remise"]
)

# Bouton de tirage au sort
if st.session_state.choices:
    if st.button("🎰 Tirer au sort"):
        result = get_random_choice()
        if result:
            st.header(f"🎉 Le choix tiré est : {result} 🎉")
            st.balloons()
        else:
            st.warning("La liste est vide. Ajoutez des options !")
