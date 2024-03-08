import streamlit as st
from render_pdf import create_pdf

SHORT_STRING = 100
LONG_STRING = 1000

title = "Ficha de transparencia de los datos 🧠 V.0.0.1"
st.markdown(f"<h1 style='text-align: center; color: black;'>{title}</h1>", unsafe_allow_html=True)
st.sidebar.text_area("Dame tu feedback",value="Escribe aquí tu feedback",max_chars=LONG_STRING)

st.write("Bienvenido a la herramienta para crear una ficha de transparencia del modelo. para esto vamos a requerir algunos datos de tu modelo y de tu dataset.")
st.write("Estás listo? 🔜")

tab1, tab2 = st.tabs(["Metadata 📄", "Sobre los datos 📊"])

with tab1:

    st.header("Metadata")

    dataset_title = st.text_input("1. Título del conjunto de datos",max_chars=SHORT_STRING)
    dataset_description = st.text_area("2. Proporcona un breve resumen del conjunto de datos", max_chars=LONG_STRING)
    dataset_resume = st.text_area("3. Resume este conjunto de datos en unas pocas oraciones, incluyendo el propósito y el contenido.", max_chars=LONG_STRING)
    dataset_owner = st.text_input("4. ¿Quién es dueño del conjunto de datos?",value="Declara tanto la organización/empresa como el individuo si procede.",max_chars=SHORT_STRING)

    dataset_creator = st.text_input("5. ¿Quién creó el conjunto de datos?",value="Declara tanto la organización/empresa como el individuo si procede.",max_chars=SHORT_STRING)
    dataset_mantainer = st.text_input("6. ¿Quién mantiene actualmente el conjunto de datos?",value="Declara tanto la organización/empresa como el individuo si procede.",max_chars=SHORT_STRING)
    dataset_availability = st.radio("7. ¿El conjunto de datos está disponible públicamente?",options=["Sí","No"])
    dateset_license = None

    if dataset_availability == "Sí":
        dateset_license = st.text_input("7.1. ¿Qué licencia tiene el conjunto de datos?",value="Si es posible, proporciona un enlace a la descripción de la licencia.",max_chars=SHORT_STRING)

    dataset_porpuse = st.text_area("8. ¿Con qué propósito se creó el conjunto de datos? ¿Había una tarea específica en mente? ¿Había una brecha específica que cubrir? ",value="Proporciona una descripción",max_chars=LONG_STRING)
    dataset_invester = st.text_input("9. ¿Quién financió la creación del conjunto de datos?  Si hay una subvención asociada, proporciona el nombre del otorgante y el nombre y número de la subvención.",max_chars=SHORT_STRING)

