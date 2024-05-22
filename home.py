
import streamlit as st
from datetime import datetime
import smtplib
import ssl
from email.message import EmailMessage

from rendering import generate_pdf, download_button
from template import MODEL_CARD_HTML_TEMPLATE

import uuid
from database import client, DB_NAME, COLLECTION_NAME

db = client[DB_NAME]
collection = db[COLLECTION_NAME]

feedback_collection = db["feedback"]

class SafeDict(dict):
    def __missing__(self, key):
        return ''

# TODO: Tengo que colocar los botones para siguiente tab dentro de cada tab (que del tab0 pase al tab1 y así sucesivamente)

# Función para guardar los datos en MongoDB
def guardar_en_mongodb_feedback(datos):
    try:
        # Generar un identificador único para este documento
        datos["_id"] = str(uuid.uuid4())
        # Insertar el documento en la colección
        feedback_collection.insert_one(datos)
        st.sidebar.success("Feedback registrado con éxito.")
    except Exception as e:
        st.sidebar.error("Error al guardar feedback en base de datos")


# Función para guardar los datos en MongoDB
def guardar_en_mongodb(datos):
    try:
        # Generar un identificador único para este documento
        datos["_id"] = str(uuid.uuid4())
        # Insertar el documento en la colección
        collection.insert_one(datos)
        st.success("Datos guardados con éxito.")
    except Exception as e:
        st.error(f"Error al guardar en la base de datos: {e}")

# Método para enviar un correo electrónico
def send_feedback_email(feedback):
    try:
        # Configura los detalles del correo electrónico
        msg = EmailMessage()
        msg['Subject'] = 'Nuevo feedback para la Model UAI'
        msg['From'] = 'jspinad@gmail.com'
        msg['To'] = 'goblab@uai.cl'
        msg.set_content(feedback)

        context = ssl.create_default_context()

        # Configura los parámetros del servidor SMTP y envía el correo electrónico
        with smtplib.SMTP_SSL('smtp.gmail.com', 465,context=context) as smtp:
            smtp.login('jspinad@gmail.com', 'caar kfqv zjoo isfn')
            smtp.sendmail("jspinad@gmail.com","goblab@uai.cl",msg.as_string())
        
        guardar_en_mongodb_feedback({"feedback": feedback})
        st.success("¡Feedback enviado con éxito!")
    except Exception as e:
        st.error("Error al enviar el feedback.")
        st.error(e)

def preparar_seccion_html(clave, valor, prefijo="", sufijo=""):
    """Devuelve una cadena HTML para la sección si el valor no está vacío, de lo contrario devuelve una cadena vacía."""
    if valor:  # Verifica si el valor existe y no está vacío
        return f"{prefijo}{clave}: {valor}{sufijo}"
    return ""

# Definir una función para verificar si todos los campos obligatorios están llenos
def verificar_campos_obligatorios():
    campos_obligatorios =[
                    "nombre_modelo","desarrollador_modelo","tipo_modelo",
                    "proposito_modelo","UsoPrevisto_modelo",
                    "metricas_modelo","datos_modelo","preprocesamiento_modelo",
                    "conjunto_datos_eval_modelo","preprocesamiento_evaluacion","TA_modelo_categoriza",
                    "TA_datos_personales","dato_sensible","asuntos_centrales_modelo","TA_reclamacion"
                    ]
    
    for campo in campos_obligatorios:
        if campo not in questions or questions[campo] == "" or questions[campo] is None:
            return campo
    return "all"

st.sidebar.title("Feedback")
# Crea un formulario para el feedback
with st.sidebar.form(key='feedback_form'):
    feedback = st.text_area("💬 Si tienes alguna sugerencia o comentario, deja tu feedback aquí:")
    submit_button = st.form_submit_button(label='Enviar Feedback 🚀 ')

    if submit_button and feedback:
        send_feedback_email(feedback)
        

SHORT_STRING = 100
LONG_STRING = 1000

