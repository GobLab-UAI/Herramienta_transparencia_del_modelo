import streamlit as st

import streamlit as st
import smtplib
import ssl
from email.message import EmailMessage

from rendering import generate_pdf, download_button
from template import MODEL_CARD_HTML_TEMPLATE

class SafeDict(dict):
    def __missing__(self, key):
        return ''

# TODO: Tengo que colocar los botones para siguiente tab dentro de cada tab (que del tab0 pase al tab1 y así sucesivamente)
    
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
                    "nombre_modelo","desarrollador_modelo","fecha_modelo","tipo_modelo",
                    "proposito_modelo","UsoPrevisto_modelo",
                    "metricas_modelo","umbralDesicion_modelo","datos_modelo","preprocesamiento_modelo",
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

title = "Ficha de transparencia del modelo 🧠🪟"
st.markdown(f"<h3 style='text-align: left; color: black;'>V.0.0.1</h3>", unsafe_allow_html=True)
st.markdown(f"<h1 style='text-align: center; color: black;'>{title}</h1>", unsafe_allow_html=True)


st.write("Bienvenido a la herramienta para crear una ficha de transparencia del modelo. para esto vamos a requerir algunos datos de tu modelo.")
st.write("Estás listo? 🔜")


questions = {}

tab1, tab2 = st.tabs(["1.Detalles del modelo 📄", "2.Visión general 👁️"])
tab3, tab4, tab5, tab6 = st.tabs(["3.Clasificación ☯", "4.Métricas de rendimiento 📈", "5.Datos de entrenamiento 💿", "6.Datos de evaluación 🧪"])
tab8, tab9, tab10 = st.tabs(["7.Consideraciones éticas 🧠", "8.Advertencias y recomendaciones ⚠️", "9.Reclamación 🚨"])


with tab1:
    st.header("Detalles del modelo 📄")

    questions["nombre_modelo"] = st.text_input("1.Nombre del modelo :red[`*`]", max_chars=SHORT_STRING) #Obligatorio
    questions["desarrollador_modelo"] = st.text_area("2.¿Qué persona u organización desarrolló el modelo? :red[`*`]", placeholder=" Esto puede ser utilizado por todas las partes interesadas para inferir detalles relacionados con el desarrollo del modelo y posibles conflictos de interés.",max_chars=SHORT_STRING)#Obligatorio
    questions["version_modelo"] = st.text_input("3.¿Cuál es la versión del modelo?¿Han existido versiones anteriores?", placeholder="Versión del modelo y número de versiones",max_chars=SHORT_STRING)
    questions["fecha_modelo"] = st.date_input("4.¿Cuándo se desplegó o implementó este modelo? Esto es útil para que todas las partes interesadas se informen sobre las técnicas y fuentes de datos que probablemente estuvieron disponibles durante el desarrollo del modelo :red[`*`].", value=None) #Obligatorio
    questions["tipo_modelo"] = st.text_area("5.¿Qué tipo de modelo es? :red[`*`]", placeholder="Esto incluye detalles básicos de la arquitectura del modelo, como si es un clasificador de Naive Bayes, una Red Neuronal Convolucional, etc. Esto es probablemente relevante para desarrolladores de software y modelos, así como para personas conocedoras de aprendizaje automático, para resaltar qué tipos de suposiciones están codificadas en el sistema.",max_chars=LONG_STRING) #Obligatorio

    questions["link_modelo"] = st.text_input("6.¿Dónde se pueden encontrar recursos para obtener más información?", placeholder="Por ejemplo, link a la página institucional",max_chars=LONG_STRING)
    questions["cita_modelo"] = st.text_area("7.¿Cómo debería citarse el modelo?", max_chars=LONG_STRING)
    questions["licencia_modelo"] = st.text_input("8.¿Qué tipo de licencia tiene el modelo?", max_chars=SHORT_STRING)
    questions["contacto_modelo"] = st.text_area("9.¿Hay alguna dirección de correo electrónico a la que las personas pueden escribir para obtener más información?", max_chars=LONG_STRING)

    # Genera secciones HTML para cada sección si el valor no está vacío y si no son obligatorios

    questions["link_modelo_line"] = preparar_seccion_html("Enlace", questions["link_modelo"], prefijo="<li>", sufijo="</li>")
    questions["cita_modelo_line"] = preparar_seccion_html("¿Cómo citar?", questions["cita_modelo"], prefijo="<li>", sufijo="</li>")
    questions["licencia_modelo_line"] = preparar_seccion_html("Licencia del modelo", questions["licencia_modelo"], prefijo="<li>", sufijo="</li>")
    questions["contacto_modelo_line"] = preparar_seccion_html("Contacto", questions["contacto_modelo"], prefijo="<li>", sufijo="</li>")

