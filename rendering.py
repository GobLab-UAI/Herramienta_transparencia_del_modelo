import streamlit as st
import base64
from weasyprint import HTML
import datetime

def generate_pdf(html_content):
    pdf = HTML(string=html_content).write_pdf()
    return pdf

def download_button(object_to_download, download_filename, button_text):
    b64 = base64.b64encode(object_to_download).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{download_filename}">{button_text}</a>'
    st.markdown(href, unsafe_allow_html=True)


def form_alt():
    # Formulario para ingresar datos de la Model Card
    with st.form("model_card_form"):
        st.title("Creación de Model Card")
        
        titulo = st.text_input("Título del Modelo")
        descripcion = st.text_area("Descripción del Modelo")
        fecha_creacion = st.date_input("Fecha de Creación")
        version = st.text_input("Versión")
        tipo_modelo = st.text_input("Tipo de Modelo")
        responsable = st.text_input("Responsable del Modelo")
        fuente_datos = st.text_input("Fuente de los Datos")
        preprocesamiento = st.text_area("Preprocesamiento Aplicado")
        particion = st.text_input("Partición (Entrenamiento,Validación,Test)")
        metricas = st.text_area("Métricas de Rendimiento")
        uso_recomendado = st.text_area("Casos de Uso Recomendados")
        limitaciones = st.text_area("Limitaciones")
        sesgos = st.text_area("Evaluación de Sesgos")
        consideraciones = st.text_area("Consideraciones Éticas")
        
        submitted = st.form_submit_button("Generar Model Card")
        
        if submitted:
            # Construcción del contenido HTML para la Model Card
            html_content = f"""
            <html>
            <head>
            <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            h1, h2 {{ color: #333; }}
            p, li {{ color: #555; }}
            </style>
            </head>
            <body>
            <h1>{titulo}</h1>
            <h2>Descripción del Modelo</h2>
            <p>{descripcion}</p>
            <h2>Información del Modelo</h2>
            <p><strong>Fecha de Creación:</strong> {fecha_creacion}</p>
            <p><strong>Versión:</strong> {version}</p>
            <p><strong>Tipo de Modelo:</strong> {tipo_modelo}</p>
            <p><strong>Responsable del Modelo:</strong> {responsable}</p>
            <h2>Datos</h2>
            <p><strong>Fuente de los Datos:</strong> {fuente_datos}</p>
            <p><strong>Preprocesamiento Aplicado:</strong> {preprocesamiento}</p>
            <p><strong>Partición:</strong> {particion}</p>
            <h2>Rendimiento del Modelo</h2>
            <p>{metricas}</p>
            <h2>Uso del Modelo</h2>
            <p>{uso_recomendado}</p>
            <p><strong>Limitaciones:</strong> {limitaciones}</p>
            <h2>Ética y Equidad</h2>
            <p>{sesgos}</p>
            <p>{consideraciones}</p>
            </body>
            </html>
            """
            
            # Generación del PDF
            pdf = generate_pdf(html_content)
            
            # Botón de descarga
            download_button(pdf, "model_card.pdf", "Descargar Model Card en PDF")
    return None

