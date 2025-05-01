import paho.mqtt.client as paho
import time
import streamlit as st
import json
import platform

# Estilo visual cibernético
st.set_page_config(page_title="CyberControl MQTT", layout="centered", page_icon="🧬")
st.markdown("""
<style>
body {
    background-color: #0f0f1a;
    color: #00ffcc;
}
h1, h2, h3 {
    color: #00ffff;
    font-family: 'Orbitron', sans-serif;
}
button, .stButton>button {
    background-color: #1f1f2e;
    color: #00ffcc;
    border: 1px solid #00ffcc;
    border-radius: 5px;
}
.stSlider>div>div>div {
    background: linear-gradient(to right, #00ffcc, #0077ff);
}
.st-emotion-cache-1v0mbdj {
    background-color: #14141f;
}
</style>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# Título
st.title("🧬 CyberControl MQTT")
st.caption("Interfaz de control y envío de señales mediante protocolo MQTT en tiempo real")

# Información del sistema
st.markdown(f"💻 Versión de Python: `{platform.python_version()}`")

# Variables
values = 0.0
act1 = "OFF"

# MQTT Callbacks
def on_publish(client, userdata, result):
    print("Dato publicado.")
    pass

def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received = str(message.payload.decode("utf-8"))
    st.success(f"📡 Mensaje recibido: `{message_received}`")

# Conexión MQTT
broker = "157.230.214.127"
port = 1883
client1 = paho.Client("GIT-HUB")
client1.on_message = on_message

# Controles
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

# Slider para valores analógicos
st.markdown("### 🎚️ Control de señal analógica")
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
st.markdown("<center><sub>CyberControl MQTT - by NeuronLink Systems</sub></center>", unsafe_allow_html=True)
