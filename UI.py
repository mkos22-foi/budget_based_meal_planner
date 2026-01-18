from customtkinter import *
import customtkinter
import main

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.title('Obrok Generator')
root.geometry('1400x1000') 
root.resizable(False, False)

def generiranje():
    budzet = entBudzet.get()
    kalorije = entKalorije.get()
    cilj = optCilj.get()
    
    txtIzlaz.delete("0.0", "end")
    txtIzlaz.insert("0.0", "Računam, pričekajte trenutak...\n")
    root.update() 

    rezultat_tekst = main.generiraj(budzet, kalorije, cilj)
    
    txtIzlaz.delete("0.0", "end") 
    txtIzlaz.insert("0.0", rezultat_tekst)


root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)


lblNaslov = customtkinter.CTkLabel(root, text="IDEALAN OBROK", font=("Ubuntu", 60, "bold"))
lblNaslov.grid(row=0, column=0, columnspan=2, pady=(50, 60))


lblBudzet = customtkinter.CTkLabel(root, text="Budžet:", font=("Ubuntu", 30))
lblBudzet.grid(row=1, column=0, pady=10, sticky="e", padx=20)

entBudzet = customtkinter.CTkEntry(root, placeholder_text="npr. 1.5", 
                                   height=60, width=400, font=("Ubuntu", 30))
entBudzet.grid(row=1, column=1, pady=10, sticky="w", padx=20)


lblKalorije = customtkinter.CTkLabel(root, text="Kalorije:", font=("Ubuntu", 30))
lblKalorije.grid(row=2, column=0, pady=10, sticky="e", padx=20)

entKalorije = customtkinter.CTkEntry(root, placeholder_text="npr. 700", 
                                     height=60, width=400, font=("Ubuntu", 30))
entKalorije.grid(row=2, column=1, pady=10, sticky="w", padx=20)


lblCilj = customtkinter.CTkLabel(root, text="Cilj:", font=("Ubuntu", 30))
lblCilj.grid(row=3, column=0, pady=10, sticky="e", padx=20)

optCilj = customtkinter.CTkComboBox(root, values=["Mršavljenje", "Održavanje", "Masa"],
                                    height=60, width=400, font=("Ubuntu", 30),
                                    state="readonly")
optCilj.set("Mršavljenje") 
optCilj.grid(row=3, column=1, pady=10, sticky="w", padx=20)


btnGeneriraj = customtkinter.CTkButton(root, text="PRONAĐI", width=500, height=80, font=("Ubuntu", 35, "bold"), 
                                       fg_color="blue", command=generiranje) 
btnGeneriraj.grid(row=4, column=0, columnspan=2, pady=50)


txtIzlaz = customtkinter.CTkTextbox(root, width=1200, height=350, 
                                    font=("Ubuntu", 30)) 
txtIzlaz.grid(row=5, column=0, columnspan=2, pady=20)


root.mainloop()