def diccionario_test():
    return {'nombre_modelo': 'Proyecto de prueba', 
              'desarrollador_modelo': 'Elaborado por el Goblab', 
              'version_modelo': 'V2.0.1', 
              'fecha_modelo': datetime.date(2024, 3, 20), 
              'tipo_modelo': 'Es un clasificador de Naive bayes con una profundidad de 10 y ensamblado dentro de un random forest', 
              'link_modelo': 'https://sqlflow.gudusoft.com/', 'cita_modelo': 'Storer, J., Hubley, R., Rosen, J. et al. The Dfam community resource of transposable element families, sequence models, and genome annotations. Mobile DNA 12, 2 (2021). https://doi.org/10.1186/s13100-020-00230-y', 
              'licencia_modelo': 'El modelo tiene licencia MIT', 
              'contacto_modelo': 'jspinad@gmail.com', 
              'proposito_modelo': 'El modelo se pensó para clasificar los reportes negativos de las centrales de riesgo, predicciones espaciales respecto a temas de lo que se requiere.', 
              'TA_porque_modelo': 'por la eficiencia que requiere tener el modelo', 
              'TA_alcanzar_resultados': 'El modelo alcanza sus resultados no sé como y no entiendo esta pregunta.', 
              'UsoPrevisto_modelo': 'El uso previsto de la herramienta es para realizar predicciones de fraude, la idea es que los usuarios puedan realizar muchas cosas al respecto con este tema y otras cosas más que pueden ir en este sentido.', 
              'UsosNocontext_modelo': 'Esto no debe confundirse con el sitema que se encuentra publicado dentro del paginado de las cosas.', 
              'TA_classModelo': 'No', 
              'TA_classModelo_categorias': None, 
              'TA_classModel_metodologia': None, 
              'TA_classModelo_efecto_variables': None, 
              'TA_classModelo_relevancia_categoria': None, 
              'metricas_modelo': ' F1 - score', 
              'umbralDesicion_modelo': 0.7, 
              'calculo_mediciones_modelo': 'Se hace una validación cruzada que es el promedio.', 
              'datos_modelo': 'Se usó una base de datos completa con cosas ', 
              'preprocesamiento_modelo': 'Si, se realiza normalización de datos.', 
              'conjunto_datos_eval_modelo': 'se usaron datos complementarios ', 
              'eleccion_evaluacion': 'Fué una decisión de las cuales no se tiene conocimiento.', 
              'preprocesamiento_evaluacion': 'se realizaron recortes de la base de datos.', 
              'TA_modelo_categoriza': 'No', 
              'TA_razones_decision_negativa_personas': 'Ninguna de las cosas', 
              'TA_datos_personales': 'Sí', 
              'TA_razones_datos_personales': 'Utiliza la ID y la cédula.', 
              'dato_sensible': 'Sí', 
              'dato_sensible_tipo': 'la cédula, el sexo y la cantidad de ingresos al mes del usuario', 
              'asuntos_centrales_modelo': 'No', 
              'asuntos_centrales_tipo': None, 
              'estrategias_mitigaciones_modelo': 'No se realizan estrategias de mitigación', 
              'riesgos_uso_modelo': 'No se puede determinar en el momento.', 
              'casos_uso_conocidos': 'No se tienen casos de uso conocido que sean problemáticos.', 
              'otra_consideracion': 'Si hay unas consideraciones éticas que se deben tener en cuenta para realizar cosas dentro de lo que se requiere.', 
              'prueba_adicional': 'No se sugieren pruebas adicionales.', 
              'grupo_relevante': 'No, se incluyeron todos', 
              'recomendaciones_adicionales': 'No', 
              'caracteristicas_ideales': 'Se debe tener una forma de poder cargar la información.', 
              'TA_reclamacion': 'No', 
              'TA_via_reclamacion': None    
            }

def model_card_test(diccionario):
    return {'nombre_modelo': 'Modelo Predictivo de No Cobro de PGU',
     'desarrollador_modelo': 'Instituto de prevision social ',
     'version_modelo': 'version 1',
     'fecha_modelo': datetime.date(2023,5,15),
     'tipo_modelo': 'Modelo de aprendizaje supervisado,tipo clasificación\nRed Neuronal Simple del tipo MLP',
     'link_modelo': '',
     'cita_modelo': '',
     'licencia_modelo': '',
     'contacto_modelo': '',
     'proposito_modelo': '•\tEste modelo fue diseñado y desarrollado para predecir que pensionados de la Pensión Garantizada Universal (PGU) no cobraran su beneficios en el ultimo mes que estan disponibles en los proveedores de pago, BancoEstado y Caja de Compensación Los Héroes, a objeto de que el Intituto de Previsón Social (IPS) los contacte y notifique, mediante email y/o SMS, para que acudan a cobrarlos.',
     'TA_porque_modelo': 'Porque eran muchos datos ',
     'TA_alcanzar_resultados': '',
     'UsoPrevisto_modelo': 'El modelo sera usado para apoyar la toma de decisiones del proceso mensual de contactabilidad de pensionados de PGU, para notificarlos que acudan a cobrar sus pensiones. Por tanto , es un modelo cuyo uso sera asistencial. ',
     'UsosNocontext_modelo': '',
     'TA_classModelo': 'Sí',
     'TA_classModelo_categorias': 'Cobros y No Cobros ',
     'TA_classModel_metodologia': 'Red Neuronal MLP ',
     'TA_classModelo_efecto_variables': 'Las variables mas importantes son Edad, Urbanidad y Cobro Mes Anterior ',
     'TA_classModelo_relevancia_categoria': 'Para poder saber a quienes contactar y a quienes no ',
     'metricas_modelo': 'Accuracy y Sensitivity ',
     'umbralDesicion_modelo': 0.5,
     'calculo_mediciones_modelo': 'Matriz de confusion ',
     'datos_modelo': 'Los datos de entrenamiento corresponde a 1 año de PGU que no habian sido cobradas hasta el mes subsiguiente al de su emisión y que transcurrido otro mes se clasifican entre Cobro (estado Pagado) y No Cobro (estado Caducado).\nCorresponden a 70.500 registros recolectados enre febrero de 2022 y enero de 2023. ',
     'preprocesamiento_modelo': 'Se limpiaron los registros en los que faltaban 3 o mas atributos\nEn los que faltaba 1 o 2 se relleno con un promedio ',
     'conjunto_datos_eval_modelo': 'De los datos recolectados se uso un split del 20% para test.',
     'eleccion_evaluacion': 'Porque eran los que estaban disponibles y eran apropiados al problema ',
     'preprocesamiento_evaluacion': 'Mismo proceso que los datos de entrenamiento',
     'TA_modelo_categoriza': 'Sí',
     'TA_razones_decision_negativa_personas': 'No se sabe',
     'TA_datos_personales': 'Sí',
     'TA_razones_datos_personales': 'RUT, edad, estado civil, nacionalidad y estado vital',
     'dato_sensible': 'Sí',
     'dato_sensible_tipo': 'Edad y genero',
     'asuntos_centrales_modelo': 'Sí',
     'asuntos_centrales_tipo': 'Pension garantizada universal (PGU)',
     'estrategias_mitigaciones_modelo': 'Se realizó una evaluación de impacto ex antes detectandose riegos bajos.',
     'riesgos_uso_modelo': 'Que no se notifique a una persona que no iba a cobrar, y el beneficio caduque ',
     'casos_uso_conocidos': 'No',
     'otra_consideracion': 'En forma ex post se realizó una evaluación de sesgo y equidad estadistica con Aequitas. No se encontraron sesgos o inequidades atribuibles al modelo.',
     'prueba_adicional': 'Se recomienda realizar este proceso en forma bimensual, ya que se obtendrian resultados similares a hacerlo de forma mensual, pero se requiere la mitad del esfuerzo.\n',
     'grupo_relevante': 'No',
     'recomendaciones_adicionales': 'Es muy sensible para el buen desempeño del proceso, donde se usa este modelo, contar con una buena data de contactabilidad.', 
     'caracteristicas_ideales': 'Datos de personas que se puedan contactar',
     'TA_reclamacion': 'No',
     'TA_via_reclamacion': None}

