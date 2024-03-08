
# This repository contains some of the work from Python courses I've taken

## The three folders contain work from these courses

- Grundläggande programmering i Python(Borås)
- Programmera mera i Python (Borås)
- Introduction to Python(Linköping)

<br>

#### If you have any questions regarding the work, please contact me


## Example of a simple program that creates user choice outputs 

```Python
import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd 


# Skapar kopia av dataframen från cia_factbook.csv 
df_cia_factbook = pd.read_csv('cia_factbook.csv', sep=';')

# Skapar kopia av dataframen från worldcities.csv
df_worldcities = pd.read_csv('worldcities.csv',sep=';')

# Skapar kopia av dataframen från worldpubind.csv
df_worldpubind = pd.read_csv('worldpubind.csv', sep=';')

# Skapar ny kolumn för tätheten
df_cia_factbook.loc[:,'density'] =  df_cia_factbook['population'] /   df_cia_factbook['area'] 

# Tar bort NaN och inf från nya variabeln
df_cia_factbook = df_cia_factbook.dropna(subset='density')
df_cia_factbook = df_cia_factbook.query('density != inf')


def meny():
    print('')
    print('Hej! Välkommen till programmet "Demografi" \n Välj ett av följande alternativ')
    print('')
    print('1: Under medelstora länders area, födelseantal per 1000 och förväntad livslängd efter vissa kriterier')
    print('2: De 5 länderna med lägst och högst antal internetanvändare per 100000')
    print('3: De fem länderna med högst negativ och positiv befolkningsförändring per 1000')
    print('4: Avsluta programmet')
    
# Skapar alternativ 1
def menyalternativ1():
    # Befolkningsmedelvärde
    Bmedel = df_cia_factbook['population'].mean()
    # Genomsnittsarea
    Amedel = df_cia_factbook['area'].mean()   
    
    # Mask för att välja länder som uppfyller kriterier
    mask = (df_cia_factbook['population'] > Bmedel) & \
           (df_cia_factbook['area'] < Amedel) & \
           (df_cia_factbook['birth_rate'].between(15,24 )) & \
           (df_cia_factbook['life_exp_at_birth'] > 70) 
            
    # Filtrerar med mask och droppar Nan
    filt_meny1 = df_cia_factbook[mask][['country', 'area', 'birth_rate', 'life_exp_at_birth']].dropna(subset=['country', 'area', 'birth_rate', 'life_exp_at_birth'])
    # Avrundning nedåt
    filt_meny1[['birth_rate','life_exp_at_birth']] = filt_meny1[['birth_rate','life_exp_at_birth']].apply(np.floor)
    # Heltal
    filt_meny1[['area','birth_rate','life_exp_at_birth']] = filt_meny1[['area','birth_rate','life_exp_at_birth']].applymap('{:.0f}'.format)
    # Printen ska ha svenska namn
    filt_meny1 = filt_meny1.rename(columns={"country": "Land", "area": "Area", "birth_rate": "Födelsetal", "life_exp_at_birth": "Livslängd"})
    # Enheter ska stå under namnet
    filt_meny1.columns = pd.MultiIndex.from_tuples(zip(filt_meny1.columns, ["", "[km2]", "[per 1000 inv]", "[år]"]))
    # Visar filtrerad tabell
    print(filt_meny1.to_string(index=False))
   
# Skapar alternativ 2
def menyalternativ2():
    # Visa länder med högst och lägst internetmognad
    # Skapa en ny kolumn internet_user_density
    df_cia_factbook['internet_user_density'] = df_cia_factbook['internet_users'] / df_cia_factbook['population'] * 100000
    # Skapa en boolsk mask som filtrerar ut länder med och utan NaN-värden
    mask = ~df_cia_factbook['internet_user_density'].isnull()
    # Filtrerar ut det som ska visas och sorterar
    filt_meny2 = df_cia_factbook[mask][['country', 'population', 'internet_user_density']].sort_values(by='internet_user_density', ascending=False)

    
    # formatera population decimaler
    filt_meny2[['population']] = filt_meny2[['population']].applymap('{:.0f}'.format)
    # En decimal
    filt_meny2[['internet_user_density']] = np.around(filt_meny2[['internet_user_density']],decimals=1)
    print(filt_meny2)
    # Ändrar till svenska namn
    filt_meny2 = filt_meny2.rename(columns={"country": "Land", "population": "Folkmängd","internet_user_density":"Antal internetanvändare" })
    # Lägger in enhet 
    filt_meny2.columns = pd.MultiIndex.from_tuples([('Land', ''), ('Folkmängd', ''), ('Antal internetanvändare', '[per 1000 000 inv]')])
    
    # Visa de fem länderna med lägst internetmognad
    print("Länder med lägst internetmognad per 100 000 invånare:")
    print(filt_meny2.tail().sort_values(by=('Antal internetanvändare',  '[per 1000 000 inv]')).to_string(index=False))
    # Visa de fem länderna med högst internetmognad'
    print('')
    print("Länder med högst internetmognad per 100 000 invånare:")
    # Skriv ut tabellvärdena
    print(filt_meny2.head().to_string(index=False))
    


# Skapar alternativ 3
def menyalternativ3():
    # Visa länder med störst positiv och negativ befolkningsförändring
    # Beräkna population_growth_rate och population_change
    df_cia_factbook['population_growth_rate'] = (df_cia_factbook['birth_rate'] - df_cia_factbook['death_rate'] + df_cia_factbook['net_migration_rate'])
    df_cia_factbook['population_change'] =( (df_cia_factbook['population'] * (df_cia_factbook['population_growth_rate']))/10 )/ df_cia_factbook['population']
    
    # Väljer kolumner och droppar nan
    filt_meny3 = df_cia_factbook[['country','birth_rate','death_rate','net_migration_rate', 'population_change']].dropna()

    # Tar ut de fem största och lägsta
    top_max = filt_meny3.nlargest(5, "population_change")
    top_min = filt_meny3.nsmallest(5, "population_change")
    
    # lägger ihop max och min
    table_data = pd.concat([top_max[["country", "birth_rate", "death_rate", "net_migration_rate", "population_change"]],
                        top_min[["country", "birth_rate", "death_rate", "net_migration_rate", "population_change"]]])

    # Ändrar till svenska namn
    table_data = table_data.rename(columns={"country": "Land", "birth_rate": "Antal födslar","death_rate":"Antal döda","net_migration_rate": "Netto migration","population_change":"Befolkningsförändring" })
    # Lägger in enhet 
    table_data.columns = pd.MultiIndex.from_tuples([('Land', ''), ('Antal födslar', '[Per 1000 inv]'), ('Antal döda', '[per 1000 inv]'),('Netto migration', '[per 1000 inv]'),('Befolkningsförändring', '[% av folmängd]')])
    
    # Visar tabellen och sorterar 
    print('Länder där befolkning minskar mest')
    print(table_data.tail().sort_values(by=('Befolkningsförändring', '[% av folmängd]')).to_string(index=False))
    print('')
    print('Länder där befolkning ökar mest')
    print(table_data.head().sort_values(by=('Befolkningsförändring', '[% av folmängd]'),ascending=False).to_string(index=False))
   
    # sorterar data
    table_data = table_data.sort_values(by=('Befolkningsförändring', '[% av folmängd]'))
    
    # Skapar färgindex där blå är positiva och orange negativa
    table_data['color'] = table_data['Befolkningsförändring', '[% av folmängd]'].apply(lambda x: 'blue' if x >= 0 else 'orange')

    # plottar stapeldiagrammet
    ax = table_data['Befolkningsförändring', '[% av folmängd]'].plot(kind='bar', color=table_data['color'], figsize=(8,6))

    # Sätter ticklabels på x-axeln
    ax.set_xticklabels(table_data['Land'].tolist(), rotation=45, ha="right")

    # Y-rubrik
    ax.set_ylabel('Befolkningsförändring [% av folkmängd]')

    # titel
    ax.set_title('Länder med minst och störst befolkningsökning')

    # visar plotten
    plt.show()

# Programmet körs om till att alternativ 4 har valts
def demografi():
    # Variabeln som styr om programmet ska fortsätta köras
    run = True
    while run:
        # Printar alternativen och ger användaren möjligheten att välja
        meny()
        # Variabeln där användaren väljer meny
        alternativ = input('Välj ett alternativ(1-4):')
        print('')
        # Om alternativ 1 väljs
        if alternativ == "1":
            menyalternativ1()
        # Om alternativ 2 väljs
        elif alternativ == "2":
            menyalternativ2()
        # Om alternativ 3 väljs
        elif alternativ == "3":
            menyalternativ3()
        # Om alternativ 4 väljs
        elif alternativ == "4":
            # Programmet avlutas
            run = False
        else:
            # För att få användaren att välja rätt varde
            print("Felaktigt val. Försök igen.")
    # Så att användaren vet att programmet avslutas
    print("Programmet avslutas.")    
        
      
# Testa funktionen
demografi()
    

```

<br>
<br>

<div align="center">
  <img src="https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExYnZtNnc1NnNneTNlN2V4cjVvODFvaThhemE2NHZ4OGNmbXBiN2h6eCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/KAq5w47R9rmTuvWOWa/giphy.gif" width="400" height="300"/>
</div>


