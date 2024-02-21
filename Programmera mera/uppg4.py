# -*- coding: utf-8 -*-


# ------------------------------------------------------------------------------------------------------------------------
# Uppgift 4
# ------------------------------------------------------------------------------------------------------------------------
# Skriv din kod här:
# Moduler
import matplotlib.pyplot as plt 
import pandas as pd 
import numpy as np

# datamaterialet
try:
    df_worldpubind = pd.read_csv('worldpubind.csv', sep=';')
except :
    print("Felaktig sökväg/filnamn/working directory, kolla upp så att allt är rätt")

# a 
# Beräknar procentuella befolkningsutvecklingen per land
df_worldpubind['population_change'] = ((df_worldpubind["2021"] - df_worldpubind["1960"]) / df_worldpubind["1960"]) * 100

# Sortera efter procentuell befolkningsförändring, droppar nan
df_sorted = df_worldpubind.sort_values(by=('population_change')).dropna()

# Skapar 2 dataframes med de 5 största och minsta
top5_neg = df_sorted.tail(5)
top5_pos = df_sorted.head(5)

# lägger ihop max och min
pop_table = pd.concat([top5_pos[["Country Name", "population_change"]],
                     top5_neg[["Country Name", "population_change"]]])


# Ändrar till svenska namn
pop_table = pop_table.rename(columns={"Country Name": "Land", "population_change": "Befolkningsförändring"})
# Lägger in multilevelnamn
pop_table.columns = pd.MultiIndex.from_tuples([('Land', ''), ('Befolkningsförändring', 'mellan 1960 och 2021')])

# Två decimaler
pop_table[[('Befolkningsförändring', 'mellan 1960 och 2021')]] = np.around(pop_table[[('Befolkningsförändring', 'mellan 1960 och 2021')]],decimals=2)


# Skriver ut tabellerna
print('Befolkningsutvecklingen hos ett antal länder under åren 1960-2021\n')
print('-'*65)
print('De 5 länder med störst negativ befolkningsförändring:')
print(pop_table.head().to_string(index=False))
print('')
print('De 5 länder med störst positiv befolkningsförändring:')
print(pop_table.tail().sort_values(by=('Befolkningsförändring', 'mellan 1960 och 2021'),ascending=False).to_string(index=False))


# Lista med färger
colors = ['red', 'orange', 'yellow', 'green', 'blue']

# visar de negativa förändringarna, ger dem färg efter ordning
plt.bar(pop_table.head()["Land"], pop_table.head()[('Befolkningsförändring', 'mellan 1960 och 2021')],color=[colors[i] for i in range(5)])
#titel
plt.title("De 5 länder med störst negativ befolkningsförändring:")
# Y-titel
plt.ylabel("Befolkningsförändring i (%)")
# X-ticks vridna
plt.xticks(rotation=45)
# visar grafen
plt.show()

# visar de negativa förändringarna och sorterar om, ger dem färg efter ordning
plt.bar(pop_table.tail()["Land"], pop_table.tail()[('Befolkningsförändring', 'mellan 1960 och 2021')].sort_values(ascending=False),color=[colors[i] for i in range(5)])
#titel
plt.title("De 5 länder med störst positiv befolkningsförändring:")
# Y-titel
plt.ylabel("Befolkningsförändring i (%)")
# X-ticks vridna
plt.xticks(rotation=45)
# visar grafen
plt.show()









# ------------------------
# b
#-------------------------
# Skapar tidseriegraf som kommer låta användaren välja ett land som ska printas
def tidseriegraf():
    # Användaren väljer ett land
    land = input('Välj ett land du vill se(engelsk stavning):')
    
    
    # Testar om det inmatade värdet går att köra
    try:
        # Filtrerar efter land och väljer ut åren
        row_land = df_worldpubind.loc[df_worldpubind['Country Name']==land].filter(regex='\d+')
    
        # Tom lista
        change = []

        # Iterera över åren från 1961 till 2021
        for i in range(1961, 2022):
                # Beräkna förändringen mellan åren
                skillnad  = ((row_land[str(i)] - row_land[str(i-1)]) / row_land[str(i-1)]) * 100
                # lägger i lista på plats i
                change.append(skillnad.values[0]) 
       
        # Skapa en ny DataFrame med förändringsvärdena och index för åren på raderna med nan för första året
        change_row = pd.DataFrame({"population_change": [np.nan] + change}, index=row_land.columns)
        
        # Transponerar raden till kolumn så att det går att merga med change_row
        row_land = row_land.transpose()
        
        # Slå ihop de två DataFrame-objekten
        merged = change_row.join(row_land)
        
        # En Array för åren till x-axeln
        year = np.arange(1960,2022,dtype='int')
        
        # Skapar plotten med 2 olika y-axlar ------------------------
        
        fig = plt.figure()
        ax1 = fig.add_axes([0,0,1,1])
        # År mot förändring, väljer färg och label för att skilja på linjerna
        ax1.plot(year, merged["population_change"],color='b' ,label=(land + '- befolkningsförändring'))
        # X-axel
        ax1.set_xlabel("År")
        #  Titel på vänsta Y-axeln
        ax1.set_ylabel("Befolknigsförändring [%]", color='b')
        # Titel på hela grafen
        ax1.set_title(f"Procentuell befolkningsförändring i {land} 1961-2020")
        ax1.tick_params(axis = "y")
        # PLats på legenden
        ax1.legend(loc="upper left")

        # Y-axel 2
        ax2 = ax1.twinx()
        # år mot folkmängd med andra färger än förra linjen
        ax2.plot(year, merged[merged.columns[1]], color='r', label=(land + '- folkmängd'))
        # Y-axel
        ax2.set_ylabel("Folkmängd",color = "r")
        # Ticks högra Y-axeln
        ax2.tick_params(axis = "y")
        # Legendens plats till linje 2
        ax2.legend(loc="upper right")
       
        plt.show()
    # om det inte går att plotta landet 
    except:
        print('Landet kan ej visas, kontrollera stavning eller testa ett annat land och kör om tidsseriegraf()')

# För att testa koden
tidseriegraf()




