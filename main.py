import pandas as pd
import pywhatkit as kit
import time
import random
import streamlit as st
import warnings
warnings.filterwarnings("ignore")


# Función para enviar mensajes con opción de aleatorios o único
def enviar_mensajes(df, aleatorio, mensaje_unico, configuracion_mensajes):
    for index, row in df.iterrows():
        nombre = row['Nombre'].split()[0]  # Obtener el primer nombre
        celular = row['Celular']

        # Agregar '+' al inicio si no está presente
        if not str(celular).startswith('+'):
            celular = f"+{celular}"

        # Construir el mensaje según la configuración
        if aleatorio:
            mensaje = f"{random.choice(configuracion_mensajes['introducciones']).format(nombre=nombre)}\n\n"
            mensaje += f"{random.choice(configuracion_mensajes['apoyo_ingeniero'])}\n\n"
            mensaje += f"{random.choice(configuracion_mensajes['detalle_candidato'])}\n\n"
            mensaje += f"{random.choice(configuracion_mensajes['apoyo_unillanos'])}\n\n"
            mensaje += f"{random.choice(configuracion_mensajes['transformacion_digital'])}\n\n"
            mensaje += f"{random.choice(configuracion_mensajes['urgencia_votar_hoy'])}\n\n"
            mensaje += f"{random.choice(configuracion_mensajes['conclusion'])}"
        else:
            mensaje = mensaje_unico.format(nombre=nombre)

        try:
            # Enviar mensaje instantáneamente y cerrar la pestaña después
            st.write(f"Enviando mensaje a {nombre} ({celular})")
            kit.sendwhatmsg_instantly(celular, mensaje, tab_close=True)
            time.sleep(1)  # 10 segundos entre mensajes
        except Exception as e:
            st.error(f"Error al enviar mensaje a {nombre} ({celular}): {e}")

# Configuración de mensajes predefinidos
def cargar_configuracion_mensajes():
    return {
        "introducciones": [
            "¡Hola {nombre}! 👋 ¿Cómo estás?",
            "¡Hola {nombre}! Espero que todo esté marchando genial. 🌟",
            "👋🏼 ¡Hola {nombre}! Que tengas un excelente día.",
        ],
        "apoyo_ingeniero": [
            "Quiero invitarte 🙌 a que apoyemos al ingeniero Omar Beltran en la consulta previa de designación del rector para el periodo 2025-2027.",
            "Te invito 🔔 a votar por el ingeniero Omar Beltran en la consulta previa de designación del rector para el periodo 2025-2027.",
            "🤝 ¡Unámonos para apoyar al ingeniero Omar Beltran en la consulta previa de designación del rector para el periodo 2025-2027!",
        ],
        "detalle_candidato": [
            "Omar es ingeniero electrónico 🎓 egresado de la Facultad de Ciencias Básicas e Ingenierías y ha sido un unillanista ejemplar durante más de 27 años.",
            "El ingeniero Omar 💼 es un egresado de nuestra Facultad de Ciencias Básicas e Ingenierías con una trayectoria intachable de más de 27 años.",
            "Con 27 años de experiencia como unillanista, Omar Beltran, ingeniero electrónico 📚 de nuestra Facultad de Ciencias Básicas e Ingenierías, conoce mejor que nadie el pasado y el futuro de Unillanos.",
        ],
        "apoyo_unillanos": [
            "Es momento de apoyar 💪 a nuestra querida alma mater, Unillanos, y generar un cambio real.",
            "Debemos respaldar a nuestra alma mater 🌱, Unillanos, y trabajar juntos por un cambio significativo.",
            "🏫 Apoyar a nuestra querida Unillanos es fundamental para construir el cambio que necesitamos.",
        ],
        "transformacion_digital": [
            "La propuesta de transformación digital que Omar ha planteado 💻 es verdaderamente diferenciadora.",
            "Omar ha presentado una propuesta de transformación digital 🚀 que se destaca y es clave para el futuro de Unillanos.",
            "Lo que más me entusiasma 🔧 es la transformación digital que Omar propone, una propuesta única y necesaria.",
        ],
        "urgencia_votar_hoy": [
            "⏰ ¡Recuerda que las votaciones son hoy! Tu apoyo es crucial para lograr el cambio que Unillanos necesita.",
            "🚨 ¡No olvides que las votaciones son hoy! Es el momento de hacer la diferencia y apoyar al ingeniero Omar.",
            "📅 ¡Hoy es el día de votar! No dejes pasar la oportunidad de contribuir al futuro de Unillanos con tu voto.",
        ],
        "conclusion": [
            "Estoy seguro de que con su plan de gobierno y ejes estratégicos ✨, Omar puede llevar a Unillanos hacia un futuro brillante.",
            "Omar Beltran 🏅, con su experiencia y visión, es la mejor opción para llevar a Unillanos hacia adelante.",
            "Confío en que Omar hará un excelente trabajo 🌟 como rector y que su plan de gobierno es justo lo que Unillanos necesita.",
        ],
    }

# Mensaje único por defecto
mensaje_unico_predeterminado = (
    "¡Hola {nombre}! 👋\n\n"
    "Quiero invitarte a que apoyemos al ingeniero Omar Beltran en la consulta previa de designación del rector para el periodo 2025-2027. "
    "Omar es ingeniero electrónico egresado de la Facultad de Ciencias Básicas e Ingenierías y ha sido un unillanista ejemplar durante más de 27 años. "
    "Es momento de apoyar a nuestra querida alma mater, Unillanos, y generar un cambio real con la propuesta de transformación digital que Omar ha planteado, "
    "la cual es verdaderamente diferenciadora. 🏫💻\n\n"
    "Recuerda que las votaciones son hoy ⏰. ¡Tu apoyo es crucial!"
)