def test_real_info(diccionario):
    return {'nombre_modelo': 'Modelo Predictivo de No Cobro de PGU',
     'desarrollador_modelo': 'Instituto de prevision social',
     'version_modelo': 'Version 1',
     'fecha_modelo': datetime.date(2023, 5, 15),
     'tipo_modelo': 'Es un modelo de clasificacion de Red Neuronal Simple del tipo MLP,  programado en Python usando la librería Scikitlearn\n',
     'link_modelo': '',
     'cita_modelo': '',
     'licencia_modelo': '',
     'contacto_modelo': '',
     'link_modelo_line': '',
     'cita_modelo_line': '',
     'licencia_modelo_line': '',
     'contacto_modelo_line': '',
     'proposito_modelo': 'Este modelo fue diseñado y desarrollado para predecir que pensionados de la Pensión Garantizada Universal (PGU) no cobraran su beneficios en el ultimo mes que estan disponibles en los proveedores de pago, BancoEstado y Caja de Compensación Los Héroes, a objeto de que el Intituto de Previsón Social (IPS) los contacte y notifique, mediante email y/o SMS, para que acudan a cobrarlos.',
     'TA_porque_modelo': 'Por el volumen de los datos ',
     'TA_alcanzar_resultados': 'El modelo sera usado para apoyar la toma de decisiones del proceso mensual de contactabilidad de pensionados de PGU, para notificarlos que acudan a cobrar sus pensiones. Por tanto, es un modelo cuyo uso sera asistencial. ',
     'UsoPrevisto_modelo': 'El uso previsto es que se encuentren a las personas cuyo pago de PGU venceria el mes proximo. El usuario puede esperar que se encuentren todas las personas que necesitan ser notificadas para el cobro de su pension',
     'UsosNocontext_modelo': 'No puede predecir sobre otros beneficios todavia ',
     'TA_porque_modelo_line': '<li>Razones de usar el modelo para tomar decisiones: Por el volumen de los datos </li>',
     'TA_alcanzar_resultados_line': '<li>Forma en la que el modelo obtiene resultados: El modelo sera usado para apoyar la toma de decisiones del proceso mensual de contactabilidad de pensionados de PGU,para notificarlos que acudan a cobrar sus pensiones. Por tanto , es un modelo cuyo uso sera asistencial. </li>',
     'UsosNocontext_modelo_line': '<li>Usos fuera del alcance del modelo: No puede predecir sobre otros beneficios todavia </li>',
     'TA_classModelo': 'Sí',
     'TA_classModelo_categorias': 'No cobro y cobro ',
     'TA_classModel_metodologia': 'el modelo se basa en las variables de edad, urbanidad y cobros pasados para predecir',
     'TA_classModelo_efecto_variables': '',
     'TA_classModelo_relevancia_categoria': 'Gracias a la categoria que predice el modelo, se puede contactar a las personas que lo necesitan ',
     'TA_classModelo_visible': '',
     'TA_classModel_metodologia_line': '<li>Mecanismo utilizado para clasificar datos: el modelo se basa en las variables de edad, urbanidad y cobros pasados para predecir</li>',
     'TA_classModelo_efecto_variables_line': '',
     'TA_classModelo_relevancia_categoria_line': '<li>Relevancia de la categoría para el modelo: Gracias a la categoria que predice el modelo, se puede contactar a las personas que lo necesitan </li>',
     'metricas_modelo': 'Las metricas de desempeño principales usadas son Accuracy (79%) y Sensitivity (77%)',
     'umbralDesicion_modelo': 0.5,
     'calculo_mediciones_modelo': '',
     'calculo_mediciones_modelo_line': '',
     'datos_modelo': 'Los datos de entrenamiento corresponde a 1 año de PGU que no habian sido cobradas hasta el mes subsiguiente al de su emisión, y que transcurrido otro mes se clasifican entre Cobro (estado Pagado) y No Cobro (estado Caducado).\nCorresponden a 70.500 registros recolectados enre febrero de 2022 y enero de 2023. ',
     'preprocesamiento_modelo': 'Se eliminaron los registros en los que faltaban 3 datos o mas, y para aquellos en los que faltaban 1 o 2 datos se relleno con el promedio',
     'conjunto_datos_eval_modelo': 'De los datos explicados anteriormente, se uso un split del 20% para test.',
     'eleccion_evaluacion': '',
     'preprocesamiento_evaluacion': 'Se limpiaron de la misma manera que los datos de entrenamiento ',
     'eleccion_evaluacion_line': '',
     'TA_modelo_categoriza': 'Sí',
     'TA_razones_decision_negativa_personas': 'No se tiene una respuesta, pero las variables claves son edad, urbanidad y cobros anteriores ',
     'TA_razones_decision_negativa_personas_line': '<p>Circunstancias de decisión negativa: No se tiene una respuesta, pero las variables claves son edad, urbanidad y cobros anteriores </p>',
     'TA_datos_personales': 'Sí',
     'TA_razones_datos_personales': 'RUT, edad, genero, banco, metodo de cobro', 
     'TA_razones_datos_personales_line': '<p>Datos personales utilizados: : RUT,edad,genero,banco,metodo de cobro</p>',
     'dato_sensible': 'Sí',
     'dato_sensible_tipo': 'RUT',
     'dato_sensible_tipo_line': '<p>Datos sensibles utilizados: : RUT</p>',
     'asuntos_centrales_modelo': 'Sí',
     'asuntos_centrales_tipo': 'Cobro de pension garantizada universal ',
     'asuntos_centrales_tipo_line': '<p>Asuntos centrales para la vida: Cobro de pension garantizada universal </p>',
     'estrategias_mitigaciones_modelo': 'Se realizó una evaluación de impacto al inicio del proyecto, identificando que se tendria riesgos bajos al implementar el modelo. ',
     'riesgos_uso_modelo': '<p><strong>Riesgos del modelo</strong>: Que no se contacte a una persona que lo necesita, si es que no se cuenta con los datos de contactabilidad </p>',
     'casos_uso_conocidos': 'No ',
     'otra_consideracion': '',
     'estrategias_mitigaciones_modelo_line': '<p><strong>Estrategias de mitigación de riesgos</strong>: Se realizó una evaluación de impacto al inicio del proyecto, identificando que se tendria riesgos bajos al implementar el modelo. </p>',
     'casos_uso_conocidos_line': '<p><strong>Casos de uso problemáticos</strong>: No </p>',
     'otra_consideracion_line': '',
     'prueba_adicional': 'No',
     'grupo_relevante': 'No',
     'recomendaciones_adicionales': 'Se recomienda realizar este proceso en forma bimensual, ya que se obtendrian resultados similares a hacerlo de forma mensual, pero se requiere la mitad del esfuerzo.',
     'caracteristicas_ideales': 'Base de datos con atributos de identificación de las personas como: Edad, Genero, Estado Civil, Estado Vital y Nacionalidad, atributos de ubicación geografica como: Comuna donde vive, Urbanidad de Comuna y Region y atributos del comportamiento pasado de cobro: Forma de Pago, Pagos sin cobrar, Monto acumulado sin cobrar y Si cobro el mes pasado\n',
     'prueba_adicional_line': '<p><strong>Pruebas adicionales</strong>: No</p>',
     'grupo_relevante_line': '<p><strong>Grupos relevantes no representados</strong>: No</p>',
     'TA_reclamacion': 'No',
     'TA_via_reclamacion': None,
     'TA_reclamacion_visible': False,
     'year': '2024',
     'elaboration_date': 'Marzo de 2024'
    }