import paho.mqtt.client as paho
import time
import streamlit as st
import json
import platform

# Estilo visual cibernético robusto
st.set_page_config(page_title="CyberControl MQTT", layout="centered", page_icon="🧬")
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500&display=swap" rel="stylesheet">
<style>
    html, body, [class*="css"]  {
        background-color: #0f0f1a;
        color: #00ffcc;
        font-family: 'Orbitron', sans-serif;
    }
    h1, h2, h3, h4, h5 {
        color: #00ffff;
        font-family: 'Orbitron', sans-serif;
    }
    .stButton>button {
        background-color: #1f1f2e;
        color: #00ffcc;
        border: 1px solid #00ffcc;
        border-radius: 8px;
        padding: 0.5em 1.5em;
        font-size: 16px;
    }
    .stSlider .st-bo {
        background: linear-gradient(to right, #00ffcc, #0077ff) !important;
    }
    .stSlider .st-cg {
        color: #00ffcc !important;
    }
    .st-cf {
        color: #00ffcc !important;
    }
    .stTextInput>div>div>input {
        background-color: #1f1f2e;
        color: #00ffcc;
        border: 1px solid #00ffcc;
    }
</style>
""", unsafe_allow_html=True)

# Título
st.title("🧬 CyberControl MQTT")
st.caption("Interfaz de control y envío de señales mediante protocolo MQTT en tiempo real")

# Info del sistema
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

# Botones ON/OFF
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

# Slider y envío de valor analógico
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
