
-- 1. Bảng Chi nhánh thư viện
CREATE TABLE branch (
    branch_id VARCHAR(10) PRIMARY KEY,
    manager_id VARCHAR(10),
    branch_name VARCHAR(50),
    branch_address VARCHAR(100),
    contact_no VARCHAR(15),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Bảng Nhân viên
CREATE TABLE employees (
    emp_id VARCHAR(10) PRIMARY KEY,
    emp_name VARCHAR(50),
    position VARCHAR(30),
    salary NUMERIC(10,2),  -- PostgreSQL thường dùng NUMERIC thay vì DECIMAL
    branch_id VARCHAR(10),
    contact_no VARCHAR(15),
    email VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (branch_id) REFERENCES branch(branch_id)
);

-- 3. Bảng Thành viên/Độc giả
CREATE TABLE members (
    member_id VARCHAR(10) PRIMARY KEY,
    member_name VARCHAR(50),
    member_address VARCHAR(100),
    phone_number VARCHAR(15),
    email VARCHAR(50),
    reg_date DATE,
    membership_type VARCHAR(20),
    membership_end_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Bảng Sách
CREATE TABLE books (
    isbn VARCHAR(50) PRIMARY KEY,
    book_title VARCHAR(100),
    category_id VARCHAR(10),
    rental_price NUMERIC(10,2),
    publisher VARCHAR(50),
    publication_year INTEGER,  -- PostgreSQL dùng INTEGER thay vì INT
    shelf_location VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. Bảng Bản sao sách
CREATE TABLE book_copies (
    copy_id VARCHAR(10) PRIMARY KEY,
    isbn VARCHAR(50),
    branch_id VARCHAR(10),
    status VARCHAR(15),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_book FOREIGN KEY (isbn) REFERENCES books(isbn),
    CONSTRAINT fk_branch FOREIGN KEY (branch_id) REFERENCES branch(branch_id),
    CONSTRAINT check_status CHECK (status IN ('available', 'borrowed', 'reserved', 'maintenance', 'lost'))
);

-- 6. Bảng Đặt trước sách
CREATE TABLE book_reservations (
    reservation_id VARCHAR(10) PRIMARY KEY,
    member_id VARCHAR(10),
    copy_id VARCHAR(10),
    reservation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reservation_status VARCHAR(15),
    expiration_date TIMESTAMP,
    CONSTRAINT fk_member FOREIGN KEY (member_id) REFERENCES members(member_id),
    CONSTRAINT fk_copy FOREIGN KEY (copy_id) REFERENCES book_copies(copy_id)
);

-- 7. Bảng Mượn sách
CREATE TABLE issued_status (
    issued_id VARCHAR(10) PRIMARY KEY,
    member_id VARCHAR(10),
    copy_id VARCHAR(10),
    issued_date DATE DEFAULT CURRENT_DATE,
    due_date DATE,
    issued_emp_id VARCHAR(10),
    branch_id VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (member_id) REFERENCES members(member_id),
    FOREIGN KEY (copy_id) REFERENCES book_copies(copy_id),
    FOREIGN KEY (issued_emp_id) REFERENCES employees(emp_id),
    FOREIGN KEY (branch_id) REFERENCES branch(branch_id)
);

-- 8. Bảng Trả sách
CREATE TABLE return_status (
    return_id VARCHAR(10) PRIMARY KEY,
    issued_id VARCHAR(10),
    return_date DATE DEFAULT CURRENT_DATE,
    fine_amount NUMERIC(10,2),
    return_condition VARCHAR(20),
    return_emp_id VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (issued_id) REFERENCES issued_status(issued_id),
    FOREIGN KEY (return_emp_id) REFERENCES employees(emp_id)
);

-- 9. Bảng Tác giả
CREATE TABLE authors (
    author_id VARCHAR(10) PRIMARY KEY,
    author_name VARCHAR(50),
    nationality VARCHAR(30),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 10. Bảng Thể loại sách
CREATE TABLE categories (
    category_id VARCHAR(10) PRIMARY KEY,
    category_name VARCHAR(30),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 11. Bảng liên kết Sách-Tác giả
CREATE TABLE book_authors (
    isbn VARCHAR(50),
    author_id VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (isbn, author_id),
    FOREIGN KEY (isbn) REFERENCES books(isbn),
    FOREIGN KEY (author_id) REFERENCES authors(author_id)
);

-- 12. Bảng Tiền phạt
CREATE TABLE fines (
    fine_id VARCHAR(10) PRIMARY KEY,
    member_id VARCHAR(10),
    issued_id VARCHAR(10),
    fine_amount NUMERIC(10,2),
    fine_date DATE DEFAULT CURRENT_DATE,
    payment_status VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (member_id) REFERENCES members(member_id),
    FOREIGN KEY (issued_id) REFERENCES issued_status(issued_id)
);