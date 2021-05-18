import string
from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generator():
    global password_entry
    password = ''

    for x in range(0, 4):
        password = random.choice(string.ascii_uppercase) + random.choice(string.ascii_lowercase) + random.choice(
            string.digits) + random.choice(string.punctuation)
    for y in range(random.randint(8, 20) - 4):
        password = password + random.choice(
            string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation)
    print(password)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def add_password():
    global password_entry, email_entry, website_entry
    new_data = {
        website_entry.get(): {
            "email": email_entry.get(),
            "password": password_entry.get()
        }
    }
    if len(password_entry.get()) == 0 or len(website_entry.get()) == 0 or len(email_entry.get()) == 0:
        messagebox.showerror(title='No Input given', message='One or more fields of data are empty')
    else:
        try:
            with open('data.json', mode='r') as file:
                data = json.load(file)
                data.update(new_data)

        except FileNotFoundError:
            with open('data.json', mode='w') as file:
                json.dump(new_data, file, indent=4)

        else:
            with open('data.json', mode='w') as file:
                json.dump(data, file, indent=4)

        finally:
            password_entry.delete(0, END)
            website_entry.delete(0, END)


# ---------------------------- SEARCH JSON ------------------------------- #
def search():
    global website_entry
    website = website_entry.get()
    try:
        with open('data.json', mode='r') as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showerror(title='Oops Something went wrong', message="You have not saved any Website")
    else:
        if website in data:
            messagebox.showinfo(title=website_entry.get(), message=f'Your Password is: {data[website]["password"]}')
            pyperclip.copy(data[website]["password"])
        else:
            messagebox.showerror(title='Not Found!', message="You have not saved password for this Website")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title('MyPasswordManager')
window.config(padx=20, pady=20)

canvas = Canvas(width=200, height=200)
canvas.grid(column=1, row=0)
logo = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=logo)

# Labels
website_label = Label(text='Website:')
website_label.grid(column=0, row=1)
email_label = Label(text='Email/Username:')
email_label.grid(column=0, row=2)
password_label = Label(text='Password:')
password_label.grid(column=0, row=3)

# Entries
website_entry = Entry(width=36)
website_entry.grid(column=1, row=1)
website_entry.focus()
email_entry = Entry(width=36)
email_entry.grid(column=1, row=2)
email_entry.insert(0, "vanshkela2@gmail.com")
password_entry = Entry(width=36)
password_entry.grid(column=1, row=3)

# Buttons
search_button = Button(text='Search', command=search, width=16)
search_button.grid(column=2, row=1)
generate_button = Button(text="Generate Password", command=generator, width=16)
generate_button.grid(column=2, row=3)
add_button = Button(text="Add", width=50, command=add_password)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()