col1, col2, col3 = st.columns(3)

# Mostrar la primera imagen en la primera columna
with col1:
    st.write("")
    st.image("_statics/Logo_herramientas_algoritmos.png")
with col2:
    #st.image("_statics/UAI.png")
    pass
# Mostrar la segunda imagen en la segunda columna
with col3:
    st.image("_statics/Goblab.png")

title = "Ficha de transparencia"
st.markdown(f"<h3 style='text-align: left; color: black;'>V.2.0.0</h3>", unsafe_allow_html=True)
st.markdown(f"<h1 style='text-align: center; color: black;'>{title}</h1>", unsafe_allow_html=True)

st.write("""La presente herramienta es un apoyo para la elaboración de una ficha de transparencia para sistemas de decisiones automatizadas o semiautomatizadas (SDA), con el propósito de ayudar a los organismos públicos a cumplir con los estándares de transparencia algorítmica de sus sistemas. 
         
Está destinada para ser utilizada en SDA que hayan completado la fase de desarrollo y evaluación, antes de la fase de implementación de la solución. Para más información sobre las fases, consultar la Guía Permitido Innovar (https://www.lab.gob.cl/permitido-innovar).
La ficha de transparencia es un documento que proporciona información relevante sobre la naturaleza, aspectos técnicos, funcionales y del proyecto del SDA. Desempeña un papel fundamental en la promoción de la transparencia, la rendición de cuentas y el uso ético de los algoritmos. La herramienta facilita la creación de esta ficha: ayuda a la identificación de la información relevante sobre el SDA que se debe transparentar y la presenta de manera clara, visible y comprensible tanto para los involucrados en el proceso institucional como para cualquier persona interesada.

La herramienta consta de un total de 44 preguntas distribuidas en 9 secciones. Para completar adecuadamente todos los campos de la ficha, se requiere la participación de un equipo multidisciplinario de la institución, que incluya roles como el jefe de proyecto, analista de datos, responsable de datos, equipo legal, y encargado de comunicaciones y todos los demás que considere la institución. 

Todas las preguntas marcadas con un asterisco (:red[*]) son preguntas obligatorias. Al terminar de responder las preguntas, se debe marcar el botón **“descargar ficha”** para acceder a la ficha de transparencia en formato *PDF*. 
    
Durante el uso de la herramienta, la información no es almacenada por la plataforma, para resguardar la privacidad de los datos que sean ingresados en los campos.

Esta herramienta se basa en el enfoque de Model Cards for Model Reporting (Mitchell, 2019). """)

st.write("Estás listo? 🔜")


questions = {}

tab1, tab2 = st.tabs(["1.Visión general 👁️", "2.Detalles del modelo 📄"])
tab3, tab4, tab5, tab6 = st.tabs(["3.Clasificación ☯", "4.Métricas de rendimiento 📈", "5.Datos de entrenamiento 💿", "6.Datos de evaluación 🧪"])
tab8, tab9, tab10 = st.tabs(["7.Consideraciones éticas 🧠", "8.Advertencias y recomendaciones ⚠️", "9.Reclamación 🚨"])

