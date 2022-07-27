from tkinter import *
import random
import sqlite3


class PasswordGenerator():
    password = ''
    password_length = 15
    include_symbols = True
    include_capital_letters = True
    include_numbers = True
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
        password_structure = ['letters']    
        self.letters_part = ''
        self.symbols_part = ''
        self.numbers_part = ''
        
        if self.include_symbols:
            password_structure.append('symbols')
        if self.include_numbers:
            password_structure.append('numbers')

        length = self.password_length
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
        
        self.password = ''
        password_parts =  self.letters_part + self.symbols_part + self.numbers_part
        for element in range(len(password_parts)):
            password_element = random.choice(password_parts)
            self.password += password_element
            password_parts.replace(password_element, '', 1)


    def generate_letters_part_of_password(self):
        if self.include_capital_letters:
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


    def save_password(self):
        pass


    def show_saved_passwords(slef):
        pass


    def hide_saved_passwords(self):
        pass


pw = PasswordGenerator()
pw.generate_password()



