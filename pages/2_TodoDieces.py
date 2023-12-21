import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import time

def main():

    # Emoji of a camera: 
    ### PAGE CONFIG ###

    st.set_page_config(page_title="2_TodoDieces", 
                       layout="centered")
    
    ############## SIDEBAR ##############

    st.sidebar.title("Menú")
    st.sidebar.markdown("Aquí puedes encontrar información sobre el proyecto y el autor.")
    st.sidebar.markdown("---")
    st.sidebar.subheader("Sobre el proyecto")
    

    ############## MAIN ##############
    
    st.title("UJI TODO DIECES: LA WEB OFICIAL")

    ############## GOOGLE SHEETS ##############

    usar_nube = False       # TODO: Desactivar para no usar recursos de la nube

    if usar_nube:
        # AJUSTES INICIALES

        scope = ["https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive"]

        credentials = ServiceAccountCredentials.from_json_keyfile_name('/home/diego/Documents/A-PARA/3-Resources/Programming_projects/1PROJECTS/Streamlit-Chatbot-Interface/.streamlit/gs_credentials.json', scope)

        client = gspread.authorize(credentials)


        # ACTUALIZAR DATOS LOCALES   (API)

        sheet = client.open("TodoDieces").sheet1

        data = sheet.get_all_values()

        if len(data) > 0:
            headers = data[0]
            rows = data[1:]

            df = pd.DataFrame(rows, columns=headers)
            df.to_csv('/mount/src/chatbot_diego/data.csv', index=False)
            print("File created successfully.")
        else:
            print("No data available in the sheet.")



    # CARGAR DATOS LOCALES EN TABLA DE STREAMLIT
    
    with st.expander("Ver tabla de notas"):

        df = pd.read_csv('/mount/src/chatbot_diego/data.csv')
        st.dataframe(df)


    # DIAGRAMA DE BARRAS

    with st.expander("Ver diagrama de barras"):

        st.info("Función en construcción.")

        data22 = {
        'Diego': [7.0, 10.0, 8.75, 10.0],
        'Ismael': [10.0, 0.0, 10.0, 0.0],
        'Guillem': [10.0, 10.0, 10.0, 5.0],
        'David': [10.0, 10.0, 10.0, 10.0],
        'Nicolás': [6.0, 10.0, 10.0, 5.0]
        }
        df22 = pd.DataFrame(data22)

        st.bar_chart(df22)
        st.line_chart(df22)
        st.scatter_chart(df22)
        st.area_chart(df22)



    # CREAR NUEVA AVALUACIÓN

    asignaturas = ["Programación", "Estadística", "Matemáticas", "Ética", "Xarxes"]
    pruebas = ["Parcial", "Laboratorio/Cuestionario", "Final"]


    sec_nuevo_test = st.expander("Crear nueva avaluación?")

    # TODO: Boton que actualice todo

    with sec_nuevo_test:

        # ASIGNATURA, PRUEBA Y FECHA

        columnas_prueba = st.columns(2)
        with columnas_prueba[0]:
            asignatura = st.selectbox("Asignatura:", asignaturas, index=None, placeholder="Escoge una asignatura")            # df["ASIGNATURA"].unique()       para coger del excel
        with columnas_prueba[1]: 
            prueba = st.selectbox("Prueba:", pruebas, index=None, placeholder="Escoge un tipo de prueba")
        fecha = st.date_input("Fecha: ")

        # NOTAS

        for col_person, col in zip(range(0, 5), st.columns(5)):
            col.text_input("Nota de: " + df.columns[col_person+3])
            
        # CREAR
            
        boton_nuevo_test = st.button("Crear test")  

        if boton_nuevo_test:
            
            if not prueba or not fecha or not asignatura:
                texto_warning = "Debes introducir los siguientes datos:"
                if not asignatura:
                    texto_warning = texto_warning + "\n- Asignatura"
                if not prueba:
                    texto_warning = texto_warning + "\n- Prueba"
                if not fecha:
                    texto_warning = texto_warning + "\n- Fecha"
                st.warning(texto_warning)

            else:
                with st.spinner("Creando test..."):
                    time.sleep(1)
                # Agregamos una nueva fila al final del dataframe
                st.info("Función en construcción.")





    # ACTUALIZAR NOTAS FALTANTES
        
    notas_faltantes = st.expander("Actualizar notas faltantes?", expanded=True)
    si_notas_faltantes = notas_faltantes.radio("Si/No", ("Si", "No"), index=1)
    if si_notas_faltantes == "Si":
        with notas_faltantes:
            st.info("Función en construcción.")
            for col_person in range(3, len(df.columns)):
                st.markdown("**Notas faltantes de " + df.columns[col_person] + ":**")
                for fila_nota in range(0, len(df)):
                    if pd.isna(df.iloc[fila_nota, col_person]):
                        st.text_input("\n" + df.iloc[fila_nota, 0] + " de la asignatura " + df.iloc[fila_nota, 1] + " el dia " + df.iloc[fila_nota, 2] + ": ", key=str(fila_nota) + str(col_person))

     
    # ELIMINAR TESTS ANTIGUOS # TODO

    eliminar_tests = st.expander("Eliminar tests antiguos?")

    with eliminar_tests:
        st.info("Función en construcción.")
        # st.markdown("Selecciona los tests que quieres eliminar:")
        # for fila in range(0, len(df)):
        #     st.checkbox("Eliminar " + df.iloc[fila, 0] + " de la asignatura " + df.iloc[fila, 1] + " el dia " + df.iloc[fila, 2] + "?")




    # ACTUALIZAR NUBE
    
    if usar_nube:
        button_nube = st.button("Actualizar datos")
        if button_nube:
            with st.spinner("Actualizando datos..."):
                df = pd.read_csv('/mount/src/chatbot_diego/data.csv')

                df = df.astype(str)  # Convert float values to strings

                df.columns.values.tolist()
                df.values.tolist()

                sheet.update([df.columns.values.tolist()] + df.values.tolist())

            st.success("Datos actualizados correctamente.")






if __name__ == "__main__":
    main()