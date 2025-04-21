-- Drop tables if they exist (optional, for easier re-running)
DROP TABLE IF EXISTS Order_Items;
DROP TABLE IF EXISTS Orders;
DROP TABLE IF EXISTS Products;
DROP TABLE IF EXISTS Categories;
DROP TABLE IF EXISTS Customers;

-- Create Categories table
CREATE TABLE Categories (
    category_id INT PRIMARY KEY IDENTITY(1,1), -- Use IDENTITY for SQL Server. Auto-increment for MYSQL. SERIAL FOR PostgreSQL.
    category_name VARCHAR(255) NOT NULL UNIQUE
);

-- Create Customers table
CREATE TABLE Customers (
    customer_id INT PRIMARY KEY IDENTITY(1,1), -- Use IDENTITY for SQL Server auto-increment
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    address TEXT,
    phone VARCHAR(50) -- Increased size to accommodate longer phone numbers
);

-- Create Products table
CREATE TABLE Products (
    product_id INT PRIMARY KEY IDENTITY(1,1), -- Use IDENTITY for SQL Server auto-increment
    product_name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL CHECK (price >= 0),
    category_id INT,
    FOREIGN KEY (category_id) REFERENCES Categories(category_id) ON DELETE SET NULL ON UPDATE CASCADE
);

-- Create Orders table
CREATE TABLE Orders (
    order_id INT PRIMARY KEY IDENTITY(1,1), -- Use IDENTITY for SQL Server auto-increment
    customer_id INT,
    order_date DATE NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL CHECK (total_amount >= 0),
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id) ON DELETE CASCADE ON UPDATE CASCADE -- Cascade delete/update if customer is removed/changed
);

-- Create Order_Items table (Junction table for Orders and Products)
CREATE TABLE Order_Items (
    order_id INT,
    product_id INT,
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10, 2) NOT NULL CHECK (unit_price >= 0), -- Price at the time of order
    PRIMARY KEY (order_id, product_id), -- Composite primary key
    FOREIGN KEY (order_id) REFERENCES Orders(order_id) ON DELETE CASCADE ON UPDATE CASCADE, -- Cascade delete/update if order is removed/changed
    FOREIGN KEY (product_id) REFERENCES Products(product_id) ON DELETE NO ACTION ON UPDATE CASCADE -- Use NO ACTION (default behavior, similar to RESTRICT) for SQL Server
);

-- Add indexes for frequently queried columns (optional but recommended) # Building index can speed up query performance. Use it for frequently quired columns.
CREATE INDEX idx_customer_email ON Customers(email);
CREATE INDEX idx_product_name ON Products(product_name);
CREATE INDEX idx_category_name ON Categories(category_name);
CREATE INDEX idx_order_date ON Orders(order_date);
