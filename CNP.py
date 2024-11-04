import random
import pandas as pd
import time
import matplotlib.pyplot as plt
from datetime import datetime
from distributie_date import distributie_masculin, distributie_feminin


# Liste de nume pentru atribuirea CNP-urilor
nume_masculin = ["Andrei", "Mihai", "Vlad", "George", "Adrian"]
nume_feminin = ["Maria", "Ana", "Elena", "Ioana", "Diana"]

# Codurile județelor pentru generarea CNP-urilor
judete = {
    1: "ALBA", 2: "ARAD", 3: "ARGES", 4: "BACAU", 5: "BIHOR", 6: "BISTRITA-NASAUD", 7: "BOTOSANI",
    8: "BRASOV", 9: "BRAILA", 10: "BUZAU", 11: "CARAS-SEVERIN", 12: "CLUJ", 13: "CONSTANTA", 14: "COVASNA",
    15: "DAMBOVITA", 16: "DOLJ", 17: "GALATI", 18: "GORJ", 19: "HARGHITA", 20: "HUNEDOARA",
    21: "IALOMITA", 22: "IASI", 23: "ILFOV", 24: "MARAMURES", 25: "MEHEDINTI", 26: "MURES",
    27: "NEAMT", 28: "OLT", 29: "PRAHOVA", 30: "SATU MARE", 31: "SALAJ", 32: "SIBIU",
    33: "SUCEAVA", 34: "TELEORMAN", 35: "TIMIS", 36: "TULCEA", 37: "VASLUI", 38: "VALCEA",
    39: "VRANCEA", 40: "BUCURESTI", 41: "BUCURESTI - SECTOR 1", 42: "BUCURESTI - SECTOR 2",
    43: "BUCURESTI - SECTOR 3", 44: "BUCURESTI - SECTOR 4", 45: "BUCURESTI - SECTOR 5",
    46: "BUCURESTI - SECTOR 6", 51: "CALARASI", 52: "GIURGIU"
}

# Funcția pentru generarea unui CNP valid
def genereaza_cnp(sex, an_nastere, luna_nastere, zi_nastere, cod_judet):
    if an_nastere < 1900:
        S = 1 if sex == 'M' else 2
    elif 1900 <= an_nastere < 2000:
        S = 1 if sex == 'M' else 2
    elif 2000 <= an_nastere < 2100:
        S = 5 if sex == 'M' else 6

    S = str(S)
    AA = str(an_nastere % 100).zfill(2)
    LL = str(luna_nastere).zfill(2)
    ZZ = str(zi_nastere).zfill(2)
    JJ = str(cod_judet).zfill(2)
    NNN = str(random.randint(1, 999)).zfill(3)
    cnp_fara_control = f"{S}{AA}{LL}{ZZ}{JJ}{NNN}"
    C = calculeaza_cifra_control(cnp_fara_control)
    return cnp_fara_control + C

# Funcția pentru calcularea cifrei de control
def calculeaza_cifra_control(cnp_fara_control):
    cheie = "279146358279"
    suma = sum(int(cnp_fara_control[i]) * int(cheie[i]) for i in range(12))
    rest = suma % 11
    return "1" if rest == 10 else str(rest)

# Funcția pentru generarea unui CNP aleator
def selecteaza_judet_varsta(sex):
    print(f"[DEBUG] Începem selecția pentru un județ și o vârstă din distribuția de {sex.lower()}.")
    distributie = distributie_masculin if sex == 'M' else distributie_feminin

    try:
        # Selectăm aleator un județ
        judet = random.choice(list(distributie.keys()))
        print(f"[DEBUG] Județ selectat: {judet}")

        # Extragem lista de procente pentru vârste din județul selectat
        procente_varste = distributie[judet]

        # Selectăm aleator o categorie de vârstă pe baza distribuției
        varsta = random.choices(
            population=range(len(procente_varste)),
            weights=procente_varste,
            k=1
        )[0]

        # Convertim indexul la intervalul de vârstă corespunzător
        varste_intervale = ['0 - 4', '5 - 9', '10 - 14', '15 - 19', '20 - 24', '25 - 29',
                            '30 - 34', '35 - 39', '40 - 44', '45 - 49', '50 - 54',
                            '55 - 59', '60 - 64', '65 - 69', '70 - 74', '75 - 79',
                            '80 - 85', '85+']
        interval_varsta = varste_intervale[varsta]

        print(f"[DEBUG] Varsta selectată: {interval_varsta}")
        return judet, interval_varsta

    except Exception as e:
        print(f"[ERROR] A apărut o eroare la selecția județului și vârstei: {e}")
        return None, None