with tab1:

    st.header("Visión general del modelo 📊")

    questions["nombre_modelo"] = st.text_input("1.Nombre del modelo :red[*]", max_chars=SHORT_STRING) #Obligatorio
    questions["tipo_modelo"] = st.text_area("2.¿Qué tipo de modelo es? :red[*] :red[antes 5]", placeholder="Esto incluye detalles básicos de la arquitectura del modelo, como si es un clasificador de Naive Bayes, una Red Neuronal Convolucional, etc. Esto es probablemente relevante para desarrolladores de software y modelos, así como para personas conocedoras de aprendizaje automático, para resaltar qué tipos de suposiciones están codificadas en el sistema.",max_chars=LONG_STRING) #Obligatorio
    questions["proposito_modelo"] = st.text_area("3.Describa el propósito y funcionalidad del modelo :red[*] :red[antes 10]", max_chars=LONG_STRING) #Obligatorio
    questions["TA_porque_modelo"] = st.text_area("4.*¿Por qué se decidió utilizar este SDA en lugar de otro tipo de solución?* :red[antes 11]", max_chars=LONG_STRING)
    questions["TA_alcanzar_resultados"] = st.text_area("5.*¿Cómo el modelo alcanza u obtiene sus resultados?* :red[antes 12]",placeholder="Describa el flujo de funciomaiento de su sistema para generar un resultado" , max_chars=LONG_STRING)
    questions["UsoPrevisto_modelo"] = st.text_area("6.¿Cuál es el uso previsto del 'modelo'? :red[*] :red[antes 13]", placeholder="¿Qué puede esperar el usuario directo del modelo al emplearlo?. Esta sección detalla si el modelo se desarrolló con tareas generales o específicas en mente. Los casos de uso pueden estar definidos de manera amplia o estrecha según lo que los desarrolladores pretendan. Por ejemplo, si el modelo se construyó simplemente para etiquetar imágenes, esta tarea debería indicarse como el caso de uso principal previsto.", max_chars=LONG_STRING) #Obligatorio
    questions["UsosNocontext_modelo"] = st.text_area("7.¿Qué usos están fuera del alcance del modelo? :red[antes 14]", placeholder="Aquí, la ficha del modelo debería resaltar la tecnología con la que el modelo podría confundirse fácilmente, o contextos relacionados a los que los usuarios podrían intentar aplicar el modelo.", max_chars=LONG_STRING)

    # Genera secciones HTML para cada sección si el valor no está vacío

    questions["TA_porque_modelo_line"] = preparar_seccion_html("Razones de usar el modelo para tomar decisiones", questions["TA_porque_modelo"], prefijo="<li>", sufijo="</li>")
    questions["TA_alcanzar_resultados_line"] = preparar_seccion_html("Forma en la que el modelo obtiene resultados", questions["TA_alcanzar_resultados"], prefijo="<li>", sufijo="</li>")
    
    questions["UsosNocontext_modelo_line"] = preparar_seccion_html("Usos fuera del alcance del modelo", questions["UsosNocontext_modelo"], prefijo="<li>", sufijo="</li>")


with tab2:
    st.header("Detalles del modelo 📄")

    
    questions["desarrollador_modelo"] = st.text_area("8.¿Qué persona u organización desarrolló el modelo? :red[*] :red[antes 2]", placeholder=" Esto puede ser utilizado por todas las partes interesadas para inferir detalles relacionados con el desarrollo del modelo y posibles conflictos de interés.",max_chars=SHORT_STRING)#Obligatorio
    questions["version_modelo"] = st.text_input("9.¿Cuál es la versión del modelo? :red[antes 3]", placeholder="Describa el número de la versión del modelo. Ej: 1.0.0",max_chars=SHORT_STRING)
    questions["fecha_modelo"] = st.date_input("10.¿Cuándo se desplegó o implementó este modelo? :red[antes 4] Esto es útil para que todas las partes interesadas se informen sobre las técnicas y fuentes de datos que probablemente estuvieron disponibles durante el desarrollo del modelo.", value=None) #Obligatorio
    if questions["fecha_modelo"] is not None: #TODO: Revisar el render de la pregunta ya que no es obligatoria
        questions["fecha_modelo"] = questions["fecha_modelo"].strftime("%d/%m/%Y")
    else:
        questions["fecha_modelo"] = ""

    

    questions["link_modelo"] = st.text_input("11.¿Dónde se pueden encontrar recursos para obtener información adicional del proyecto? :red[antes 6]", placeholder="Por ejemplo, link a la página institucional",max_chars=LONG_STRING)
    questions["cita_modelo"] = st.text_area("12.¿Cómo debería citarse el modelo? :red[antes 7]", max_chars=LONG_STRING)
    questions["licencia_modelo"] = st.text_input("13.¿Qué tipo de licencia tiene el modelo? :red[antes 8]", max_chars=SHORT_STRING)
    questions["contacto_modelo"] = st.text_area("14.¿Hay algún canal de reclamos o sugerencias mediante los cuales las personas puedan solicitar más información? :red[antes 9]", max_chars=LONG_STRING)

    # Genera secciones HTML para cada sección si el valor no está vacío y si no son obligatorios

    questions["link_modelo_line"] = preparar_seccion_html("Enlace", questions["link_modelo"], prefijo="<li>", sufijo="</li>")
    questions["cita_modelo_line"] = preparar_seccion_html("¿Cómo citar?", questions["cita_modelo"], prefijo="<li>", sufijo="</li>")
    questions["licencia_modelo_line"] = preparar_seccion_html("Licencia del modelo", questions["licencia_modelo"], prefijo="<li>", sufijo="</li>")
    questions["contacto_modelo_line"] = preparar_seccion_html("Contacto", questions["contacto_modelo"], prefijo="<li>", sufijo="</li>")


