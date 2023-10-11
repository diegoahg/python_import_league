import pandas as pd
import os


def normalize_name(input_team):
  teams = {
    "BOROA": "DEFENSOR BOROA",
    "OVALLE": "JUVENTUD OVALLE",
    "PISTONO": "JOSE PISTONO",
    "VECINAL": "JUVENTUD VECINAL",
    "ESTOCOLMO": "ESTOCOLMO",
    "FLAMENGO": "FLAMENGO",
    "10 DE MARZO": "10 DE MARZO",
    "CHAYAIHUE": "CHAYAIHUE",
    "INDEPENDIENTE": "INDEPENDIENTE",
    "PICHANGA": "PICHANGA",
    "SAO PAULO": "SAO PAULO",
    "BOCA JUNIORS": "BOCA JUNIORS",
    "BOCA": "BOCA JUNIORS",
    "BOCAJUNIORS": "BOCA JUNIORS",
    "PICHANFA": "PICHANGA"
    }
  return teams[input_team]

def normalize_serie(serie):
  series = {
    "1RA ADULTO": "1RA ADULTO",
    "PRIMERA": "1RA ADULTO",
    "2DA ADULTO": "2DA ADULTO",
    "SEGUNDA": "2DA ADULTO",
    "SENIORS": "SENIORS",
    "SUB 12": "SUB 12",
    "SUB 15": "SUB 15",
    "SUB 17": "SUB 17",
    "SUB17": "SUB 17"
    }
  return series[serie]

def normalize_date(day):
  days = {
    "VIERNES 13": "2023/10/13",    # MODHERE
    "SABADO 14": "2023/10/14",     # MODHERE
    "DOMINGO 15": "2023/10/15",    # MODHERE
    "DOMINGO 16": "2023/10/15",    # MODHERE
    }
  return days[day]

def normalize_turno(turnos):
  turno =turnos.split("/")
  return f"{normalize_name(turno[0])}", f"{normalize_name(turno[1])}"

def formato_hora(texto):
    # Reemplazar "HRS" por ":00" y "." por ":"
    texto_formateado = texto.replace(" HRS", "HRS")
    texto_formateado = texto_formateado.replace("HRS", ":00")
    texto_formateado = texto_formateado.replace(".", ":")
    
    return texto_formateado

#--------------MAIN--------------#

nro_fecha = "4"   # MODHERE
# Leer datos del archivo Excel
input_excel_filename = "FechasExcel/FECHA " +  nro_fecha + " CAMPEONATO CLAUSURA.xlsx"
# Cargar el archivo Excel en un DataFrame
df = pd.read_excel(input_excel_filename)

# Limpieza de Excel
df = df.set_axis(df.iloc[0], axis=1) # Se deja la segunda fila(ahora es la primera) como encabezadp
df.drop(0, axis=0, inplace=True)     # Se saca segunda fila duplicada como encabezado
df = df[df['LOCAL'].notna()]         # Se eliminan los partidos que tienen espacios en blanco como LOCAL
print(df)

# Procesar los datos y construir los datos para el archivo CSV de salida
output_data_primera = []
output_data_segunda = []
output_data_sub17   = []
output_data_sub15   = []
output_data_sub12   = []

# Definir el diccionario de series
series = {
    "1RA ADULTO": [],
    "2DA ADULTO": [],
    "SENIORS": [],
    "SUB 12": [],
    "SUB 15": [],
    "SUB 17": []
}

for _, row in df.iterrows():
    turno1, turno2 = normalize_turno(row['TURNO'])
    serie          = normalize_serie(row['SERIE'])
    date           = normalize_date(row['FECHA'])
    time           = f"{formato_hora(row['HORARIO'])}"
    venue          = "Estadio Dávila"
    teams_local    = f"{normalize_name(row['LOCAL'])}"
    teams_visit    = f"{normalize_name(row['VISITA'])}"
    day            = "FECHA " + nro_fecha

    series[serie].append([date, time , venue, teams_local, teams_visit, day])
# Exportar los datos de cada serie a archivos CSV
for serie, data in series.items():
    path="Fecha" + nro_fecha
    if not os.path.exists(path):
      os.makedirs(path)
    output_csv_filename = f"{serie.lower().replace(' ', '_')}.csv"
    output_data = []
    output_data.extend(data)
    
    output_df = pd.DataFrame(output_data, columns=['Date', 'Teams', 'Venue', 'Home', 'Away', 'Day'])
    output_df.to_csv(path + "/" + output_csv_filename, index=False)
    
    print(f"Los datos de la serie '{serie}' se han exportado a '{output_csv_filename}'.")
