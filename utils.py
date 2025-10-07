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
        id_vars=['ID','No. Ente Cliente','No. Identificación Cliente','Tipo Producto','Nombre Completo Ejecutivo','No.Usuario Responsable'],                        # Columna que se repetirá
        value_vars=columnas_a_unificar,      # Columnas a convertir en filas
        value_name='Operacion'              # Nombre de la nueva columna con los valores
    )

    melted = melted.drop('variable',axis=1)

    return melted

def dejar_solo_numeros(data, column):
    df = data.copy()
    df[column]=df[column].str.replace(r'\D', '', regex=True)
    return df
