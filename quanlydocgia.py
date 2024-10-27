import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
from datetime import datetime, timedelta

class MemberManagement:
    def __init__(self, parent, show_main_callback):
        self.parent = parent
        self.show_main_callback = show_main_callback
        
        # Tạo biến cho các entry
        self.member_id_var = tk.StringVar()
        self.member_name_var = tk.StringVar()
        self.member_address_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.reg_date_var = tk.StringVar()
        self.membership_type_var = tk.StringVar()
        self.membership_end_var = tk.StringVar()
        self.search_var = tk.StringVar()
        
        # Kết nối database
        self.conn = self.connect_db()
        
        # Tạo giao diện
        self.create_widgets()
        self.load_members()

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
            text="QUẢN LÝ ĐỘC GIẢ",
            font=("Helvetica", 16, "bold")
        )
        title_label.pack(side="left", expand=True)

        # Frame thông tin độc giả
        member_frame = ttk.LabelFrame(self.parent, text="Thông tin độc giả")
        member_frame.pack(padx=10, pady=5, fill="x")

        # Grid layout cho input fields
        input_fields = [
            ("Mã độc giả:", self.member_id_var),
            ("Họ và tên:", self.member_name_var),
            ("Địa chỉ:", self.member_address_var),
            ("Số điện thoại:", self.phone_var),
            ("Email:", self.email_var),
            ("Ngày đăng ký:", self.reg_date_var),
            ("Loại thẻ:", self.membership_type_var),
            ("Ngày hết hạn:", self.membership_end_var)
        ]
        
        for i, (label_text, var) in enumerate(input_fields):
            row = i // 2
            col = (i % 2) * 2
            
            ttk.Label(member_frame, text=label_text).grid(row=row, column=col, padx=5, pady=5, sticky="e")
            
            if label_text == "Loại thẻ:":
                # Combobox cho loại thẻ
                membership_types = ['Standard', 'Premium']
                combo = ttk.Combobox(member_frame, textvariable=var, values=membership_types, state='readonly', width=30)
                combo.grid(row=row, column=col+1, padx=5, pady=5, sticky="w")
                combo.bind('<<ComboboxSelected>>', self.update_end_date)
            else:
                entry = ttk.Entry(member_frame, textvariable=var, width=30)
                entry.grid(row=row, column=col+1, padx=5, pady=5, sticky="w")

        # Frame chứa các nút chức năng
        button_frame = ttk.Frame(self.parent)
        button_frame.pack(pady=10)

        # Các nút chức năng
        buttons = [
            ("Thêm", self.add_member, '#4CAF50'),
            ("Sửa", self.update_member, '#2196F3'),
            ("Xóa", self.delete_member, '#f44336'),
            ("Làm mới", self.clear_form, '#FF9800')
        ]

        for text, command, color in buttons:
            btn = tk.Button(
                button_frame,
                text=text,
                command=command,
                bg=color,
                fg='white',
                font=('Helvetica', 11),
                padx=20,
                pady=5
            )
            btn.pack(side=tk.LEFT, padx=5)

        # Frame tìm kiếm
        search_frame = ttk.LabelFrame(self.parent, text="Tìm kiếm")
        search_frame.pack(padx=10, pady=5, fill="x")

        ttk.Entry(search_frame, textvariable=self.search_var, width=50).pack(side="left", padx=5, pady=5)
        ttk.Button(search_frame, text="Tìm kiếm", command=self.search_members).pack(side="left", padx=5, pady=5)
        ttk.Button(search_frame, text="Hiển thị tất cả", command=self.load_members).pack(side="left", padx=5, pady=5)

        # Treeview
        tree_frame = ttk.Frame(self.parent)
        tree_frame.pack(padx=10, pady=5, fill="both", expand=True)

        columns = ("Mã độc giả", "Họ và tên", "Địa chỉ", "Số điện thoại", 
                  "Email", "Ngày đăng ký", "Loại thẻ", "Ngày hết hạn")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10)

        # Định dạng các cột
        column_widths = [100, 150, 150, 100, 150, 100, 100, 100]
        for col, width in zip(columns, column_widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width)

        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        # Binding sự kiện click vào tree
        self.tree.bind('<<TreeviewSelect>>', self.item_selected)

        # Set ngày đăng ký là ngày hiện tại cho form mới
        self.reg_date_var.set(datetime.now().strftime("%Y-%m-%d"))

    def go_back(self):
        self.parent.destroy()
        self.show_main_callback()

    def update_end_date(self, event=None):
        if self.membership_type_var.get():
            reg_date = datetime.strptime(self.reg_date_var.get(), "%Y-%m-%d")
            if self.membership_type_var.get() == "Premium":
                end_date = reg_date + timedelta(days=365)  # 1 năm
            else:
                end_date = reg_date + timedelta(days=180)  # 6 tháng
            self.membership_end_var.set(end_date.strftime("%Y-%m-%d"))

    def load_members(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            cur = self.conn.cursor()
            cur.execute("""
                SELECT member_id, member_name, member_address, phone_number, 
                       email, reg_date, membership_type, membership_end_date
                FROM members
                ORDER BY member_name
            """)
            
            for row in cur.fetchall():
                self.tree.insert("", "end", values=row)
            
            cur.close()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải danh sách độc giả: {str(e)}")

    def item_selected(self, event):
        selected_items = self.tree.selection()
        if selected_items:
            values = self.tree.item(selected_items[0])['values']
            
            self.member_id_var.set(values[0])
            self.member_name_var.set(values[1])
            self.member_address_var.set(values[2])
            self.phone_var.set(values[3])
            self.email_var.set(values[4])
            self.reg_date_var.set(values[5])
            self.membership_type_var.set(values[6])
            self.membership_end_var.set(values[7])

    def validate_input(self):
        if not all([self.member_id_var.get(), self.member_name_var.get(), 
                   self.phone_var.get(), self.email_var.get()]):
            messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin bắt buộc!")
            return False
        return True

    def add_member(self):
        if not self.validate_input():
            return

        try:
            cur = self.conn.cursor()
            
            # Kiểm tra member_id đã tồn tại
            cur.execute("SELECT member_id FROM members WHERE member_id = %s", 
                       (self.member_id_var.get(),))
            if cur.fetchone():
                messagebox.showwarning("Cảnh báo", "Mã độc giả đã tồn tại!")
                return

            cur.execute("""
                INSERT INTO members (
                    member_id, member_name, member_address, phone_number, 
                    email, reg_date, membership_type, membership_end_date
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                self.member_id_var.get(),
                self.member_name_var.get(),
                self.member_address_var.get(),
                self.phone_var.get(),
                self.email_var.get(),
                self.reg_date_var.get(),
                self.membership_type_var.get(),
                self.membership_end_var.get()
            ))
            
            self.conn.commit()
            messagebox.showinfo("Thành công", "Thêm độc giả mới thành công!")
            self.clear_form()
            self.load_members()
            
        except Exception as e:
            self.conn.rollback()
            messagebox.showerror("Lỗi", f"Không thể thêm độc giả: {str(e)}")
        finally:
            cur.close()

    def update_member(self):
        if not self.validate_input():
            return

        if not self.tree.selection():
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn độc giả cần cập nhật!")
            return

        try:
            cur = self.conn.cursor()
            cur.execute("""
                UPDATE members 
                SET member_name = %s,
                    member_address = %s,
                    phone_number = %s,
                    email = %s,
                    reg_date = %s,
                    membership_type = %s,
                    membership_end_date = %s
                WHERE member_id = %s
            """, (
                self.member_name_var.get(),
                self.member_address_var.get(),
                self.phone_var.get(),
                self.email_var.get(),
                self.reg_date_var.get(),
                self.membership_type_var.get(),
                self.membership_end_var.get(),
                self.member_id_var.get()
            ))
            
            self.conn.commit()
            messagebox.showinfo("Thành công", "Cập nhật thông tin độc giả thành công!")
            self.clear_form()
            self.load_members()
            
        except Exception as e:
            self.conn.rollback()
            messagebox.showerror("Lỗi", f"Không thể cập nhật thông tin độc giả: {str(e)}")
        finally:
            cur.close()

    def delete_member(self):
        if not self.tree.selection():
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn độc giả cần xóa!")
            return

        if not messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa độc giả này?"):
            return

        try:
            cur = self.conn.cursor()
            
            # Kiểm tra độc giả có đang mượn sách
            cur.execute("""
                SELECT COUNT(*) 
                FROM issued_status 
                WHERE member_id = %s AND status = 'borrowed'
            """, (self.member_id_var.get(),))
            
            if cur.fetchone()[0] > 0:
                messagebox.showwarning("Cảnh báo", 
                    "Không thể xóa độc giả này vì đang có sách chưa trả!")
                return

            cur.execute("DELETE FROM members WHERE member_id = %s", 
                       (self.member_id_var.get(),))
            
            self.conn.commit()
            messagebox.showinfo("Thành công", "Xóa độc giả thành công!")
            self.clear_form()
            self.load_members()
            
        except Exception as e:
            self.conn.rollback()
            messagebox.showerror("Lỗi", f"Không thể xóa độc giả: {str(e)}")
        finally:
            cur.close()

    def search_members(self):
        search_text = self.search_var.get()
        if not search_text:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập từ khóa tìm kiếm!")
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            cur = self.conn.cursor()
            cur.execute("""
                SELECT member_id, member_name, member_address, phone_number, 
                       email, reg_date, membership_type, membership_end_date
                FROM members
                WHERE LOWER(member_id) LIKE LOWER(%s)
                   OR LOWER(member_name) LIKE LOWER(%s)
                   OR LOWER(phone_number) LIKE LOWER(%s)
                ORDER BY member_name
            """, (f"%{search_text}%", f"%{search_text}%", f"%{search_text}%"))
            rows = cur.fetchall()
            if not rows:
                messagebox.showinfo("Thông báo", "Không tìm thấy kết quả phù hợp!")
            else:
                for row in rows:
                    self.tree.insert("", "end", values=row)
            
            cur.close()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi tìm kiếm: {str(e)}")

    def clear_form(self):
        self.member_id_var.set("")
        self.member_name_var.set("")
        self.member_address_var.set("")
        self.phone_var.set("")
        self.email_var.set("")
        self.reg_date_var.set(datetime.now().strftime("%Y-%m-%d"))
        self.membership_type_var.set("")
        self.membership_end_var.set("")
        self.search_var.set("")
        
        # Xóa selection trong tree
        for item in self.tree.selection():
            self.tree.selection_remove(item)