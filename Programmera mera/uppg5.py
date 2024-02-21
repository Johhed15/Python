# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------------------------------------------------
# Uppgift 5
# ------------------------------------------------------------------------------------------------------------------------
# Skriv din kod här:
# Moduler
import matplotlib.pyplot as plt 
import pandas as pd 

# Datamaterialet
try:
    df_worldcities = pd.read_csv('worldcities.csv',sep=';')
except :
    print("Felaktig sökväg/filnamn/working directory, kolla upp så att allt är rätt")

    
# Tar bort eventuella nan som kan störa ihopslagningarna / grupperingar    
df_worldcities = df_worldcities.dropna(subset=["country", "population"])
    
# Skapar en ny DataFrame med antal städer per land och sortera den i fallande ordning efter antal städer
df_cities_per_land = df_worldcities.groupby("country").size().reset_index(name="num_cities")
df_cities_per_land = df_cities_per_land.sort_values("num_cities", ascending=False).reset_index(drop=True)


# Skapar en ny DataFrame med den största staden per land och antalet invånare i den staden
df_storstad = df_worldcities.groupby("country").apply(lambda x: x.loc[x.population.idxmax()]).reset_index(drop=True)
df_storstad = df_storstad[["country", "city", "population"]]

# Mergar de två DataFrame-objekten till en tabell med land, antal städer, största stad och antal invånare i staden, land som ID för mergen
df_combined = pd.merge(df_cities_per_land, df_storstad, on="country")

# Byter namn på tabellens kolumner till svenska 
df_combined = df_combined.rename(columns={"country": "Land", "num_cities": "Antal städer","city":"Största stad","population": "Antal inv i största staden"})

# Gör antal inv per stad till utan decimal
df_combined[['Antal inv i största staden']] = df_combined[['Antal inv i största staden']].applymap('{:.0f}'.format)

# Skriver ut tabellens 10 första värden 
print('De 10 länder med flest antal städer')
print('-'*68)
print(df_combined.head(10).to_string(index=False))

# Ändrar kolumnen till numeriskt för att Y-axeln ska bli rätt
df_combined["Antal inv i största staden"] = df_combined["Antal inv i största staden"].astype(int)

# Skapar två stapeldiagram med subplot-kommandot
fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(10, 10))

# Övre stapeldiagrammet: antal städer per land
ax1.bar(df_combined.head(10)["Land"], df_combined.head(10)["Antal städer"], color="blue")
# Titel
ax1.set_title("Länder med flest antal städer")
# Y-axel-titel
ax1.set_ylabel("Antal städer")

# Undre stapeldiagrammet: antal invånare i största staden per land
ax2.bar(df_combined.head(10)["Största stad"], df_combined.head(10)["Antal inv i största staden"], color="orange")
# Titel
ax2.set_title("Antal invånare i största staden i respektive land")
# Y-axel-titel
ax2.set_ylabel("Antal invånare")
# Luta x-axeln på det undre stapeldiagrammet för att undvika överlappning med x-etiketterna på det övre stapeldiagrammet
plt.setp(ax2.get_xticklabels(), rotation=45, ha="right")

# Visa diagrammen
plt.show()


    
