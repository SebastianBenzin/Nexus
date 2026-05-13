import pandas as pd


df_lokacije = pd.read_csv("mars_lokacije.csv", sep=';', decimal=',')
df_uzorci = pd.read_csv("mars_uzorci.csv", sep=';', decimal=',')
df_spajanje = pd.merge(df_lokacije, df_uzorci, on='ID_Uzorka')
df_notemp = df_spajanje[df_spajanje['Temp_Tla_C'] != 150.0]
df_cisto = df_notemp[df_notemp['H2O_Postotak'].astype(str).str.len() < 6].copy()
df_cisto['H2O_Postotak'] = pd.to_numeric(df_cisto['H2O_Postotak'])
kandidati = df_cisto[(df_cisto['Metan_Senzor'] == 'Pozitivno') & (df_cisto['Organske_Molekule'] == 'Da')]
prosjek_temp = kandidati['Temp_Tla_C'].mean()
print(f"Prosječna temp je: {prosjek_temp:.2f} °C")