with tab3:
    st.header("  Clasificación ☯")
    questions["TA_classModelo"] = st.radio("15.  ¿Es el modelo de clasificación?",options=["Sí","No"],index=1)
    questions["TA_classModelo_categorias"] = None
    questions["TA_classModel_metodologia"] = None
    questions["TA_classModelo_efecto_variables"] = None
    questions["TA_classModelo_relevancia_categoria"] = None

    if questions["TA_classModelo"] == "Sí":
        questions["TA_classModelo_visible"] = ""
        #Obligatorios
        questions["TA_classModelo_categorias"] = st.text_area("16.  ¿Qué perfiles o categorías asigna o existen? :red[*]", max_chars=SHORT_STRING)#Obligatorio
        
        #Opcionales
        questions["TA_classModel_metodologia"] = st.text_area("17.¿Qué forma, metodología o mecanismo usa el modelo para clasificar los datos? ¿Cuáles son los umbrales de decisión?", max_chars=SHORT_STRING)
        questions["TA_classModelo_efecto_variables"] = st.text_area("18.  ¿Qué efecto tiene cada variable o parámetro en la asignación de categoría, etiqueta, perfil o posición?", max_chars=SHORT_STRING)
        questions["TA_classModelo_relevancia_categoria"] = st.text_area("19.  ¿Por qué la categoría, perfil o prioridad es relevante para que el modelo alcance sus resultados?", max_chars=LONG_STRING)

        questions["TA_classModel_metodologia_line"] = preparar_seccion_html("Mecanismo utilizado para clasificar datos", questions["TA_classModel_metodologia"], prefijo="<li>", sufijo="</li>")
        questions["TA_classModelo_efecto_variables_line"] = preparar_seccion_html("Efecto de las variables en la asignación de las categorías", questions["TA_classModelo_efecto_variables"], prefijo="<li>", sufijo="</li>")
        questions["TA_classModelo_relevancia_categoria_line"] = preparar_seccion_html("Relevancia de la categoría para el modelo", questions["TA_classModelo_relevancia_categoria"], prefijo="<li>", sufijo="</li>")
    else:
        questions["TA_classModelo_visible"] = "hidden"

with tab4: 
    st.header("Métricas de rendimiento 📈")
    #Obligatorios
    questions["metricas_modelo"] = st.text_area("20.¿Qué métricas utiliza para medir el rendimiento de su modelo? :red[*]", max_chars=LONG_STRING)
    questions["umbralDesicion_modelo"] =  st.slider("21.¿Cuál es el umbral de decisión del modelo?", min_value=0.0, max_value=1.0, value=0.5, step=0.1) #TODO: Revisar el render si no hay valor.
    #Opcionales
    questions["calculo_mediciones_modelo"] = st.text_area("22.¿Cómo se calculan las mediciones y estimaciones de estas métricas?", placeholder="Por ejemplo, esto puede incluir desviación estándar, varianza, intervalos de confianza o divergencia KL. También se deben incluir detalles sobre cómo se aproximan estos valores (por ejemplo, promedio de 5 ejecuciones, validación cruzada de 10 pliegues).", max_chars=LONG_STRING)

    questions["calculo_mediciones_modelo_line"] = preparar_seccion_html("Forma en la que se estiman las métricas:", questions["calculo_mediciones_modelo"], prefijo="<p>", sufijo="</p>")

