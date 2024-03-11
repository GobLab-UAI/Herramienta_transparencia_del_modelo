import streamlit as st
from streamlit_webrtc import webrtc_streamer
import base64
from weasyprint import HTML

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
        particion = st.text_input("Partición (Entrenamiento, Validación, Test)")
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