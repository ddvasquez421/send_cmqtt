import paho.mqtt.client as paho
import time
import streamlit as st
import json
import platform
import threading

# --- Streamlit Page Configuration ---
# !!! ESTO DEBE SER LA PRIMERA LLAMADA A UN COMANDO st.!!!
st.set_page_config(page_title="CyberControl MQTT", layout="wide", page_icon="🧬") # Cambiado a 'wide' para más espacio cyberpunk
# --- End Page Configuration ---


# --- CSS for Exaggerated Cyberpunk Aesthetics ---
# Selectores ajustados y colores exagerados
cyberpunk_css = """
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500&family=Share+Tech+Mono&display=swap" rel="stylesheet">
<style>
/* Aplicar fuente y fondo a la app principal */
[data-testid="stAppViewContainer"] {
    font-family: 'Share Tech Mono', monospace; /* Fuente monoespacio para cuerpo */
    /* Intento de fondo GIF - puede variar según la implementación de Streamlit */
    /* Mantenemos tu GIF, puede ser difícil que cubra 100% siempre */
    background: url('https://media.giphy.com/media/3o6ZtaO9BZHcOjmErm/giphy.gif') no-repeat center center fixed;
    background-size: cover;
    background-color: #0a001a; /* Fondo de respaldo muy oscuro */
    color: #00ffff !important; /* Color de texto principal (cian neón) */
}

/* Asegurar que otros elementos usen la fuente principal */
div {
    font-family: 'Share Tech Mono', monospace;
}

/* Títulos y encabezados con fuente Orbitron y brillo */
h1, h2, h3, h4, h5 {
    font-family: 'Orbitron', sans-serif !important;
    color: #ff00ff !important; /* Magenta neón */
    text-shadow: 0 0 5px #ff00ff, 0 0 15px #ff00ff, 0 0 30px #ff00ff; /* Efecto de brillo */
    margin-top: 0.8em; /* Espacio superior */
    margin-bottom: 0.4em; /* Espacio inferior */
}

h1 { font-size: 2.5em !important; text-align: center; } /* Título principal más grande y centrado */
h3 { color: #00ff00 !important; text-shadow: 0 0 5px #00ff00; } /* Subtítulos en verde neón */


/* Estilo para Botones */
[data-testid="stButton"] button {
    background: rgba(0, 255, 255, 0.1); /* Cian semi-transparente */
    border: 2px solid #00ffff !important; /* Borde cian neón */
    color: #00ffff !important; /* Texto cian neón */
    padding: 0.75em 2em;
    font-size: 1em; /* Tamaño de fuente relativo */
    border-radius: 5px; /* Bordes ligeramente redondeados */
    box-shadow: 0 0 8px #00ffff, 0 0 12px #00ffff inset; /* Sombra exterior e interior para brillo */
    transition: all 0.3s ease-in-out;
    letter-spacing: 0.1em; /* Espaciado entre letras */
    text-transform: uppercase; /* Texto en mayúsculas */
}

[data-testid="stButton"] button:hover {
    background-color: #00ffff !important; /* Fondo cian sólido al pasar el ratón */
    color: #0d001a !important; /* Texto oscuro */
    box-shadow: 0 0 12px #00ffff, 0 0 20px #00ffff, 0 0 30px #00ffff inset; /* Brillo más intenso */
}

/* Estilo para Slider */
/* El track completo del slider */
[data-testid="stSlider"] div[role="slider"] {
    background: #1a0033 !important; /* Fondo oscuro del track */
    border-radius: 8px;
    height: 8px; /* Altura del track */
}

/* La barra de progreso del slider */
[data-testid="stSlider"] div[role="slider"] div:nth-child(1) {
     background: linear-gradient(to right, #ff00ff, #00ffff) !important; /* Gradiente magenta a cian */
     border-radius: 8px;
}

/* El pulgar (handle) del slider */
[data-testid="stSlider"] div[role="slider"] div:nth-child(2) {
    background: #00ffff !important; /* Cian sólido */
    border: 3px solid #ff00ff !important; /* Borde magenta */
    width: 20px; /* Tamaño del pulgar */
    height: 20px;
    top: -6px; /* Ajuste vertical */
    box-shadow: 0 0 8px #00ffff; /* Brillo para el pulgar */
}

/* Estilo para label y valor del slider */
[data-testid="stSlider"] label,
[data-testid="stText"] { /* Selector común para texto generado por st.write */
    color: #00ff00 !important; /* Verde neón para valores */
    font-size: 1.1em;
    margin-bottom: 0.5em;
}


/* Estilo para Input de texto */
[data-testid="stTextInput"] input {
    background-color: #1a0033 !important; /* Fondo oscuro */
    color: #00ff00 !important; /* Texto verde neón */
    border: 1px solid #00ff00 !important; /* Borde verde neón */
    border-radius: 5px;
    padding: 0.75em;
    box-shadow: 0 0 5px #00ff00 inset; /* Brillo interior */
    font-family: 'Share Tech Mono', monospace; /* Asegurar fuente monoespacio */
}

/* Estilo para label de input */
[data-testid="stTextInput"] label {
     color: #ff00ff !important; /* Magenta neón */
     font-size: 1.1em;
     margin-bottom: 0.5em;
}
/* Placeholder text color */
[data-testid="stTextInput"] input::placeholder {
    color: #888888 !important; /* Gris oscuro */
    opacity: 0.8 !important;
}


/* Estilo para File Uploader */
[data-testid="stFileUploader"] {
    background-color: #1a0033 !important; /* Fondo oscuro */
    border: 2px dashed #ff00ff !important; /* Borde punteado magenta neón */
    border-radius: 5px;
    padding: 1em;
    text-align: center;
    color: #00ff00 !important; /* Texto verde neón */
}
[data-testid="stFileUploader"] label {
     color: #00ff00 !important; /* Texto dentro del label */
}
[data-testid="stFileUploader"] button {
     /* Estilo específico para el botón 'Browse files' dentro del uploader */
     background: rgba(255, 0, 255, 0.1) !important; /* Magenta semi-transparente */
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
    background-color: #33004d !important; /* Un púrpura oscuro */
    color: #00ffff !important; /* Cian neón */
    font-family: 'Orbitron', sans-serif !important; /* Fuente de encabezado */
    padding: 0.7em 1em !important;
    border-radius: 5px;
    border: 1px solid #00ffff !important;
    margin-bottom: 0.5em;
    cursor: pointer; /* Indicar que es clickeable */
    box-shadow: 0 0 5px #00ffff;
}
[data-testid="stExpander"] div[data-testid="stExpanderToggleIcon"] {
     color: #00ffff !important; /* Color del icono de expansión */
}
[data-testid="stExpander"] div[data-testid="stVerticalBlock"] {
     /* Contenido del expander */
     border-left: 2px solid #ff00ff !important; /* Borde magenta a la izquierda del contenido */
     padding-left: 1em;
     margin-left: 0.5em;
}


/* Línea divisoria */
hr {
    border-top: 2px dashed #ff00ff !important; /* Línea punteada magenta neón */
    margin-top: 2em;
    margin-bottom: 2em;
}

/* Estilo para mensajes de estado (success, warning, error) */
[data-testid="stAlert"]-success {
    background-color: rgba(0, 255, 0, 0.1) !important; /* Verde neón semi-transparente */
    color: #00ff00 !important; /* Texto verde neón */
    border-left: 5px solid #00ff00 !important; /* Borde verde */
    border-radius: 5px;
}
[data-testid="stAlert"]-warning {
    background-color: rgba(255, 255, 0, 0.1) !important; /* Amarillo neón semi-transparente */
    color: #ffff00 !important; /* Texto amarillo neón */
    border-left: 5px solid #ffff00 !important; /* Borde amarillo */
    border-radius: 5px;
}
[data-testid="stAlert"]-error {
    background-color: rgba(255, 0, 0, 0.1) !important; /* Rojo neón semi-transparente */
    color: #ff0000 !important; /* Texto rojo neón */
    border-left: 5px solid #ff0000 !important; /* Borde rojo */
    border-radius: 5px;
}
/* Añadir para info si lo usas */
[data-testid="stAlert"]-info {
    background-color: rgba(0, 255, 255, 0.1) !important; /* Cian neón semi-transparente */
    color: #00ffff !important; /* Texto cian neón */
    border-left: 5px solid #00ffff !important; /* Borde cian */
    border-radius: 5px;
}


/* Estilo para el footer (si Streamlit lo renderiza) */
footer {
    color: #ff00ff !important; /* Magenta neón */
    font-size: 0.9em;
    text-align: center;
    margin-top: 3em;
}

/* Ajustes para el caption */
.st-be { /* Clase probable para st.caption */
    color: #00ff00 !important; /* Verde neón */
    text-align: center;
    display: block; /* Asegurar que se centre */
    margin-bottom: 2em;
}

/* Posible ajuste para st.write output si no es st.text */
/* Asegura que el texto de st.write (como el valor del slider) tenga el color correcto */
.stMarkdown {
     color: #00ffff !important; /* Cian neón */
}


/* Scrollbar con estilo neón */
::-webkit-scrollbar {
    width: 12px; /* Ancho de la barra de scroll */
}

::-webkit-scrollbar-track {
    background: #1a0033; /* Fondo oscuro del track */
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(to bottom, #00ffff, #ff00ff); /* Gradiente neón en el pulgar */
    border-radius: 10px;
    border: 2px solid #0d001a; /* Borde oscuro */
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(to bottom, #ff00ff, #00ffff); /* Invertir gradiente al pasar el ratón */
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
topic_subscribe_cmqtt_r = "cmqtt_r" # Asumo un tópico de respuesta si existe


# --- Funciones de Callback MQTT (NO llamar st. aquí) ---
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado al broker MQTT!")
        # Suscribirse a tópicos aquí si necesitas recibir mensajes
        # client.subscribe(topic_subscribe_cmqtt_r)
        # Opcional: Actualizar estado de conexión en session_state si es seguro (puede requerir manejo de hilos más avanzado)
        # st.session_state['mqtt_connected'] = True
    else:
        print(f"Fallo la conexión, codigo: {rc}")
        # Opcional: Actualizar estado de conexión con error
        # st.session_state['mqtt_connected'] = False
        # st.session_state['mqtt_error'] = f"Connect failed: {rc}"


def on_publish(client, userdata, result):
    # print("Dato publicado.") # Comentado para reducir ruido en consola
    pass # No llamar st.success aquí

def on_message(client, userdata, msg):
    # Este callback se ejecuta en otro hilo. NO LLAMAR st.XXX aquí.
    # Solo actualiza el estado de Streamlit de forma segura.
    try:
        message_payload = msg.payload.decode("utf-8")
        print(f"Mensaje recibido en tópico {msg.topic}: {message_payload}")
        # Guardar el último mensaje recibido en Streamlit Session State
        st.session_state['last_mqtt_message'] = f"Tópico: {msg.topic}, Mensaje: {message_payload}"
        # Usar una bandera para indicar que hay un nuevo mensaje y forzar un rerun
        st.session_state['new_mqtt_message'] = True
        # Para que Streamlit se actualice, necesitamos forzar un rerun.
        # Esto *puede* causar problemas si los mensajes llegan muy rápido.
        # Una forma es usar un truco con excepciones o componentes personalizados.
        # Forzar un rerun aquí directamente puede ser inestable.
        # La forma más segura es que el usuario interactúe o usar un componente personalizado (st_mqtt_client).
        # Por ahora, dependemos del siguiente rerun por interacción del usuario.
        # Si necesitas tiempo real, considera st_mqtt_client o técnicas más avanzadas.

    except Exception as e:
        print(f"Error procesando mensaje MQTT: {e}")
        # st.session_state['mqtt_error'] = f"Error mensaje: {e}" # Peligroso llamar st. aquí


# --- Inicialización del cliente MQTT y conexión (una sola vez) ---
# Cachea el cliente para que no se re-inicialice en cada rerun
@st.cache_resource
def init_mqtt_client():
    print("Inicializando cliente MQTT...")
    # Añadir identificador de cliente para MQTT
    client_id = f"streamlit-mqtt-client-{time.time()}" # ID único basado en tiempo
    client = paho.Client(paho.CallbackAPIVersion.VERSION2, client_id)
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_message = on_message # Asigna el callback on_message

    # Configurar Will Message (opcional, para notificar si la app se desconecta inesperadamente)
    # client.will_set("status/streamlit", "Offline", 1, False)

    try:
        print(f"Intentando conectar a broker {broker}:{port}...")
        client.connect(broker, port, 60) # Conectar
        # Iniciar el loop de red en un hilo separado para recibir mensajes
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
# Esto se hará en cada rerun, pero la suscripción es idempotente en MQTT.
if mqtt_client and mqtt_client.is_connected():
     try:
         # Nota: La suscripción también puede hacerse en on_connect para asegurar que ocurre post-reconexión
         mqtt_client.subscribe(topic_subscribe_cmqtt_r)
         # print(f"Suscrito al tópico: {topic_subscribe_cmqtt_r}") # Puede ser ruidoso
     except Exception as e:
         print(f"Error al suscribirse a tópico {topic_subscribe_cmqtt_r}: {e}")
         # st.error(f"Error al suscribirse a tópico {topic_subscribe_cmqtt_r}") # Cuidado con llamar st. aquí


# Inicializar estado de sesión si no existe
if 'act1_state' not in st.session_state:
    st.session_state['act1_state'] = "OFF"
if 'last_mqtt_message' not in st.session_state:
    st.session_state['last_mqtt_message'] = None
if 'new_mqtt_message' not in st.session_state:
     st.session_state['new_mqtt_message'] = False # Bandera para nuevo mensaje


# --- Título principal ---
# El título ahora está centrado y con brillo gracias al CSS
st.title("🧬 CyberControl MQTT")
# La leyenda también está centrada y con color por el CSS
st.caption("Interfaz neón para control de dispositivos mediante protocolo MQTT en tiempo real")

# Estado de conexión MQTT (simple indicador)
if mqtt_client and mqtt_client.is_connected():
    st.markdown("<span style='color: #00ff00;'>🟢 CONECTADO AL NEON-BROKER</span>", unsafe_allow_html=True)
else:
    st.markdown("<span style='color: #ff0000;'>🔴 DESCONECTADO DEL NEON-BROKER</span>", unsafe_allow_html=True)


# Versión del sistema
st.markdown(f"💻 Versión de Python: `{platform.python_version()}`")


# Mostrar último mensaje MQTT recibido si hay uno nuevo (se activa en el siguiente rerun)
if st.session_state.get('new_mqtt_message', False):
    if st.session_state.get('last_mqtt_message'):
        # Usamos st.markdown para aplicar el color y fuente neón al mensaje
        st.info(f"```json\n{st.session_state['last_mqtt_message']}\n```") # Usar st.info para un estilo de caja diferente
        # st.success(f"📡 Mensaje recibido: `{st.session_state['last_mqtt_message']}`") # O usar st.success con el CSS modificado

    st.session_state['new_mqtt_message'] = False # Resetear la bandera después de mostrar


# --- Control binario ---
st.markdown("### 🔌 Control binario")
col1, col2 = st.columns(2)

# El estado de 'act1' se guarda en session_state
current_act1_state = st.session_state['act1_state']

with col1:
    if st.button('🟢 ENCENDER (ON)'):
        if mqtt_client and mqtt_client.is_connected():
            act1_to_send = "ON"
            message = json.dumps({"Act1": act1_to_send})
            result = mqtt_client.publish(topic_publish_cmqtt_s, message)
            # Verifica el resultado de la publicación si es necesario
            # if result.rc == paho.MQTT_ERR_SUCCESS:
            st.success(f"✅ Señal enviada: {act1_to_send}")
            st.session_state['act1_state'] = act1_to_send # Actualizar estado en session_state
        else:
            st.error("Cliente MQTT no conectado. No se pudo enviar señal.")


with col2:
    if st.button('🔴 APAGAR (OFF)'):
        if mqtt_client and mqtt_client.is_connected():
            act1_to_send = "OFF"
            message = json.dumps({"Act1": act1_to_send})
            result = mqtt_client.publish(topic_publish_cmqtt_s, message)
             # Verifica el resultado de la publicación si es necesario
            # if result.rc == paho.MQTT_ERR_SUCCESS:
            st.warning(f"⛔ Señal enviada: {act1_to_send}")
            st.session_state['act1_state'] = act1_to_send # Actualizar estado en session_state
        else:
            st.error("Cliente MQTT no conectado. No se pudo enviar señal.")

# Mostrar el estado actual conocido (opcional)
# st.markdown(f"Estado conocido de Act1: `{current_act1_state}`") # Comentado, menos es más cyberpunk


# --- Control analógico ---
st.markdown("### 🎚️ Señal analógica")
analog_value = st.slider('SELECCIONA VALOR ANALÓGICO:', 0.0, 100.0)
# Usamos st.write que será estilizado por el CSS
st.write(f"VALOR SELECCIONADO: `{analog_value}`")


if st.button('📤 ENVIAR VALOR ANALÓGICO'):
    if mqtt_client and mqtt_client.is_connected():
        message = json.dumps({"Analog": float(analog_value)})
        result = mqtt_client.publish(topic_publish_cmqtt_a, message)
        # Verifica el resultado de la publicación si es necesario
        # if result.rc == paho.MQTT_ERR_SUCCESS:
        st.success(f"📈 Valor analógico enviado: `{analog_value}`")
    else:
        st.error("Cliente MQTT no conectado. No se pudo enviar valor.")

# Footer
st.markdown("---")
st.markdown("<center><small>🧠 CyberControl MQTT - Neón Network Interface v3.0 (Cyberpunk Exagerado)</small></center>", unsafe_allow_html=True)

# Nota sobre mensajes en tiempo real: Streamlit no está diseñado para actualizar
# la UI continuamente desde hilos secundarios. Para recibir mensajes MQTT
# y mostrarlos instantáneamente SIN interacción del usuario, necesitarías
# usar un componente Streamlit personalizado que maneje la comunicación asíncrona
# y notifique a Streamlit para reruns (como st_mqtt_client si es compatible).
# La implementación actual solo mostrará el último mensaje recibido después de la siguiente
# interacción del usuario que cause un rerun.
