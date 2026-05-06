import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class MovieLibrary:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library")
        self.root.geometry("800x600")

        # Файл для хранения данных
        self.movies_file = "movies.json"
        self.movies = []

        # Загрузка данных
        self.load_movies()

        # Создание интерфейса
        self.create_widgets()
        self.refresh_table()

    def create_widgets(self):
        # Вкладка добавления фильма
        tab_control = ttk.Notebook(self.root)
        tab_add = ttk.Frame(tab_control)
        tab_filter = ttk.Frame(tab_control)

        tab_control.add(tab_add, text="Добавить фильм")
        tab_control.add(tab_filter, text="Фильтр")
        tab_control.pack(expand=1, fill="both")

        # Форма добавления фильма
        form_frame = ttk.LabelFrame(tab_add, text="Информация о фильме")
        form_frame.pack(fill="x", padx=10, pady=10)

        # Поля ввода
        tk.Label(form_frame, text="Название:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_title = tk.Entry(form_frame, width=40)
        self.entry_title.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Жанр:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_genre = tk.Entry(form_frame, width=40)
        self.entry_genre.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Год выпуска:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_year = tk.Entry(form_frame, width=40)
        self.entry_year.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="(число от 1800 до 2100)").grid(row=2, column=2, padx=5, pady=5, sticky="w")

        tk.Label(form_frame, text="Рейтинг:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.entry_rating = tk.Entry(form_frame, width=40)
        self.entry_rating.grid(row=3, column=1, padx=5, pady=5)
        tk.Label(form_frame, text="(от 0 до 10)").grid(row=3, column=2, padx=5, pady=5, sticky="w")

        # Кнопка добавления
        ttk.Button(tab_add, text="Добавить фильм", command=self.add_movie).pack(pady=10)

        # Таблица фильмов
        table_frame = ttk.LabelFrame(tab_add, text="Коллекция фильмов")
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(table_frame, columns=("Название", "Жанр", "Год", "Рейтинг"), show="headings")
        for col in ("Название", "Жанр", "Год", "Рейтинг"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Вкладка фильтрации
        filter_frame = ttk.LabelFrame(tab_filter, text="Параметры фильтрации")
        filter_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(filter_frame, text="Жанр:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.filter_genre = ttk.Combobox(filter_frame, state="readonly")
        self.filter_genre.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(filter_frame, text="Год:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.filter_year = tk.Entry(filter_frame, width=20)
        self.filter_year.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(tab_filter, text="Применить фильтр", command=self.apply_filters).pack(pady=10)
        ttk.Button(tab_filter, text="Сбросить фильтр", command=self.reset_filters).pack(pady=5)

    def validate_input(self):
        """Проверка корректности ввода"""
        title = self.entry_title.get().strip()
        genre = self.entry_genre.get().strip()
        year = self.entry_year.get().strip()
        rating = self.entry_rating.get().strip()

        if not title or not genre:
            messagebox.showerror("Ошибка", "Название и жанр не должны быть пустыми.")
            return False

        try:
            year_int = int(year)
            if not (1800 <= year_int <= 2100):
                messagebox.showerror("Ошибка", "Год должен быть числом от 1800 до 2100.")
                return False
        except ValueError:
            messagebox.showerror("Ошибка", "Год должен быть числом.")
            return False

        try:
            rating_float = float(rating)
            if not (0 <= rating_float <= 10):
                messagebox.showerror("Ошибка", "Рейтинг должен быть числом от 0 до 10.")
                return False
        except ValueError:
            messagebox.showerror("Ошибка", "Рейтинг должен быть числом.")
            return False

        return True

    def add_movie(self):
        """Добавление нового фильма"""
        if self.validate_input():
            movie = {
                "title": self.entry_title.get(),
                "genre": self.entry_genre.get(),
                "year": int(self.entry_year.get()),
                "rating": float(self.entry_rating.get())
            }
            self.movies.append(movie)
            self.save_movies()
            self.refresh_table()
            self.clear_fields()
            messagebox.showinfo("Успех", "Фильм успешно добавлен!")

    def load_movies(self):
        """Загрузка фильмов из JSON-файла"""
        if os.path.exists(self.movies_file):
            try:
                with open(self.movies_file, "r", encoding="utf-8") as f:
                    self.movies = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.movies = []
                messagebox.showwarning("Предупреждение", "Файл фильмов повреждён или пуст.")
        else:
            self.movies = []

    def save_movies(self):
        """Сохранение фильмов в JSON-файл"""
        try:
            with open(self.movies_file, "w", encoding="utf-8") as f:
                json.dump(self.movies, f, ensure_ascii=False, indent=2)
            # Обновляем список жанров для фильтра
            self.update_genre_filter()
        except IOError:
            messagebox.showerror("Ошибка", "Не удалось сохранить данные.")

    def refresh_table(self):
        """Обновление таблицы с фильмами"""
        # Очищаем таблицу
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Заполняем таблицу данными
        for movie in self.movies:
            self.tree.insert("", "end", values=(
                movie["title"],
                movie["genre"],
                movie["year"],
                f"{movie['rating']:.1f}"
            ))

        # Обновляем фильтр жанров
        self.update_genre_filter()

    def clear_fields(self):
        """Очистка полей ввода после добавления фильма"""
        self.entry_title.delete(0, tk.END)
        self.entry_genre.delete(0, tk.END)
        self.entry_year.delete(0, tk.END)
        self.entry_rating.delete(0, tk.END)

    def update_genre_filter(self):
        """Обновляет список жанров в фильтре"""
        genres = sorted(set(movie["genre"] for movie in self.movies))
        self.filter_genre["values"] = ["Все жанры"] + genres
        if genres:
            self.filter_genre.set("Все жанры")
        else:
            self.filter_genre.set("")

    def apply_filters(self):
        """Применение фильтров к таблице"""
        filtered_movies = self.movies.copy()

        # Фильтр по жанру
        selected_genre = self.filter_genre.get()
        if selected_genre and selected_genre != "Все жанры":
            filtered_movies = [m for m in filtered_movies if m["genre"] == selected_genre]

        # Фильтр по году
        year_filter = self.filter_year.get().strip()
        if year_filter:
            try:
                year_int = int(year_filter)
                filtered_movies = [m for m in filtered_movies if m["year"] == year_int]
            except ValueError:
                messagebox.showerror("Ошибка", "Год в фильтре должен быть числом.")
                return

        # Обновляем таблицу с отфильтрованными данными
        self._display_filtered_movies(filtered_movies)

    def _display_filtered_movies(self, movies_list):
        """Отображает отфильтрованный список фильмов в таблице"""
        # Очищаем таблицу
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Заполняем отфильтрованными данными
        for movie in movies_list:
            self.tree.insert("", "end", values=(
                movie["title"],
                movie["genre"],
                movie["year"],
                f"{movie['rating']:.1f}"
            ))

    def reset_filters(self):
        """Сброс фильтров и отображение всех фильмов"""
        self.filter_genre.set("Все жанры")
        self.filter_year.delete(0, tk.END)
        self.refresh_table()

# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = MovieLibrary(root)
    root.mainloop()
