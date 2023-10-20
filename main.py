from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
               'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F',
               'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
               'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = [choice(letters) for _ in range(randint(8, 10))]
    password_list += [choice(symbols) for _ in range(randint(2, 4))]
    password_list += [choice(numbers) for _ in range(randint(2, 4))]

    shuffle(password_list)

    generated_password = "".join(password_list)
    entry_password.delete(0, END)
    entry_password.insert(0, generated_password)
    pyperclip.copy(generated_password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = entry_website.get().title()
    username = entry_username.get()
    password = entry_password.get()
    new_data = {
        website: {
            "email/username": username,
            "password": password
        }
    }

    # check for empty fields
    if len(website) == 0 or len(username) == 0 or len(password) == 0:
        messagebox.showwarning(title="Warning!", message="You cannot leave a field empty!")
        return

    # save confirmation
    confirmation_message = f"Details entered:\nEmail/Username: {username}\nPassword: {password}\nDo you want to save?"
    is_ok = messagebox.askokcancel(title="Save Confirmation", message=confirmation_message)

    # save if confirmed
    if is_ok:
        clear()

        try:
            with open("data.json", mode="r") as data_file:
                # read the old data
                try:
                    data = json.load(data_file)
                except json.decoder.JSONDecodeError:
                    data = {}
                # update the data with the new data
                data.update(new_data)

        except FileNotFoundError:
            data = new_data

        finally:
            with open("data.json", mode="w") as data_file:
                # write the data
                json.dump(data, data_file, indent=4)


def clear():
    entry_website.delete(0, END)
    entry_username.delete(0, END)
    entry_password.delete(0, END)


# ---------------------------- FIND PASSWORD ------------------------------- #


def find_password():

    def show_no_record_error():
        messagebox.showerror(title="Error", message="No such record")

    try:
        with open("data.json", mode="r") as data_file:
            try:
                data = json.load(data_file)
            except json.decoder.JSONDecodeError:
                show_no_record_error()

    except FileNotFoundError:
        open("data.json", mode="w").close()
        show_no_record_error()

    else:
        website = entry_website.get().title()
        if website in data:
            user_info = data[website]["email/username"]
            user_password = data[website]["password"]
            messagebox.showinfo(title="Info", message=f"mail/username: {user_info}\npassword: {user_password}")
            pyperclip.copy(user_password)
        else:
            show_no_record_error()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# logo
logo_image = PhotoImage(file="logo.png")
canvas = Canvas(width=200, height=200)
canvas.create_image(100, 100, image=logo_image)
canvas.grid(column=1, row=0)

# website name
label_website = Label(text="Website: ")
label_website.grid(column=0, row=1, sticky="E")
entry_website = Entry(width=35)
entry_website.grid(column=1, row=1, sticky="EW")
entry_website.focus()

# email/username
label_username = Label(text="Email/Username: ")
label_username.grid(column=0, row=2, sticky="EW")
entry_username = Entry()
entry_username.grid(column=1, row=2, columnspan=2, sticky="EW")

# password
label_password = Label(text="Password: ")
label_password.grid(column=0, row=3, sticky="E")
entry_password = Entry()
entry_password.grid(column=1, row=3, sticky="EW")
button_generate = Button(text="Generate Password", command=generate_password)
button_generate.grid(column=2, row=3, sticky="EW")

# add button
button_add = Button(text="Add", command=save)
button_add.grid(column=1, row=4, columnspan=2, sticky="EW")

# search button
button_search = Button(text="Search", command=find_password)
button_search.grid(column=2, row=1, sticky="EW")

window.mainloop()
