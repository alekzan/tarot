from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

# Environment setup
load_dotenv(override=True)
os.environ.get("GROQ_API_KEY")

llm = ChatGroq(model="llama-3.1-70b-versatile", temperature=0.7)
# llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)


def agent_tarotista(nombre, fecha_nacimiento, color_favorito, estado_animo):
    # Prompt
    prompt = PromptTemplate(
        template="""
        Haz una lectura de tarot personalizada para {nombre}, nacido el {fecha_nacimiento}. 
        Usa la energía del número y el poder místico de su color favorito {color_favorito}. 
        Explora cómo su estado de ánimo, {estado_animo}, influye en su destino actual.

        Realiza una lectura profunda y reveladora, conectando con las fuerzas ocultas del universo para ofrecer una predicción esotérica. Asegúrate de que el mensaje sea inspirador, misterioso y lleno de sabiduría antigua.
        Da tu respuesta en formato markdown y utiliza emojis místicos.
        No olvides darle su número de la suerte y el animal místico que le representa.
        """,
        input_variables=[
            "nombre",
            "fecha_nacimiento",
            "color_favorito",
            "estado_animo",
        ],
    )

    chain = prompt | llm
    try:
        tarot = chain.invoke(
            {
                "nombre": nombre,
                "fecha_nacimiento": fecha_nacimiento,
                "color_favorito": color_favorito,
                "estado_animo": estado_animo,
            }
        )

        return tarot
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
