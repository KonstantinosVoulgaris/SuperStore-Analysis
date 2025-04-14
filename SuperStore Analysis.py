import sqlite3
from tabulate import tabulate

# Σύνδεση με τη βάση δεδομένων (ή δημιουργία νέας)
conn = sqlite3.connect('superstore.db')
cursor = conn.cursor()

# Διαγραφή του πίνακα αν υπάρχει ήδη (για να αποφύγουμε σφάλματα)
cursor.execute('DROP TABLE IF EXISTS superstore;')

# Δημιουργία πίνακα Superstore
cursor.execute('''
CREATE TABLE superstore (
    OrderID INTEGER PRIMARY KEY,
    ProductID TEXT,
    Category TEXT,
    Sales REAL,
    Profit REAL,
    Quantity INTEGER,
    Discount REAL,
    OrderDate TEXT,
    ShipDate TEXT,
    Region TEXT,
    City TEXT
);
''')

# Εισαγωγή δεδομένων στον πίνακα
cursor.executemany('''
INSERT INTO superstore (OrderID, ProductID, Category, Sales, Profit, Quantity, Discount, OrderDate, ShipDate, Region, City)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
''', [
    (1, 'P001', 'Technology', 250.00, 50.00, 2, 0.1, '2025-03-01', '2025-03-03', 'East', 'New York'),
    (2, 'P002', 'Furniture', 400.00, 80.00, 1, 0.15, '2025-03-02', '2025-03-04', 'West', 'Los Angeles'),
    (3, 'P003', 'Office Supplies', 150.00, 30.00, 5, 0.05, '2025-03-02', '2025-03-06', 'East', 'Boston'),
    (4, 'P004', 'Technology', 500.00, 120.00, 3, 0.2, '2025-03-03', '2025-03-05', 'South', 'Houston'),
    (5, 'P005', 'Office Supplies', 100.00, 20.00, 2, 0.1, '2025-03-04', '2025-03-07', 'North', 'Chicago'),
    (6, 'P006', 'Furniture', 200.00, 40.00, 1, 0.1, '2025-03-05', '2025-03-08', 'West', 'San Francisco'),
    (7, 'P007', 'Technology', 300.00, 60.00, 4, 0.15, '2025-03-06', '2025-03-09', 'East', 'Philadelphia'),
    (8, 'P008', 'Furniture', 350.00, 70.00, 2, 0.2, '2025-03-07', '2025-03-10', 'South', 'Miami'),
    (9, 'P009', 'Office Supplies', 80.00, 15.00, 4, 0.05, '2025-03-08', '2025-03-11', 'North', 'Seattle'),
    (10, 'P010', 'Technology', 600.00, 150.00, 6, 0.1, '2025-03-09', '2025-03-12', 'East', 'New York')
])

# Εκτύπωση όλων των δεδομένων του πίνακα superstore με tabulate
cursor.execute('SELECT * FROM superstore;')
rows = cursor.fetchall()

# Εκτύπωση σε όμορφο πίνακα
print("\nSuperstore data:")
headers = [description[0] for description in cursor.description]  # Τα ονόματα των στηλών
print(tabulate(rows, headers=headers, tablefmt="grid"))

# 1. Ποιες είναι οι 5 πιο κερδοφόρες κατηγορίες;
cursor.execute(''' SELECT Category, SUM(Profit) AS Total_Profit FROM superstore GROUP BY Category ORDER BY Total_Profit DESC LIMIT 5; ''')
print("Top 5 most profitable categories:")
print(cursor.fetchall())
print()

# 2. Ποιες περιοχές έχουν τις περισσότερες πωλήσεις;
cursor.execute(''' SELECT Region, SUM(Sales) AS Total_Sales FROM superstore GROUP BY Region ORDER BY Total_Sales DESC; ''')
print("\nRegions with highest sales:")
print(cursor.fetchall())
print()

# 3. Ποιες είναι οι κορυφαίοι 10 πελάτες σε πωλήσεις (πόλεις);
cursor.execute(''' SELECT City, SUM(Sales) AS Total_Sales FROM superstore GROUP BY City ORDER BY Total_Sales DESC LIMIT 10; ''')
print("\nTop 10 cities with highest sales:")
print(cursor.fetchall())
print()

# 4. Ποιες είναι οι 5 πιο πουλημένες κατηγορίες (βάσει ποσότητας);
cursor.execute(''' SELECT Category, SUM(Quantity) AS Total_Quantity FROM superstore GROUP BY Category ORDER BY Total_Quantity DESC LIMIT 5; ''')
print("\nTop 5 most sold categories by quantity:")
print(cursor.fetchall())
print()

# 5. Ποιες πόλεις είχαν τα περισσότερα κέρδη;
cursor.execute('''SELECT City, SUM(Profit) AS Total_Profit FROM superstore GROUP BY City ORDER BY Total_Profit DESC LIMIT 5; ''')
print("\nTop 5 cities with highest profit:")
print(cursor.fetchall())
print()

# 6. Ποιες παραγγελίες είχαν την μεγαλύτερη έκπτωση;
cursor.execute(''' SELECT OrderID, Discount, Sales, Profit FROM superstore ORDER BY Discount DESC LIMIT 5;''')
print("\nTop 5 orders with highest discount:")
print(cursor.fetchall())
print()

# Κλείσιμο σύνδεσης με τη βάση δεδομένων
conn.commit()
conn.close()


