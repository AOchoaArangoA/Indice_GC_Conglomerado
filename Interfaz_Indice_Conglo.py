# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 15:36:30 2021

@author: Administrador
"""

import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from io import BytesIO

def EnviarExcel_total(df): 
    salida = BytesIO()
    writer = pd.ExcelWriter(salida, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Prueba_Índice')
    writer.save()
    processed_dta = salida.getvalue()
    return processed_dta

def get_table_total(df):     
    val = EnviarExcel_total(df)
    b64 = base64.b64encode(val)
    href = f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="Índice_AOA.xlsx">Descargar Información Índices Individuales y Agregados</a>'
    return href



st.image('Gob_Ant2.png', caption = 'Imagen Goberanción de Antioquia', width =700)
st.title('Índice de Gobierno Corporativo de la Gobernación de Antioquia')

st.markdown("""
Esta aplicación posee la información y la metodología correspondiente a la formulación y construcción del índice de Gobierno Corporativo para las 24 entidades que comprender el Conglomerado.

 **Descripción: ** Esta aplicación trata de implementar metodologías cualitativas para la evaluación y seguimiento de las buenas prácticas de Gobierno Corporativo. La metodología cualitativa trata de obtener información relevante de expertos en el tema, y que el mismo tiempo saben que aspectos son más relevantes para los objetivos de la Gobernación.
