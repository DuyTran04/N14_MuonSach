import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Statistics:
    def __init__(self, parent, show_main_callback):
        self.parent = parent
        self.show_main_callback = show_main_callback
        
        # Kết nối database
        self.conn = self.connect_db()
        
        # Tạo giao diện
        self.create_widgets()
        
        # Load dữ liệu thống kê
        self.load_statistics()

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
            text="BÁO CÁO THỐNG KÊ",
            font=("Helvetica", 16, "bold")
        )
        title_label.pack(side="left", expand=True)

        # Notebook để chứa các tab thống kê
        self.notebook = ttk.Notebook(self.parent)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=5)

        # Tab 1: Thống kê tổng quan
        self.overview_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.overview_tab, text="Tổng quan")

        # Tab 2: Thống kê mượn sách
        self.borrow_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.borrow_tab, text="Thống kê mượn sách")

        # Tab 3: Thống kê trả muộn và phạt
        self.fine_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.fine_tab, text="Thống kê phạt")

        # Tab 4: Thống kê theo thể loại
        self.category_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.category_tab, text="Thống kê theo thể loại")

        # Tạo nội dung cho các tab
        self.create_overview_tab()
        self.create_borrow_tab()
        self.create_fine_tab()
        self.create_category_tab()

    def create_overview_tab(self):
        # Frame cho các metrics
        metrics_frame = ttk.LabelFrame(self.overview_tab, text="Thống kê tổng quan")
        metrics_frame.pack(fill="x", padx=10, pady=5)

        # Grid layout cho metrics
        self.metric_labels = {}
        metrics = [
            "Tổng số sách",
            "Tổng số độc giả",
            "Sách đang được mượn",
            "Số lượt mượn sách",
            "Tổng tiền phạt",
            "Số độc giả đang bị phạt"
        ]

        for i, metric in enumerate(metrics):
            row = i // 2
            col = i % 2
            frame = ttk.Frame(metrics_frame)
            frame.grid(row=row, column=col, padx=10, pady=5, sticky="w")
            
            ttk.Label(frame, text=f"{metric}:", font=('Helvetica', 10)).grid(row=0, column=0, sticky="w")
            value_label = ttk.Label(frame, text="0", font=('Helvetica', 10, 'bold'))
            value_label.grid(row=0, column=1, padx=10)
            self.metric_labels[metric] = value_label

        # Frame cho biểu đồ
        chart_frame = ttk.LabelFrame(self.overview_tab, text="Biểu đồ thống kê")
        chart_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Tạo figure cho matplotlib
        self.fig_overview = plt.Figure(figsize=(10, 6))
        self.canvas_overview = FigureCanvasTkAgg(self.fig_overview, master=chart_frame)
        self.canvas_overview.get_tk_widget().pack(fill="both", expand=True)

    def create_borrow_tab(self):
        # Frame cho bộ lọc
        filter_frame = ttk.Frame(self.borrow_tab)
        filter_frame.pack(fill="x", padx=10, pady=5)

        # Thời gian thống kê
        ttk.Label(filter_frame, text="Thời gian:").pack(side="left", padx=5)
        self.time_period = ttk.Combobox(filter_frame, values=["7 ngày", "30 ngày", "90 ngày"], state="readonly")
        self.time_period.pack(side="left", padx=5)
        self.time_period.set("30 ngày")
        
        ttk.Button(filter_frame, text="Cập nhật", command=self.update_borrow_stats).pack(side="left", padx=5)

        # Frame cho biểu đồ
        chart_frame = ttk.Frame(self.borrow_tab)
        chart_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Tạo figure cho matplotlib
        self.fig_borrow = plt.Figure(figsize=(10, 6))
        self.canvas_borrow = FigureCanvasTkAgg(self.fig_borrow, master=chart_frame)
        self.canvas_borrow.get_tk_widget().pack(fill="both", expand=True)

    def create_fine_tab(self):
        # Frame cho bảng thống kê phạt
        fine_frame = ttk.Frame(self.fine_tab)
        fine_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Treeview cho thống kê phạt
        columns = ("Độc giả", "Số lần vi phạm", "Tổng tiền phạt", "Đã thanh toán", "Chưa thanh toán")
        self.fine_tree = ttk.Treeview(fine_frame, columns=columns, show="headings")

        for col in columns:
            self.fine_tree.heading(col, text=col)
            self.fine_tree.column(col, width=150)

        # Scrollbar
        scrollbar = ttk.Scrollbar(fine_frame, orient="vertical", command=self.fine_tree.yview)
        self.fine_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.fine_tree.pack(fill="both", expand=True)

    def create_category_tab(self):
        # Frame cho biểu đồ
        chart_frame = ttk.Frame(self.category_tab)
        chart_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Tạo figure cho matplotlib
        self.fig_category = plt.Figure(figsize=(10, 6))
        self.canvas_category = FigureCanvasTkAgg(self.fig_category, master=chart_frame)
        self.canvas_category.get_tk_widget().pack(fill="both", expand=True)

    def load_statistics(self):
        if not self.conn:
            return

        try:
            cur = self.conn.cursor()

            # Thống kê tổng quan
            # 1. Tổng số sách
            cur.execute("SELECT COUNT(*) FROM books")
            total_books = cur.fetchone()[0]
            self.metric_labels["Tổng số sách"].config(text=str(total_books))

            # 2. Tổng số độc giả
            cur.execute("SELECT COUNT(*) FROM members")
            total_members = cur.fetchone()[0]
            self.metric_labels["Tổng số độc giả"].config(text=str(total_members))

            # 3. Sách đang được mượn
            cur.execute("SELECT COUNT(*) FROM book_copies WHERE status = 'borrowed'")
            borrowed_books = cur.fetchone()[0]
            self.metric_labels["Sách đang được mượn"].config(text=str(borrowed_books))

            # 4. Số lượt mượn sách
            cur.execute("SELECT COUNT(*) FROM issued_status")
            total_borrows = cur.fetchone()[0]
            self.metric_labels["Số lượt mượn sách"].config(text=str(total_borrows))

            # 5. Tổng tiền phạt
            cur.execute("SELECT COALESCE(SUM(fine_amount), 0) FROM fines")
            total_fines = cur.fetchone()[0]
            self.metric_labels["Tổng tiền phạt"].config(text=f"{total_fines:,.0f} VND")

            # 6. Số độc giả đang bị phạt
            cur.execute("SELECT COUNT(DISTINCT member_id) FROM fines WHERE payment_status = 'unpaid'")
            members_with_fines = cur.fetchone()[0]
            self.metric_labels["Số độc giả đang bị phạt"].config(text=str(members_with_fines))

            # Vẽ biểu đồ tổng quan
            self.plot_overview_charts(cur)

            # Vẽ biểu đồ mượn sách
            self.plot_borrow_charts(cur)

            # Load thống kê phạt
            self.load_fine_statistics(cur)

            # Vẽ biểu đồ thể loại
            self.plot_category_charts(cur)

            cur.close()

        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi tải thống kê: {str(e)}")

    def plot_overview_charts(self, cur):
        # Lấy dữ liệu cho biểu đồ cột: Số lượng sách theo thể loại
        cur.execute("""
            SELECT c.category_name, COUNT(b.isbn)
            FROM categories c
            LEFT JOIN books b ON c.category_id = b.category_id
            GROUP BY c.category_name
            ORDER BY COUNT(b.isbn) DESC
            LIMIT 5
        """)
        categories, book_counts = zip(*cur.fetchall())

        # Vẽ biểu đồ
        self.fig_overview.clear()
        ax = self.fig_overview.add_subplot(111)
        ax.bar(categories, book_counts)
        ax.set_title("Top 5 thể loại sách phổ biến")
        ax.set_ylabel("Số lượng sách")
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        self.fig_overview.tight_layout()
        self.canvas_overview.draw()

    def plot_borrow_charts(self, cur):
        # Lấy dữ liệu cho biểu đồ đường: Số lượt mượn sách theo thời gian
        days = int(self.time_period.get().split()[0])
        cur.execute("""
            SELECT DATE(issued_date), COUNT(*)
            FROM issued_status
            WHERE issued_date >= CURRENT_DATE - INTERVAL '%s days'
            GROUP BY DATE(issued_date)
            ORDER BY DATE(issued_date)
        """, (days,))
        dates, counts = zip(*cur.fetchall())

        # Vẽ biểu đồ
        self.fig_borrow.clear()
        ax = self.fig_borrow.add_subplot(111)
        ax.plot(dates, counts, marker='o')
        ax.set_title(f"Số lượt mượn sách trong {days} ngày qua")
        ax.set_ylabel("Số lượt mượn")
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        self.fig_borrow.tight_layout()
        self.canvas_borrow.draw()

    def load_fine_statistics(self, cur):
        # Xóa dữ liệu cũ
        for item in self.fine_tree.get_children():
            self.fine_tree.delete(item)

        # Lấy thống kê phạt
        cur.execute("""
            SELECT m.member_name,
                   COUNT(f.fine_id) as violation_count,
                   SUM(f.fine_amount) as total_fine,
                   SUM(CASE WHEN f.payment_status = 'paid' THEN f.fine_amount ELSE 0 END) as paid_amount,
                   SUM(CASE WHEN f.payment_status = 'unpaid' THEN f.fine_amount ELSE 0 END) as unpaid_amount
            FROM members m
            JOIN fines f ON m.member_id = f.member_id
            GROUP BY m.member_name
            ORDER BY total_fine DESC
        """)

        for row in cur.fetchall():
            self.fine_tree.insert("", "end", values=(
                row[0],
                row[1],
                f"{row[2]:,.0f} VND",
                f"{row[3]:,.0f} VND",
                f"{row[4]:,.0f} VND"
            ))

    def plot_category_charts(self, cur):
        # Lấy dữ liệu cho biểu đồ tròn: Tỷ lệ mượn sách theo thể loại
        cur.execute("""
            SELECT c.category_name, COUNT(i.issued_id)
            FROM categories c
            JOIN books b ON c.category_id = b.category_id
            JOIN issued_status i ON b.isbn = i.issued_book_isbn
            GROUP BY c.category_name
            ORDER BY COUNT(i.issued_id) DESC
        """)
        results = cur.fetchall()
        categories = [row[0] for row in results]
        counts = [row[1] for row in results]

        # Vẽ biểu đồ
        self.fig_category.clear()
        ax = self.fig_category.add_subplot(111)
        ax.pie(counts, labels=categories, autopct='%1.1f%%')
        ax.set_title("Tỷ lệ mượn sách theo thể loại")
        self.fig_category.tight_layout()
        self.canvas_category.draw()

    def update_borrow_stats(self):
        """Cập nhật biểu đồ thống kê mượn sách khi thay đổi khoảng thời gian"""
        try:
            cur = self.conn.cursor()
            self.plot_borrow_charts(cur)
            cur.close()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi cập nhật thống kê: {str(e)}")

    def export_statistics(self):
        """Xuất báo cáo thống kê ra file"""
        try:
            cur = self.conn.cursor()
            
            # Tạo nội dung báo cáo
            report_content = "BÁO CÁO THỐNG KÊ THƯ VIỆN\n"
            report_content += f"Ngày xuất báo cáo: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            
            # Thống kê tổng quan
            report_content += "1. THỐNG KÊ TỔNG QUAN\n"
            metrics = ["Tổng số sách", "Tổng số độc giả", "Sách đang được mượn",
                      "Số lượt mượn sách", "Tổng tiền phạt", "Số độc giả đang bị phạt"]
            
            for metric in metrics:
                value = self.metric_labels[metric].cget("text")
                report_content += f"{metric}: {value}\n"
            
            # Thống kê mượn sách
            report_content += "\n2. THỐNG KÊ MƯỢN SÁCH GẦN ĐÂY\n"
            cur.execute("""
                SELECT DATE(issued_date), COUNT(*)
                FROM issued_status
                WHERE issued_date >= CURRENT_DATE - INTERVAL '30 days'
                GROUP BY DATE(issued_date)
                ORDER BY DATE(issued_date)
            """)
            
            for date, count in cur.fetchall():
                report_content += f"Ngày {date}: {count} lượt mượn\n"
            
            # Thống kê phạt
            report_content += "\n3. THỐNG KÊ PHẠT\n"
            cur.execute("""
                SELECT m.member_name,
                       COUNT(f.fine_id) as violation_count,
                       SUM(f.fine_amount) as total_fine,
                       SUM(CASE WHEN f.payment_status = 'paid' 
                           THEN f.fine_amount ELSE 0 END) as paid_amount,
                       SUM(CASE WHEN f.payment_status = 'unpaid' 
                           THEN f.fine_amount ELSE 0 END) as unpaid_amount
                FROM members m
                JOIN fines f ON m.member_id = f.member_id
                GROUP BY m.member_name
                ORDER BY total_fine DESC
            """)
            
            for row in cur.fetchall():
                report_content += f"\nĐộc giả: {row[0]}\n"
                report_content += f"Số lần vi phạm: {row[1]}\n"
                report_content += f"Tổng tiền phạt: {row[2]:,.0f} VND\n"
                report_content += f"Đã thanh toán: {row[3]:,.0f} VND\n"
                report_content += f"Chưa thanh toán: {row[4]:,.0f} VND\n"
            
            # Thống kê theo thể loại
            report_content += "\n4. THỐNG KÊ THEO THỂ LOẠI\n"
            cur.execute("""
                SELECT c.category_name, COUNT(i.issued_id)
                FROM categories c
                JOIN books b ON c.category_id = b.category_id
                JOIN issued_status i ON b.isbn = i.issued_book_isbn
                GROUP BY c.category_name
                ORDER BY COUNT(i.issued_id) DESC
            """)
            
            for category, count in cur.fetchall():
                report_content += f"{category}: {count} lượt mượn\n"
            
            # Lưu báo cáo
            filename = f"library_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(report_content)
            
            messagebox.showinfo("Thành công", f"Đã xuất báo cáo thành công!\nTên file: {filename}")
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi xuất báo cáo: {str(e)}")
        finally:
            cur.close()

    def go_back(self):
        self.parent.destroy()
        self.show_main_callback()