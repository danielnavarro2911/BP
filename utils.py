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

def descargar_y_limpar(url,sheet,gs):
    gs.connect_with_spreadsheet(url)
    data=gs.get_data(sheet)

    data = data.iloc[:,[0, 7, 8, 14, 19, 20, 21]].drop(0).reset_index(drop=True)

    data=melt(data)
    data=data.dropna(subset='Operacion')
    data=data[data['Operacion']!='0']

    data=dejar_solo_numeros(data,'Operacion')

    return data
