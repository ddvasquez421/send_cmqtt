import paho.mqtt.client as paho
import time
import streamlit as st
import json
import platform
import threading # Necesitamos threading para el loop del cliente MQTT

# --- Streamlit Page Configuration ---
# !!! ESTO DEBE SER LA PRIMERA LLAMADA A UN COMANDO st.!!!
st.set_page_config(page_title="CyberControl MQTT", layout="centered", page_icon="🧬")
# --- End Page Configuration ---


# --- CSS for Neon/Cyber Aesthetics ---
# Los selectores se han ajustado para ser más robustos usando data-testid
neon_css = """
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500&display=swap" rel="stylesheet">
<style>
/* Aplicar fuente y fondo a la app principal */
[data-testid="stAppViewContainer"] {
    font-family: 'Orbitron', sans-serif;
    /* Intento de fondo GIF - puede variar según la implementación de Streamlit */
    background: url('https://media.giphy.com/media/3o6ZtaO9BZHcOjmErm/giphy.gif') no-repeat center center fixed;
    background-size: cover;
    color: #00fff7 !important; /* Color de texto general */
}

/* Asegurar que otros elementos dentro de la app también usen la fuente */
div {
    font-family: 'Orbitron', sans-serif;
}


h1, h2, h3, h4, h5 {
    color: #00ffff !important; /* Importante para asegurar el color */
    text-shadow: 0 0 10px #00ffff;
}

/* Estilo para botones */
[data-testid="stButton"] button {
    background: transparent;
    border: 2px solid #00fff7 !important;
    color: #00fff7 !important;
    padding: 0.75em 2em;
    font-size: 16px;
    border-radius: 12px;
    box-shadow: 0 0 10px #00fff7, 0 0 20px #00b7ff;
    transition: all 0.3s ease-in-out;
    display: inline-block; /* Asegura que el hover funcione bien */
    width: 100%; /* Para que ocupe el ancho de la columna */
}

[data-testid="stButton"] button:hover {
    background-color: #00fff7 !important;
    color: black !important;
    box-shadow: 0 0 25px #00fff7;
}

/* Estilo para Slider */
/* La barra de progreso del slider */
[data-testid="stSlider"] div[role="slider"] div:nth-child(1) {
    background: linear-gradient(to right, #00fff7, #00b7ff) !important;
    border-radius: 8px;
}

/* El pulgar (handle) del slider */
[data-testid="stSlider"] div[role="slider"] div:nth-child(2) {
    background: #00ffff !important;
    border: 2px solid #00fff7 !important;
}

/* El track vacío del slider */
[data-testid="stSlider"] div[role="slider"] div:nth-child(3) {
     background: #1f1f2e !important; /* Fondo oscuro similar al input */
}


/* Estilo para label de slider y otros elementos de texto */
[data-testid="stSlider"] label,
.st-cc /* Posible clase para texto de slider value */ {
    color: #00fff7 !important;
}


/* Estilo para Input de texto */
[data-testid="stTextInput"] input {
    background-color: #1f1f2e !important;
    color: #00ffcc !important; /* Color del texto ingresado */
    border: 1px solid #00ffcc !important;
    border-radius: 8px;
    padding: 0.75em; /* Añadir padding para que coincida con botones */
}

/* Estilo para label de input */
[data-testid="stTextInput"] label {
     color: #00fff7 !important;
}


hr {
    border-top: 1px solid #00fff7 !important;
}

footer {
    color: #00fff7 !important;
}

/* Estilo para mensajes de éxito, advertencia, etc. */
[data-testid="stAlert"]-success {
    background-color: rgba(0, 255, 247, 0.1) !important; /* Fondo semi-transparente neón */
    color: #00fff7 !important;
    border-left: 5px solid #00fff7 !important;
}
[data-testid="stAlert"]-warning {
    background-color: rgba(255, 165, 0, 0.1) !important; /* Fondo semi-transparente naranja */
    color: orange !important;
    border-left: 5px solid orange !important;
}
/* Puedes añadir para info y error si los usas */

</style>
"""

# Inject the CSS into the Streamlit app (Ahora después de set_page_config)
st.markdown(neon_css, unsafe_allow_html=True)
# --- End CSS ---


# Configuración del cliente MQTT
broker = "157.230.214.127"
port = 1883
topic_publish_cmqtt_s = "cmqtt_s"
topic_publish_cmqtt_a = "cmqtt_a"
topic_subscribe_cmqtt_r = "cmqtt_r" # Asumo un tópico de respuesta si existe


# --- Funciones de Callback MQTT (NO llamar st. aquí) ---
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado al broker MQTT!")
        # Suscribirse a tópicos aquí si necesitas recibir mensajes
        # client.subscribe(topic_subscribe_cmqtt_r)
    else:
        print(f"Fallo la conexión, codigo: {rc}")
        # Podrías guardar un estado de error en session_state aquí, pero con cuidado
        # st.session_state['mqtt_status'] = 'error_connect' # Peligroso llamar st. aquí

def on_publish(client, userdata, result):
    print("Dato publicado.")
    # No llamar st.success aquí

def on_message(client, userdata, msg):
    # Este callback se ejecuta en otro hilo. NO LLAMAR st.XXX aquí.
    # Solo actualiza el estado de Streamlit de forma segura.
    try:
        message_payload = msg.payload.decode("utf-8")
        print(f"Mensaje recibido en tópico {msg.topic}: {message_payload}")
        # Guardar el último mensaje recibido en Streamlit Session State
        st.session_state['last_mqtt_message'] = f"Tópico: {msg.topic}, Mensaje: {message_payload}"
        # Podrías usar una bandera para indicar que hay un nuevo mensaje
        st.session_state['new_mqtt_message'] = True
        # No llamar st.success(f"📡 Mensaje recibido: `{message_payload}`") aquí
    except Exception as e:
        print(f"Error procesando mensaje MQTT: {e}")
        # st.session_state['mqtt_error'] = f"Error mensaje: {e}" # Peligroso llamar st. aquí