with tab2:

    st.header("Visión general del modelo 📊")

    questions["proposito_modelo"] = st.text_area("10.Describa el propósito y funcionalidad del modelo :red[`*`]", max_chars=LONG_STRING) #Obligatorio
    questions["TA_porque_modelo"] = st.text_area("11.*TA: ¿Por qué se utiliza el modelo para tomar decisiones y no otro mecanismo?* ", max_chars=LONG_STRING)
    questions["TA_alcanzar_resultados"] = st.text_area("12.*TA: ¿Cómo el modelo alcanza u obtiene sus resultados?*",placeholder="Describa el flujo de funciomaiento de su sistema para generar un resultado" , max_chars=LONG_STRING)
    questions["UsoPrevisto_modelo"] = st.text_area("13.¿Cuál es el uso previsto y las expectativas del usuario? :red[`*`]", placeholder="Esta sección detalla si el modelo se desarrolló con tareas generales o específicas en mente. Los casos de uso pueden estar definidos de manera amplia o estrecha según lo que los desarrolladores pretendan. Por ejemplo, si el modelo se construyó simplemente para etiquetar imágenes, esta tarea debería indicarse como el caso de uso principal previsto.", max_chars=LONG_STRING) #Obligatorio
    questions["UsosNocontext_modelo"] = st.text_area("14.¿Qué usos están fuera del alcance del modelo?", placeholder="Aquí, la ficha del modelo debería resaltar la tecnología con la que el modelo podría confundirse fácilmente, o contextos relacionados a los que los usuarios podrían intentar aplicar el modelo.", max_chars=LONG_STRING)

    # Genera secciones HTML para cada sección si el valor no está vacío

    questions["TA_porque_modelo_line"] = preparar_seccion_html("Razones de usar el modelo para tomar decisiones", questions["TA_porque_modelo"], prefijo="<li>", sufijo="</li>")
    questions["TA_alcanzar_resultados_line"] = preparar_seccion_html("Forma en la que el modelo obtiene resultados", questions["TA_alcanzar_resultados"], prefijo="<li>", sufijo="</li>")
    
    questions["UsosNocontext_modelo_line"] = preparar_seccion_html("Usos fuera del alcance del modelo", questions["UsosNocontext_modelo"], prefijo="<li>", sufijo="</li>")

with tab3:
    st.header("TA: Clasificación ☯")
    questions["TA_classModelo"] = st.radio("15.TA: ¿Es el modelo de clasificación?",options=["Sí","No"],index=1)
    questions["TA_classModelo_categorias"] = None
    questions["TA_classModel_metodologia"] = None
    questions["TA_classModelo_efecto_variables"] = None
    questions["TA_classModelo_relevancia_categoria"] = None

    if questions["TA_classModelo"] == "Sí":
        questions["TA_classModelo_visible"] = ""
        #Obligatorios
        questions["TA_classModelo_categorias"] = st.text_area("16.TA: ¿Qué perfiles o categorías asigna o existen? :red[`*`]", max_chars=SHORT_STRING)#Obligatorio
        
        #Opcionales
        questions["TA_classModel_metodologia"] = st.text_area("17.¿Qué forma, metodología o mecanismo usa el modelo para clasificar los datos? ¿Cuáles son los umbrales de decisión?", max_chars=SHORT_STRING)
        questions["TA_classModelo_efecto_variables"] = st.text_area("18.TA: ¿Qué efecto tiene cada variable o parámetro en la asignación de categoría, etiqueta, perfil o posición?", max_chars=SHORT_STRING)
        questions["TA_classModelo_relevancia_categoria"] = st.text_area("19.TA: ¿Por qué la categoría, perfil o prioridad es relevante para que el modelo alcance sus resultados?", max_chars=LONG_STRING)

        questions["TA_classModel_metodologia_line"] = preparar_seccion_html("Mecanismo utilizado para clasificar datos", questions["TA_classModel_metodologia"], prefijo="<li>", sufijo="</li>")
        questions["TA_classModelo_efecto_variables_line"] = preparar_seccion_html("Efecto de las variables en la asignación de las categorías", questions["TA_classModelo_efecto_variables"], prefijo="<li>", sufijo="</li>")
        questions["TA_classModelo_relevancia_categoria_line"] = preparar_seccion_html("Relevancia de la categoría para el modelo", questions["TA_classModelo_relevancia_categoria"], prefijo="<li>", sufijo="</li>")
    else:
        questions["TA_classModelo_visible"] = "hidden"