def genereaza_cnp_aleator():
    sex = random.choice(['M', 'F'])
    judet, varsta = selecteaza_judet_varsta(sex)
    print(f"[DEBUG] Selecție: Sex - {sex}, Județ - {judet}, Vârstă - {varsta}")

    varsta_interval = varsta.split(' - ')
    if len(varsta_interval) == 2:
        varsta_min = int(varsta_interval[0])
        varsta_max = int(varsta_interval[1])
    else:
        varsta_min = int(varsta_interval[0].replace('+', ''))
        varsta_max = varsta_min + 5

    an_nastere = datetime.now().year - random.randint(varsta_min, varsta_max)
    luna_nastere = random.randint(1, 12)
    zi_maxima = 28 if luna_nastere == 2 else 30 if luna_nastere in [4, 6, 9, 11] else 31
    zi_nastere = random.randint(1, zi_maxima)
    cod_judet = list(judete.keys())[list(judete.values()).index(judet)]
    print(f"[DEBUG] Generăm CNP pentru: An - {an_nastere}, Lună - {luna_nastere}, Zi - {zi_nastere}, Cod județ - {cod_judet}")
    return genereaza_cnp(sex, an_nastere, luna_nastere, zi_nastere, cod_judet)

# Generăm 1.000.000 de CNP-uri și le asociem nume
def genereaza_cnpuri(nr_cnpuri):
    cnpuri = []
    for _ in range(nr_cnpuri):
        cnp = genereaza_cnp_aleator()
        nume = random.choice(nume_masculin if cnp[0] in ['1', '5'] else nume_feminin)
        cnpuri.append({'CNP': cnp, 'Nume': nume})
    return cnpuri

# Salvare CNP-uri într-un fișier Excel
def salvare_cnpuri_in_excel(cnpuri, output_path):
    df = pd.DataFrame(cnpuri)
    df.to_excel(output_path, index=False)
    print(f"CNP-urile au fost salvate în {output_path}")


# Generăm structura hash pentru distribuția CNP-urilor cu verificare de unicitate
def genereaza_hash_cnpuri(nr_cnpuri):
    hash_table = {}
    while len(hash_table) < nr_cnpuri:
        cnp = genereaza_cnp_aleator()
        # Verificăm dacă CNP-ul există deja în hash_table pentru a evita dublurile
        if cnp not in hash_table:
            nume = random.choice(nume_masculin if cnp[0] in ['1', '5'] else nume_feminin)
            hash_table[cnp] = {'Nume': nume}
    return hash_table


# Funcția pentru căutarea a 1.000 de CNP-uri și măsurarea detaliată a timpului de căutare
def cauta_cnpuri(hash_table, nr_cnpuri_de_cautat=1000):
    cnpuri_existente = list(hash_table.keys())
    cnpuri_de_cautat = random.sample(cnpuri_existente, nr_cnpuri_de_cautat)

    # Liste pentru măsurători
    timpi_cautare = []
    iteratii_cautare = []

    for cnp in cnpuri_de_cautat:
        start_time = time.time()
        # Căutăm în hash_table și contorizăm căutarea ca 1 iterație
        num_iteratii = 1
        gasit = hash_table.get(cnp, None)

        # Măsurăm durata și adăugăm la liste
        timpi_cautare.append(time.time() - start_time)
        iteratii_cautare.append(num_iteratii)

    # Calculăm statistici pentru analiza performanței
    timp_mediu_cautare = sum(timpi_cautare) / len(timpi_cautare)
    nr_mediu_iteratii = sum(iteratii_cautare) / len(iteratii_cautare)

    # Afisăm statistici și le salvăm într-un DataFrame
    print(f"Timp mediu de căutare: {timp_mediu_cautare:.8f} secunde")
    print(f"Număr mediu de iterații: {nr_mediu_iteratii:.2f}")

    df_statistici = pd.DataFrame({
        'CNP': cnpuri_de_cautat,
        'Timp Cautare (secunde)': timpi_cautare,
        'Iteratii': iteratii_cautare
    })
    return df_statistici, timp_mediu_cautare, nr_mediu_iteratii

