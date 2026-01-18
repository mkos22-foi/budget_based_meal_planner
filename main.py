import constraint as cs
import hrana as fd
import random

def generiraj(budzet, kalorije, cilj):
    
    try:
        budzet = float(budzet)
        kalorije = float(kalorije)
    except ValueError:
        return "Unesite ispravne vrijednosti za budžet i kalorije!"

    
    meso = ["Piletina", "Puretina", "Govedina", "Svinjetina", "Tuna", "Losos", "Oslić", "Sardine", "Jaja"]
    ugljikohidrati = ["Riža", "Zobene pahuljice", "Tjestenina", "Krumpir", "Batat", "Kruh"]
    povrce_voce = ["Brokula", "Špinat", "Mrkva", "Tikvice", "Paprika", "Rajčica", "Banana", "Jabuka", "Borovnice", "Jagode", "Naranča"]
    masti_orasasto = ["Maslinovo ulje", "Kikiriki maslac", "Maslac", "Bademi", "Orasi"]

    rjesenje = None

    for pokusaj in range(100):
        kandidati = []

        kandidati.append(random.choice(meso))
        kandidati.append(random.choice(ugljikohidrati))
        kandidati.append(random.choice(masti_orasasto))
        broj_povrca = random.randint(1, 2)
        kandidati.extend(random.sample(povrce_voce, broj_povrca))

        problem = cs.Problem()

        for nam in kandidati:
            max_grama = fd.baza_namirnica[nam]["max"]

            if nam in meso:
                problem.addVariable(nam, range(100, max_grama + 1, 50))
            elif nam in masti_orasasto:
                problem.addVariable(nam, range(0, 50 + 1, 25))
            else:
                problem.addVariable(nam, range(0, max_grama + 1, 50))

            
        def func_budzet(*grams):
            ukupna_cijena = 0
            broj_namirnica = len(grams)
            for i in range(broj_namirnica):
                tezina = grams[i]
                ime = kandidati[i]
                cijena = fd.izracunaj_cjenu(ime, tezina)
                ukupna_cijena += cijena
            if ukupna_cijena <= budzet:
                return True
            else:
                return False
            
        problem.addConstraint(func_budzet, kandidati)
                
        def func_kalorije(*grams):
            ukupno_kcal = 0
            broj_namirnica = len(grams)
            for i in range(broj_namirnica):
                tezina = grams[i]       
                ime = kandidati[i]         
                kcal_100g = fd.baza_namirnica[ime]['kcal']    
                kcal_stavke = (kcal_100g / 100) * tezina        
                ukupno_kcal += kcal_stavke                 
                
            if (kalorije-50) <= ukupno_kcal <= (kalorije+50):  
                return True
            else:
                return False
        problem.addConstraint(func_kalorije, kandidati)
                
        def func_macros(*grams):
            p_grama = 0 
            u_grama = 0 
            m_grama = 0
            broj_namirnica = len(grams)
            for i in range(broj_namirnica):
                tezina = grams[i]
                ime = kandidati[i]
                podaci = fd.baza_namirnica[ime]
                faktor = tezina / 100
                p_grama += (podaci['P'] * faktor)   
                u_grama += (podaci['U'] * faktor)  
                m_grama += (podaci['M'] * faktor)  
            
            kcal_p = p_grama * 4
            kcal_u = u_grama * 4
            kcal_m = m_grama * 9
            total = kcal_p + kcal_u + kcal_m
                
            if total == 0: 
                return False

            udio_p = kcal_p / total   
            udio_u = kcal_u / total    
            udio_m = kcal_m / total  

            if cilj == "Mršavljenje":
                min_P = 0.35
                max_P = 0.45
                
                min_U = 0.30
                max_U = 0.50
                
                min_M = 0.10
                max_M = 0.30

            else:
                min_P = 0.25
                max_P = 0.35
                
                min_U = 0.30
                max_U = 0.50
                
                min_M = 0.20
                max_M = 0.40

            if udio_p < min_P or udio_p > max_P:
                return False
                
            if udio_u < min_U or udio_u > max_U:
                return False

            if udio_m < min_M or udio_m > max_M:
                return False

            return True
        
        problem.addConstraint(func_macros, kandidati)
            

        def func_balans(*grams):
            ime_mesa = kandidati[0]
            ime_ugljiko = kandidati[1]
            ime_masti = kandidati[2]
            
            tezina_masti = grams[2] 

            if ime_mesa == "Svinjetina":
                if tezina_masti > 25:
                    return False

            if ime_ugljiko == "Zobene pahuljice":
                if ime_mesa != "Jaja":
                    return False

            if ime_masti == "Kikiriki maslac":
                if ime_mesa in ["Tuna", "Losos", "Oslić", "Sardine", "Svinjetina", "Govedina"]:
                    return False
                if ime_ugljiko not in ["Zobene pahuljice", "Kruh", "Batat"]:
                    return False

            if ime_mesa == "Tuna" and ime_masti == "Maslac":
                 return False

            return True

        problem.addConstraint(func_balans, kandidati)

        
        rjesenje = problem.getSolution()

        if rjesenje:
            break 

    if rjesenje:
        tekst_ispisa = ""
        tekst_ispisa += "GENERIRANI OBROK:\n"
        tekst_ispisa += "-------------------------------------------------------------\n"
        
        ukupna_cijena = 0; ukupno_kcal = 0
        ukupno_P = 0; ukupno_U = 0; ukupno_M = 0

        for namirnica in rjesenje:
            gramaza = rjesenje[namirnica]

            if gramaza == 0:
                continue  

            cijena = fd.izracunaj_cjenu(namirnica, gramaza)
            podaci = fd.baza_namirnica[namirnica]
            kcal = (podaci['kcal'] / 100) * gramaza
            
            tekst_ispisa += f"- {namirnica}: {gramaza}g ({cijena:.2f} €) - {int(kcal)} kcal\n"


            ukupna_cijena += cijena
            ukupno_kcal += kcal
            ukupno_P += (podaci['P']/100)*gramaza
            ukupno_U += (podaci['U']/100)*gramaza
            ukupno_M += (podaci['M']/100)*gramaza

        tekst_ispisa += "-------------------------------------------------------------\n"
        tekst_ispisa += f"UKUPNO: {ukupna_cijena:.2f} € | {int(ukupno_kcal)} kcal\n"
        tekst_ispisa += f"MAKROSI: P: {int(ukupno_P)}g | U: {int(ukupno_U)}g | M: {int(ukupno_M)}g"
        
        return tekst_ispisa 

    else:
        return "Nisam uspio složiti obrok....\nProbajte promijeniti budžet ili kalorije"
