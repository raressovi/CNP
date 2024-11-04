import pandas as pd
import random

def citire_distributie_populatie(file_path):
    """
    Citește fișierul Excel de la calea specificată și returnează un DataFrame cu datele.
    """
    try:
        # Citim datele din fișierul Excel
        print(f"[DEBUG] Încercăm să citim datele din fișierul: {file_path}")
        df = pd.read_excel(file_path)
        print(f"[DEBUG] Datele au fost citite cu succes din {file_path}.")
        print(f"[DEBUG] Coloanele disponibile în DataFrame sunt: {df.columns.tolist()}")
        return df
    except Exception as e:
        print(f"[ERROR] A apărut o eroare la citirea fișierului Excel: {e}")
        return None


def selecteaza_judet_si_varsta(distributie_df):
    """
    Selectează aleator un județ și o vârstă din distribuția dată.
    """
    try:
        print("[DEBUG] Începem selecția pentru un județ și o vârstă.")

        # Selectăm un județ aleator din lista disponibilă
        judet = random.choice(distributie_df['JUDET'])
        print(f"[DEBUG] Județ selectat: {judet}")

        # Selectăm aleator o grupă de vârstă bazată pe procentele din coloane
        varste = distributie_df.columns[1:]  # Ignorăm coloana 'JUDET'
        procente = distributie_df[distributie_df['JUDET'] == judet].iloc[0, 1:]

        # Normalizăm procentele (dacă nu sunt deja între 0 și 1)
        procente = procente.str.replace('%', '').astype(float)
        procente /= procente.sum()  # Asigurăm că suma este 1

        # Selectăm grupa de vârstă bazată pe distribuția procentuală
        grupa_varsta = random.choices(varste, weights=procente, k=1)[0]
        print(f"[DEBUG] Grupa de vârstă selectată: {grupa_varsta}")

        return judet, grupa_varsta
    except Exception as e:
        print(f"[ERROR] A apărut o eroare la selecția județului și vârstei: {e}")
        return None, None

# Exemple de utilizare
if __name__ == "__main__":
    file_path_masculin = "C:\\Users\\Rares\\Desktop\\Python master anul I\\Masculin.xlsx"
    file_path_feminin = "C:\\Users\\Rares\\Desktop\\Python master anul I\\Feminin.xlsx"

    # Citim distribuțiile pentru masculin și feminin
    print("[DEBUG] Citim distribuția de populație pentru masculin.")
    distributie_masculin = citire_distributie_populatie(file_path_masculin)

    print("[DEBUG] Citim distribuția de populație pentru feminin.")
    distributie_feminin = citire_distributie_populatie(file_path_feminin)

    # Exemplu de selecție a unui județ și a unei vârste din distribuția de masculin
    if distributie_masculin is not None:
        print("[DEBUG] Începem selecția pentru un județ și o vârstă din distribuția de masculin.")
        judet, varsta = selecteaza_judet_si_varsta(distributie_masculin)
        print(f"[DEBUG] Rezultatul selecției: Județ - {judet}, Vârstă - {varsta}")