with tab2:

    st.header("Sobre los datos")

    dataset_format = st.selectbox("10. ¿Cuál es el formato del conjunto de datos?",options=["csv", "txt", "xml", "json", "shp", "dbf", "geotiff", "netcdf", "sas", "sav", "tiff", "pdf", "Otro"])
    other_format = None
    if dataset_format == "Otro":
        other_format = st.text_input("10.1. ¿Cuál es el formato del conjunto de datos?",max_chars=SHORT_STRING)

    dataset_instances = st.number_input("11. ¿Cuántas instancias (filas, ejemplos) hay en el conjunto de datos?. Por ejemplo: 10,000 puntos de datos, 200 imágenes, etc.",min_value=0, max_value=1000000000, value=0, step=1)
    
    dataset_recopilation_on_going = st.radio("¿La recopilación de datos aún está en curso?",options=["Sí","No"])
    if dataset_recopilation_on_going == "Sí":
        st.write("12. ¿En qué período de tiempo se recopilaron los datos? Por ejemplo, un conjunto de datos podría publicarse en 2022 pero haberse recopilado entre 2005 y 2010.")
        dataset_recopilation_date_begin = st.date_input("Inicio",value=None)
        dataset_recopilation_date_end = "En curso"
    else:
        st.write("12. ¿En qué período de tiempo se recopilaron los datos? Por ejemplo, un conjunto de datos podría publicarse en 2022 pero haberse recopilado entre 2005 y 2010.")
        col1, col2 = st.columns(2)
        with col1:
            dataset_recopilation_date_begin = st.date_input("Inicio",format="YYYY-MM-DD",value="today")
        with col2:
            dataset_recopilation_date_end = st.date_input("Fin",format="YYYY-MM-DD",value="today")
        
    dataset_data_adquisition = st.text_area("13. ¿Cómo se adquirió la data asociada con cada instancia?",value="¿Los datos fueron directamente observables (por ejemplo, texto sin procesar, reportados por sujetos (por ejemplo, respuestas de encuestas) o inferidos/derivados indirectamente de otros datos (por ejemplo, estimaciones basadas en modelos para edad o idioma)? Si los datos fueron reportados por sujetos o inferidos/derivados indirectamente de otros datos, ¿se validaron/verificaron los datos? En caso afirmativo, describa cómo.",max_chars=LONG_STRING)
    dataset_data_adquisition_tech = st.text_area("14. ¿Qué herramientas, servicios o tecnologías se utilizaron para recopilar los datos?",value="Si hubo varios pasos, por favor inclúyalos todos. Las herramientas y servicios podrían incluir: API de software, aparatos o sensores de hardware, aplicaciones, visitas puerta a puerta, etc. También indique cómo se utilizaron.",max_chars=LONG_STRING)
    dataset_sampling_method = st.text_area("15. Si el conjunto de datos es una muestra de un conjunto más grande, ¿cuál fue la estrategia de muestreo? ",value="Por ejemplo, determinista, probabilístico con probabilidades de muestreo específicas.",max_chars=LONG_STRING)
    dataset_quality = st.radio("16. ¿Los datos han sido revisados en cuanto a calidad técnica?  Por ejemplo, verificación de consistencia en los tipos de datos, brechas en la completitud de los datos, etc. ",options=["Sí","No"],index=1)
    if dataset_quality == "Sí":
        dataset_quality_description = st.text_area("Proporciona más información",max_chars=LONG_STRING)
    else:
        dataset_quality_description = ""
    dataset_ethic_revision = st.radio("17. ¿Se llevaron a cabo procesos de revisión ética? Por ejemplo, aprobación de un comité de revisión institucional, proceso interno o de revisión ética de terceros, un informe sobre el impacto potencial en los sujetos de datos, etc. ",options=["Sí","No"],index=1)
    if dataset_ethic_revision == "Sí":
        dataset_ethic_revision_description = st.text_area("Amplía tu respuesta",max_chars=LONG_STRING)
    else:
        dataset_ethic_revision_description = ""
    dataset_other_fonts = st.radio("18. ¿El conjunto de datos incluye información de otras fuentes? Otras fuentes pueden incluir: otros conjuntos de datos, artículos de investigación, tweets, sitios web, etc.  ",options=["Sí","No"],index=1)
    if dataset_other_fonts == "Sí":
        ext_resources = st.radio("18.1. ¿enlaza o depende de recursos externos?, ",options=["Sí","No"],index=1)
        if ext_resources == "Sí":
            ext_resources_persistence = st.radio("I.¿Hay garantías de que existirán y permanecerán constantes con el tiempo?",options=["Sí","No"],index=1)
            if ext_resources_persistence == "Sí":
                ext_resources_persistence_description = st.text_area("Amplía tu respuesta",max_chars=SHORT_STRING)
            else:
                ext_resources_persistence_description = ""

            ext_resources_archive_versions = st.radio("II.¿Hay versiones archivadas oficiales del conjunto de datos completo? (es decir, que incluyan los recursos externos tal como existían en el momento en que se creó el conjunto de datos)",options=["Sí","No"],index=1)
            if ext_resources_archive_versions == "Sí":
                ext_resources_archive_versions_description = st.text_area("Amplía tu respuesta por favor",max_chars=SHORT_STRING)
            else:
                ext_resources_archive_versions_description = ""
            
            ext_resources_restrictions = st.radio("III.¿Hay restricciones (por ejemplo, licencias, tarifas) asociadas con alguno de los recursos externos que puedan aplicarse a un consumidor de datos?",options=["Sí","No"],index=1)
            if ext_resources_restrictions == "Sí":
                ext_resources_restrictions_description = st.text_area("Describa todos los recursos externos y cualquier restricción asociada con ellos y proporcione enlaces u otros puntos de acceso, según corresponda.",max_chars=SHORT_STRING)
            else:
                ext_resources_restrictions_description = ""
    else: 
        ext_resources = "No"
        ext_resources_persistence = ""
        ext_resources_persistence_description = ""
        ext_resources_archive_versions = ""
        ext_resources_archive_versions_description = ""
        ext_resources_restrictions = ""
        ext_resources_restrictions_description = ""
    
    dataset_data_confidentiality = st.radio("19. ¿El conjunto de datos contiene datos que podrían considerarse confidenciales? Por ejemplo, datos protegidos por privilegio legal o por confidencialidad médico-paciente, datos que incluyen el contenido de comunicaciones no públicas de individuos.",options=["Sí","No"],index=1)
    if dataset_data_confidentiality == "Sí":
        dataset_data_confidentiality_description = st.text_area("proporcione una descripción",max_chars=LONG_STRING)
    else:
        dataset_data_confidentiality_description = ""

    data = {
        "dataset_title": dataset_title,
        "dataset_description": dataset_description,
        "dataset_resume": dataset_resume,
        "dataset_owner": dataset_owner,
        "dataset_creator": dataset_creator,
        "dataset_mantainer": dataset_mantainer,
        "dataset_availability": dataset_availability,
        "dateset_license": dateset_license,
        "dataset_porpuse": dataset_porpuse,
        "dataset_invester": dataset_invester,
        "dataset_format": dataset_format,
        #"other_format": other_format,
        "dataset_instances": dataset_instances,
        "dataset_recopilation_on_going": dataset_recopilation_on_going,
        #"dataset_recopilation_date_begin": dataset_recopilation_date_begin,
        #"dataset_recopilation_date_end": dataset_recopilation_date_end,
        "dataset_data_adquisition": dataset_data_adquisition,
        "dataset_data_adquisition_tech": dataset_data_adquisition_tech,
        "dataset_sampling_method": dataset_sampling_method,
        "dataset_quality": dataset_quality,
        "dataset_quality_description": dataset_quality_description,
        "dataset_ethic_revision": dataset_ethic_revision,
        "dataset_ethic_revision_description": dataset_ethic_revision_description,
        "dataset_other_fonts": dataset_other_fonts,
        "ext_resources": ext_resources,
        "ext_resources_persistence": ext_resources_persistence,
        "ext_resources_persistence_description": ext_resources_persistence_description,
        "ext_resources_archive_versions": ext_resources_archive_versions,
        "ext_resources_archive_versions_description": ext_resources_archive_versions_description,
        "ext_resources_restrictions": ext_resources_restrictions,
        "ext_resources_restrictions_description": ext_resources_restrictions_description,
        "dataset_data_confidentiality": dataset_data_confidentiality,
        "dataset_data_confidentiality_description": dataset_data_confidentiality_description
    }


    # Create PDF
    pdf_file_path = create_pdf(data)

    # Offer the PDF for download
    with open(pdf_file_path, "rb") as file:
        st.download_button(
            label="Descargar Ficha PDF",
            data=file,
            file_name=pdf_file_path,
            mime="application/octet-stream"
        )