# Interfaz de Streamlit
st.title("Envío de Mensajes Masivos por WhatsApp")
st.write("Carga tu archivo Excel con los contactos y envía mensajes personalizados.")

# Tabs para las diferentes funciones
tab1, tab2, tab3 = st.tabs(["Enviar Mensajes", "Configuración de Mensajes", "Emojis"])

# Tab para enviar mensajes
with tab1:
    st.header("Instructivo para Envío de Mensajes Masivos")

    st.write("""
    **Paso 1:** Carga un archivo Excel con los contactos a los que deseas enviar mensajes.
    
    - El archivo debe contener **dos columnas**:
      1. **Nombre**: El nombre de la persona (puede ser el nombre completo).
      2. **Celular**: El número de celular en formato internacional, comenzando con '+' seguido del código del país y el número (ejemplo: +573001234567).
    
    **Paso 2:** Revisa la vista previa de los contactos cargados para asegurarte de que los datos son correctos.
    
    **Paso 3:** Configura los mensajes en el Tab de "Configuración de Mensajes". Puedes elegir entre enviar mensajes aleatorios o un mensaje único a todos los contactos.
    
    **Paso 4:** Una vez que estés listo, presiona el botón **"Enviar Mensajes"** para iniciar el envío.
    """)

    st.subheader("Formato de la Tabla a Cargar")

    st.write("""
    Asegúrate de que tu archivo Excel siga este formato:
    
    | Nombre        | Celular       |
    |---------------|---------------|
    | Juan Pérez    | +573001234567 |
    | María García  | +573002345678 |
    | Carlos López  | +573003456789 |
    
    **Nota:** Asegúrate de incluir el símbolo `+` al inicio del número de celular.
    """)

    uploaded_file = st.file_uploader("Sube tu archivo Excel", type=["xlsx"])

    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        st.write("Vista previa de los contactos cargados:")
        st.dataframe(df.head())

        if st.button("Enviar Mensajes"):
            aleatorio = st.session_state.get("aleatorio", True)
            mensaje_unico = st.session_state.get("mensaje_unico", mensaje_unico_predeterminado)
            configuracion_mensajes = st.session_state.get("configuracion_mensajes", cargar_configuracion_mensajes())
            
            # Barra de progreso
            progress_bar = st.progress(0)
            total_contacts = len(df)
            
            for i, row in df.iterrows():
                enviar_mensajes(df.iloc[i:i+1], aleatorio, mensaje_unico, configuracion_mensajes)
                progress_bar.progress((i + 1) / total_contacts)

            st.success("Todos los mensajes han sido enviados.")



# Tab para configuración de mensajes
with tab2:
    st.write("Edita las secciones de los mensajes predefinidos:")

    # Switch para mensajes aleatorios o mensaje único
    modo_mensaje = st.radio(
        "Modo de Envío",
        ("Mensajes Aleatorios", "Mensaje Único"),
        index=0,
        key="modo_mensaje"
    )

    aleatorio = (modo_mensaje == "Mensajes Aleatorios")
    st.session_state["aleatorio"] = aleatorio

    if aleatorio:
        st.write("**Edición de Mensajes Aleatorios**")
        # Cargar configuración actual
        configuracion_mensajes = cargar_configuracion_mensajes()

        # Mostrar editores de texto para cada sección
        for key, value in configuracion_mensajes.items():
            st.write(f"**{key.replace('_', ' ').title()}**")
            for i in range(len(value)):
                configuracion_mensajes[key][i] = st.text_area(f"{key.replace('_', ' ').title()} {i+1}", value=value[i], key=f"{key}_{i}")

        st.session_state["configuracion_mensajes"] = configuracion_mensajes
    else:
        st.write("**Edición del Mensaje Único**")
        
        # Inicializar mensaje_unico en session_state si no existe
        if "mensaje_unico" not in st.session_state:
            st.session_state["mensaje_unico"] = mensaje_unico_predeterminado
        
        # Instanciar el widget text_area sin modificar session_state después
        mensaje_unico = st.text_area("Mensaje Único", key="mensaje_unico")


# Tab para Emojis
with tab3:
    st.write("**Emojis para copiar y pegar:**")
    
    # Lista de emojis relevantes para el tema
    emojis = [
        "👋", "🌟", "👋🏼", "🙌", "🔔", "🤝", 
        "🎓", "💼", "📚", "💪", "🌱", "🏫", 
        "💻", "🚀", "🔧", "⏰", "🚨", "📅", 
        "✨", "🏅", "🌟", "💬", "✅", "📣", 
        "🤓", "📊", "📈", "🗳️", "✉️", "📞", 
        "🔗", "🖥️", "📱", "🖊️", "📝", "🎯", 
        "🔍", "🎉", "🏆", "🎀", "🎁", "🔝", 
        "⭐", "🌍", "🌐", "🎯", "⚙️", "🏛️", 
        "🎖️", "💡", "🧠", "🌱", "📜", "📚",
        "🎓", "🕰️", "🗓️", "🚩", "🌄", "🛠️"
    ]

    # Mostrar emojis en un formato fácil de copiar con tamaño mayor
    cols = st.columns(5)  # Ajusta el número de columnas según prefieras
    for i, emoji in enumerate(emojis):
        cols[i % 5].markdown(f"<h1 style='text-align: center;'>{emoji}</h1>", unsafe_allow_html=True)