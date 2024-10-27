import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
from ttkthemes import ThemedStyle
from quanlysach import BookManagement
from muonsach import BorrowBooks
from trasach import ReturnBooks
from quanlydocgia import MemberManagement
from thongke import Statistics

class LibraryManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Borrowing Books From A Library")
        self.root.geometry("1200x700")
        
        # Tạo style
        self.style = ThemedStyle(self.root)
        self.style.set_theme("arc")
        
        # Kết nối database
        self.conn = self.connect_db()
        
        # Tạo giao diện chính
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
        # Frame chính
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Tiêu đề
        title_frame = ttk.Frame(self.main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 50))
        
        title_label = ttk.Label(
            title_frame, 
            text="Borrowing Books From A Library",
            font=("Helvetica", 24, "bold")
        )
        title_label.pack(anchor="center")
        
        # Frame cho các nút chức năng
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(expand=True)
        
        # Style cho các nút
        button_style = {
            'font': ('Helvetica', 12),
            'padx': 20,
            'pady': 10,
            'width': 20,
            'relief': tk.RAISED,
            'borderwidth': 2
        }
        
        # Màu sắc cho từng nút
        button_colors = ['#4CAF50', '#2196F3', '#f44336', '#FF9800', '#9C27B0']
        
        # Các nút chức năng
        buttons = [
            ("Quản Lý Sách", self.open_book_management),
            ("Mượn Sách", self.open_borrow_books),
            ("Trả Sách", self.open_return_books),
            ("Quản Lý Độc Giả", self.open_manage_members),
            ("Báo Cáo Thống Kê", self.open_reports)
        ]
        
        # Tạo 2 frame con để chia nút thành 2 hàng
        top_button_frame = ttk.Frame(button_frame)
        top_button_frame.pack(pady=10)
        
        bottom_button_frame = ttk.Frame(button_frame)
        bottom_button_frame.pack(pady=10)
        
        # Thêm các nút vào frame
        for i, (text, command) in enumerate(buttons):
            btn = tk.Button(
                top_button_frame if i < 3 else bottom_button_frame,
                text=text,
                command=command,
                bg=button_colors[i],
                fg='white',
                **button_style
            )
            btn.pack(side=tk.LEFT, padx=10)

            # Hiệu ứng hover cho nút
            def on_enter(e, btn=btn):
                btn['bg'] = self.adjust_color(btn['bg'], -20)

            def on_leave(e, btn=btn, color=button_colors[i]):
                btn['bg'] = color

            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)

    def adjust_color(self, color, amount):
        """Điều chỉnh màu sắc cho hiệu ứng hover"""
        def clamp(x): 
            return max(0, min(x, 255))
            
        if color.startswith('#'):
            color = color[1:]
            
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        rgb = tuple(clamp(x + amount) for x in rgb)
        
        return f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'

    def hide_main_window(self):
        self.root.withdraw()  # Ẩn cửa sổ chính

    def show_main_window(self):
        self.root.deiconify()  # Hiện lại cửa sổ chính

    def open_book_management(self):
        self.hide_main_window()  # Ẩn cửa sổ chính
        book_window = tk.Toplevel()
        book_window.title("Quản Lý Sách")
        book_window.geometry("1200x700")
        
        def on_closing():
            book_window.destroy()
            self.show_main_window()  # Hiện lại cửa sổ chính
            
        book_window.protocol("WM_DELETE_WINDOW", on_closing)  # Xử lý khi đóng cửa sổ
        BookManagement(book_window, self.show_main_window)

    def open_borrow_books(self):
        self.hide_main_window()
        borrow_window = tk.Toplevel()
        borrow_window.title("Mượn Sách")
        borrow_window.geometry("1200x700")
        
        def on_closing():
            borrow_window.destroy()
            self.show_main_window()
            
        borrow_window.protocol("WM_DELETE_WINDOW", on_closing)
        BorrowBooks(borrow_window, self.show_main_window)

    def open_return_books(self):
        self.hide_main_window()
        return_window = tk.Toplevel()
        return_window.title("Trả Sách")
        return_window.geometry("1200x700")
        
        def on_closing():
            return_window.destroy()
            self.show_main_window()
            
        return_window.protocol("WM_DELETE_WINDOW", on_closing)
        ReturnBooks(return_window, self.show_main_window)

    def open_manage_members(self):
        self.hide_main_window()
        members_window = tk.Toplevel()
        members_window.title("Quản Lý Độc Giả")
        members_window.geometry("1200x700")
        
        def on_closing():
            members_window.destroy()
            self.show_main_window()
            
        members_window.protocol("WM_DELETE_WINDOW", on_closing)
        MemberManagement(members_window, self.show_main_window)

    def open_reports(self):
        self.hide_main_window()
        reports_window = tk.Toplevel()
        reports_window.title("Báo Cáo Thống Kê")
        reports_window.geometry("1200x700")
        
        def on_closing():
            reports_window.destroy()
            self.show_main_window()
            
        reports_window.protocol("WM_DELETE_WINDOW", on_closing)
        Statistics(reports_window, self.show_main_window)

if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg='white')
    app = LibraryManagementSystem(root)
    root.mainloop()