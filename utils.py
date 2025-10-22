import pandas as pd

def melt(df):
    df.rename(columns={
        'No. Operación o Tarjeta 3 (En caso de no Aparecer en Listados)': 'No. Operacion o Tarjeta 3'
    }, inplace=True)

    #las columnas que quieres unificar
    columnas_a_unificar = [
        'No. Operación o Tarjeta',
        'No. Operación o Tarjeta 2',
        'No. Operacion o Tarjeta 3'
    ]

    
    melted= pd.melt(
        df,
        id_vars=['ID','No. Ente Cliente','No. Identificación Cliente','Tipo Producto'],                        # Columna que se repetirá
        value_vars=columnas_a_unificar,      # Columnas a convertir en filas
        value_name='Operacion'              # Nombre de la nueva columna con los valores
    )

    melted = melted.drop('variable',axis=1)

    return melted

def dejar_solo_numeros(data, column):
    df = data.copy()
    df[column]=df[column].str.replace(r'\D', '', regex=True)
    return df
def limpieza_palabras(series):
    tildes ={"á": "a","é": "e","í": "i","ó": "o","ú": "u"}
    series=series.map(lambda x : x.lower())
    series=series.map(lambda x : ''.join(tildes.get(c,c) for c in x))
    return series
#quitamos espacios y no aplica
def limpieza_operacion_palabras(data,column):

    df=data.copy()
    df[column]=df[column].str.replace('.','')
    df[column]=df[column].str.replace(' ','')
    df[column]=df[column].str.lower()
    df=df[df[column]!='noaplica']

    return df.reset_index(drop = True)
def limpieza_tipocredito_palabras(data,column):
    df=data.copy()
    df[column]=df[column].str.replace('con vc','')
    df[column]=df[column].str.strip()

    return df
#limpiamos los / de operaciones
def explode(data,column,divisor):

    df=data.copy()
    
    df[column]=df[column].str.split(divisor)
    df=df.explode(column)

    df[column]=df[column].str.strip()
    df=df[df[column]!='']

    return df.reset_index(drop=True)
def descargar_y_limpar(url,sheet,gs):
    gs.connect_with_spreadsheet(url)
    data=gs.get_data(sheet)

    data = data.iloc[:,[0, 7, 8, 14, 19, 20, 21]].drop(0).reset_index(drop=True)
    
    data=data.astype(str)

    data=melt(data)
    #data=data.dropna(subset='Operacion')
    #data=data[data['Operacion']!='0']
    
    

    data['Tipo Producto']=limpieza_palabras(data['Tipo Producto'])

    data=limpieza_operacion_palabras(data,'Operacion')

    data=limpieza_tipocredito_palabras(data,'Tipo Producto')

    for divisor in ['/',',','y','&','.']:
        data=explode(data,'Operacion',divisor)
        

    data=dejar_solo_numeros(data,'Operacion')

    #data=data[data['Operacion']!='']
    data['Operacion']=data['Operacion'].str.strip()
    data['Operacion']=data['Operacion'].map(lambda x : '' if x=='0' else x)

    data=data.drop_duplicates()

    return data
