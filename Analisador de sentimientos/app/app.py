# Importamos las librerías necesarias
from openai import OpenAI # Para conectarnos con los modelos GPT de OpenAI
from flask import Flask, request, render_template # Para crear la aplicación web
import os  # Para manejar variables de entorno como la API key

# Guardar la clave de OpenAI (permite usar el modelo GPT-4)
os.environ["OPENAI_API_KEY"] = "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"

app = Flask(__name__)
client = OpenAI()
# Lista de emociones con sus emojis
EMOJIS = {
    "alegría": "😄",
    "tristeza": "😢",
    "miedo": "😨",
    "ira": "😠",
    "sorpresa": "😲",
    "amor": "😍"
}
# Función que pregunta a GPT-4 cuál es la emoción
def detectar_emocion_gpt4(texto):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Eres un analizador emocional. Devuelve una sola emoción entre: alegría, tristeza, miedo, ira, sorpresa, amor. No digas 'neutral'."},
            {"role": "user", "content": texto}
        ],
        temperature=0.7
    )
    emocion = response.choices[0].message.content.strip()
    return emocion
# Página principal
@app.route('/', methods=['GET', 'POST'])
def index():
    emocion_detectada = ""
    emoji = ""
    if request.method == 'POST':
        # Recibe lo que escribió el usuario
        texto = request.form['texto']
        # Detecta emoción
        emocion_detectada = detectar_emocion_gpt4(texto).lower()
        # Busca el emoji
        emoji = EMOJIS.get(emocion_detectada, "")
    return render_template('index.html', emocion=emocion_detectada.capitalize(), emoji=emoji)

if __name__ == '__main__':
    app.run(debug=True)
