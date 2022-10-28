#importando as bibliotecas
import pandas as pd
import plotly.express as px
#abrindo o grafico no mesmo notebook

#importando os dados enconding utf-8 (EUA)
#.head verifica se a importação ocorreu

# download do dataset em https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents?datasetId=199387&sortBy=dateRun&tab=profile
importa_df=pd.read_csv('US_Accidents_Dec21_updated.csv', encoding='utf-8', sep=',')
importa_df.head()

#para importar somente os 100.000 primeiros registros
acidentes = importa_df.head(100000)
acidentes.head()

#verifica a quantidade de linhas e colunas
#acidentes.shape()

#remove duplicatas
acidentes=acidentes.drop_duplicates()
#acidentes.shape()

#ver o nome das colunas e o que trazem
acidentes.info()

#trocar o nome de colunas confusas
acidentes_renomeado=acidentes.rename(columns={"TMC": "Traffic_Message_Channel", "Number":"Street_Number"})
acidentes_renomeado.info()

#tratar colunas start_time e end_time
acidentes_renomeado.Start_Time = pd.to_datetime(acidentes_renomeado.Start_Time)
acidentes_renomeado.End_Time = pd.to_datetime(acidentes_renomeado.End_Time)

#validação se as variáveis estão na forma de data
acidentes_renomeado.info()

#soma todos os valores nulos por coluna
acidentes_renomeado.isnull().sum()

# Por possuírem valores em texto ou se um preenchimento numérico possa atrapalhar a análise da variável:
# End Lat — preencher com “N/A”
# End Lng — preencher com “N/A”
# Street_Number — preencher com “N/A”
# City — preencher com “N/A”
# Sunrise_Sunset — preencher com “N/A”
# Civil_Twilight — preencher com “N/A”
# Nautical_Twilight — preencher com “N/A”
# Astronomical_Twilight — preencher com “N/A”
# Timezone — preencher com “N/A”
# Airport_Code — preencher com “N/A”
# Weather_Timestamp — preencher com “N/A”
# Wind_Direction — preencher com “N/A”
# Weather_Condition — preencher com “N/A”
# Por ser comum ter valores baixos:
# Traffic_Message_Channel — preencher com o valor 999 ou com o valor 0
# Zipcode — preencher com 99999
# Temperature (F) — preencher com 999
# Wind_Chill(F) — preencher com 999
# Por nunca ter valores iguais a 0:
# Humidity(%) — preencher com 0
# Pressure(in) — preencher com 0
# Visibility(mi) — preencher com 0
# Wind_Speed(mph) — preencher com 0
# Precipitation(in) — preencher com 0

acidentes_renomeado['End_Lat'] = acidentes_renomeado['End_Lat'].fillna('N/A')
acidentes_renomeado['End_Lng'] = acidentes_renomeado['End_Lng'].fillna('N/A')
acidentes_renomeado['Street_Number'] = acidentes_renomeado['Street_Number'].fillna('N/A')
acidentes_renomeado['City'] = acidentes_renomeado['City'].fillna('N/A')
acidentes_renomeado['Sunrise_Sunset'] = acidentes_renomeado['Sunrise_Sunset'].fillna('N/A')
acidentes_renomeado['Civil_Twilight'] = acidentes_renomeado['Civil_Twilight'].fillna('N/A')
acidentes_renomeado['Nautical_Twilight'] = acidentes_renomeado['Nautical_Twilight'].fillna('N/A')
acidentes_renomeado['Astronomical_Twilight'] = acidentes_renomeado['Astronomical_Twilight'].fillna('N/A')
acidentes_renomeado['Timezone'] = acidentes_renomeado['Timezone'].fillna('N/A')
acidentes_renomeado['Airport_Code'] = acidentes_renomeado['Airport_Code'].fillna('N/A')
acidentes_renomeado['Weather_Timestamp'] = acidentes_renomeado['Weather_Timestamp'].fillna('N/A')
acidentes_renomeado['Wind_Direction'] = acidentes_renomeado['Wind_Direction'].fillna('N/A')
acidentes_renomeado['Weather_Condition'] = acidentes_renomeado['Weather_Condition'].fillna('N/A')

#acidentes_renomeado['Traffic_Message_Channel'] = acidentes_renomeado['Traffic_Message_Channel'].fillna(999)
acidentes_renomeado['Zipcode'] = acidentes_renomeado['Zipcode'].fillna(999)
acidentes_renomeado['Temperature(F)'] = acidentes_renomeado['Temperature(F)'].fillna(999)
acidentes_renomeado['Wind_Chill(F)'] = acidentes_renomeado['Wind_Chill(F)'].fillna(999)

acidentes_renomeado['Humidity(%)'] = acidentes_renomeado['Humidity(%)'].fillna(0)
acidentes_renomeado['Pressure(in)'] = acidentes_renomeado['Pressure(in)'].fillna(0)
acidentes_renomeado['Visibility(mi)'] = acidentes_renomeado['Visibility(mi)'].fillna(0)
acidentes_renomeado['Wind_Speed(mph)'] = acidentes_renomeado['Wind_Speed(mph)'].fillna(0)
acidentes_renomeado['Precipitation(in)'] = acidentes_renomeado['Precipitation(in)'].fillna(0)

#validando se todos os campos estão preenchidos
acidentes_renomeado.isnull().sum()

#ver os dados estatísticos da base de dados
acidentes_renomeado.describe()

# Como funciona a severidade?
# Severidade 1: não requer assistência externa, veículos podem ser removidos sozinhos, costuma durar entre 5 a 10 minutos
# Severidade 2: veículo requer assistência ou guincho para ser retirado, precisa de autoridades envolvidas, dura entre 15–40 minutos
# Severidade 3: bem similar à Severidade 2, podendo durar mais de horas, a principal diferença é o envolvimento de bombeiros e possíveis machucados ou morte
# Severidade 4: dura mais de uma hora, costuma envolver carros longos como caminhões, é um evento de Severidade 2 e 3 só que em larga escala
acidente_regiao=acidentes_renomeado.groupby(['Severity', 'City'])['Severity'].count().reset_index(name='Qtd')
acidente_regiao
fig = px.bar(acidente_regiao,x = 'City', y = 'Qtd', hover_data=['Severity'], labels={'City': 'Cidade', 'Qtd': 'Quantidade de Acidentes'}, color='Qtd')
fig.show()

acidente_sunrise = acidentes_renomeado.groupby(['Severity', 'City', 'Sunrise_Sunset'])['Severity'].count().reset_index(name='Qtd')
acidente_sunrise
graph = px.scatter(acidente_sunrise, x = 'City', y = 'Severity',  color='Severity', size = 'Qtd', hover_data=['Severity'])
graph.show()

acidente_clima = acidentes_renomeado.groupby(['Severity', 'City', 'Sunrise_Sunset'])['Severity'].count().reset_index(name='Qtd')
acidente_clima
px.lmplot(x = 'Temperature(F)', y='Precipitation(in)', hue = 'Severity', data = acidente_clima)
