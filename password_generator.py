from tkinter import *
import random
import sqlite3

root = Tk()
root.title("Password Generator")
root.geometry('400x480+200+100')
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

mainframe = Frame(root)
mainframe.grid(column=0, row=0,sticky=(N, W, E, S))

password = StringVar()
include_symbols = BooleanVar()
include_symbols.set(True)
include_numbers = BooleanVar()
include_numbers.set(True)
include_capital_letters = BooleanVar()
include_capital_letters.set(True)
password_length = StringVar()
password_length.set(15)
note = StringVar()
note.set('Enter a note')
password_to_delete = StringVar()
password_to_delete.set('Password to delete')

# Colors
color1 = '#b1bcf0'
color2 = '#eddf98'
color3 = '#c8ffb5'
color4 = '#ed9898'

checkbuttons_dict = {
    'checkbutton_include_symbols':{'text':'Symbols', 'variable':include_symbols, 'column':1, 'row':4, 'columnspan':2},
    'checkbutton_include_numbers':{'text':'Numbers', 'variable':include_numbers, 'column':3, 'row':4, 'columnspan':2},
    'checkbutton_include_capital_letters':{'text':'Capital letters', 'variable':include_capital_letters, 'column':5, 'row':4, 'columnspan':3},
}

for checkbutton in checkbuttons_dict:
    Checkbutton(
        mainframe,
        text = checkbuttons_dict[checkbutton]['text'],
        variable = checkbuttons_dict[checkbutton]['variable'],
    ).grid(
        column = checkbuttons_dict[checkbutton]['column'],
        row = checkbuttons_dict[checkbutton]['row'],
        columnspan = checkbuttons_dict[checkbutton]['columnspan'],
        padx = 10, pady = 10, sticky=(N, W, E, S)
    )

buttons_dict = {
    'button_generate_password':{'text':'Generate Password', 'background':color1,  'command': lambda: pw.generate_password(), 'column': 2,  'row': 1,  'columnspan': 5},
    'button_save_password':{'text':'Save password', 'background': color2,  'command': lambda: db.save_password(), 'column': 1,  'row': 6,  'columnspan': 3},
    'button_show_saved_passwords':{'text':'Show saved passwords', 'background':color3,  'command': lambda: db.show_saved_passwords(), 'column': 1,  'row': 7,  'columnspan': 3},
    'button_delete_password_from_db':{'text':'Delete password', 'background': color4,  'command': lambda: db.delete_saved_password(), 'column': 1,  'row': 9,  'columnspan': 3},
}

for button in buttons_dict:
    Button(
        mainframe,
        text = buttons_dict[button]['text'],
        background = buttons_dict[button]['background'],
        command = buttons_dict[button]['command'],
    ).grid(
        column = buttons_dict[button]['column'],
        row = buttons_dict[button]['row'],
        columnspan = buttons_dict[button]['columnspan'],
        padx = 10, pady = 10, sticky=(N, W, E, S)
    )

entry_dict = {
    'note_for_password':{'textvariable': note, 'background': color2, 'width': 20, 'column': 4,  'row': 6,  'columnspan': 4, 'sticky':(N, W, E, S), 'justify':'left'},
    'output_password':{'textvariable': password, 'background': color1, 'width': 20, 'column': 0,  'row': 0,  'columnspan': 8, 'sticky':(N, W, E, S), 'justify':'center'},
    'input_password_length':{'textvariable': password_length, 'background': color1, 'width': 5, 'column': 1,  'row': 5,  'columnspan': 2, 'sticky':(N, E), 'justify':'right'},
    'password_to_delete':{'textvariable': password_to_delete, 'background': color4, 'width': 20, 'column': 4,  'row': 9,  'columnspan': 4, 'sticky':(N, W, E, S), 'justify':'left'}
}

for entry in entry_dict:
    Entry(
        mainframe,
        textvariable = entry_dict[entry]['textvariable'],
        background = entry_dict[entry]['background'],
        justify = entry_dict[entry]['justify'],
        width = entry_dict[entry]['width'],
    ).grid(
        column = entry_dict[entry]['column'],
        row = entry_dict[entry]['row'],
        columnspan = entry_dict[entry]['columnspan'],
        padx = 10, pady = 10,
        sticky= entry_dict[entry]['sticky'],
    )