with tab4: 
    st.header("Métricas de rendimiento 📈")
    #Obligatorios
    questions["metricas_modelo"] = st.text_area("20.¿Qué métricas utiliza para medir el rendimiento de su modelo? :red[`*`]", max_chars=LONG_STRING)
    questions["umbralDesicion_modelo"] =  st.slider("21.¿Cuál es el umbral de decisión del modelo? :red[`*`]", min_value=0.0, max_value=1.0, value=0.5, step=0.1)
    #Opcionales
    questions["calculo_mediciones_modelo"] = st.text_area("22.¿Cómo se calculan las mediciones y estimaciones de estas métricas?", placeholder="Por ejemplo, esto puede incluir desviación estándar, varianza, intervalos de confianza o divergencia KL. También se deben incluir detalles sobre cómo se aproximan estos valores (por ejemplo, promedio de 5 ejecuciones, validación cruzada de 10 pliegues).", max_chars=LONG_STRING)

    questions["calculo_mediciones_modelo_line"] = preparar_seccion_html("Forma en la que se estiman las métricas:", questions["calculo_mediciones_modelo"], prefijo="<p>", sufijo="</p>")

with tab5:
    st.header("Datos de entrenamiento 💿")
    #Obligatorios
    questions["datos_modelo"] = st.text_area("23.¿Qué datos se utilizaron para el entrenamiento del modelo? :red[`*`]", max_chars=LONG_STRING) 
    questions["preprocesamiento_modelo"] = st.text_area("24.¿Se aplicaron pasos de pre-procesamiento o limpieza a los datos? ¿Cuáles? :red[`*`]", max_chars=LONG_STRING) 

with tab6:
    st.header("Datos de evaluación 🧪")
    
    questions["conjunto_datos_eval_modelo"] = st.text_area("25.¿Qué conjuntos de datos se utilizaron para evaluar el modelo? :red[`*`]", max_chars=LONG_STRING) #Obligatoria
    questions["eleccion_evaluacion"] = st.text_area("26.¿Por qué se eligieron estos conjuntos de datos?", max_chars=LONG_STRING)
    questions["preprocesamiento_evaluacion"] = st.text_area("27.¿Cómo se preprocesaron los datos para la evaluación? :red[`*`]", placeholder="(por ejemplo, tokenización de oraciones, recorte de imágenes, cualquier filtrado como eliminar imágenes sin caras)", max_chars=LONG_STRING) #Obligatoria

    questions["eleccion_evaluacion_line"] = preparar_seccion_html("<strong>Justificación de la elección del modelo</strong>", questions["eleccion_evaluacion"], prefijo="<p>", sufijo="</p>")

#with tab7:
#    st.header("Análisis cuantitativo #️⃣")

#    st.write("""Los análisis cuantitativos deben desagregarse, es decir, desglosarse según los factores elegidos. Los análisis cuantitativos deben proporcionar los resultados de la evaluación del modelo según las métricas seleccionadas, 
#             brindando valores de intervalo de confianza cuando sea posible. La paridad en las diferentes métricas entre los subgrupos poblacionales desglosados corresponde a cómo se define a menudo la equidad. """)

#    questions["analisis_modelo"] = st.text_area("28.¿Cómo le fue al modelo con respecto a cada factor?", max_chars=LONG_STRING)
#    questions["analisis_errores_modelo"] = st.text_area("29.¿Cómo le fue al modelo con respecto a la intersección de los factores evaluados?", max_chars=LONG_STRING)