with tab5:
    st.header("Datos de entrenamiento 💿")
    #Obligatorios
    questions["datos_modelo"] = st.text_area("23.¿Qué datos se utilizaron para el entrenamiento del modelo? :red[*]", max_chars=LONG_STRING) 
    questions["preprocesamiento_modelo"] = st.text_area("24.¿Se aplicaron pasos de pre-procesamiento o limpieza a los datos? ¿Cuáles? :red[*]", max_chars=LONG_STRING) 

with tab6:
    st.header("Datos de evaluación 🧪")
    
    questions["conjunto_datos_eval_modelo"] = st.text_area("25.¿Qué conjuntos de datos se utilizaron para evaluar el modelo? :red[*]", max_chars=LONG_STRING) #Obligatoria
    questions["eleccion_evaluacion"] = st.text_area("26.¿Por qué se eligieron estos conjuntos de datos?", max_chars=LONG_STRING)
    questions["preprocesamiento_evaluacion"] = st.text_area("27.¿Cómo se preprocesaron los datos para la evaluación? :red[*]", placeholder="(por ejemplo, tokenización de oraciones, recorte de imágenes, cualquier filtrado como eliminar imágenes sin caras)", max_chars=LONG_STRING) #Obligatoria

    questions["eleccion_evaluacion_line"] = preparar_seccion_html("<strong>Justificación de la elección del modelo</strong>", questions["eleccion_evaluacion"], prefijo="<p>", sufijo="</p>")

#with tab7:
#    st.header("Análisis cuantitativo #️⃣")

#    st.write("""Los análisis cuantitativos deben desagregarse, es decir, desglosarse según los factores elegidos. Los análisis cuantitativos deben proporcionar los resultados de la evaluación del modelo según las métricas seleccionadas, 
#             brindando valores de intervalo de confianza cuando sea posible. La paridad en las diferentes métricas entre los subgrupos poblacionales desglosados corresponde a cómo se define a menudo la equidad. """)

#    questions["analisis_modelo"] = st.text_area("28.¿Cómo le fue al modelo con respecto a cada factor?", max_chars=LONG_STRING)
#    questions["analisis_errores_modelo"] = st.text_area("29.¿Cómo le fue al modelo con respecto a la intersección de los factores evaluados?", max_chars=LONG_STRING)

