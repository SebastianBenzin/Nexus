# Projekt Nexus: Analiza telemetrije i navigacija (Krater Jezero)

## A. Izvršni sažetak (Executive Summary)
Glavni cilj ove misije je provedba opsežne analize telemetrijskih podataka prikupljenih s područja kratera Jezero na Marsu. Sustav obrađuje ulazne CSV podatke s koordinatama i uzorcima tla kako bi prepoznao ključne geološke i atmosferske značajke terena. Konačni cilj ovog analitičkog procesa je izrada i slanje automatiziranog navigacijskog naloga koji će osigurati sigurno kretanje terenskog robota kroz zadane točke interesa (waypoints).

## B. Metodologija obrade podataka (Data Wrangling)
Tijekom inicijalne analize ulaznih `DataFrame` objekata detektirana je visoka prisutnost senzorskog šuma. Primijenjena je metodologija logičkog filtriranja podataka (Data Filtering) kako bi se osigurao integritet analitičkog modela:
* **Ekstremne temperature:** Korištenjem uvjetnog filtriranja u Pandas biblioteci, uklonjeni su svi zapisi s temperaturama ispod -150°C i iznad 20°C, koji ukazuju na grešku u kalibraciji termalnog senzora.
* **Anomalije u pH vrijednostima:** Podaci koji izlaze izvan očekivanog raspona pH vrijednosti za marsovsko tlo (filtrirano na raspon 5.0 - 9.0) izolirani su i odbačeni kako ne bi kontaminirali završne izračune.

## C. Geoprostorna analiza i vizualizacija
U nastavku je prikazan središnji dokazni materijal provedene analize s grafičkim prikazima i interpretacijom.

### 1. Korelacija geoloških parametara
![Graf korelacije parametara](graf_1.png)
*Interpretacija:* Prikaz korelacije pokazuje snažnu povezanost između detektirane razine vlage i specifičnog mineralnog sastava na zadanim koordinatama.

### 2. Toplinska karta i rasprostranjenost metana
![Toplinska karta metana](graf_4_mapa_metana.png)
*Interpretacija:* Toplinska karta jasno ukazuje na visoku koncentraciju metana u sjeverozapadnom kvadrantu kratera, što sugerira potrebu za detaljnijim ispitivanjem tog sektora.

### 3. Satelitska mapa (Extent mapiranje)
![Extent satelitska mapa](graf_5.png)
*Tehnički koncept:* Za završnu satelitsku mapu primijenjen je koncept *extent* mapiranja granica. Pomoću graničnih (bounding box) koordinata (sjever, jug, istok, zapad), raspršeni podaci sa senzora precizno su i kontekstualno pozicionirani na stvarnu pozadinsku satelitsku snimku pomoću stvarnih GPS koordinata. Ovo je ključno za pouzdanu orijentaciju terenskog robota.

## D. Komunikacijski protokol (JSON Uplink)
Mrežni paket dizajniran je za slanje navigacijskih naredbi prema terenskom robotu. Za automatizirano generiranje naredbi implementirana je iterativna petlja (npr. `for` petlja u Pythonu) koja prolazi kroz pročišćeni `DataFrame` i dinamički puni JSON strukturu. Time je izbjegnuto ručno kodiranje (hardcoding) i omogućena je skalabilnost sustava.

Ispod je prikazan isječak ugniježđenog JSON niza koji modul šalje sustavu:

```json
{
  "mission_id": "NEXUS-01",
  "target_crater": "Jezero",
  "navigation_commands": [
    {
      "waypoint_id": 1,
      "latitude": 18.4447,
      "longitude": 77.4529,
      "action": "sample_collection"
    },
    {
      "waypoint_id": 2,
      "latitude": 18.4510,
      "longitude": 77.4580,
      "action": "sensor_calibration"
    }
  ]
}
E. Inženjerski dnevnik (Troubleshooting Log)
Tijekom razvoja sustava uspješno su detektirane i otklonjene sljedeće prepreke:

Greška kod spajanja tablica (Separator mismatch): Pri pokušaju učitavanja izvorne datoteke mars_uzorci.csv, biblioteka Pandas je vratila ParserError. Problem je bio u pogrešnom separatoru unutar CSV datoteke (korištena je točka sa zarezom ; umjesto standardnog zareza ,). Riješeno je dodavanjem argumenta sep=';' unutar funkcije pd.read_csv().

Rušenje skripte zbog pogrešnog tipa podataka (Type Casting): Tijekom generiranja JSON uplinka, skripta se srušila pri serijalizaciji jer su NumPy vrijednosti tipa int64 nekompatibilne sa standardnim json modulom. Rješeno korištenjem .astype(int) metode u Pythonu ili prelaskom na pretvorbu unutar Pandas biblioteke prije konačnog eksporta.
