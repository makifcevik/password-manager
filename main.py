from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip


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
    website = entry_website.get()
    username = entry_username.get()
    password = entry_password.get()

    # check for empty fields
    if len(website) == 0 or len(username) == 0 or len(password) == 0:
        messagebox.showwarning(title="Warning!", message="You cannot leave a field empty!")
        return

    # save confirmation
    is_ok = messagebox.askokcancel(title="Save Confirmation", message=f"Details entered:\n"
                                                                      f"Email/Username: {username}\n"
                                                                      f"Password: {password}\n"
                                                                      f"Do you want to save?")

    # save if confirmed
    if is_ok:
        clear()
        with open("data.txt", mode="a") as save_file:
            save_file.write(f"{website} | {username} | {password}\n")


def clear():
    entry_website.delete(0, END)
    entry_username.delete(0, END)
    entry_password.delete(0, END)


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
entry_website.grid(column=1, row=1, columnspan=2, sticky="EW")
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

# add
button_add = Button(text="Add", command=save)
button_add.grid(column=1, row=4, columnspan=2, sticky="EW")

window.mainloop()
