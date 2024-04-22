# Herramienta de Transparencia del modelo - UAI

Este es el repositorio de la herramienta de transparencia de modelos para documentar el funcionamiento sobre el apoyo en la toma de decisiones de los modelos de decisiones automatizadas que se basan en IA, desarrollada por el equipo del proyecto de algoritmos éticos responsables del GobLab en la Universidad Adolfo Ibáñez.

## Descripción

Esta herramienta puede ser utilizada por cualquier persona, equipo u organización que desee transparentar el uso de sus modelos. La herramienta permite, por medio de una interfáz gráfica, exponer un cuestionario para responder preguntas sobre el modelo, los datos y las decisiones que se toman con el modelo. Además, la herramienta permite generar un reporte en formato PDF con las respuestas del cuestionario. renderizadas en formato de `model card`.

## Instalación

Para instalar la herramienta, se debe clonar el repositorio y luego instalar las dependencias necesarias. Para clonar el repositorio, se debe ejecutar el siguiente comando:

```bash
git clone 

```

Luego, se debe crear un ambiente virtual en python e instalar las dependencias necesarias. Para ello, se debe ejecutar el siguiente comando:

```bash
cd Herrramienta_transparencia_del_modelo
python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

Finalmente, se debe ejecutar el siguiente comando para iniciar la herramienta:

```bash
streamlit run home.py
```

>[!NOTE]
>
>Esta herramienta no comparte tus datos, ya que todo el procesamiento se realiza en tu computadora y no se envía a ningún servidor externo, pero si almacenamos el feedback que nos des para mejorar su funcionamiento.


## Uso de la herramienta

Para usar la herramienta, debes responder cada una de las preguntas que se presentan en la interfaz gráfica. Luego, debes hacer clic en el botón `Generar model card` para obtener el reporte en formato PDF.

>[!NOTE]
>
>La herramienta no generá el informe si no respondes las preguntas marcadas con un asterisco (*) ya que son obligatorias.


Finalmente, una vez completadas las preguntas obligatorias, se debe hacer clic en el botón `Generar model card` para obtener el reporte en formato PDF y poder descargarlo.

>[!NOTE]
>
>Para realizar el model card se recomienda tener a la mano información sobre el modelo, los datos y las decisiones que se toman con el modelo. Considere la necesidad de un experto técnico del proyecto para responder las preguntas de manera correcta.

## Agradecimientos

ANID + Subdirección de Investigación Aplicada/Concurso IDeA I+D 2023 + ID23I10357