# --- Inicialización del cliente MQTT y conexión (una sola vez) ---
@st.cache_resource # Cachea el cliente para que no se re-inicialice en cada rerun
def init_mqtt_client():
    print("Inicializando cliente MQTT...")
    client = paho.Client(paho.CallbackAPIVersion.VERSION2, "GIT-HUB-Streamlit") # Usar API v2 si es posible
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_message = on_message

    try:
        client.connect(broker, port, 60) # Conectar
        # El loop del cliente debe correr en segundo plano
        # client.loop_start() # Inicia un hilo para el loop de red
        # O, si solo publicas, no necesitas loop_start()
        # Si necesitas on_message, SÍ necesitas client.loop_start() o client.loop_forever()
        # Pero loop_forever bloquea, así que loop_start en otro hilo es mejor
        # Vamos a iniciar el loop en un hilo aparte para que on_message funcione
        client_thread = threading.Thread(target=client.loop_forever)
        client_thread.daemon = True # Permite que el hilo termine cuando la app principal lo haga
        client_thread.start()
        print("Cliente MQTT conectado y loop iniciado.")
        return client
    except Exception as e:
        st.error(f"❌ Error al conectar con el broker MQTT: {e}")
        print(f"Error al conectar con el broker MQTT: {e}")
        return None


mqtt_client = init_mqtt_client() # Inicializar o recuperar el cliente cacheado

# Inicializar estado de sesión si no existe
if 'act1_state' not in st.session_state:
    st.session_state['act1_state'] = "OFF"
if 'last_mqtt_message' not in st.session_state:
    st.session_state['last_mqtt_message'] = None
if 'new_mqtt_message' not in st.session_state:
     st.session_state['new_mqtt_message'] = False # Bandera para nuevo mensaje


# --- Título principal ---
st.title("🧬 CyberControl MQTT")
st.caption("Interfaz neón para control de dispositivos mediante protocolo MQTT en tiempo real")

# Versión del sistema
st.markdown(f"💻 Versión de Python: `{platform.python_version()}`")

# Mostrar último mensaje MQTT recibido si hay uno nuevo
if st.session_state.get('new_mqtt_message', False):
    if st.session_state.get('last_mqtt_message'):
        st.success(f"📡 Mensaje recibido: `{st.session_state['last_mqtt_message']}`")
    st.session_state['new_mqtt_message'] = False # Resetear la bandera


# --- Botones ON/OFF ---
st.markdown("### 🔌 Control binario")
col1, col2 = st.columns(2)

# El estado de 'act1' se guarda en session_state
current_act1_state = st.session_state['act1_state']

with col1:
    # Usar el estado guardado para decidir si el botón ON debe publicar
    if st.button('🟢 Encender (ON)'):
        if mqtt_client:
            act1_to_send = "ON"
            message = json.dumps({"Act1": act1_to_send})
            result = mqtt_client.publish(topic_publish_cmqtt_s, message)
            # Verifica el resultado de la publicación si es necesario
            # result.rc == paho.MQTT_ERR_SUCCESS
            st.success(f"✅ Señal enviada: {act1_to_send}")
            st.session_state['act1_state'] = act1_to_send # Actualizar estado en session_state
        else:
            st.error("Cliente MQTT no conectado.")


with col2:
    # Usar el estado guardado para decidir si el botón OFF debe publicar
    if st.button('🔴 Apagar (OFF)'):
        if mqtt_client:
            act1_to_send = "OFF"
            message = json.dumps({"Act1": act1_to_send})
            result = mqtt_client.publish(topic_publish_cmqtt_s, message)
             # Verifica el resultado de la publicación si es necesario
            # result.rc == paho.MQTT_ERR_SUCCESS
            st.warning(f"⛔ Señal enviada: {act1_to_send}")
            st.session_state['act1_state'] = act1_to_send # Actualizar estado en session_state
        else:
            st.error("Cliente MQTT no conectado.")

# Mostrar el estado actual conocido (opcional)
st.markdown(f"Estado conocido de Act1: `{current_act1_state}`")


# --- Control analógico ---
st.markdown("### 🎚️ Señal analógica")
# Streamlit maneja el estado del slider automáticamente
analog_value = st.slider('Selecciona el valor analógico a enviar:', 0.0, 100.0)
st.write(f"🔢 Valor seleccionado: `{analog_value}`")

if st.button('📤 Enviar valor analógico'):
    if mqtt_client:
        message = json.dumps({"Analog": float(analog_value)})
        result = mqtt_client.publish(topic_publish_cmqtt_a, message)
         # Verifica el resultado de la publicación si es necesario
        # result.rc == paho.MQTT_ERR_SUCCESS
        st.success(f"📈 Valor analógico enviado: `{analog_value}`")
    else:
        st.error("Cliente MQTT no conectado.")


# Footer
st.markdown("---")
st.markdown("<center><small>🧠 CyberControl MQTT - Neón Network Interface v2.1 (Corregido)</small></center>", unsafe_allow_html=True)

# Nota: Si necesitas mostrar mensajes recibidos en tiempo real
# de forma más dinámica sin reruns constantes, tendrías que
# explorar opciones más avanzadas como el componente st_mqtt_client
# o usar colas de mensajes y rerun programados, lo cual es más complejo.
# Esta versión solo muestra el último mensaje recibido al siguiente rerun.
