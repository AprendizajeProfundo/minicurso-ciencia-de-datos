# Copyright 2022 Aprendizaje Profundo, All rights reserved.
#
# Licensed under the MIT License;
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://opensource.org/licenses/MIT
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# Developed by Alvaro Mauricio Montenegro Reyes and Daniel Mauricio Montenegro Reyes
# ==================================================================================
def limpiar_textos(textos):
    #==========================Librerías==========================
    import pandas as pd
    import datetime
    import num2words
    import re
    #==========================Input Datos==========================
    # Si es dataframe, no cambiar nada
    if isinstance(textos, pd.DataFrame):
        datos = textos.copy()
    # Si es Serie, formar dataframe
    elif isinstance(textos, pd.Series):
        datos = pd.DataFrame(textos,columns=[textos.name])
    # Si no es nada (lista de textos), generar un dataframe
    else:
        datos = pd.DataFrame([])
        datos['Texto'] = textos
        #Transformar todo a string
        datos['Texto'] = datos['Texto'].astype(str)
    
    # Nombres de las columnas
    textos_col_name               = datos.columns.values[0]
    textos_col_name_limpio        = f'{textos_col_name}_limpio'
    #print(textos_col_name)
    #==========================Limpieza General==========================
    print('Limpiando Texto...',end='    ')
    t0 = datetime.datetime.now()
    # Poner en minúsculas
    datos[textos_col_name_limpio] = datos[textos_col_name].str.lower()
    # Quitar links
    datos[textos_col_name_limpio] = datos[textos_col_name_limpio].str.replace('https?:\/\/.*[\r\n]*',' ',regex=True)
    # Quitar Puntuaciones, etc...
    datos[textos_col_name_limpio] = datos[textos_col_name_limpio].str.replace('[^\w\s\.\,]',' ',regex=True)
    # Quitar dígitos (O será mejor transformarlos a texto??)
    #datos[textos_col_name_limpio] = datos[textos_col_name_limpio].replace('\d+','',regex=True)
    ###### Se transforman digitos a texto para ver cómo actúa el modelo. ###########
    datos[textos_col_name_limpio] = datos[textos_col_name_limpio].apply(lambda x: re.sub('\d+',lambda y: '_'+num2words.num2words(int(y.group(0))),x))
    # Quitar espacios extra
    datos[textos_col_name_limpio] = datos[textos_col_name_limpio].replace('\s\s+',' ',regex=True)
    # Quitar espacio al inicio y al final
    datos[textos_col_name_limpio] = datos[textos_col_name_limpio].str.strip()
    t1 = datetime.datetime.now()
    print('Tiempo de Procesamiento: {}'.format(t1 - t0))
    return datos
    