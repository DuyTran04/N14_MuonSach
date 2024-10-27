import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
from datetime import datetime

class ReturnBooks:
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
        self.return_date_var = tk.StringVar()
        self.fine_amount_var = tk.StringVar()
        
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
            text="TRẢ SÁCH",
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

        # Treeview hiển thị sách đang mượn
        borrowed_frame = ttk.LabelFrame(self.parent, text="Sách đang mượn")
        borrowed_frame.pack(padx=10, pady=5, fill="both", expand=True)

        # Tạo Treeview
        columns = ("Mã mượn", "Tên sách", "Ngày mượn", "Ngày hẹn trả", "Trạng thái")
        self.borrowed_tree = ttk.Treeview(borrowed_frame, columns=columns, show="headings", height=5)

        # Định dạng các cột
        for col in columns:
            self.borrowed_tree.heading(col, text=col)
            self.borrowed_tree.column(col, width=150)

        # Scrollbar cho Treeview
        scrollbar = ttk.Scrollbar(borrowed_frame, orient="vertical", command=self.borrowed_tree.yview)
        self.borrowed_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.borrowed_tree.pack(fill="both", expand=True, padx=5, pady=5)

        # Binding sự kiện chọn sách
        self.borrowed_tree.bind('<<TreeviewSelect>>', self.on_select_book)

        # Frame thông tin trả sách
        return_frame = ttk.LabelFrame(self.parent, text="Thông tin trả sách")
        return_frame.pack(padx=10, pady=5, fill="x")

        # Grid layout cho thông tin trả sách
        ttk.Label(return_frame, text="Ngày trả:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(return_frame, textvariable=self.return_date_var, width=20).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(return_frame, text="Tiền phạt:").grid(row=0, column=2, padx=5, pady=5)
        ttk.Entry(return_frame, textvariable=self.fine_amount_var, width=20, state="readonly").grid(row=0, column=3, padx=5, pady=5)

        # Nút trả sách
        return_button = tk.Button(
            self.parent,
            text="Trả sách",
            command=self.return_book,
            bg='#4CAF50',
            fg='white',
            font=('Helvetica', 12),
            padx=20,
            pady=10
        )
        return_button.pack(pady=20)

        # Set ngày trả là ngày hiện tại
        self.return_date_var.set(datetime.now().strftime("%Y-%m-%d"))

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
            
            # Tìm thông tin độc giả
            cur.execute("""
                SELECT member_name FROM members 
                WHERE member_id = %s
            """, (member_id,))
            
            member = cur.fetchone()
            if member:
                self.member_name_var.set(member[0])
                self.load_borrowed_books()
            else:
                messagebox.showwarning("Cảnh báo", "Không tìm thấy độc giả!")
                self.member_name_var.set("")
            
            cur.close()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi tìm độc giả: {str(e)}")

    def load_borrowed_books(self):
        # Xóa dữ liệu cũ trong tree
        for item in self.borrowed_tree.get_children():
            self.borrowed_tree.delete(item)

        try:
            cur = self.conn.cursor()
            cur.execute("""
                SELECT i.issued_id, b.book_title, i.issued_date, i.due_date, i.status
                FROM issued_status i
                JOIN books b ON i.issued_book_isbn = b.isbn
                WHERE i.member_id = %s AND i.status = 'borrowed'
                ORDER BY i.issued_date DESC
            """, (self.member_id_var.get(),))
            
            for row in cur.fetchall():
                self.borrowed_tree.insert("", "end", values=row)
            
            cur.close()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi tải danh sách sách đang mượn: {str(e)}")

    def on_select_book(self, event):
        selected_items = self.borrowed_tree.selection()
        if selected_items:
            issued_id = self.borrowed_tree.item(selected_items[0])['values'][0]
            self.calculate_fine(issued_id)

    def calculate_fine(self, issued_id):
        try:
            cur = self.conn.cursor()
            cur.execute("""
                SELECT due_date
                FROM issued_status
                WHERE issued_id = %s
            """, (issued_id,))
            
            due_date = cur.fetchone()[0]
            return_date = datetime.strptime(self.return_date_var.get(), "%Y-%m-%d").date()
            
            if return_date > due_date:
                days_late = (return_date - due_date).days
                fine_amount = days_late * 5000  # 5,000 VND per day
                self.fine_amount_var.set(f"{fine_amount:,} VND")
            else:
                self.fine_amount_var.set("0 VND")
                
            cur.close()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi tính tiền phạt: {str(e)}")

    def return_book(self):
        if not self.borrowed_tree.selection():
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn sách cần trả!")
            return

        selected_item = self.borrowed_tree.selection()[0]
        issued_id = self.borrowed_tree.item(selected_item)['values'][0]

        try:
            cur = self.conn.cursor()
            
            # Cập nhật trạng thái mượn sách
            cur.execute("""
                UPDATE issued_status
                SET status = 'returned', return_date = %s
                WHERE issued_id = %s
            """, (self.return_date_var.get(), issued_id))

            # Lấy ISBN của sách
            cur.execute("""
                SELECT issued_book_isbn
                FROM issued_status
                WHERE issued_id = %s
            """, (issued_id,))
            
            isbn = cur.fetchone()[0]

            # Cập nhật trạng thái sách
            cur.execute("""
                UPDATE book_copies
                SET status = 'available'
                WHERE isbn = %s AND status = 'borrowed'
                LIMIT 1
            """, (isbn,))

            # Thêm tiền phạt nếu có
            fine_amount = self.fine_amount_var.get().replace(" VND", "").replace(",", "")
            if int(fine_amount) > 0:
                cur.execute("""
                    INSERT INTO fines (member_id, issued_id, fine_amount, fine_date, payment_status)
                    VALUES (%s, %s, %s, %s, 'unpaid')
                """, (self.member_id_var.get(), issued_id, fine_amount, self.return_date_var.get()))

            self.conn.commit()
            messagebox.showinfo("Thành công", "Trả sách thành công!")
            
            # Cập nhật lại danh sách sách đang mượn
            self.load_borrowed_books()
            self.fine_amount_var.set("")
            
        except Exception as e:
            self.conn.rollback()
            messagebox.showerror("Lỗi", f"Lỗi khi trả sách: {str(e)}")
        finally:
            cur.close()