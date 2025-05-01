import paho.mqtt.client as paho
import time
import streamlit as st
import json
import platform

# Muestra la versión de Python junto con detalles adicionales
st.write("Versión de Python:", platform.python_version())

values = 0.0
act1="OFF"

def on_publish(client, userdata, result):  #create function for callback
    print("el dato ha sido publicado \n")
    pass

def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received = str(message.payload.decode("utf-8"))
    st.write(message_received)

# Estilo Cyberpunk y Futurista
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');
        
        body {
            background-color: #121212;  /* Fondo oscuro */
            color: #00FF00;  /* Verde neón */
            font-family: 'Press Start 2P', cursive;  /* Fuente retro/futurista */
            text-shadow: 0 0 10px #00FF00, 0 0 20px #00FF00, 0 0 30px #00FF00;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #FF00FF;  /* Morado brillante para los títulos */
            text-shadow: 0 0 10px #FF00FF, 0 0 20px #FF00FF, 0 0 30px #FF00FF;
        }
        .stButton>button {
            color: #000000;
            background-color: #FF00FF;
            border: 2px solid #FF00FF;
            font-family: 'Press Start 2P', cursive;
        }
        .stSlider>div>div>input {
            background-color: #333333;
            color: #FF00FF;
            border: 2px solid #FF00FF;
        }
        .stTextInput input {
            color: #FF00FF;
            background-color: #333333;
            border: 2px solid #FF00FF;
        }
        .stCanvas {
            border: 2px solid #FF00FF;
            box-shadow: 0px 0px 30px 10px rgba(255, 0, 255, 0.5); /* Efecto neón */
        }
        .stSidebar {
            background-color: #333333; /* Fondo oscuro para la barra lateral */
        }
        .stMarkdown {
            color: #00FFFF; /* Texto en azul cian para los textos */
        }
    </style>
""", unsafe_allow_html=True)

# Título de la aplicación
st.title("Cyberpunk MQTT Control")

# Cargar la imagen "roboto2"
image_path = "Roboto2.png"
try:
    image = st.image(image_path, caption="Imagen Roboto2 Cargada", use_container_width=True)
except FileNotFoundError:
    st.write("La imagen 'roboto2.png' no se encontró. Por favor, colócala en el directorio adecuado.")

# MQTT Broker
broker = "157.230.214.127"
port = 1883
client1 = paho.Client("GIT-HUB")
client1.on_message = on_message

# Botones de control para encender y apagar
if st.button('ON'):
    act1 = "ON"
    client1 = paho.Client("GIT-HUB")
    client1.on_publish = on_publish
    client1.connect(broker, port)
    message = json.dumps({"Act1": act1})
    ret = client1.publish("cmqtt_s", message)

elif st.button('OFF'):
    act1 = "OFF"
    client1 = paho.Client("GIT-HUB")
    client1.on_publish = on_publish
    client1.connect(broker, port)
    message = json.dumps({"Act1": act1})
    ret = client1.publish("cmqtt_s", message)

# Control de valores analógicos
values = st.slider('Selecciona el rango de valores', 0.0, 100.0)
st.write('Valores:', values)

if st.button('Enviar valor analógico'):
    client1 = paho.Client("GIT-HUB")
    client1.on_publish = on_publish
    client1.connect(broker, port)
    message = json.dumps({"Analog": float(values)})
    ret = client1.publish("cmqtt_a", message)

# Mostrar el estado de la conexión MQTT
if act1 == "ON":
    st.write("Control MQTT activado. Enviando datos...")
elif act1 == "OFF":
    st.write("Control MQTT desactivado. Sin datos.")