textlabel_password_length = Label(mainframe, text = 'Password length', width = 15, anchor=W)
textlabel_password_length.grid(column=3, row=5, columnspan=4, padx=10, pady=10, sticky=(N, W))

textlabel_saved_passwords = Text(mainframe, width = 10, height=10, background= color3)
textlabel_saved_passwords.grid(column=1, row=8, columnspan=8, padx=10, pady=10, sticky=(N, W, E, S))
textlabel_saved_passwords.insert(1.0, 'Click on the button to show saved passwords')

for column in range(8):
    mainframe.columnconfigure(column, weight = 1)

for row in range(9):
    mainframe.rowconfigure(row, weight=1)


class PasswordGenerator():

    symbols = """~`!@#$%^&*()_-+={[}]|\:;"'<,>.?/"""
    symbols_length = 0
    symbols_part = ''
    numbers = '0123456789'
    numbers_length = 0
    numbers_part = ''
    letters = 'abcdefghijklmnopqrstuvwxyz'
    letters_length = 0
    letters_part = ''

    
    def generate_password(self):
        try:
            password_structure = ['letters']    
            self.letters_part = ''
            self.symbols_part = ''
            self.numbers_part = ''
            
            if include_symbols.get():
                password_structure.append('symbols')
            if include_numbers.get():
                password_structure.append('numbers')

            length = int(password_length.get())
            for element in password_structure:
                if element != password_structure[-1]: 
                    element_length = random.randint(1,length-len(password_structure))
                    length -= element_length
                else:
                    element_length = length               

                if element == 'symbols':
                    self.symbols_length = element_length
                    self.generate_symbols_part_of_password()
                elif element == 'numbers':
                    self.numbers_length = element_length
                    self.generate_numbers_part_of_password()
                else:
                    self.letters_length = element_length
                    self.generate_letters_part_of_password()
            
            password.set('')
            password_parts =  self.letters_part + self.symbols_part + self.numbers_part
            for element in range(len(password_parts)):
                password_element = random.choice(password_parts)
                password.set(password.get() + password_element)
                password_parts.replace(password_element, '', 1)
        except:
            self.generate_password()
            print('exception')


    def generate_letters_part_of_password(self):
        if include_capital_letters.get():
            for letter in range(self.letters_length):
                capital_letter = random.choice((True,False))
                if capital_letter:
                    self.letters_part += random.choice(self.letters).upper()
                else:
                    self.letters_part += random.choice(self.letters).lower()
        else:
            for letter in range(self.letters_length):
                self.letters_part += random.choice(self.letters)


    def generate_symbols_part_of_password(self):
        for symbol in range(self.symbols_length):
            self.symbols_part += random.choice(self.symbols)


    def generate_numbers_part_of_password(self):
        for number in range(self.numbers_length):
            self.numbers_part += random.choice(self.numbers)



class Database(PasswordGenerator):
    note_for_db = ''

    def create_database(self):
        conn = sqlite3.connect('passwords_db.db')
        cursor = conn.cursor()

        cursor.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='passwords'")
        if cursor.fetchone()[0] != 1 :
            cursor.execute("CREATE TABLE passwords (password TEXT, note TEXT)")

        conn.commit()
        conn.close()


    def save_password(self):
        conn = sqlite3.connect('passwords_db.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO passwords VALUES (?, ?)", [password.get(), note.get()])
        conn.commit()
        conn.close() 
        note.set('Enter a note')


    def show_saved_passwords(slef):
        conn = sqlite3.connect('passwords_db.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM passwords")
        all_saved_passwords = cursor.fetchall()
        conn.commit()
        conn.close()
        textlabel_saved_passwords.delete(1.0, END)
        row = 1.0
        for password in all_saved_passwords:
            textlabel_saved_passwords.insert(row, f'{password[0]} | {password[1]} \n')
            row += 1


    def delete_saved_password(self):
        conn = sqlite3.connect('passwords_db.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM passwords WHERE password=?", (password_to_delete.get(),))
        conn.commit()
        conn.close()
        password_to_delete.set('Password to delete')
        self.show_saved_passwords()



pw = PasswordGenerator()
db = Database()
pw.generate_password()
db.create_database()
root.mainloop()





