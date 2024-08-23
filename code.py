import customtkinter as ctk
import os
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox, ttk, IntVar
import csv
import mysql.connector
from datetime import datetime
from datetime import date
import locale
from tkinter import simpledialog

# Set locale to French for date and time
locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

# Configuration de la connexion à la base de données MySQL
connection_params = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "python_project",
}

def CenterWindowToDisplay(Screen: ctk, width: int, height: int, scale_factor: float = 1.0):
    """Centers the window to the main display/monitor"""
    screen_width = Screen.winfo_screenwidth()
    screen_height = Screen.winfo_screenheight()
    x = int(((screen_width/2) - (width/2)) * scale_factor)
    y = int(((screen_height/2) - (height/1.5)) * scale_factor)
    return f"{width}x{height}+{x}+{y}"
def get_stock_data():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password= "",
        database="python_project"
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM articles")
    data = mycursor.fetchall()
    mydb.close()
    return data

def get_total_articles():
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='python_project'
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT COUNT(*) FROM articles")
    result = mycursor.fetchone()
    total_articles = result[0]
    mydb.close()
    return total_articles

def get_total_providers():
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='python_project'
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT COUNT(*) FROM fournisseur")
    result = mycursor.fetchone()
    total_providers = result[0]
    mydb.close()
    return total_providers
def get_total_users():
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='python_project'
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT COUNT(*) FROM categorie")
    result = mycursor.fetchone()
    total_users = result[0]
    mydb.close()
    return total_users

def greet_users():
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='python_project'
    )
    # mycursor = mydb.cursor()
    # name = 'Saki'
    # query = mycursor.execute(f"SELECT usr_name FROM users WHERE usr_name= 'Saki'")
    # #current_user = mycursor.fetchone()

    # mydb.close()
    # return query


def get_product_ids():
    try:
        db = mysql.connector.connect(**connection_params)
        cursor = db.cursor()
        cursor.execute("SELECT id FROM articles")
        ids = [str(row[0]) for row in cursor.fetchall()]  
        db.close()
        return ids
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur s'est produite lors de la récupération des IDs: {e}")
        return []


def get_product_categories():
    try:
        db = mysql.connector.connect(**connection_params)
        cursor = db.cursor()
        cursor.execute("SELECT nom_categorie FROM categorie")
        categories = [str(row[0]) for row in cursor.fetchall()]  
        db.close()
        return categories
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur s'est produite lors de la récupération des Categories: {e}")
        return []


def get_product_fournisseur():
    try:
        db = mysql.connector.connect(**connection_params)
        cursor = db.cursor()
        cursor.execute("SELECT nom_fournisseur FROM fournisseur")
        fournisseur = [str(row[0]) for row in cursor.fetchall()]  
        db.close()
        return fournisseur
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur s'est produite lors de la récupération des fournisseurs: {e}")
        return []
    
# Fonction pour ajouter un produit à la base de données MySQl
def ajouter_article(entry_nom, dropdown_categories, dropdown_fournisseurs, entry_prix, quantity_var):
    nom_article = entry_nom.get()
    categorie = dropdown_categories.get()
    fournisseur = dropdown_fournisseurs.get()
    prix = entry_prix.get()
    quantite_en_stock = int(quantity_var.get())

    try:
        conn = mysql.connector.connect(**connection_params)
        cursor = conn.cursor()

        # Insertion dans la table fournisseur
        cursor.execute("INSERT INTO fournisseur (nom_fournisseur) VALUES (%s)", (fournisseur,))
        conn.commit()  

        cursor.execute("SELECT id FROM fournisseur WHERE nom_fournisseur = %s", (fournisseur,))
        id_fournisseur = cursor.fetchone()
        if id_fournisseur is not None:
            id_fournisseur = id_fournisseur[0]

        # Insertion dans la table categorie
        cursor.execute("INSERT  INTO categorie (nom_categorie) VALUES (%s)", (categorie,))
        conn.commit() 

        cursor.execute("SELECT id FROM categorie WHERE nom_categorie = %s", (categorie,))
        id_categorie = cursor.fetchone()
        if id_categorie is not None:
            id_categorie = id_categorie[0]

        # Insertion dans la table articles
        cursor.execute("INSERT INTO articles (produit, prix, quantity, id_fournisseur, id_categorie) VALUES (%s, %s, %s, %s, %s)",
                       (nom_article, prix, quantite_en_stock, id_fournisseur, id_categorie))
        conn.commit() 

        messagebox.showinfo("Succès", "Article ajouté avec succès!")
    except mysql.connector.Error as err:
        messagebox.showerror("Erreur", f"Une erreur s'est produite lors de l'ajout: {err}")
    finally:
        cursor.close()
        conn.close()

