import paho.mqtt.client as paho
import time
import streamlit as st
import json
import platform
import threading

# --- Streamlit Page Configuration ---
st.set_page_config(page_title="CyberControl MQTT", layout="wide", page_icon="🧬")
# --- End Page Configuration ---

# --- CSS for Exaggerated Cyberpunk Aesthetics ---
cyberpunk_css = """
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500&family=Share+Tech+Mono&display=swap" rel="stylesheet">
<style>
[data-testid="stAppViewContainer"] {
    font-family: 'Share Tech Mono', monospace;
    background: url('https://media.giphy.com/media/3o6ZtaO9BZHcOjmErm/giphy.gif') no-repeat center center fixed;
    background-size: cover;
    background-color: #0a001a;
    color: #00ffff !important;
}

div {
    font-family: 'Share Tech Mono', monospace;
}

h1, h2, h3, h4, h5 {
    font-family: 'Orbitron', sans-serif !important;
    color: #ff00ff !important;
    text-shadow: 0 0 5px #ff00ff, 0 0 15px #ff00ff, 0 0 30px #ff00ff;
    margin-top: 0.8em;
    margin-bottom: 0.4em;
}

h1 { font-size: 2.5em !important; text-align: center; }
h3 { color: #00ff00 !important; text-shadow: 0 0 5px #00ff00; }


/* Estilo para Botones */
[data-testid="stButton"] button {
    background: rgba(0, 255, 255, 0.1);
    border: 2px solid #00ffff !important;
    color: #00ffff !important;
    padding: 0.75em 2em;
    font-size: 1em;
    border-radius: 5px;
    box-shadow: 0 0 8px #00ffff, 0 0 12px #00ffff inset;
    transition: all 0.3s ease-in-out;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

[data-testid="stButton"] button:hover {
    background-color: #00ffff !important;
    color: #0d001a !important;
    box-shadow: 0 0 12px #00ffff, 0 0 20px #00ffff, 0 0 30px #00ffff inset;
}

/* Estilo para Slider */
[data-testid="stSlider"] div[role="slider"] {
    background: #1a0033 !important;
    border-radius: 8px;
    height: 8px;
}

[data-testid="stSlider"] div:nth-child(1) div[role="slider"] div:nth-child(1) {
     background: linear-gradient(to right, #ff00ff, #00ffff) !important;
     border-radius: 8px;
}

[data-testid="stSlider"] div:nth-child(1) div[role="slider"] div:nth-child(2) {
    background: #00ffff !important;
    border: 3px solid #ff00ff !important;
    width: 20px;
    height: 20px;
    top: -6px;
    box-shadow: 0 0 8px #00ffff;
}

[data-testid="stSlider"] label,
[data-testid="stText"] {
    color: #00ff00 !important;
    font-size: 1.1em;
    margin-bottom: 0.5em;
}

/* Estilo para Input de texto */
[data-testid="stTextInput"] input {
    background-color: #1a0033 !important;
    color: #00ff00 !important;
    border: 1px solid #00ff00 !important;
    border-radius: 5px;
    padding: 0.75em;
    box-shadow: 0 0 5px #00ff00 inset;
    font-family: 'Share Tech Mono', monospace;
}

[data-testid="stTextInput"] label {
     color: #ff00ff !important;
     font-size: 1.1em;
     margin-bottom: 0.5em;
}
[data-testid="stTextInput"] input::placeholder {
    color: #888888 !important;
    opacity: 0.8 !important;
}

/* Estilo para File Uploader */
[data-testid="stFileUploader"] {
    background-color: #1a0033 !important;
    border: 2px dashed #ff00ff !important;
    border-radius: 5px;
    padding: 1em;
    text-align: center;
    color: #00ff00 !important;
}
[data-testid="stFileUploader"] label {
     color: #00ff00 !important;
}
[data-testid="stFileUploader"] button {
     background: rgba(255, 0, 255, 0.1) !important;
     border: 1px solid #ff00ff !important;
     color: #ff00ff !important;
     box-shadow: 0 0 5px #ff00ff !important;
}
[data-testid="stFileUploader"] button:hover {
     background: #ff00ff !important;
     color: #0d001a !important;
     box-shadow: 0 0 10px #ff00ff !important;
}

/* Estilo para Expander */
[data-testid="stExpander"] label {
    background-color: #33004d !important;
    color: #00ffff !important;
    font-family: 'Orbitron', sans-serif !important;
    padding: 0.7em 1em !important;
    border-radius: 5px;
    border: 1px solid #00ffff !important;
    margin-bottom: 0.5em;
    cursor: pointer;
    box-shadow: 0 0 5px #00ffff;
}
[data-testid="stExpander"] div[data-testid="stExpanderToggleIcon"] {
     color: #00ffff !important;
}
[data-testid="stExpander"] div[data-testid="stVerticalBlock"] {
     border-left: 2px solid #ff00ff !important;
     padding-left: 1em;
     margin-left: 0.5em;
}

/* Línea divisoria */
hr {
    border-top: 2px dashed #ff00ff !important;
    margin-top: 2em;
    margin-bottom: 2em;
}

/* Estilo para mensajes de estado */
[data-testid="stAlert"]-success {
    background-color: rgba(0, 255, 0, 0.1) !important;
    color: #00ff00 !important;
    border-left: 5px solid #00ff00 !important;
    border-radius: 5px;
}
[data-testid="stAlert"]-warning {
    background-color: rgba(255, 255, 0, 0.1) !important;
    color: #ffff00 !important;
    border-left: 5px solid #ffff00 !important;
    border-radius: 5px;
}
[data-testid="stAlert"]-error {
    background-color: rgba(255, 0, 0, 0.1) !important;
    color: #ff0000 !important;
    border-left: 5px solid #ff0000 !important;
    border-radius: 5px;
}
[data-testid="stAlert"]-info {
    background-color: rgba(0, 255, 255, 0.1) !important;
    color: #00ffff !important;
    border-left: 5px solid #00ffff !important;
    border-radius: 5px;
}

/* Estilo para el footer */
footer {
    color: #ff00ff !important;
    font-size: 0.9em;
    text-align: center;
    margin-top: 3em;
}

/* Ajustes para el caption */
.st-be {
    color: #00ff00 !important;
    text-align: center;
    display: block;
    margin-bottom: 2em;
}

/* Estilo para st.write output */
.stMarkdown {
     color: #00ffff !important;
}

/* Scrollbar con estilo neón */
::-webkit-scrollbar {
    width: 12px;
}

::-webkit-scrollbar-track {
    background: #1a0033;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(to bottom, #00ffff, #ff00ff);
    border-radius: 10px;
    border: 2px solid #0d001a;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(to bottom, #ff00ff, #00ffff);
}

</style>
"""

