import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2

class BookManagement:
    def __init__(self, root, return_to_main_menu):
        self.root = root
        self.root.title("Quản Lý Sách")
        self.root.geometry("1200x700")
        self.return_to_main_menu = return_to_main_menu
        
        # Kết nối cơ sở dữ liệu
        self.conn = self.connect_db()
        self.cursor = self.conn.cursor()
        
        # Tạo giao diện
        self.create_widgets()

    def connect_db(self):
        try:
            conn = psycopg2.connect(
                database="muonsach",
                user="postgres",
                password="123456",
                host="localhost",
                port="5432"
            )
            return conn
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể kết nối database: {str(e)}")
            return None

    def create_widgets(self):
        # Frame tiêu đề
        title_label = ttk.Label(self.root, text="Quản Lý Sách", font=("Helvetica", 24, "bold"))
        title_label.pack(pady=20)

        # Frame tìm kiếm sách
        search_frame = ttk.Frame(self.root)
        search_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

        search_label = ttk.Label(search_frame, text="Tìm kiếm sách:")
        search_label.pack(side=tk.LEFT, padx=(0, 10))
        self.search_entry = ttk.Entry(search_frame, width=50)
        self.search_entry.pack(side=tk.LEFT, padx=(0, 10))
        search_button = ttk.Button(search_frame, text="Tìm kiếm", command=self.search_books)
        search_button.pack(side=tk.LEFT)

        # Frame danh sách sách
        self.book_tree = ttk.Treeview(self.root, columns=("isbn", "title", "category", "price", "publisher", "year", "location"), show="headings")
        self.book_tree.heading("isbn", text="ISBN")
        self.book_tree.heading("title", text="Tiêu đề")
        self.book_tree.heading("category", text="Thể loại")
        self.book_tree.heading("price", text="Giá thuê")
        self.book_tree.heading("publisher", text="Nhà xuất bản")
        self.book_tree.heading("year", text="Năm xuất bản")
        self.book_tree.heading("location", text="Vị trí")
        self.book_tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Frame nút chức năng
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)

        add_button = ttk.Button(button_frame, text="Thêm Sách", command=self.add_book)
        add_button.pack(side=tk.LEFT, padx=10)
        edit_button = ttk.Button(button_frame, text="Sửa Sách", command=self.edit_book)
        edit_button.pack(side=tk.LEFT, padx=10)
        delete_button = ttk.Button(button_frame, text="Xóa Sách", command=self.delete_book)
        delete_button.pack(side=tk.LEFT, padx=10)

        # Hiển thị tất cả sách
        self.display_books()

    def display_books(self):
        # Xóa các dòng hiện tại trong treeview
        for row in self.book_tree.get_children():
            self.book_tree.delete(row)

        # Lấy và hiển thị danh sách sách
        try:
            self.cursor.execute("SELECT isbn, book_title, category_id, rental_price, publisher, publication_year, shelf_location FROM books")
            books = self.cursor.fetchall()
            for book in books:
                self.book_tree.insert("", tk.END, values=book)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lấy danh sách sách: {str(e)}")

    def search_books(self):
        query = self.search_entry.get()
        if not query:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập thông tin để tìm kiếm")
            return

        # Tìm kiếm sách theo tiêu đề hoặc ISBN
        try:
            self.cursor.execute(
                "SELECT isbn, book_title, category_id, rental_price, publisher, publication_year, shelf_location "
                "FROM books WHERE isbn LIKE %s OR book_title ILIKE %s",
                (f"%{query}%", f"%{query}%")
            )
            books = self.cursor.fetchall()

            # Xóa các dòng hiện tại và hiển thị kết quả tìm kiếm
            for row in self.book_tree.get_children():
                self.book_tree.delete(row)

            for book in books:
                self.book_tree.insert("", tk.END, values=book)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tìm kiếm sách: {str(e)}")

    def add_book(self):
        BookForm(self.root, self.conn, self.display_books)

    def edit_book(self):
        selected_item = self.book_tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn sách để sửa")
            return

        book_values = self.book_tree.item(selected_item[0])["values"]
        BookForm(self.root, self.conn, self.display_books, book_values)

    def delete_book(self):
        selected_item = self.book_tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn sách để xóa")
            return

        book_isbn = self.book_tree.item(selected_item[0])["values"][0]
        confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa sách này?")
        if confirm:
            try:
                self.cursor.execute("DELETE FROM books WHERE isbn = %s", (book_isbn,))
                self.conn.commit()
                messagebox.showinfo("Thông báo", "Xóa sách thành công")
                self.display_books()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể xóa sách: {str(e)}")


class BookForm(tk.Toplevel):
    def __init__(self, parent, conn, refresh_callback, book_data=None):
        super().__init__(parent)
        self.conn = conn
        self.refresh_callback = refresh_callback
        self.book_data = book_data

        self.title("Thêm/Sửa Sách")
        self.geometry("400x400")
        self.create_form()

    def create_form(self):
        labels = ["ISBN", "Tiêu đề", "Thể loại", "Giá thuê", "Nhà xuất bản", "Năm xuất bản", "Vị trí"]
        self.entries = {}

        for i, label in enumerate(labels):
            lbl = ttk.Label(self, text=label)
            lbl.grid(row=i, column=0, pady=5, padx=10, sticky=tk.W)
            entry = ttk.Entry(self)
            entry.grid(row=i, column=1, pady=5, padx=10)
            self.entries[label] = entry

        if self.book_data:
            for i, value in enumerate(self.book_data):
                self.entries[labels[i]].insert(0, value)

        save_button = ttk.Button(self, text="Lưu", command=self.save_book)
        save_button.grid(row=len(labels), column=0, columnspan=2, pady=10)

    def save_book(self):
        values = [entry.get() for entry in self.entries.values()]
        if any(not v for v in values):
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin")
            return

        try:
            cursor = self.conn.cursor()
            if self.book_data:
                cursor.execute(
                    "UPDATE books SET book_title=%s, category_id=%s, rental_price=%s, publisher=%s, "
                    "publication_year=%s, shelf_location=%s WHERE isbn=%s",
                    (values[1], values[2], values[3], values[4], values[5], values[6], values[0])
                )
            else:
                cursor.execute(
                    "INSERT INTO books (isbn, book_title, category_id, rental_price, publisher, publication_year, shelf_location) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    values
                )
            self.conn.commit()
            self.refresh_callback()
            self.destroy()
            messagebox.showinfo("Thông báo", "Lưu sách thành công")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lưu sách: {str(e)}")