with tab8:
    st.header("Consideraciones éticas 🧠")

    questions["TA_modelo_categoriza"] = st.radio("30.TA: ¿El modelo categoriza o perfila a las personas? :red[`*`]",options=["Sí","No"]) #obligatorio
    # Esta depende de la anterior
    if questions["TA_modelo_categoriza"] == "Sí":
        questions["TA_razones_decision_negativa_personas"] = st.text_area("31.TA: ¿Qué circunstancias llevan a una decisión negativa respecto de la persona?", max_chars=LONG_STRING)
        questions["TA_razones_decision_negativa_personas_line"] = preparar_seccion_html("Circunstancias de decisión negativa", questions["TA_razones_decision_negativa_personas"], prefijo="<p>", sufijo="</p>")
    
    questions["TA_datos_personales"] = st.radio("32.TA: ¿El modelo utiliza datos personales? :red[`*`]",options=["Sí","No"]) #obligatorio
    questions["TA_razones_datos_personales"] = None

    if questions["TA_datos_personales"] == "Sí":
        questions["TA_razones_datos_personales"] = st.text_area("32.1.¿Cuáles?", max_chars=SHORT_STRING)
        questions["TA_razones_datos_personales_line"] = preparar_seccion_html("Datos personales utilizados: ", questions["TA_razones_datos_personales"], prefijo="<p>", sufijo="</p>")
    

    questions["dato_sensible"] = st.radio("33.¿El modelo utiliza algún dato sensible (por ejemplo, clases protegidas)? :red[`*`]",options=["Sí","No"]) #obligatorio
    questions["dato_sensible_tipo"] = None

    if questions["dato_sensible"] == "Sí":
        questions["dato_sensible_tipo"] = st.text_area("33.1.¿Cuáles tipos de datos sensibles se utilizaron?", max_chars=SHORT_STRING) 
        
        questions["dato_sensible_tipo_line"] = preparar_seccion_html("Datos sensibles utilizados: ", questions["dato_sensible_tipo"], prefijo="<p>", sufijo="</p>")
    
    questions["asuntos_centrales_modelo"] = st.radio("34.¿Se pretende que el modelo informe decisiones sobre asuntos centrales para la vida o el florecimiento humano, como la salud o la seguridad? ¿O podría usarse de esa manera? :red[`*`]",options=["Sí","No"]) #obligatorio
    questions["asuntos_centrales_tipo"] = None

    if questions["asuntos_centrales_modelo"] == "Sí":
        questions["asuntos_centrales_tipo"] = st.text_area("34.1.¿Cuáles? :red[`*`]", max_chars=SHORT_STRING) #obligatorio
        questions["asuntos_centrales_tipo_line"] = preparar_seccion_html("Asuntos centrales para la vida", questions["asuntos_centrales_tipo"], prefijo="<p>", sufijo="</p>")
    
    questions["estrategias_mitigaciones_modelo"] = st.text_area("35.¿Qué estrategias de mitigación de riesgos se utilizaron durante el desarrollo del modelo? :red[`*`]", max_chars=LONG_STRING) #Opcional
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
    st.header("TA: Reclamación 🚨")

    st.write("En caso de ser necesario apelar a una decisión del modelo, debe de existir un método establecido para hacer llegar los reclamos de los usuarios. ")

    questions["TA_reclamacion"] = st.radio("43.TA: ¿Existe una vía de reclamación especial respecto de las decisiones del modelo? :red[`*`]",options=["Sí","No"]) #obligatorio pero debe tener un texto al renderizar
    questions["TA_via_reclamacion"] = None
    
    if questions["TA_reclamacion"] == "Sí":
        questions["TA_reclamacion_visible"] = True
        questions["TA_via_reclamacion"] = st.text_area("44.TA: ¿Cuál es la forma de acceder a la vía de reclamación? :red[`*`]", max_chars=LONG_STRING) #Obligatorio
        questions["TA_via_reclamacion_line"] = preparar_seccion_html("<strong>Vía de reclamación</strong>", questions["TA_via_reclamacion"], prefijo="<p>", sufijo="</p>")
    else: 
        questions["TA_reclamacion_visible"] = False


submitted = st.button("Generar Model Card")

if submitted:
    # Generación del PDF
    campos_verificados = verificar_campos_obligatorios()
    
    if campos_verificados != "all":
        st.error("No se han completado todos los campos obligatorios. Por favor, complete el campo: " + campos_verificados)  
    else:

        questions["year"] = "2024" 
        questions["elaboration_date"] = "Marzo de 2024"
        try:
            print(questions)
            pdf = generate_pdf(MODEL_CARD_HTML_TEMPLATE.format_map(SafeDict(questions)))
            st.success("Model Card generada con éxito.")
            # Botón de descarga
            download_button(pdf, "model_card.pdf", "Descargar Model Card en PDF")

        except Exception as e:
            st.error("Error al generar la Model Card, intentelo más tarde.")
            