# Inject the CSS into the Streamlit app
st.markdown(cyberpunk_css, unsafe_allow_html=True)
# --- End CSS ---


# Configuración del cliente MQTT
broker = "157.230.214.127"
port = 1883
topic_publish_cmqtt_s = "cmqtt_s"
topic_publish_cmqtt_a = "cmqtt_a"
topic_subscribe_cmqtt_r = "cmqtt_r"


# --- Funciones de Callback MQTT (NO llamar st. aquí) ---
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado al broker MQTT!")
        # Puedes suscribirte a tópicos aquí si necesitas recibir mensajes
        # client.subscribe(topic_subscribe_cmqtt_r)
    else:
        print(f"Fallo la conexión, codigo: {rc}")

def on_publish(client, userdata, result):
    pass

def on_message(client, userdata, msg):
    # Este callback se ejecuta en otro hilo. NO LLAMAR st.XXX aquí.
    try:
        message_payload = msg.payload.decode("utf-8")
        print(f"Mensaje recibido en tópico {msg.topic}: {message_payload}")
        st.session_state['last_mqtt_message'] = f"Tópico: {msg.topic}, Mensaje: {message_payload}"
        st.session_state['new_mqtt_message'] = True
    except Exception as e:
        print(f"Error procesando mensaje MQTT: {e}")

# --- Inicialización del cliente MQTT y conexión (una sola vez) ---
@st.cache_resource
def init_mqtt_client():
    print("Inicializando cliente MQTT...")
    client_id = f"streamlit-mqtt-client-{time.time()}"
    client = paho.Client(paho.CallbackAPIVersion.VERSION2, client_id)
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_message = on_message

    try:
        print(f"Intentando conectar a broker {broker}:{port}...")
        client.connect(broker, port, 60)
        print("Iniciando loop de red en hilo separado...")
        client.loop_start()
        print("Cliente MQTT conectado y loop iniciado.")
        return client
    except Exception as e:
        st.error(f"❌ Error al conectar con el broker MQTT: {e}")
        print(f"Error al conectar con el broker MQTT: {e}")
        return None

# Inicializar o recuperar el cliente cacheado
mqtt_client = init_mqtt_client()

# Suscribirse al tópico de respuesta después de conectar si el cliente es válido
if mqtt_client and mqtt_client.is_connected():
     try:
         mqtt_client.subscribe(topic_subscribe_cmqtt_r)
         print(f"Suscrito al tópico: {topic_subscribe_cmqtt_r}")
     except Exception as e:
         print(f"Error al suscribirse a tópico {topic_subscribe_cmqtt_r}: {e}")


