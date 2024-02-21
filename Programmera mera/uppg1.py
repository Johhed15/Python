# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------------------------------------------------
# Uppgift 1
# ------------------------------------------------------------------------------------------------------------------------
# Skriv din kod här:

# Pandas används för att läsa in datamaterialet 
import pandas as pd 


# Felhantering för att inte generera error
try:
    #   Skapar kopia av dataframen från cia_factbook.csv 
    df_cia_factbook = pd.read_csv('cia_factbook.csv', sep=';')

    # Skapar kopia av dataframen från worldcities.csv
    df_worldcities = pd.read_csv('worldcities.csv',sep=';')

    # Skapar kopia av dataframen från worldpubind.csv
    df_worldpubind = pd.read_csv('worldpubind.csv', sep=';')

except:
    print("Felaktig sökväg/filnamn/working directory, kolla upp så att allt är rätt")

