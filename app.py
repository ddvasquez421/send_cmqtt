import paho.mqtt.client as paho
import time
import streamlit as st
import json
import platform

# Configuración visual
st.set_page_config(page_title="CyberControl MQTT", layout="centered", page_icon="🧬")
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500&display=swap" rel="stylesheet">
<style>
html, body, [class*="css"] {
    font-family: 'Orbitron', sans-serif;
    background: url('https://media.giphy.com/media/3o6ZtaO9BZHcOjmErm/giphy.gif') no-repeat center center fixed;
    background-size: cover;
    color: #00fff7 !important;
}

h1, h2, h3, h4, h5 {
    color: #00ffff;
    text-shadow: 0 0 10px #00ffff;
}

.stButton>button {
    background: transparent;
    border: 2px solid #00fff7;
    color: #00fff7;
    padding: 0.75em 2em;
    font-size: 16px;
    border-radius: 12px;
    box-shadow: 0 0 10px #00fff7, 0 0 20px #00b7ff;
    transition: all 0.3s ease-in-out;
}

.stButton>button:hover {
    background-color: #00fff7;
    color: black;
    box-shadow: 0 0 25px #00fff7;
}

.stSlider > div > div > div {
    background: linear-gradient(to right, #00fff7, #00b7ff) !important;
    border-radius: 8px;
}

.stSlider label, .st-cf, .st-cg, .st-eb {
    color: #00fff7 !important;
}

.stTextInput>div>div>input {
    background-color: #1f1f2e;
    color: #00ffcc;
    border: 1px solid #00ffcc;
}

hr {
    border-top: 1px solid #00fff7;
}

footer {
    color: #00fff7;
}
</style>
""", unsafe_allow_html=True)

# Título principal
st.title("🧬 CyberControl MQTT")
st.caption("Interfaz neón para control de dispositivos mediante protocolo MQTT en tiempo real")

# Versión del sistema
st.markdown(f"💻 Versión de Python: `{platform.python_version()}`")

# Variables iniciales
values = 0.0
act1 = "OFF"

# Funciones de MQTT
def on_publish(client, userdata, result):
    print("Dato publicado.")
    pass

def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received = str(message.payload.decode("utf-8"))
    st.success(f"📡 Mensaje recibido: `{message_received}`")

# Configuración del cliente MQTT
broker = "157.230.214.127"
port = 1883
client1 = paho.Client("GIT-HUB")
client1.on_message = on_message

# Botones ON/OFF
st.markdown("### 🔌 Control binario")
col1, col2 = st.columns(2)
with col1:
    if st.button('🟢 Encender (ON)'):
        act1 = "ON"
        client1 = paho.Client("GIT-HUB")
        client1.on_publish = on_publish
        client1.connect(broker, port)
        message = json.dumps({"Act1": act1})
        client1.publish("cmqtt_s", message)
        st.success("✅ Señal enviada: ON")

with col2:
    if st.button('🔴 Apagar (OFF)'):
        act1 = "OFF"
        client1 = paho.Client("GIT-HUB")
        client1.on_publish = on_publish
        client1.connect(broker, port)
        message = json.dumps({"Act1": act1})
        client1.publish("cmqtt_s", message)
        st.warning("⛔ Señal enviada: OFF")

# Control analógico
st.markdown("### 🎚️ Señal analógica")
values = st.slider('Selecciona el valor analógico a enviar:', 0.0, 100.0)
st.write(f"🔢 Valor seleccionado: `{values}`")

if st.button('📤 Enviar valor analógico'):
    client1 = paho.Client("GIT-HUB")
    client1.on_publish = on_publish
    client1.connect(broker, port)
    message = json.dumps({"Analog": float(values)})
    client1.publish("cmqtt_a", message)
    st.success(f"📈 Valor analógico enviado: `{values}`")

# Footer
st.markdown("---")
st.markdown("<center><small>🧠 CyberControl MQTT - Neón Network Interface v2.0</small></center>", unsafe_allow_html=True)