def executa_cautari_multiple(hash_table, num_runde=10, nr_cnpuri_de_cautat=1000):
    toate_statisticile = []

    for runda in range(1, num_runde + 1):
        print(f"[INFO] Începem runda {runda} de căutare")
        # Căutăm 1000 de CNP-uri și obținem statistici de performanță pentru fiecare rundă
        statistici_runda, timp_mediu, nr_mediu_iteratii = cauta_cnpuri(hash_table, nr_cnpuri_de_cautat)

        # Adăugăm rezultatele rundei curente la listă
        toate_statisticile.append({
            'Runda': runda,
            'Timp Mediu Cautare (secunde)': timp_mediu,
            'Nr. Mediu Iteratii': nr_mediu_iteratii
        })

    # Creăm DataFrame-ul final care va fi utilizat pentru analiza statistică și generarea graficelor
    df_statistici_runde = pd.DataFrame(toate_statisticile)
    print(df_statistici_runde)  # Afișează structura pentru verificare

    return df_statistici_runde
# Funcția pentru generarea graficelor de analiză a performanței
def genereaza_grafice_statistici(df_runde_statistici, output_folder):
    # Grafic de linie pentru timpul mediu de căutare în fiecare rundă
    plt.figure(figsize=(10, 5))
    plt.plot(df_runde_statistici['Runda'], df_runde_statistici['Timp Mediu Cautare (secunde)'], marker='o', linestyle='-')
    plt.title("Timpul Mediu de Căutare per Rundă")
    plt.xlabel("Runda")
    plt.ylabel("Timp Mediu de Căutare (secunde)")
    plt.grid(True)
    plt.savefig(f"{output_folder}/timp_mediu_cautare_per_runda.png")
    plt.show()

    # Grafic pentru media numărului de iterații per rundă
    plt.figure(figsize=(10, 5))
    plt.plot(df_runde_statistici['Runda'], df_runde_statistici['Nr. Mediu Iteratii'], marker='o', linestyle='-', color='orange')
    plt.title("Numărul Mediu de Iterații per Rundă")
    plt.xlabel("Runda")
    plt.ylabel("Numărul Mediu de Iterații")
    plt.grid(True)
    plt.savefig(f"{output_folder}/nr_mediu_iteratii_per_runda.png")
    plt.show()

    # Scatter plot pentru timpul de căutare în toate rundele pentru o vedere mai detaliată
    plt.figure(figsize=(10, 5))
    plt.scatter(df_runde_statistici['Runda'], df_runde_statistici['Timp Mediu Cautare (secunde)'], color='blue', label="Timp Mediu Cautare")
    plt.title("Distribuția Timpului Mediu de Căutare în Toate Rundele")
    plt.xlabel("Runda")
    plt.ylabel("Timp Mediu de Căutare (secunde)")
    plt.legend()
    plt.grid(True)
    plt.savefig(f"{output_folder}/scatter_timp_mediu_cautare.png")
    plt.show()




# Generăm structura hash pentru distribuția CNP-urilor și salvăm într-un fișier Excel
nr_total_cnpuri = 1_000_000
hash_table_cnpuri = genereaza_hash_cnpuri(nr_total_cnpuri)

# Salvăm toate CNP-urile generate într-un fișier Excel
output_path = r"C:\Users\Rares\Desktop\Python master anul I\CNP_Generate_Test.xlsx"
df_cnpuri = pd.DataFrame([{'CNP': cnp, 'Nume': data['Nume']} for cnp, data in hash_table_cnpuri.items()])
df_cnpuri.to_excel(output_path, index=False)
print(f"[INFO] CNP-urile au fost salvate în {output_path}")

# Rulăm 10 runde de căutare și măsurăm statisticile
df_runde_statistici = executa_cautari_multiple(hash_table_cnpuri, num_runde=10, nr_cnpuri_de_cautat=1000)

# Salvăm graficele pentru rundele multiple într-un folder specificat
output_folder = r"C:\Users\Rares\Desktop\Python master anul I"
genereaza_grafice_statistici(df_runde_statistici, output_folder)
print("[INFO] Graficele statistice au fost generate și salvate.")

# Căutăm și măsurăm statisticile pentru 1.000 de CNP-uri într-o rundă suplimentară
df_statistici, timp_mediu, nr_mediu_iteratii = cauta_cnpuri(hash_table_cnpuri, 1000)

# Salvăm rezultatele căutării suplimentare într-un fișier Excel
output_statistici_path = r"C:\Users\Rares\Desktop\Python master anul I\Statistici_Cautare_CNP.xlsx"
df_statistici.to_excel(output_statistici_path, index=False)
print(f"[INFO] Statistici de căutare salvate în {output_statistici_path}")
print(f"[INFO] Timp mediu de căutare: {timp_mediu:.8f} secunde")
print(f"[INFO] Număr mediu de iterații: {nr_mediu_iteratii:.2f}")

