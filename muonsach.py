import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
from datetime import datetime, timedelta

class BorrowBooks:
    def __init__(self, parent, show_main_callback):
        self.parent = parent
        self.show_main_callback = show_main_callback
        
        # Tạo biến cho các entry
        self.member_id_var = tk.StringVar()
        self.member_name_var = tk.StringVar()
        self.book_isbn_var = tk.StringVar()
        self.book_title_var = tk.StringVar()
        self.issued_date_var = tk.StringVar()
        self.due_date_var = tk.StringVar()
        
        # Kết nối database
        self.conn = self.connect_db()
        
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
        # Frame chứa nút Quay lại và tiêu đề
        header_frame = ttk.Frame(self.parent)
        header_frame.pack(fill="x", padx=10, pady=5)
        
        # Nút Quay lại
        back_button = tk.Button(
            header_frame,
            text="⬅ Quay lại",
            font=('Helvetica', 10),
            command=self.go_back,
            bg='#f0f0f0',
            padx=10,
            pady=5
        )
        back_button.pack(side="left")
        
        # Tiêu đề
        title_label = ttk.Label(
            header_frame,
            text="MƯỢN SÁCH",
            font=("Helvetica", 16, "bold")
        )
        title_label.pack(side="left", expand=True)

        # Frame thông tin độc giả
        member_frame = ttk.LabelFrame(self.parent, text="Thông tin độc giả")
        member_frame.pack(padx=10, pady=5, fill="x")

        # Mã độc giả và nút tìm
        member_search_frame = ttk.Frame(member_frame)
        member_search_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(member_search_frame, text="Mã độc giả:").pack(side="left", padx=5)
        ttk.Entry(member_search_frame, textvariable=self.member_id_var, width=20).pack(side="left", padx=5)
        ttk.Button(member_search_frame, text="Tìm độc giả", command=self.search_member).pack(side="left", padx=5)
        
        # Tên độc giả
        member_info_frame = ttk.Frame(member_frame)
        member_info_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(member_info_frame, text="Tên độc giả:").pack(side="left", padx=5)
        ttk.Entry(member_info_frame, textvariable=self.member_name_var, width=40, state="readonly").pack(side="left", padx=5)

        # Frame thông tin sách
        book_frame = ttk.LabelFrame(self.parent, text="Thông tin sách")
        book_frame.pack(padx=10, pady=5, fill="x")

        # ISBN và nút tìm
        book_search_frame = ttk.Frame(book_frame)
        book_search_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(book_search_frame, text="ISBN:").pack(side="left", padx=5)
        ttk.Entry(book_search_frame, textvariable=self.book_isbn_var, width=20).pack(side="left", padx=5)
        ttk.Button(book_search_frame, text="Tìm sách", command=self.search_book).pack(side="left", padx=5)
        
        # Tên sách
        book_info_frame = ttk.Frame(book_frame)
        book_info_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(book_info_frame, text="Tên sách:").pack(side="left", padx=5)
        ttk.Entry(book_info_frame, textvariable=self.book_title_var, width=60, state="readonly").pack(side="left", padx=5)

        # Frame thông tin mượn sách
        borrow_frame = ttk.LabelFrame(self.parent, text="Thông tin mượn sách")
        borrow_frame.pack(padx=10, pady=5, fill="x")

        # Ngày mượn và ngày hẹn trả
        date_frame = ttk.Frame(borrow_frame)
        date_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(date_frame, text="Ngày mượn:").pack(side="left", padx=5)
        ttk.Entry(date_frame, textvariable=self.issued_date_var, width=20, state="readonly").pack(side="left", padx=5)
        
        ttk.Label(date_frame, text="Ngày hẹn trả:").pack(side="left", padx=5)
        ttk.Entry(date_frame, textvariable=self.due_date_var, width=20, state="readonly").pack(side="left", padx=5)

        # Nút Mượn sách
        borrow_button = tk.Button(
            self.parent,
            text="Mượn sách",
            command=self.borrow_book,
            bg='#4CAF50',
            fg='white',
            font=('Helvetica', 12),
            padx=20,
            pady=10
        )
        borrow_button.pack(pady=20)

        # Treeview hiển thị danh sách sách đã mượn
        tree_frame = ttk.Frame(self.parent)
        tree_frame.pack(padx=10, pady=5, fill="both", expand=True)

        columns = ("Mã mượn", "Tên sách", "Ngày mượn", "Ngày hẹn trả", "Trạng thái")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10)

        # Định dạng các cột
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        # Set ngày mượn là ngày hiện tại
        current_date = datetime.now()
        self.issued_date_var.set(current_date.strftime("%Y-%m-%d"))
        # Set ngày hẹn trả là 14 ngày sau
        due_date = current_date + timedelta(days=14)
        self.due_date_var.set(due_date.strftime("%Y-%m-%d"))

        # Load danh sách mượn sách
        self.load_borrowed_books()

    def go_back(self):
        self.parent.destroy()
        self.show_main_callback()

    def search_member(self):
        member_id = self.member_id_var.get()
        if not member_id:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập mã độc giả!")
            return

        try:
            cur = self.conn.cursor()
            cur.execute("""
                SELECT member_name FROM members 
                WHERE member_id = %s
            """, (member_id,))
            
            result = cur.fetchone()
            if result:
                self.member_name_var.set(result[0])
            else:
                messagebox.showwarning("Cảnh báo", "Không tìm thấy độc giả!")
                self.member_name_var.set("")
            
            cur.close()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi tìm độc giả: {str(e)}")

    def search_book(self):
        isbn = self.book_isbn_var.get()
        if not isbn:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập ISBN!")
            return

        try:
            cur = self.conn.cursor()
            cur.execute("""
                SELECT b.book_title, bc.status
                FROM books b
                JOIN book_copies bc ON b.isbn = bc.isbn
                WHERE b.isbn = %s
            """, (isbn,))
            
            result = cur.fetchone()
            if result:
                if result[1] == 'available':
                    self.book_title_var.set(result[0])
                else:
                    messagebox.showwarning("Cảnh báo", "Sách này đã được mượn!")
                    self.book_title_var.set("")
            else:
                messagebox.showwarning("Cảnh báo", "Không tìm thấy sách!")
                self.book_title_var.set("")
            
            cur.close()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi tìm sách: {str(e)}")

    def borrow_book(self):
        if not all([self.member_id_var.get(), self.member_name_var.get(),
                   self.book_isbn_var.get(), self.book_title_var.get()]):
            messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin!")
            return

        try:
            cur = self.conn.cursor()
            
            # Kiểm tra số lượng sách đang mượn của độc giả
            cur.execute("""
                SELECT COUNT(*) FROM issued_status
                WHERE member_id = %s AND return_date IS NULL
            """, (self.member_id_var.get(),))
            
            current_borrows = cur.fetchone()[0]
            if current_borrows >= 3:
                messagebox.showwarning("Cảnh báo", "Độc giả đã mượn tối đa số lượng sách cho phép!")
                return

            # Tạo mã mượn sách mới
            cur.execute("""
                SELECT 'IS' || LPAD(CAST(COALESCE(MAX(SUBSTRING(issued_id FROM 3)::integer), 0) + 1 AS VARCHAR), 3, '0')
                FROM issued_status
            """)
            new_issued_id = cur.fetchone()[0]

            # Thêm thông tin mượn sách
            cur.execute("""
                INSERT INTO issued_status (issued_id, member_id, issued_book_isbn, 
                                         issued_date, due_date, status)
                VALUES (%s, %s, %s, %s, %s, 'borrowed')
            """, (new_issued_id, self.member_id_var.get(), self.book_isbn_var.get(),
                 self.issued_date_var.get(), self.due_date_var.get()))

            # Cập nhật trạng thái sách
            cur.execute("""
                UPDATE book_copies 
                SET status = 'borrowed'
                WHERE isbn = %s AND status = 'available'
                LIMIT 1
            """, (self.book_isbn_var.get(),))

            self.conn.commit()
            messagebox.showinfo("Thành công", "Mượn sách thành công!")
            
            # Reset form và load lại danh sách
            self.clear_form()
            self.load_borrowed_books()
            
        except Exception as e:
            self.conn.rollback()
            messagebox.showerror("Lỗi", f"Lỗi khi mượn sách: {str(e)}")
        finally:
            cur.close()

    def load_borrowed_books(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            cur = self.conn.cursor()
            cur.execute("""
                SELECT i.issued_id, i.member_id, i.issued_date, i.due_date, b.book_title
                FROM issued_status i
                JOIN book_copies c ON i.copy_id = c.copy_id
                JOIN books b ON c.isbn = b.isbn

            """, (self.member_id_var.get(),))
            
            for row in cur.fetchall():
                self.tree.insert("", "end", values=row)
            
            cur.close()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi tải danh sách: {str(e)}")

    def clear_form(self):
        self.book_isbn_var.set("")
        self.book_title_var.set("")
        current_date = datetime.now()
        self.issued_date_var.set(current_date.strftime("%Y-%m-%d"))
        due_date = current_date + timedelta(days=14)
        self.due_date_var.set(due_date.strftime("%Y-%m-%d"))