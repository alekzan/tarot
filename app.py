import streamlit as st
import streamlit.components.v1 as components
import base64
import sqlite3
import os
import uuid
import datetime


from agents_tarot import agent_tarotista

# Ensure the data directory exists
os.makedirs("data", exist_ok=True)

# Set the date range
min_date = datetime.date.today() - datetime.timedelta(days=90 * 365)  # Hace 90 años
max_date = datetime.date.today() - datetime.timedelta(days=16 * 365)  # Hace 16 años


# Function to convert image to base64
def img_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()


# Function to initialize the database schema
def initialize_db():
    conn = sqlite3.connect("data/user_data.db")
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS users (
            nombre text,
            fecha_nacimiento text,
            color_favorito text,
            estado_animo text,
            correo text
        )"""
    )
    conn.commit()
    conn.close()


# Function to save user data
def save_user_data(
    nombre,
    fecha_nacimiento,
    color_favorito,
    estado_animo,
    correo,
):
    conn = sqlite3.connect("data/user_data.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO users (nombre, fecha_nacimiento, color_favorito, estado_animo, correo) VALUES (?, ?, ?, ?, ?)",
        (
            nombre,
            fecha_nacimiento,
            color_favorito,
            estado_animo,
            correo,
        ),
    )
    conn.commit()
    conn.close()


def main():
    st.set_page_config(
        page_title="Tarot MAI MAI - Conoce tu Destino Místico",
        page_icon="🔮",
    )

    if "config" not in st.session_state:
        thread_id_number = str(uuid.uuid4())
        st.session_state.config = {"configurable": {"thread_id": thread_id_number}}

    # Initialize the database schema
    initialize_db()

    # Convert the image to base64 and display it at the top of the sidebar
    img_path = "images/bola.jpg"  # Replace with the correct path to your image
    img_base64 = img_to_base64(img_path)
    st.sidebar.markdown(
        f"""
        <style>
        .cover-glow {{
            width: 100%;  /* Adjust the width as needed */
            height: auto; /* Maintain the aspect ratio */
            padding: 3px;
            box-shadow: 1px 2px 23px 0px rgba(188,150,255,0.75);
            border-radius: 30px;
        }}
        </style>
        <img src="data:image/png;base64,{img_base64}" class="cover-glow">
        """,
        unsafe_allow_html=True,
    )
    # Sidebar content
    st.sidebar.title("Bienvenid@ al Tarot MAI MAI")
    st.sidebar.markdown(
        """
        Llena tus datos y nuestro Lector del Tarot te dirá qué te depara el futuro.
        Si quieres conocer la joyería que mejor va con tu interior místico, visita nuestra tienda en línea: 
        [MAI MAI](https://www.maimai.com.mx/)
        """,
        unsafe_allow_html=True,
    )

    # Main content
    st.title("🔮 Conoce Tu Destino Místico")
    st.subheader("Llena tus datos para recibir una lectura personalizada de tarot.")

    # Form to collect user information
    with st.form("tarot_form"):
        nombre = st.text_input("Tu nombre")
        fecha_nacimiento = st.date_input(
            "Fecha de nacimiento", min_value=min_date, max_value=max_date
        )
        color_favorito = st.text_input("Tu color favorito")
        estado_animo = st.selectbox(
            "¿Cómo te sientes hoy?",
            [
                "Lista para conquistar el mundo",
                "Un poco perdida",
                "Curiosa sobre mi futuro",
                "En busca de respuestas",
            ],
        )
        correo = st.text_input("Tu correo electrónico")

        # Button to submit the form
        analizar_tarot = st.form_submit_button("Analizar mi tarot")

    # Process form submission
    if analizar_tarot:
        if not (nombre and color_favorito and estado_animo and correo):
            st.warning("Por favor, completa todos los campos obligatorios.")
        else:
            # Save user data
            save_user_data(
                nombre, str(fecha_nacimiento), color_favorito, estado_animo, correo
            )

            with st.spinner("Consultando las cartas del tarot..."):
                # Call the agent_tarotista function from agents_tarot.py
                tarot_response = agent_tarotista(
                    nombre, str(fecha_nacimiento), color_favorito, estado_animo
                )
                tarot_response = tarot_response.content

                # Display the tarot reading
                st.markdown(
                    f"### Tu Lectura del Tarot:\n\n{tarot_response}",
                    unsafe_allow_html=True,
                )

    st.markdown(
        "<div style='text-align: center; color: #a491ff;'>Creado por MAI MAI. Todos los derechos reservados</div>",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