def ajouter_categorie():
    nom_categorie = simpledialog.askstring("Ajouter Catégorie", "Nom de la catégorie:")
    if nom_categorie:
        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='python_project'
            )
            cursor = conn.cursor()
            cursor.execute("INSERT INTO categorie (nom_categorie) VALUES (%s)", (nom_categorie,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Succès", "Categorie ajouté avec succès!")
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite lors de l'ajout de la categorie: {e}")


def ajouter_fournisseur():
    nom_fournisseur = simpledialog.askstring("Ajouter Fournisseur", "Nom du Fournisseur:")
    if nom_fournisseur:
        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='python_project'
            )
            cursor = conn.cursor()
            cursor.execute("INSERT INTO fournisseur (nom_fournisseur) VALUES (%s)", (nom_fournisseur,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Succès", "Fournisseur ajouté avec succès!")
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite lors de l'ajout du Fournisseur: {e}")


    
def fill_product_details(event):
    
    selected_id = event.widget.get()
    print(f"Détails du produit pour l'ID : {selected_id}")

def fill_modify_details(event):
    
    selected_product = event.widget.get()
    print(f"Détails du produit pour l'ID : {selected_product}")


# Fonction pour modifier un produit existant dans la base de données MySQL
def modifier_produit(entry_id, entry_name, entry_price, quantity_var, entry_fournisseur, entry_categorie):
    article_id = entry_id.get()
    name = entry_name.get()
    price = entry_price.get()
    quantity = quantity_var.get()
    fournisseur_name = entry_fournisseur.get()
    categorie_name = entry_categorie.get()

    try:
        db = mysql.connector.connect(**connection_params)
        cursor = db.cursor()

        # Update article table
        cursor.execute("UPDATE articles SET produit=%s, prix=%s, quantity=%s WHERE id=%s",
                       (name, price, quantity, article_id))

        # Update fournisseur table
        cursor.execute("UPDATE fournisseur SET nom_fournisseur=%s WHERE id=(SELECT id_fournisseur FROM articles WHERE id=%s)",
                       (fournisseur_name, article_id))

        # Update categorie table
        cursor.execute("UPDATE categorie SET nom_categorie=%s WHERE id=(SELECT id_categorie FROM articles WHERE id=%s)",
                       (categorie_name, article_id))

        db.commit()
        db.close()
        messagebox.showinfo("Succès", "Article modifié avec succès!")
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur s'est produite: {e}")

    
def modifier_fournisseur(entry_id, entry_modify):
    id = entry_id.get()
    fournisseur = entry_modify.get()

    try:
        db = mysql.connector.connect(**connection_params)
        cursor = db.cursor()
        cursor.execute("UPDATE fournisseur SET nom_fournisseur=%s WHERE id=%s", (fournisseur, id))
        db.commit()
        db.close()
        messagebox.showinfo("Succès", "Fournisseur modifié avec succès!")
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur s'est produite: {e}")
     

def modifier_categorie(entry_id, entry_modify):
    id = entry_id.get()
    categorie = entry_modify.get()

    try:
        db = mysql.connector.connect(**connection_params)
        cursor = db.cursor()
        cursor.execute("UPDATE categorie SET nom_categorie=%s WHERE id=%s", (categorie, id))
        db.commit()
        db.close()
        messagebox.showinfo("Succès", "Categorie modifié avec succès!")
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur s'est produite: {e}")

# Fonction pour supprimer l'enregistrement de la base de données
def delete_record(entry_id, entry_delete):
    table = entry_delete.get().strip()
    record_id = entry_id.get().strip()
    
    if not table:
        messagebox.showerror("Erreur", "Veuillez sélectionner une table.")
        return
    
    if not record_id:
        messagebox.showerror("Erreur", "Veuillez entrer un ID.")
        return
    
    try:
        record_id = int(record_id)
    except ValueError:
        messagebox.showerror("Erreur", "Veuillez entrer un ID valide.")
        return

    try:
        db = mysql.connector.connect(**connection_params)
        cursor = db.cursor()

        sql_query = f"DELETE FROM {table} WHERE id = %s"
        cursor.execute(sql_query, (record_id,))
        db.commit()

        if cursor.rowcount == 0:
            messagebox.showinfo("Information", "Aucun enregistrement trouvé avec cet ID.")
        else:
            messagebox.showinfo("Succès", "Enregistrement supprimé avec succès.")

    except mysql.connector.Error as err:
        messagebox.showerror("Erreur", f"Erreur lors de la suppression de l'enregistrement: {err}")
    finally:
        cursor.close()
        db.close()
    
# Fonctionnalités pour importer et exporter des fichiers CSV
def exporter():
    try:
        filepath = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not filepath:
            return

        db = mysql.connector.connect(**connection_params)
        cursor = db.cursor()

        tables = {
            "articles": ["ID", "Prix", "Produit", "Quantité", "Categorie", "Fournisseur"],
            "fournisseur": ["ID", "Nom_Fournisseur"],
            "categorie": ["ID", "Nom_Categorie"]
        }

        with open(filepath, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            for table, headers in tables.items():
                cursor.execute(f"SELECT * FROM {table}")
                data = cursor.fetchall()


                writer.writerow([f"Table: {table}"])
                writer.writerow(headers)

            
                writer.writerows(data)

            
                writer.writerow([])

        db.close()

        messagebox.showinfo("Succès", "Données exportées avec succès!")
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur s'est produite lors de l'exportation: {e}")

def importer():
    try:
        filepath = filedialog.askopenfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not filepath:
            return

        # Lire le fichier CSV et organiser les données par table
        table_data = {
            "articles": [],
            "fournisseur": [],
            "categorie": []
        }

        current_table = None
        headers = None

        with open(filepath, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            
            for row in reader:
                if row and row[0].startswith("Table:"):
                    current_table = row[0].split(":")[1].strip()
                    headers = next(reader, None)
                elif current_table and headers:
                    table_data[current_table].append(row) 

        db = mysql.connector.connect(**connection_params)
        cursor = db.cursor()

        # Supprimer les enregistrements existants
        for table in table_data.keys():
            cursor.execute(f"DELETE FROM {table}")
          

        # Insérer les nouvelles données
        for table, rows in table_data.items():
            if table == "articles":
                query = "INSERT INTO articles (id, prix, produit, quantity, id_categorie, id_fournisseur) VALUES (%s, %s, %s, %s, %s, %s)"
            elif table == "fournisseur":
                query = "INSERT INTO fournisseur (id, nom_fournisseur) VALUES (%s, %s)"
            elif table == "categorie":
                query = "INSERT INTO categorie (id, nom_categorie) VALUES (%s, %s)"

            for row in rows: 
                try:
                    cursor.execute(query, row)
                except mysql.connector.Error as err:
                    print(f"Error inserting row {row} into table {table}: {err}")

        db.commit()
        db.close()

        messagebox.showinfo("Succès", "Données importées avec succès!")
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur s'est produite lors de l'importation: {e}")
def afficher_produits(frame):
    try:
        db = mysql.connector.connect(**connection_params)
        cursor = db.cursor()
        cursor.execute("""
            SELECT articles.id, articles.produit, articles.prix, articles.quantity, categorie.nom_categorie, fournisseur.nom_fournisseur
            FROM articles 
            JOIN categorie categorie ON articles.id_categorie = categorie.id
            JOIN fournisseur fournisseur ON articles.id_fournisseur = fournisseur.id
        """)
        rows = cursor.fetchall()
        db.close()

        columns = ("ID", "Nom", "Prix", "Quantité", "Categorie", "Fournisseur")

        tree = ttk.Treeview(frame, columns=columns, show='headings')
        tree.heading("ID", text="ID")
        tree.heading("Nom", text="Nom")
        tree.heading("Prix", text="Prix")
        tree.heading("Quantité", text="Quantité")
        tree.heading("Categorie", text="Categorie")
        tree.heading("Fournisseur", text="Fournisseur")

        for row in rows:
            tree.insert("", "end", values=row)

        tree.pack(expand=True, fill='both')
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur s'est produite lors de l'affichage des produits: {e}")
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Stocky votre Gestionnaire de Stocks")
        self.geometry(f"{1280}x{600}")
        self.config(background='white')

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        self.logo_image = ctk.CTkImage(Image.open(os.path.join(image_path, "stock.png")), size=(200, 250))

        # create navigation frame
        self.frame_1 = ctk.CTkFrame(master=self,corner_radius=15, fg_color="#245263",height=100)
        self.frame_1.grid(padx=20, pady=20, row=0, column=0,)
        self.frame_1.grid_rowconfigure(0, weight=1)
        self.frame_1.grid_columnconfigure(0, weight=1)

        self.navigation_frame = ctk.CTkFrame(self.frame_1, corner_radius=15, fg_color="#245263")
        self.navigation_frame.grid(row=0, column=0, padx=10, pady=10,)

        
        self.acceuil_button = ctk.CTkButton(self.navigation_frame, corner_radius=10, height=40, border_spacing=10, text="Acceuil",
                                            anchor="center", fg_color="#245263", font=ctk.CTkFont(size=20, weight="bold"), text_color='white',
                                            command=self.acceuil_button_event)
        self.acceuil_button.grid(row=0, column=0, sticky="ew", padx=15, pady=15)

        self.ajouter_button = ctk.CTkButton(self.navigation_frame, corner_radius=10, height=40, border_spacing=10, text="Ajouter",
                                            font=ctk.CTkFont(size=20, weight="bold"), text_color='white', fg_color="#245263",
                                            anchor="center", command=self.ajouter_button_event)
        self.ajouter_button.grid(row=1, column=0,padx=15, pady=15, sticky="ew")

        self.modifier_button = ctk.CTkButton(self.navigation_frame, corner_radius=10, height=40, border_spacing=10, text="Modifier",
                                             font=ctk.CTkFont(size=20, weight="bold"), text_color='white', fg_color="#245263",
                                             anchor="center", command=self.modifier_button_event)
        self.modifier_button.grid(row=2, column=0,padx=15, pady=15, sticky="ew")

        self.supprimer_button = ctk.CTkButton(self.navigation_frame, corner_radius=10, height=40, border_spacing=10, text="Supprimer",
                                              font=ctk.CTkFont(size=20, weight="bold"), text_color='white', fg_color="#245263",
                                              anchor="center", command=self.supprimer_button_event)
        self.supprimer_button.grid(row=3, column=0,padx=15, pady=15, sticky="ew")

        # create home frame
        self.acceuil_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="white")
        current_date = ctk.CTkLabel(self.acceuil_frame,text=date.today().strftime("%A %d %B %Y"), bg_color='white',font=ctk.CTkFont(size=20))
        current_date.pack()
        current_date.place(x=850, y=22)

        user_greetings= ctk.CTkLabel(self.acceuil_frame, text=f'Bienvenu Sur Stocky !',font= ctk.CTkFont(size=20, weight='bold'), text_color="#245263", fg_color='white',bg_color='white')
        user_greetings.pack(pady=20)


        db_host = "localhost"
        db_user = "root"
        db_password = "python_project"

        stock_data = get_stock_data()

        screen_1 = ctk.CTkFrame(master=self.acceuil_frame, width=225, height= 125, fg_color='#245263',corner_radius=12, bg_color='white')
        screen_1.pack(side= 'top')
        screen_1.place(x=95, y=80)
        total_art = get_total_articles()
        total_articles = ctk.CTkLabel(screen_1, text=f"Total Articles \n\n {total_art}", font=ctk.CTkFont(size=20, weight="bold"), text_color='white')
        total_articles.pack(in_= screen_1, pady=28, padx= 40)


        screen_2 = ctk.CTkFrame(master=self.acceuil_frame, width=225, height= 125, border_color='black', border_width=1, fg_color='#245263',corner_radius=12, bg_color='white')
        screen_2.pack()
        screen_2.place(x=400, y=80)
        total_provd = get_total_providers()
        total_providers = ctk.CTkLabel(screen_2, text=f"Total Fournisseurs \n\n {total_provd}", font=ctk.CTkFont(size=20, weight="bold"), text_color='white')
        total_providers.pack(in_= screen_2, pady=28, padx= 40)

        screen_3 = ctk.CTkFrame(master=self.acceuil_frame, width=225, height= 125, border_color='black', border_width=1, fg_color='#245263',corner_radius=12, bg_color='white')
        screen_3.pack()
        screen_3.place(x=750, y=80)
        total_usrs = get_total_users()
        total_providers = ctk.CTkLabel(screen_3, text=f"Total Categories \n\n {total_usrs}", font=ctk.CTkFont(size=20, weight="bold"), text_color='white')
        total_providers.pack(in_= screen_3, pady=28, padx= 40)

        table_column = ['ID','Price','Article', 'Quantity','ID_Categorie']
        scrollbar = ttk.Scrollbar()
        table = ttk.Treeview(self.acceuil_frame, show="headings",columns=table_column, height=12, yscrollcommand=scrollbar)

        for col in table_column:
            #table.heading(col, text=col)
            table.heading(col, text=col)
            table.column(col, width=180, anchor="center")

        for row in stock_data:
            table.insert('', 'end', values=row)

        self.tk.call("source", "azure.tcl")
        self.tk.call("set_theme", "light")

        table.pack()
        table.place(x=90,y=220)

        import_button = ctk.CTkButton(self.acceuil_frame,text='Import',command=importer,  fg_color= '#245263', bg_color='white', width=100)
        import_button.pack()
        import_button.place(x=760, y=550)

        export_button = ctk.CTkButton(self.acceuil_frame,text='Export',command=exporter,  fg_color= '#245263', bg_color='white', width=100)
        export_button.pack()
        export_button.place(x=900, y=550)

         # create second frame
        self.second_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="white")

        label = ctk.CTkLabel(self.second_frame, text="Ajouter un nouvel article", text_color="#245263", font=ctk.CTkFont(size=20, weight="bold"))
        label.pack(pady=20, padx=20)

        locale.setlocale(locale.LC_TIME, 'fr_FR.utf8')

        date_str = datetime.now().strftime("%A %d %B %Y")
        date_label = ctk.CTkLabel(self.second_frame, text=date_str.capitalize(), text_color="#245263", font=ctk.CTkFont(size=20))
        date_label.place(x=850, y=20)

        frame_entries = ctk.CTkFrame(self.second_frame, height=450, width=300, fg_color="white", border_width=1, corner_radius=10)
        frame_entries.pack(side="left", padx=(80, 40), pady=50)
        frame_entries.grid_propagate(False)

        label_nom = ctk.CTkLabel(frame_entries, text="Nom:",text_color="#245263", font=ctk.CTkFont(size=15, weight="bold"))
        label_nom.grid(row=0, column=0, padx=20, pady=5, sticky="w")
        entry_nom = ctk.CTkEntry(frame_entries, width=150)
        entry_nom.grid(row=1, column=0, padx=25, pady=5, sticky="ew")

        label_categories = ctk.CTkLabel(frame_entries, text="Catégorie:",text_color="#245263", font=ctk.CTkFont(size=15, weight="bold"))
        label_categories.grid(row=2, column=0, padx=20, pady=5, sticky="w")
        dropdown_categories = ctk.CTkComboBox(frame_entries, values=' ')  
        dropdown_categories.grid(row=3, column=0, padx=25, pady=5, sticky="ew")

        label_fournisseurs = ctk.CTkLabel(frame_entries, text="Fournisseur:",text_color="#245263", font=ctk.CTkFont(size=15, weight="bold"))
        label_fournisseurs.grid(row=4, column=0, padx=20, pady=5, sticky="w")
        dropdown_fournisseurs = ctk.CTkComboBox(frame_entries, values=' ')
        dropdown_fournisseurs.grid(row=5, column=0, padx=25, pady=5, sticky="ew")

        label_prix = ctk.CTkLabel(frame_entries, text="Prix:",text_color="#245263", font=ctk.CTkFont(size=15, weight="bold"))
        label_prix.grid(row=6, column=0, padx=20, pady=5, sticky="w")
        entry_prix = ctk.CTkEntry(frame_entries, width=90)
        entry_prix.grid(row=7, column=0, padx=25, pady=5, sticky="ew")

        label_quantity = ctk.CTkLabel(frame_entries, text="Quantité:", text_color="#245263", font=ctk.CTkFont(size=15, weight="bold"))
        label_quantity.grid(row=8, column=0, padx=13, pady=13, sticky="w")

        frame_quantity = ctk.CTkFrame(frame_entries, fg_color='white')
        frame_quantity.grid(row=9, column=0, padx=25, pady=2, sticky="ew")

       
        quantity_vars = IntVar(value=1)

        entry_quantity = ctk.CTkEntry(frame_quantity, textvariable=quantity_vars, width=50)
        entry_quantity.pack(side="left")

        # Fonction pour incrémenter la quantité
        def increment_quantity():
            quantity_vars.set(quantity_vars.get() + 1)

        # Fonction pour décrémenter la quantité
        def decrement_quantity():
            if quantity_vars.get() > 0: 
                quantity_vars.set(quantity_var.get() - 1)

       
        btn_incrementer = ctk.CTkButton(frame_quantity, text="+", command=increment_quantity, width=30, fg_color="#245263")
        btn_incrementer.pack(side="left", padx=5)

       
        btn_decrementer = ctk.CTkButton(frame_quantity, text="-", command=decrement_quantity, width=30, fg_color="#245263")
        btn_decrementer.pack(side="left", padx=5)


        btn_ajouter_second_frame = ctk.CTkButton(frame_entries, text="Ajouter", command=lambda:ajouter_article(entry_nom,dropdown_categories,dropdown_fournisseurs,entry_prix,quantity_var), width=50, fg_color="#245263")
        btn_ajouter_second_frame.grid(row=10, column=1, columnspan=2, padx=30, pady=2)

        label_info = ctk.CTkLabel(self.second_frame, text="")
        label_info.pack(pady=10)

        frame_labels = ctk.CTkFrame(self.second_frame, width=200, height=400, corner_radius=20, fg_color="white",border_width=1, border_color='black')
        frame_labels.pack(side="top", anchor="e", padx=(0, 150), pady=(60, 10))

        frame_image_text = ctk.CTkFrame(frame_labels, fg_color="white")
        frame_image_text.pack(pady=10, padx=10, side="left")

        image_path = "images/mascot.jpg"
        image = Image.open(image_path)
        image = image.resize((200, 250), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)

        label_image = ctk.CTkLabel(frame_image_text, image=photo, text='', fg_color='white')
        label_image.pack(side="left", padx=10)

        label_text = ctk.CTkLabel(frame_image_text, text="Un nouvel \narticle?  \nStocky le gère \npour vous!", fg_color="white", text_color="#245263", font=ctk.CTkFont(size=20, weight="bold"))
        label_text.pack(side="right", padx=15)

        buttons_frames = ctk.CTkFrame(self.second_frame, height=40, width=50, fg_color='white')
        buttons_frames.pack(side="top", pady=50, padx=30)

        btn_ajouter_categorie = ctk.CTkButton(buttons_frames, text="Ajouter Catégorie",command=ajouter_categorie,width=150, fg_color="#245263")
        btn_ajouter_categorie.grid(row=0, column=0, padx=10, pady=5)

        btn_ajouter_fournisseur = ctk.CTkButton(buttons_frames, text="Ajouter Fournisseur",command=ajouter_fournisseur,width=150, fg_color="#245263")
        btn_ajouter_fournisseur.grid(row=0, column=1, padx=10, pady=5)

        frame_buttons = ctk.CTkFrame(self.second_frame, height=40, width=50, fg_color='white')
        frame_buttons.pack(side="top", pady=25, padx=10)

        btn_exporter = ctk.CTkButton(frame_buttons, text="Exporter", command=exporter, height=30, width=50, fg_color="#245263")
        btn_exporter.grid(row=0, column=0, padx=10)

        btn_importer = ctk.CTkButton(frame_buttons, text="Importer", command=importer, height=30, width=50, fg_color="#245263")
        btn_importer.grid(row=0, column=1, padx=10)

        # create third frame
        self.third_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="white")

        label_title = ctk.CTkLabel(self.third_frame, text="Modifier un article", text_color="#245263", font=ctk.CTkFont(size=30, weight="bold"))
        label_title.pack(padx=5, pady=5)

        def get_current_date():
            return datetime.now().strftime("%A %d, %B %Y")



        
        date_frame = ctk.CTkFrame(self.third_frame, fg_color='white', corner_radius=10)
        date_frame.pack(anchor="ne", padx=0, pady=5)

        label_date = ctk.CTkLabel(date_frame, text=get_current_date(), font=ctk.CTkFont(size=20, weight="bold"), bg_color="transparent",text_color="#245263")
        label_date.pack(padx=5, pady=5)

        
        
        
        form_frame = ctk.CTkFrame(self.third_frame, corner_radius=10, fg_color='white', border_width=1, border_color='black')
        form_frame.pack(side="left", fill="both", padx=10, pady=(10,10))

        
        label_id = ctk.CTkLabel(form_frame, text="ID",text_color="#245263",font=ctk.CTkFont(size=15, weight="bold"))
        label_price = ctk.CTkLabel(form_frame, text="Prix:",text_color="#245263",font=ctk.CTkFont(size=15, weight="bold"))
        label_name = ctk.CTkLabel(form_frame, text="Nom :",text_color="#245263",font=ctk.CTkFont(size=15, weight="bold"))
        label_categorie = ctk.CTkLabel(form_frame, text="Catégorie:",text_color="#245263",font=ctk.CTkFont(size=15, weight="bold"))
        label_fournisseur = ctk.CTkLabel(form_frame, text="Fournisseur:",text_color="#245263",font=ctk.CTkFont(size=15, weight="bold"))

        
        entry_id = ctk.CTkComboBox(form_frame, values=get_product_ids(),corner_radius=8, fg_color='white', border_width=2, width=150, height=35)
        entry_id.bind("<<ComboboxSelected>>", fill_product_details)
        entry_price = ctk.CTkEntry(form_frame, corner_radius=8, fg_color='white', border_width=2, width=150, height=35)
        entry_name = ctk.CTkEntry(form_frame, corner_radius=8, fg_color='white', border_width=2, width=150, height=35)
        entry_fournisseur = ctk.CTkComboBox(form_frame, values=get_product_fournisseur(),corner_radius=8, fg_color='white', border_width=2, width=150, height=35)
        entry_fournisseur.bind("<<ComboboxSelected>>", fill_product_details)
        entry_categorie = ctk.CTkComboBox(form_frame, values=get_product_categories(),corner_radius=8, fg_color='white', border_width=2, width=150, height=35)
        entry_categorie.bind("<<ComboboxSelected>>", fill_product_details)

        
        label_id.grid(row=1, column=0, padx=10, pady=(20, 5))
        entry_id.grid(row=2, column=0, padx=10, pady=(0, 10))

        label_price.grid(row=1, column=1, padx=10, pady=(20, 5))
        entry_price.grid(row=2, column=1, padx=10, pady=(0, 10))

        label_name.grid(row=3, column=0, padx=10, pady=(20, 5))
        entry_name.grid(row=4, column=0, padx=10, pady=(0, 10))

        label_categorie.grid(row=5, column=0, padx=10, pady=(20, 5))
        entry_categorie.grid(row=6, column=0, padx=10, pady=(0, 10))

        label_fournisseur.grid(row=7, column=0, padx=10, pady=(20, 5))
        entry_fournisseur.grid(row=8, column=0, padx=10, pady=(0, 10))

        
        quantity_var = IntVar(value=1)
        quantity_frame = ctk.CTkFrame(form_frame, width=150, fg_color='white', border_width=2, corner_radius=10)
        quantity_frame.grid(row=9, column=0, padx=15, pady=10)
        label_quantity = ctk.CTkLabel(form_frame, text="Quantité:",text_color="#245263",font=ctk.CTkFont(size=15, weight="bold"))
        entry_quantity = ctk.CTkEntry(quantity_frame, textvariable=quantity_var, width=50, border_color='white', font=ctk.CTkFont(size=20, weight="bold"))

        label_quantity.grid(row=8, column=0, padx=10, pady=(80, 1))
        entry_quantity.grid(row=9, column=1, padx=10, pady=(10, 20))

        btn_quantity_minus = ctk.CTkButton(quantity_frame, text="-", command=lambda: quantity_var.set(quantity_var.get() - 1), width=50, border_width=1,border_color="#245263",fg_color='white', text_color="#245263")
        btn_quantity_plus = ctk.CTkButton(quantity_frame, text="+", command=lambda: quantity_var.set(quantity_var.get() + 1), width=50,  border_width=1,border_color="#245263",fg_color='white', text_color="#245263")

        btn_quantity_minus.grid(row=9, column=3, padx=10, pady=10)
        btn_quantity_plus.grid(row=9, column=2, padx=10, pady=10)

        btn_modify = ctk.CTkButton(form_frame, text="Modifier", fg_color="#245263", command=lambda:modifier_produit(entry_id, entry_name,entry_price,quantity_var,entry_categorie,entry_fournisseur))
        btn_modify.grid(row=10, column=0, columnspan=2, padx=10, pady=10)
        

        options_frame = ctk.CTkFrame(self.third_frame, corner_radius=10, fg_color='white', border_width=1, border_color='black', width=200)  # Set the desired height
        options_frame.pack(pady=(20, 20))  

        
        container_frame = ctk.CTkFrame(options_frame, fg_color='transparent',height=50)
        container_frame.pack(pady=10, padx=10)

        label_img = ctk.CTkLabel(container_frame, image=self.logo_image, text='')
        label_img.pack(side='left', padx=10)

        label_error = ctk.CTkLabel(container_frame, width=150, height=100, text="Une erreur ?\nLaisser Stocky\ns'en charger !", font=ctk.CTkFont(size=30, weight="normal"))
        label_error.pack(side='left', padx=10)

        label_modify = ctk.CTkLabel(self.third_frame, text='Modifier', text_color="#245263", font=ctk.CTkFont(size=15, weight="bold"))
        entry_modify = ctk.CTkComboBox(self.third_frame, values=["", ""], corner_radius=8, fg_color='white', border_width=2, width=150, height=35)

        label_modify.pack(pady=15)
        entry_modify.pack(pady=10)

        btn_modify_c = ctk.CTkButton(self.third_frame, text="Modifier Categorie", fg_color="#245263", command=lambda:modifier_categorie(entry_id,entry_modify))
        btn_modify_c.pack( padx=10, pady=10)

        btn_modify_f = ctk.CTkButton(self.third_frame, text="Modifier Fournisseur", fg_color="#245263", command=lambda:modifier_fournisseur(entry_id,entry_modify))
        btn_modify_f.pack(padx=10, pady=10)

       
        btn_frame = ctk.CTkFrame(self.third_frame, corner_radius=10,fg_color='white')
        btn_frame.pack(pady=10)
        

        btn_importer = ctk.CTkButton(btn_frame, text="Importer", fg_color="#245263", command=importer)
        btn_exporter = ctk.CTkButton(btn_frame, text="Exporter", fg_color="#245263", command=exporter)

        for btn in [btn_importer, btn_exporter]:
            btn.pack(side="left", padx=5)

        # create fourth frame
        self.fourth_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="white")

        label_title = ctk.CTkLabel(self.fourth_frame, text="Supprimer un article", text_color="#245263", font=ctk.CTkFont(size=30, weight="bold"))
        label_title.pack(padx=5, pady=5)

       
        def get_current_date():
            return datetime.now().strftime("%A %d, %B %Y ")

        
        
        date_frame = ctk.CTkFrame(self.fourth_frame, fg_color='white', corner_radius=10)
        date_frame.pack(anchor="ne", padx=1, pady=5)

        label_date = ctk.CTkLabel(date_frame, text=get_current_date(), font=ctk.CTkFont(size=20, weight="bold"), bg_color="transparent",text_color="#245263")
        label_date.pack(padx=5, pady=5)




        form_frame = ctk.CTkFrame(
            self.fourth_frame, 
            corner_radius=10, 
            fg_color='white', 
            border_width=1, 
            border_color='black', 
            width=400,
            bg_color='white',
        )
        form_frame.pack(side="left", padx=10, pady=10)

        border_frame = ctk.CTkFrame(
            form_frame,
            corner_radius=10, 
            fg_color='black',
            border_width=0    
        )
        border_frame.grid(row=0, column=0, padx=0, pady=0, sticky='nsew')

        placeholder_label = ctk.CTkLabel(
            border_frame, 
            text="Choisir l'element a supprimer ici !", 
            width=400,  
            fg_color='white',
            text_color="#245263", 
            font=ctk.CTkFont(size=15, weight="bold")
        )
        placeholder_label.pack(expand=True, fill='y', padx=1, pady=1)

        label_delete = ctk.CTkLabel(form_frame, text='Supprimer', text_color="#245263", font=ctk.CTkFont(size=15, weight="bold"))
        entry_delete = ctk.CTkComboBox(form_frame, values=["articles", "fournisseur", "categorie"], corner_radius=8, fg_color='white', border_width=2, width=150, height=35)
        entry_delete.set("")

        label_delete.grid(row=1, column=0, padx=10, pady=(20, 5))
        entry_delete.grid(row=2, column=0, padx=10, pady=(0, 10))


        label_id = ctk.CTkLabel(form_frame, text="ID", text_color="#245263", font=ctk.CTkFont(size=15, weight="bold"))
        entry_id = ctk.CTkComboBox(form_frame, values=" ", corner_radius=8, fg_color='white', border_width=2, width=150, height=35)
        entry_id.bind("<<ComboboxSelected>>", fill_product_details)



        label_id.grid(row=3, column=0, padx=10, pady=(20, 5))
        entry_id.grid(row=5, column=0, padx=10, pady=(0, 10))

        
        btn_delete = ctk.CTkButton(form_frame, text="Supprimer", fg_color="red", command=lambda:delete_record(entry_id, entry_delete))
        btn_delete.grid(row=10, column=0, columnspan=2, padx=10, pady=10)

        options_frame = ctk.CTkFrame(self.fourth_frame, corner_radius=10, fg_color='white', border_width=1, border_color='black', width=200)
        options_frame.pack(pady=(90, 50))

        container_frame = ctk.CTkFrame(options_frame, fg_color='transparent', height=50)
        container_frame.pack(pady=10, padx=10)

        label_img = ctk.CTkLabel(container_frame, image=self.logo_image, text='')
        label_img.pack(side='left', padx=10)

        label_error = ctk.CTkLabel(container_frame, width=150, height=100, text="Faisons un peu \nd'espace !", font=ctk.CTkFont(size=30, weight="normal"))
        label_error.pack(side='left', padx=10)



        
       
        btn_frame = ctk.CTkFrame(self.fourth_frame, corner_radius=10,fg_color='white')
        btn_frame.pack(pady=10)

        btn_importer = ctk.CTkButton(btn_frame, text="Importer", fg_color="#245263", command=importer)
        btn_exporter = ctk.CTkButton(btn_frame, text="Exporter", fg_color="#245263", command=exporter)

        for btn in [btn_importer, btn_exporter]:
            btn.pack(side="left", padx=5)


        

        # Default frame
        self.select_frame_by_name("acceuil")

    def select_frame_by_name(self, name):
        self.acceuil_button.configure(fg_color="#3B8ED0" if name == "acceuil" else "#245263")
        self.ajouter_button.configure(fg_color="#3B8ED0" if name == "ajouter" else "#245263")
        self.modifier_button.configure(fg_color="#3B8ED0" if name == "modifier" else "#245263")
        self.supprimer_button.configure(fg_color="#3B8ED0" if name == "supprimer" else "#245263")

        if name == "acceuil":
            self.acceuil_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.acceuil_frame.grid_forget()
        if name == "ajouter":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        if name == "modifier":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()
        if name == "supprimer":
            self.fourth_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.fourth_frame.grid_forget()
        
    def acceuil_button_event(self):
        self.select_frame_by_name("acceuil")

    def ajouter_button_event(self):
        self.select_frame_by_name("ajouter")

    def modifier_button_event(self):
        self.select_frame_by_name("modifier")

    def supprimer_button_event(self):
        self.select_frame_by_name("supprimer")



if __name__ == "__main__":
    app = App()
    app.mainloop()