with tab8:
    st.header("Consideraciones éticas 🧠")

    questions["TA_modelo_categoriza"] = st.radio("30.  ¿El modelo categoriza o perfila a las personas? :red[*]",options=["Sí","No"]) #obligatorio
    # Esta depende de la anterior
    if questions["TA_modelo_categoriza"] == "Sí":
        questions["TA_razones_decision_negativa_personas"] = st.text_area("31.  ¿Qué circunstancias llevan a una decisión negativa respecto de la persona?", max_chars=LONG_STRING)
        questions["TA_razones_decision_negativa_personas_line"] = preparar_seccion_html("Circunstancias de decisión negativa", questions["TA_razones_decision_negativa_personas"], prefijo="<p>", sufijo="</p>")
    
    questions["TA_datos_personales"] = st.radio("32.  ¿El modelo utiliza datos personales? :red[*]",options=["Sí","No"]) #obligatorio
    questions["TA_razones_datos_personales"] = None

    if questions["TA_datos_personales"] == "Sí":
        questions["TA_razones_datos_personales"] = st.text_area("32.1.¿Cuáles?", max_chars=SHORT_STRING)
        questions["TA_razones_datos_personales_line"] = preparar_seccion_html("Datos personales utilizados: ", questions["TA_razones_datos_personales"], prefijo="<p>", sufijo="</p>")
    

    questions["dato_sensible"] = st.radio("33.¿El modelo utiliza algún dato sensible (por ejemplo, ley antidiscriminación)? :red[*]",options=["Sí","No"]) #obligatorio
    questions["dato_sensible_tipo"] = None

    if questions["dato_sensible"] == "Sí":
        questions["dato_sensible_tipo"] = st.text_area("33.1.¿Cuáles tipos de datos sensibles se utilizaron?", max_chars=SHORT_STRING) 
        
        questions["dato_sensible_tipo_line"] = preparar_seccion_html("Datos sensibles utilizados: ", questions["dato_sensible_tipo"], prefijo="<p>", sufijo="</p>")
    
    questions["asuntos_centrales_modelo"] = st.radio("34.¿Se pretende que el modelo informe decisiones sobre asuntos centrales para la vida o el florecimiento humano, como la salud o la seguridad? ¿O podría usarse de esa manera? :red[*]",options=["Sí","No"]) #obligatorio
    questions["asuntos_centrales_tipo"] = None

    if questions["asuntos_centrales_modelo"] == "Sí":
        questions["asuntos_centrales_tipo"] = st.text_area("34.1.¿Cuáles? :red[*]", max_chars=SHORT_STRING) #obligatorio
        questions["asuntos_centrales_tipo_line"] = preparar_seccion_html("Asuntos centrales para la vida", questions["asuntos_centrales_tipo"], prefijo="<p>", sufijo="</p>")
    
    questions["estrategias_mitigaciones_modelo"] = st.text_area("35.¿Qué estrategias de mitigación de riesgos se utilizaron durante el desarrollo del modelo? :red[*]", max_chars=LONG_STRING) #Opcional
    questions["riesgos_uso_modelo"] = st.text_area("36.¿Qué riesgos pueden estar presentes en el uso del modelo?", placeholder="Trate de identificar a los posibles receptores, la probabilidad y la magnitud de los daños. Si no se pueden determinar, indique que se consideraron pero siguen siendo desconocidos.", max_chars=LONG_STRING) 
    questions["casos_uso_conocidos"] = st.text_area("37.¿Hay casos de uso conocidos del modelo que sean especialmente problemáticos?", max_chars=LONG_STRING) #Casos de uso problematicos
    questions["otra_consideracion"] = st.text_area("38.De existir alguna otra consideración ética adicional que se haya tenido en cuenta en el desarrollo del modelo, indicar en este apartado.", placeholder="Por ejemplo, revisión por parte de un consejo externo o pruebas con una comunidad específica.", max_chars=LONG_STRING)


    questions["riesgos_uso_modelo"] = preparar_seccion_html("<strong>Riesgos del modelo</strong>", questions["riesgos_uso_modelo"], prefijo="<p>", sufijo="</p>")
    questions["estrategias_mitigaciones_modelo_line"] = preparar_seccion_html("<strong>Estrategias de mitigación de riesgos</strong>", questions["estrategias_mitigaciones_modelo"], prefijo="<p>", sufijo="</p>")
    questions["casos_uso_conocidos_line"] = preparar_seccion_html("<strong>Casos de uso problemáticos</strong>", questions["casos_uso_conocidos"], prefijo="<p>", sufijo="</p>")
    questions["otra_consideracion_line"] = preparar_seccion_html("<strong>Otras consideraciones</strong>", questions["otra_consideracion"], prefijo="<p>", sufijo="</p>")