Por otro lado, la metodología cuantitativa utiliza herramientas de "DEA" para la creación de índices compuestos. Para implementar la metodología 'BOD' se utiliza el lenguaje de Programación R y el Código implementado es el siguiente.

            """)
            
st.markdown('#### Codigo de "Benefit of Doubt" en R')
st.code('''library(Compind)
    bod <- function(data){
    data_norm = normalise_ci(data,indic_col = c(1:6) ,c('POS', 'POS', 'POS',
                                                       'POS', 'POS', 'POS'),
                           method = 1, z.mean = 100, z.std = 10)
    CI <- ci_bod_constr(data_norm$ci_norm,up_w = 1, low_w = 0.15)
    l = data.frame(CI$ci_bod_constr_weights)
  
    return(l)
    }''', language="R")

st.markdown('''
            #### Pasos a Seguir: 
            * Ingresar los valores obtenidos por la encuesta en la casilla que se encuentra a la izquierda
            * Asignar las ponderaciones y el número de preguntas correspondientes a cada dimensión. Nota: * Si los ponderaciones no suman 1, no se realizara la agregación por una suma ponderada, sino, por un promedio simple *
            * Observar la información y las graficas
            * Si se requiere, se puede descargar la información
''')
st.sidebar.header('Información para la metodología Cualitativa ')


dicc = st.sidebar.file_uploader('Ingresa el docuemnto en .xlsx')

if dicc is not None:
    try:
        df = pd.read_excel(dicc)
    except:
        st.write('Se ingreso un docuemnto pero no es un archivo con extension .xlsx')
else: 
    st.write('No se ingreso la informacion correspondiente')
    
if st.button('Observar DataFrame y Las ponderaciones'):
    try:
         st.dataframe(df)
    except:
        st.warning('Aun no se ha ingresa la informacion correspondiente')

st.sidebar.header('Informacion sobre las ponderaciones')


def ponderaciones(): 
    pon_d1 = st.sidebar.slider('Dimension Trasnparencia', 0.0, 1.0, 0.2, key = 1)
    pon_d2 = st.sidebar.slider('Dimension Arquitectura de Control',0.0, 1.0, 0.2, key = 2)
    pon_d3 = st.sidebar.slider('Dimension Junta Directiva-Conflictos de Interés',0.0, 1.0, 0.2, key = 3)
    pon_d4 = st.sidebar.slider('Dimension Marco de Actuación y ASG',0.0, 1.0, 0.2, key = 4)
    pon_d5 = st.sidebar.slider('Dimension Propiedad y Accionistas', 0.0, 1.0, 0.1, key = 5)
    pon_d6 = st.sidebar.slider('Dimension Partes Interesadas', 0.0, 1.0, 0.1, key = 6)
    lista = np.array([pon_d1, pon_d2, pon_d3, pon_d4, pon_d5, pon_d6])
    if lista.sum() > 1 or lista.sum() < 1:
        st.sidebar.error('La suma de las ponderaciones debe dar 1, de lo contrario todas las ponderaciones seran iguales a 1 y se realizara un promedio simple')
        lista = np.array([1,1,1,1,1,1])
        return lista
    elif lista.sum()== 1: 
        return lista
        
try: 
    dicc = pd.DataFrame(dicc)

##############
#Creación de los df separados
##############
    pon = np.array(ponderaciones())
except: 
    pass

try:  
    entidades= df.iloc[:,0] #Esta parte obtiene la información de las entidades. Para este caso se debe tener el df bien especificado  
    lim_d1 = st.number_input('Ingresar el numero de preguntas de la Dimension 1', min_value=0, max_value=99, value = 5)
    dimension1 = df.iloc[:,:4]
    dimension1['Total1'] = dimension1.sum(axis =1)/lim_d1
    df1 = dimension1['Total1']

    lim_d2 = st.number_input('Ingresa el numero de preguntas de la Dimension 2', min_value=0, max_value=99, value =5)
    dimension2 = df.iloc[:,5:10]
    dimension2['Total1'] = dimension2.sum(axis =1)/lim_d2
    df2 = dimension2['Total1']

    lim_d3 = st.number_input('Ingresa el numero de preguntas de la Dimension 3', min_value=0, max_value=99, value = 5)
    dimension3 = df.iloc[:,10:15]
    dimension3['Total1'] = dimension3.sum(axis =1)/lim_d3
    df3 = dimension3['Total1']

    lim_d4 = st.number_input('Ingresa el numero de preguntas de la Dimension 4', min_value=0, max_value=99, value = 5)
    dimension4 = df.iloc[:,15:20]
    dimension4['Total1'] = dimension4.sum(axis =1)/lim_d4
    df4 = dimension4['Total1']

    lim_d5 = st.number_input('Ingresa el numero de preguntas de la Dimension 5', min_value=0, max_value=99, value = 5)
    dimension5 = df.iloc[:,20:25]
    dimension5['Total1'] = dimension5.sum(axis =1)/lim_d5
    df5 = dimension5['Total1']

    lim_d6 = st.number_input('Ingresa el numero de preguntas de la Dimension 6', min_value=0, max_value=99, value = 8)
    dimension6 = df.iloc[:,25:]
    dimension6['Total1'] = dimension6.sum(axis =1)/lim_d6
    df6 = dimension6['Total1']
except: 
     pass

try:
    total= pd.concat([entidades,df1,df2,df3,df4,df5,df6], axis = 1) 
    total.columns = ['Nombre Entidad','Partes Interesadas', 'Marco de Actuación','Transparencia', 'Junta Directiva', 'Propiedad y Accionistas', 'Arquitectura de Control']
except: 
    pass
try:
 if pon[0] == 1: 
    total['Indice_pon'] = (total['Partes Interesadas']*pon[0] + total['Marco de Actuación']*pon[1] + total['Transparencia']*pon[2]+total['Junta Directiva']*pon[3] + total['Propiedad y Accionistas']*pon[4]+total['Arquitectura de Control']*pon[5])/6
 else:
    total['Indice_pon'] = (total['Partes Interesadas']*pon[0] + total['Marco de Actuación']*pon[1] + total['Transparencia']*pon[2]+total['Junta Directiva']*pon[3] + total['Propiedad y Accionistas']*pon[4]+total['Arquitectura de Control']*pon[5])
except: 
    pass


if st.button('Mirar info'):
    try: 
        st.markdown('### Ponderaciónes')
        st.write(pd.DataFrame(pon, columns =['Ponderaciones']))
        st.markdown('### Informacion Procesada')
        st.write(total)
        st.markdown('### Nombre de la Entidad y el índice agregado')
        st.write(total[['Nombre Entidad', 'Indice_pon']])
    except:
        st.warning('No se ha ingresado la información correcta')

st.markdown('''
            ## Presentación Grafica
            En este apartado se muestran los resultados de los indicadores individuales y el índice agregado''')
try: 
    plt.figure(figsize=(10,50))
    plot =  sns.catplot(data = total,
                         orient="h")
    plot.despine(left = True)
    plt.xticks(rotation = 45)
    plt.title('Figura sobre las entidades')
    #plt.ylabel('Dimensiones Gobierno Corporativo')
    plt.xlabel('Puntaje [0-1]')
    #plt.legend()
    st.pyplot(plot)
except: 
    st.warning('Para observar la grafica se debe tener toda la información ingresada')


# try:
#     plt.figure(figsize = (10, 50))
#     plot2 = sns.lineplot(data = total.T);
#     st.pyplot(plot2)    
    
    
    
#     # sns.set_theme(style="whitegrid")

#     # rs = np.random.RandomState(365)
#     # values = rs.randn(365, 4).cumsum(axis=0)
#     # dates = pd.date_range("1 1 2016", periods=365, freq="D")
#     # data = pd.DataFrame(values, dates, columns=["A", "B", "C", "D"])
#     # data = data.rolling(7).mean()

#     # plot2 = sns.lineplot(data=data, palette="tab10", linewidth=2.5)
#     # # st.show(plot2)
    
# except: 
#     st.warning('La segunda Grafica tiene problemas')
    
try:
  st.markdown(get_table_total(total), unsafe_allow_html=True)
except: 
    st.warning('Para descargar la información primero se debe realizar todos los pasos')



# st.write(type(lim_d1))
# st.write('El numero ingresado es: ', lim_d1)