# Inicializar estado de sesión si no existe
if 'act1_state' not in st.session_state:
    st.session_state['act1_state'] = "OFF"
if 'last_mqtt_message' not in st.session_state:
    st.session_state['last_mqtt_message'] = None
if 'new_mqtt_message' not in st.session_state:
     st.session_state['new_mqtt_message'] = False

# --- Título principal ---
st.title("🧬 CyberControl MQTT")
st.caption("Interfaz neón para control de dispositivos mediante protocolo MQTT en tiempo real")

# Estado de conexión MQTT
if mqtt_client and mqtt_client.is_connected():
    st.markdown("<span style='color: #00ff00;'>🟢 CONECTADO AL NEON-BROKER</span>", unsafe_allow_html=True)
else:
    st.markdown("<span style='color: #ff0000;'>🔴 DESCONECTADO DEL NEON-BROKER</span>", unsafe_allow_html=True)

# Versión del sistema
st.markdown(f"💻 Versión de Python: `{platform.python_version()}`")

# Mostrar último mensaje MQTT recibido si hay uno nuevo (se activa en el siguiente rerun)
if st.session_state.get('new_mqtt_message', False):
    if st.session_state.get('last_mqtt_message'):
        st.info(f"```json\n{st.session_state['last_mqtt_message']}\n```")
    st.session_state['new_mqtt_message'] = False

# --- Control binario ---
st.markdown("### 🔌 Control binario")
col1, col2 = st.columns(2)

current_act1_state = st.session_state['act1_state']

with col1:
    if st.button('🟢 ENCENDER (ON)'):
        if mqtt_client and mqtt_client.is_connected():
            act1_to_send = "ON"
            message = json.dumps({"Act1": act1_to_send})
            result = mqtt_client.publish(topic_publish_cmqtt_s, message)
            if result.rc == paho.MQTT_ERR_SUCCESS:
                st.success(f"✅ Señal enviada: {act1_to_send}")
                st.session_state['act1_state'] = act1_to_send
            else:
                st.error(f"❗ Error al publicar señal ON. Código: {result.rc}")
        else:
            st.error("Cliente MQTT no conectado. No se pudo enviar señal.")

with col2:
    if st.button('🔴 APAGAR (OFF)'):
        if mqtt_client and mqtt_client.is_connected():
            act1_to_send = "OFF"
            message = json.dumps({"Act1": act1_to_send})
            result = mqtt_client.publish(topic_publish_cmqtt_s, message)
            if result.rc == paho.MQTT_ERR_SUCCESS:
                st.warning(f"⛔ Señal enviada: {act1_to_send}")
                st.session_state['act1_state'] = act1_to_send
            else:
                 st.error(f"❗ Error al publicar señal OFF. Código: {result.rc}")
        else:
            st.error("Cliente MQTT no conectado. No se pudo enviar señal.")

# --- Control analógico ---
st.markdown("### 🎚️ Señal analógica")
analog_value = st.slider('SELECCIONA VALOR ANALÓGICO:', 0.0, 100.0)
st.write(f"VALOR SELECCIONADO: `{analog_value}`")

if st.button('📤 ENVIAR VALOR ANALÓGICO'):
    if mqtt_client and mqtt_client.is_connected():
        message = json.dumps({"Analog": float(analog_value)})
        result = mqtt_client.publish(topic_publish_cmqtt_a, message)
        if result.rc == paho.MQTT_ERR_SUCCESS:
            st.success(f"📈 Valor analógico enviado: `{analog_value}`")
        else:
             st.error(f"❗ Error al publicar valor analógico. Código: {result.rc}")
    else:
        st.error("Cliente MQTT no conectado. No se pudo enviar valor.")

# Footer
st.markdown("---")
st.markdown("<center><small>🧠 CyberControl MQTT - Neón Network Interface v3.2 (Cyberpunk Exagerado - Limpio)</small></center>", unsafe_allow_html=True)

# Nota sobre mensajes en tiempo real: Reitera que la actualización instantánea
# sin interacción requiere componentes personalizados o técnicas avanzadas.
# La implementación actual actualiza el mensaje en el siguiente rerun por interacción.
st.markdown("<small><i>Nota: La visualización de mensajes MQTT recibidos se actualiza en la siguiente interacción del usuario. Para tiempo real continuo sin interacción, se requieren configuraciones avanzadas o componentes personalizados.</i></small>", unsafe_allow_html=True)