with tab9:
    st.header("Advertencias y recomendaciones ⚠️")

    questions["prueba_adicional"] = st.text_area("39.¿Los resultados sugieren alguna prueba adicional?", max_chars=LONG_STRING) #Opcional #correcciones, siguientes pasos
    questions["grupo_relevante"] = st.radio("40.¿Hubo algún grupo relevante que no estuvo representado en el conjunto de datos de evaluación?",options=["Sí","No"]) #Opcional
    questions["recomendaciones_adicionales"] = st.text_area("41.¿Existen recomendaciones adicionales para el uso del modelo? ", max_chars=LONG_STRING) #Opcional
    questions["caracteristicas_ideales"] = st.text_area("42.¿Cuáles son las características ideales de un conjunto de datos de evaluación para este modelo?", placeholder="Ejemplos: \n Carpeta con imágenes de 20x20 \n Archivo csv con las columnas: edad,genero,salario, etc \n formulario predefinido con todas las respuestas",max_chars=LONG_STRING) #que variables tiene que tener el dataset que uses para 

    questions["prueba_adicional_line"] = preparar_seccion_html("<strong>Pruebas adicionales</strong>", questions["prueba_adicional"], prefijo="<p>", sufijo="</p>")    
    questions["recomendaciones_adicionales_line"] = preparar_seccion_html("<strong>Recomendaciones adicionales</strong>", questions["recomendaciones_adicionales"], prefijo="<p>", sufijo="</p>")
    questions["caracteristicas_ideales_line"] = preparar_seccion_html("<strong>Características ideales del conjunto de datos</strong>", questions["caracteristicas_ideales"], prefijo="<p>", sufijo="</p>")
with tab10:
    st.header("  Reclamación 🚨")

    st.write("En caso de ser necesario apelar a una decisión del modelo, debe de existir un método establecido para hacer llegar los reclamos de los usuarios. ")

    questions["TA_reclamacion"] = st.radio("43.  ¿Existe una vía de reclamación especial respecto de las decisiones del modelo? :red[*]",options=["Sí","No"]) #obligatorio pero debe tener un texto al renderizar
    questions["TA_via_reclamacion"] = None
    
    if questions["TA_reclamacion"] == "Sí":
        questions["TA_reclamacion_visible"] = True
        questions["TA_via_reclamacion"] = st.text_area("44.  ¿Cuál es la forma de acceder a la vía de reclamación? :red[*]", max_chars=LONG_STRING) #Obligatorio
        questions["TA_via_reclamacion_line"] = preparar_seccion_html("<strong>Vía de reclamación</strong>", questions["TA_via_reclamacion"], prefijo="<p>", sufijo="</p>")
    else: 
        questions["TA_reclamacion_visible"] = False


submitted = st.button("Generar Ficha de transparencia")

if submitted:
    # Generación del PDF
    campos_verificados = verificar_campos_obligatorios()
    
    if campos_verificados != "all":
        st.error("No se han completado todos los campos obligatorios. Por favor, complete el campo: " + campos_verificados)  
    else:

        questions["year"] = datetime.now().year
        # Colocar el mes de elaboración
        questions["elaboration_date"] = datetime.now().month
        try:
            print(questions)
            pdf = generate_pdf(MODEL_CARD_HTML_TEMPLATE.format_map(SafeDict(questions)))
            st.success("Ficha de transparencia generada con éxito.")
            # Botón de descarga
            download_button(pdf, "ficha_transparencia.pdf", "Descargar Ficha de transparencia en PDF")

            guardar_en_mongodb(questions)

        except Exception as e:
            st.error("Error al generar la Ficha de transparencia, intentelo más tarde.")

st.sidebar.title("Agradecimientos")
st.sidebar.write("ANID + Subdirección de Investigación Aplicada/Concurso IDeA I+D 2023 + ID23I10357")
# Dividir la página en dos columnas
st.sidebar.subheader("Una iniciativa en colaboración con:")
st.sidebar.image("_statics/ANID.png",width=100)
#st.sidebar.image("_statics/BidLab.png",width=100)
