from tkinter import *
import random
import string
from cryptography.fernet import Fernet
import mysql.connector


class passwordGenerator:
    def __init__(self):
        with open("key.key", "rb") as key_file:
            self.key = key_file.read()
        self.fernet = Fernet(self.key)
    
    def generatePassword(self):
        lower = string.ascii_lowercase
        upper = string.ascii_uppercase
        digits = string.digits
        special = string.punctuation

        all_characters = lower + upper + digits + special
        password = [
            random.choice(lower),
            random.choice(upper),
            random.choice(digits),
            random.choice(special)
        ]

        length = 12
        password += random.choices(all_characters, k=length - 4)
        random.shuffle(password)
        self.generated_password = ''.join(password)
        return self.generated_password

    def encrypt_Password(self, password):
        return self.fernet.encrypt(password.encode())

    def decrypt_Password(self, encrypt_password):
        try:
            decrypted_data = self.fernet.decrypt(encrypt_password).decode()
            return decrypted_data
        except Exception as e:
            print(f"Decryption failed: {e}")
            return "Decryption Error"


class dataBaseManagement:
    def __init__(self):
        self.db_conncetion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="*******",
            database="password_manager"
        )
        self.cursor = self.db_conncetion.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS passwords(id INT AUTO_INCREMENT PRIMARY KEY, link VARCHAR(255) not null, password VARCHAR(255) not null ) ")
        self.db_conncetion.commit()

    def save_password(self, link, encrypted_password):
        self.cursor.execute("insert into passwords(link,password) values(%s,%s)", (link, encrypted_password))
        self.db_conncetion.commit()
    def delete_password(self,id):
        self.cursor.execute("delete from passwords where id = %s",(id,))
        self.db_conncetion.commit()

    def fetch_password(self):
        self.cursor.execute("select * from passwords")
        result = self.cursor.fetchall()
        return result


class passwordManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Manager")
        self.root.geometry("1000x1000")

        self.password_generator = passwordGenerator()
        self.db_manager = dataBaseManagement()

        self.main_frame = Frame(self.root)
        self.main_frame.grid(row=0, column=0, padx=10, pady=10)

        self.gp_button = Button(self.main_frame, text="Generate password", command=self.generatePassword)
        self.sp_button = Button(self.main_frame, text="Save password", command=self.save_password)

        self.password_testfield = Entry(self.main_frame, width=30, fg="grey")
        self.link_textfield = Entry(self.main_frame, width=30, fg="grey")
        self.set_placeholder(self.link_textfield, "Please enter the link")
        self.set_placeholder(self.password_testfield, "Password")

        
        self.link_textfield.grid(row=0, column=0, padx=10, pady=20)
        self.password_testfield.grid(row=0, column=1, padx=10, pady=20)
        self.gp_button.grid(row=0, column=2, padx=10, pady=20)
        self.sp_button.grid(row=0, column=3, padx=10, pady=20)

        self.display_passwords()  

    def set_placeholder(self, field, placeholder_text):
        field.insert(0, placeholder_text)

        def on_focus_in(event):
            if field.get() == placeholder_text:
                field.delete(0, END)
                field.config(fg="white")

        def on_focus_out(event):
            if not field.get():
                field.insert(0, placeholder_text)
                field.config(fg="grey")

        field.bind("<FocusIn>", on_focus_in)
        field.bind("<FocusOut>", on_focus_out)

    def generatePassword(self):
        password = self.password_generator.generatePassword()
        self.password_testfield.delete(0, END)
        self.password_testfield.insert(0, password)

    def save_password(self):
        link = self.link_textfield.get()
        password = self.password_testfield.get()

        if link and password:
            encrypted_password = self.password_generator.encrypt_Password(password)
            self.db_manager.save_password(link, encrypted_password)
            print("Password saved successfully")
            self.display_passwords()  
    def display_passwords(self):
       
        for widget in self.main_frame.winfo_children():
            if isinstance(widget, Label) or isinstance(widget, Button):
                widget.grid_forget()

        
        Label(self.main_frame, text="Link", width=30, anchor=W).grid(row=2, column=0, padx=10, pady=10)
        Label(self.main_frame, text="Password", width=30, anchor=W).grid(row=2, column=1, padx=10, pady=10)
       

        
        records = self.db_manager.fetch_password()

       
        for i, record in enumerate(records):
            print("Encrypted password:", record[2])
            decrypted_password = self.password_generator.decrypt_Password(record[2])

            Label(self.main_frame, text=record[1], width=30, anchor=W).grid(row=i+3, column=0, padx=10, pady=5)

            
            masked_password = '*' * 12
            password_label = Label(self.main_frame, text=masked_password, width=30, anchor=W)
            password_label.grid(row=i+3, column=1, padx=10, pady=5)

            
            def show_password(password_label=password_label, decrypted_password=decrypted_password):
                password_label.config(text=decrypted_password)
            def delete_password(id):
                
                self.db_manager.delete_password(id)
                self.display_passwords()
            show_button = Button(self.main_frame, text="Show Password", command=show_password)
            show_button.grid(row=i+3, column=2, padx=10, pady=5)
            delete_button = Button(self.main_frame, text="Delete Password", command= lambda id = record[0]: delete_password(id))
            delete_button.grid(row=i+3, column=3, padx=10, pady=5)
       
        self.gp_button.grid(row=0, column=2, padx=10, pady=20)
        self.sp_button.grid(row=0, column=3, padx=10, pady=20)


if __name__ == "__main__":
    root = Tk()
    app = passwordManager(root)
    root.mainloop()
