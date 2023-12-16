from openai import OpenAI

import streamlit as st

import base64
from PIL import Image
from io import BytesIO

import re
import time


def encode_image(image_file):
    """Encode image to base64 string."""
    if isinstance(image_file, str):
        image = Image.open(image_file)
    else:
        image = Image.open(image_file)
    
    # Convert RGBA images to RGB
    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")
    
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")
    
def api_on_change():
    api_key = st.session_state.input_key
    col3 = st.session_state.col3
    success_message = st.session_state.success_message

    with col3:
        if re.match(r"sk-[a-zA-Z0-9]+", api_key):
            st.session_state.api_key = api_key
            success_message.success("Clave cargada!")
            try:
                st.session_state.chat = OpenAI(api_key=st.session_state.api_key)
            except Exception as e:
                success_message.error(f"Error: {e}")

        elif api_key == "contraseña":
            st.session_state.api_key = st.session_state.secret_developer_key
            success_message.success("Clave gratuita cargada! (solo 1 uso)")
            # Inicializar cliente de OpenAI
            try:
                st.session_state.chat = OpenAI(api_key=st.session_state.api_key)
            except Exception as e:
                success_message.error(f"Error: {e}")

        elif api_key == "":
            success_message.error("No dejes el campo vacío bobo")
        else:
            success_message.error("Este tipo de clave es inválida!")

        time.sleep(1)


def main():

    # PAGE CONFIG
    st.set_page_config(page_title="DESCRIPTOR DE IMÁGENES", page_icon=":robot_face:", layout="centered")
    st.title("DESCRIPTOR DE IMÁGENES")
    st.markdown("---")
    st.subheader("Funcionamiento")
    st.markdown("1) Introduce la API KEY de OpenAI (si no tienes, escribe 'contraseña', de esta forma usarás la clave gratuita de Dieguito, pero solo puedes usarla 1 vez)"
            "\n\n2) Sube una imagen"
            "\n\n3) Si quieres, añade instrucciones personalizadas, esto no es necesario, por defecto se describirá la imagen."
            "\n\n4) Pulsa el botón de analizar imagen y espera a que se genere la descripción.\n\n\n")

    st.markdown("---")

    ################## API KEY ##################

    if "usos_dev_key" not in st.session_state:
        st.session_state.usos_dev_key = 1

    if "api_key" not in st.session_state:
        st.session_state.api_key = None

    if "secret_developer_key" not in st.session_state:
        st.session_state.secret_developer_key = st.secrets.OPENAI_API_KEY

    if "chat" not in st.session_state:
        st.session_state.chat = None

    if "input_key" not in st.session_state:
        st.session_state.input_key = None

    if "success_message" not in st.session_state:
        st.session_state.success_message = st.success.empty()


    # Layout

    col1, col2, col3 = st.columns([3, 2, 2])


    with col1:
        st.text_input("API KEY", 
                        placeholder="Introduce la API key", 
                        type="password",
                        on_change=api_on_change,
                        key="input_key")
    
    with col2:
        # Move the botton down a bit
        st.markdown("""<style>.css-1aumxhk {margin-top: 3rem;}</style>""", unsafe_allow_html=True)
        st.markdown("""<style>.css-1aumxhk {margin-top: 2rem;}</style>""", unsafe_allow_html=True)
        boton_key = st.button("Guardar API KEY")
        if boton_key:
            api_on_change()

    st.markdown("---")

    with col3:
        if "col3" not in st.session_state:
            st.session_state.col3 = col3

        st.markdown("""<style>.css-1aumxhk {margin-top: 3rem;}</style>""", unsafe_allow_html=True)
        st.markdown("""<style>.css-1aumxhk {margin-top: 2rem;}</style>""", unsafe_allow_html=True)
        # st.session_state.success_message.warning("Debes introducir una clave.")


    ################## IMAGE ##################
                
    uploaded_file = st.file_uploader("Sube una fotito", type=["png", "jpg", "jpeg"]) 
    if uploaded_file:
        # DISPLAY IMAGE
        st.image(uploaded_file, width=250)
    
    st.markdown("---")



    ################## EXTRA PROMPT ##################

    show_details = st.toggle("Agregar instrucciones?", value=False)
    if show_details:
        # Texto de detalles
        additional_details = st.text_area(
            "Añade conexto adicional: ",
            disabled=not show_details,
        )
    
    st.markdown("---")


    ################## SEND BUTTON ##################

    analyze_button = st.button("Analizar imagen")

    if uploaded_file and st.session_state['api_key'] != None and analyze_button and st.session_state['chat'] and st.session_state["usos_dev_key"] > 0:
        print("Analizando imagen...")

        # Restar uso de la clave
        st.session_state["usos_dev_key"] -= 1
        
        # Texto de carga
        with st.spinner("Analizando imagen..."):

            # Encode image
            base64_image = encode_image(uploaded_file)

            # Prompt optimizado + detalles extra
            prompt_text = (
                "Eres un analizador de imágenes."
                "Tu tarea es analizar la imagen en gran detalle."
                "Presenta tu análisis markdown, no uses los carácteres: ``` para rodear tu texto."
            )        

            if show_details and additional_details:
                prompt_text += (
                    f'\n\nContexto adicional:\n{additional_details}'
                )

            # Generar payload
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt_text},
                        {
                            "type": "image_url",
                            "image_url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    ],
                }
            ]

            # Hacer solicitud a los servidores de OpenAI
            try:
                # Sin stream

                # response = chat.chat.completions.create(
                #     model='gpt-4-vision-preview', messages=messages, max_tokens=100, stream=False
                # )

                # Con stream
                full_response = ""
                message_placeholder = st.empty()
                for completion in st.session_state["chat"].chat.completions.create(
                    model='gpt-4-vision-preview', messages=messages, max_tokens=1200, stream=True
                ):
                    # Hay contenido?
                    if completion.choices[0].delta.content is not None:
                        full_response += completion.choices[0].delta.content
                        message_placeholder.markdown(full_response + "  ")
                    
                # Mensaje final cuando se acaba el stream
                message_placeholder.markdown(full_response)

                # Poner respuesta en la app
                # st.write(completion.choices[0].messages.content)

            except Exception as e:
                st.error(f"Error: {e}")
    else:
        if not uploaded_file and analyze_button:
            st.warning("Sube una imagen!")    
        elif not st.session_state["api_key"] and analyze_button:
            st.warning("Necesitas una API KEY de OpenAI para usar esta app!")
        elif st.session_state["usos_dev_key"] <= 0 and analyze_button:
            st.warning("Has usado la clave gratuita de Dieguito demasiadas veces!")
        elif analyze_button:
            st.warning("Error")

            

if __name__ == "__main__":
    main()