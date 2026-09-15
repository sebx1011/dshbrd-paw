import pandas as pd
import numpy as np
from app.models.metrics import upsert_metrics
   


def import_csv(lambda_name, ruta_invocaciones, ruta_tasa_errores):
    df_invocaciones = pd.read_csv(ruta_invocaciones, skiprows=5, header=None, names=["Fecha y hora", "Cantidad de invocaciones"]) # Se cargan los csv de invocaciones y tasa de errores en dataframes de pandas
    df_tasa_errores = pd.read_csv(ruta_tasa_errores, skiprows=5, header=None, names=["Fecha y hora", "Errores","Tasa de exito"])



    df_tasa_errores_none = df_tasa_errores.replace({np.nan: None}) #limpieza de dataframe tasa_errores, reemplazando los valores NaN por None para poder eliminar la columna "Tasa de exito" sin perder datos importantes
    df_tasa_errores_limpio = df_tasa_errores_none.drop('Tasa de exito', axis=1) #se elimina la columna "Tasa de exito" del dataframe de tasa de errores, ya que no es necesaria para el análisis


    df_invocaciones_limpio = df_invocaciones.fillna(0)

    df_final = pd.merge(df_invocaciones_limpio, df_tasa_errores_limpio, on="Fecha y hora", how="outer")
    df_final["Fecha y hora"] = pd.to_datetime(df_final["Fecha y hora"], format="%Y/%m/%d %H:%M:%S")  # Se convierte la columna "Fecha y hora" a tipo datetime para poder realizar operaciones de fecha y hora

    for _index, row in df_final.iterrows():
        fecha = row["Fecha y hora"].date()  # Se obtiene la fecha de la columna "Fecha y hora" para poder insertarla en la base de datos
        invocaciones = int(row["Cantidad de invocaciones"]) if pd.notnull(row["Cantidad de invocaciones"]) else 0
        errores = int(row["Errores"]) if pd.notnull(row["Errores"]) else None
        upsert_metrics(lambda_name, fecha, invocaciones, errores)  # Se insertan los datos en la base de datos usando la función upsert_metrics



import_csv("episodios-generarDocumentosPreAdmision-prod", r"C:\Proyectos\Tablero PAW\dshbrd-paw\script_manual\csv\invocaciones\Invocaciones-generar_documento.csv", r"C:\Proyectos\Tablero PAW\dshbrd-paw\script_manual\csv\tasa_errores\tasa-errores_generar_documento.csv")
import_csv("episodios-firmarDocumentosPreAdmision-prod", r"C:\Proyectos\Tablero PAW\dshbrd-paw\script_manual\csv\invocaciones\Invocaciones-firmar_documento.csv", r"C:\Proyectos\Tablero PAW\dshbrd-paw\script_manual\csv\tasa_errores\tasa-errores_firmar_documento.csv")
import_csv("episodios-crearPreAdmisionHospitalizado-prod", r"C:\Proyectos\Tablero PAW\dshbrd-paw\script_manual\csv\invocaciones\Invocaciones-crear_preadmision.csv", r"C:\Proyectos\Tablero PAW\dshbrd-paw\script_manual\csv\tasa_errores\tasa-errores_crear_preadmision.csv")