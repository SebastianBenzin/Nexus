import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import requests

df_lokacije = pd.read_csv("mars_lokacije.csv", sep=';', decimal=',')
df_uzorci = pd.read_csv("mars_uzorci.csv", sep=';', decimal=',')
df_spajanje = pd.merge(df_lokacije, df_uzorci, on='ID_Uzorka')
df_notemp = df_spajanje[df_spajanje['Temp_Tla_C'] != 150.0]
df_cisto = df_notemp[df_notemp['H2O_Postotak'].astype(str).str.len() < 6].copy()
df_cisto['H2O_Postotak'] = pd.to_numeric(df_cisto['H2O_Postotak'])
kandidati = df_cisto[(df_cisto['Metan_Senzor'] == 'Pozitivno') & (df_cisto['Organske_Molekule'] == 'Da')]

# Graf 1
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df_cisto, x='Temp_Tla_C', y='H2O_Postotak', hue='Metan_Senzor')
plt.title("Odnos temperature i vlage")
plt.savefig('graf_1.png')

# Graf 2
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df_cisto, x='GPS_LONG', y='GPS_LAT', hue='Dubina_Busenja_cm', palette='viridis')
plt.title("Mapa planirane dubine bušenja")
plt.savefig('graf_2.png')

# Graf 3
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df_cisto, x='GPS_LONG', y='GPS_LAT',
                hue='Metan_Senzor', palette={'Pozitivno': 'red', 'Negativno': 'blue'})
plt.title("Detekcija metana po lokacijama")
plt.savefig('graf_3.png')

# Graf 4
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df_cisto, x='GPS_LONG', y='GPS_LAT', hue='H2O_Postotak')
plt.scatter(kandidati['GPS_LONG'], kandidati['GPS_LAT'],
            marker='*', s=250, color='red', label='Kandidati (Org. molekule + Metan)')
plt.legend()
plt.title("Lokacije idealnih kandidata za analizu")
plt.savefig('graf_4.png')


plt.figure(figsize=(12, 10))

# 1. RUČNO POSTAVLJANJE GRANICA (prema tvojoj slici)
# Ovo osigurava da slika kratera ne bude razvučena ovisno o tvojim podacima
extent_koordinate = [77.35, 77.425, 18.445, 18.515]

try:
    slika_kratera = plt.imread('jezero_crater_satellite_map.jpg')


    plt.imshow(slika_kratera, extent=extent_koordinate, aspect='auto', zorder=1)


    sns.scatterplot(data=df_cisto, x='GPS_LONG', y='GPS_LAT',
                    hue='H2O_Postotak', palette='viridis',
                    alpha=0.5, s=20, edgecolor='none', zorder=2, legend=False)


    plt.scatter(kandidati['GPS_LONG'], kandidati['GPS_LAT'],
                marker='*', s=300, color='yellow', edgecolor='black',
                label='Kritične zone bušenja', zorder=3)

    plt.title("Završna mapa misije", fontsize=14)
    plt.xlabel("Geografska dužina")
    plt.ylabel("Geografska širina")
    plt.legend(loc='upper right')

    # Postavljanje istih granica kao na slici
    plt.xlim(77.35, 77.425)
    plt.ylim(18.445, 18.515)

except FileNotFoundError:
    print("Greška: Nije pronađena slika 'jezero_crater_satellite_map.jpg'!")
    sns.scatterplot(data=df_cisto, x='GPS_LONG', y='GPS_LAT', hue='H2O_Postotak')

plt.savefig('graf_5.png', dpi=300)
plt.show()


nalozi_lista = []


for index, redak in kandidati.iterrows():
    nalog = {
        "id_uzorka": int(redak['ID_Uzorka']),
        "koordinate": {
            "lat": float(redak['GPS_LAT']),
            "long": float(redak['GPS_LONG'])
        },
        "akcije": ["NAVIGACIJA", "SONDIRANJE", "SLANJE_PODATAKA"]
    }
    nalozi_lista.append(nalog)

"""
paket = {
    "misija": "Nexus",
    "kandidati_count": len(nalozi_lista),
    "nalozi": nalozi_lista
}


response = requests.post(url_webhook, json=paket)

if response.status_code == 200:
    print("--- MISIJA USPJEŠNO IZVRŠENA ---")
    print(f"Statusni kod: {response.status_code}")
    print(f"Broj poslanih kandidata: {len(nalozi_lista)}")
else:
    print(f"Došlo je do problema. Status: {response.status_code}")
"""
