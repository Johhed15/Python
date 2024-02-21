# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------------------------------------------------
# Uppgift 2
# ------------------------------------------------------------------------------------------------------------------------
# Skriv din kod här:
# Moduler

import matplotlib.pyplot as plt 
import pandas as pd 
import re
# Datamaterial  

try:
# Skapar kopia av dataframen från cia_factbook.csv 
    df_cia_factbook = pd.read_csv('cia_factbook.csv', sep=';')
except :
    print("Felaktig sökväg/filnamn/working directory, kolla upp så att allt är rätt")

# Skapar ny kolumn för tätheten
df_cia_factbook.loc[:,'density'] =  df_cia_factbook['population'] /   df_cia_factbook['area'] 

# Tar bort NaN och inf från nya variabeln
df_cia_factbook = df_cia_factbook.dropna(subset='density')
df_cia_factbook = df_cia_factbook.query('density != inf')


# Visar det användaren väljer
def density_graph():
    # variabel som anger vad användaren vill se
    user_input = input("Ange antalet länder(max 10) eller enkilt land du vill se:")

    try:
        
### ------ Här är ändringen ------- ####
        # Rensar bort eventuella plus eller minustecken
        numerisk = re.sub("[^0-9]", "", user_input)
        # gör till int
        numerisk = int(numerisk)
        # kollar om det är positivt eller negativt inmatat och ändrar till pos/negativt
        if "+" in str(user_input):
            user_input=abs(numerisk)
        elif "-" in user_input:
            user_input = -abs(numerisk)
 ### ------ ovanför är ändringen ------- ####       
        
        # testar att göra det inmatade värdet till integer med namn x
        x = int(user_input)


        # Om fler än 10 anges ges ett direktiv åt användaren att ändra
        if abs(x) > 10:
        # Printar direktivet
            print('Fler än 10 länder har angetts')
        # Om ett positivt heltal under 11 matats in
        elif x > 0 and x <11: 
            # Anger en storlek på grafen
            fig, ax = plt.subplots(figsize=(10, 6))
        
            # Väljer ut x antal rader från df av de med störst densitet till en ny df
            top_ten = df_cia_factbook.nlargest(x,'density') 
            # Plottar land och densitet som barplot
            plt.bar(top_ten['country'], top_ten['density'])
            # Roterar labtitels på x-axeln så det blir lättare att se
            plt.xticks(rotation=45)
            # Gridmönster för x och y-axlarna med gråfärg
            plt.grid(axis='both', color='grey', linewidth=1.0)
            # Ger diagrammet en titel
            plt.title('Länder med störst befolkningstäthet')
            # Ger y-axeln en titel
            plt.ylabel('Befolkningstäthet (inv/km²)')
            # Visar diagrammet
            plt.show()
    
        # om ett negativt värde matats in
        elif x < 0 and x > -11: 
            # Anger en storlek på grafen
            fig, ax = plt.subplots(figsize=(14, 6))
            # Väljer ut abs(x) antal rader från df av de med störst densitet till en ny df
            min_ten = df_cia_factbook.nsmallest(abs(x),'density') 
            # Plottar land och densitet som barplot
            plt.bar(min_ten['country'], min_ten['density'])
            # Roterar labtitels på x-axeln så det blir lättare att se
            plt.xticks(rotation=45)
            # Gridmönster för x och y-axlarna med gråfärg
            plt.grid(axis='both', color='grey', linewidth=1.0)
            # Ger diagrammet en titel
            plt.title('Länder med lägst befolkningstäthet')
            # Ger y-axeln en titel
            plt.ylabel('Befolkningstäthet (inv/km²)')
            # Visar diagrammet
            plt.show()
        else:
                print('Antalet länder som angivits är noll eller ej ett heltal')
    
    # Om det inte är heltal så ska det valda landet printas
    except ValueError: 
        try:
            # Indexerar ut det valda landets density
            dens = df_cia_factbook.loc[df_cia_factbook['country']== user_input,'density'].iloc[0]
            # Printar det valda landet och tätheten med 2 decimaler
            print(f' Befolkningstäthet i {user_input} är {dens:.2f} inv/km²')
        except:
            print("Landet som angetts finns ej i datamaterialet eller är felstavat(Obs versal som första bokstav)")

# Testa funktionen
density_graph()





