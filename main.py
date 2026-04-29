import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

data_file = "books.json"
books = []

def load_books():
    global books
    if os.path.exists(data_file):
        with open(data_file, "r", encoding="utf-8") as f:
            books = json.load(f)
    update_table()

def save_books():
    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(books, f, ensure_ascii=False, indent=2)

def add_book():
    title = entry_title.get().strip()
    author = entry_author.get().strip()
    genre = entry_genre.get().strip()
    pages = entry_pages.get().strip()

    if not title or not author or not genre or not pages:
        messagebox.showerror("Ошибка", "Все поля должны быть заполнены")
        return

    if not pages.isdigit():
        messagebox.showerror("Ошибка", "Количество страниц должно быть числом")
        return

    books.append({
        "title": title,
        "author": author,
        "genre": genre,
        "pages": int(pages)
    })
    save_books()
    update_table()
    clear_entries()

def clear_entries():
    entry_title.delete(0, tk.END)
    entry_author.delete(0, tk.END)
    entry_genre.delete(0, tk.END)
    entry_pages.delete(0, tk.END)

def update_table():
    for row in tree.get_children():
        tree.delete(row)
    
    genre_filter = filter_genre.get()
    pages_filter = filter_pages_var.get()
    
    for book in books:
        if genre_filter and book["genre"] != genre_filter:
            continue
        if pages_filter == ">200" and book["pages"] <= 200:
            continue
        if pages_filter == "<=200" and book["pages"] > 200:
            continue
        tree.insert("", tk.END, values=(book["title"], book["author"], book["genre"], book["pages"]))

def update_genre_filter():
    genres = sorted(set(book["genre"] for book in books))
    filter_genre.set("")
    menu = filter_genre_menu["menu"]
    menu.delete(0, "end")
    menu.add_command(label="Все", command=lambda: filter_genre.set(""))
    for genre in genres:
        menu.add_command(label=genre, command=lambda g=genre: filter_genre.set(g))
    update_table()

def on_filter_change(*args):
    update_table()

root = tk.Tk()
root.title("Book Tracker - Гареев Руслан")
root.geometry("800x500")

main_frame = tk.Frame(root, padx=10, pady=10)
main_frame.pack(fill=tk.BOTH, expand=True)

input_frame = tk.LabelFrame(main_frame, text="Добавление книги", padx=10, pady=10)
input_frame.pack(fill=tk.X, pady=(0, 10))

tk.Label(input_frame, text="Название:").grid(row=0, column=0, sticky="w")
entry_title = tk.Entry(input_frame, width=30)
entry_title.grid(row=0, column=1, padx=(0, 20))

tk.Label(input_frame, text="Автор:").grid(row=0, column=2, sticky="w")
entry_author = tk.Entry(input_frame, width=20)
entry_author.grid(row=0, column=3, padx=(0, 20))

tk.Label(input_frame, text="Жанр:").grid(row=1, column=0, sticky="w")
entry_genre = tk.Entry(input_frame, width=30)
entry_genre.grid(row=1, column=1, padx=(0, 20))

tk.Label(input_frame, text="Страниц:").grid(row=1, column=2, sticky="w")
entry_pages = tk.Entry(input_frame, width=20)
entry_pages.grid(row=1, column=3, padx=(0, 20))

btn_add = tk.Button(input_frame, text="Добавить книгу", command=add_book, bg="lightgreen")
btn_add.grid(row=1, column=4, padx=10)

filter_frame = tk.LabelFrame(main_frame, text="Фильтрация", padx=10, pady=10)
filter_frame.pack(fill=tk.X, pady=(0, 10))

tk.Label(filter_frame, text="Жанр:").pack(side=tk.LEFT, padx=(0, 5))
filter_genre = tk.StringVar()
filter_genre.trace("w", on_filter_change)
filter_genre_menu = tk.OptionMenu(filter_frame, filter_genre, "Загрузка...")
filter_genre_menu.pack(side=tk.LEFT, padx=(0, 20))

tk.Label(filter_frame, text="Страницы:").pack(side=tk.LEFT, padx=(0, 5))
filter_pages_var = tk.StringVar(value="Все")
filter_pages_var.trace("w", on_filter_change)
filter_pages_menu = tk.OptionMenu(filter_frame, filter_pages_var, "Все", ">200", "<=200")
filter_pages_menu.pack(side=tk.LEFT)

table_frame = tk.Frame(main_frame)
table_frame.pack(fill=tk.BOTH, expand=True)

columns = ("Название", "Автор", "Жанр", "Страниц")
tree = ttk.Treeview(table_frame, columns=columns, show="headings")
tree.heading("Название", text="Название")
tree.heading("Автор", text="Автор")
tree.heading("Жанр", text="Жанр")
tree.heading("Страниц", text="Страниц")

scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)

tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

load_books()
update_genre_filter()

root.mainloop()
