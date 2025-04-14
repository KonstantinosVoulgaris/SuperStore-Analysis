import sqlite3
import streamlit as st
import pandas as pd

st.title("📊 Superstore Analyzer")

# Δημιουργία/φόρτωση της βάσης δεδομένων
def create_and_load_db():
    conn = sqlite3.connect('superstore.db')
    cursor = conn.cursor()

    cursor.execute('DROP TABLE IF EXISTS superstore;')

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

    conn.commit()
    return conn

conn = create_and_load_db()

# Εμφάνιση πλήρους πίνακα
if st.checkbox("📋 Εμφάνισε όλα τα δεδομένα"):
    df = pd.read_sql_query("SELECT * FROM superstore", conn)
    st.dataframe(df)

# Επιλογή ανάλυσης
query_options = {
    "Top 5 πιο κερδοφόρες κατηγορίες": '''
        SELECT Category, SUM(Profit) AS Total_Profit 
        FROM superstore 
        GROUP BY Category 
        ORDER BY Total_Profit DESC 
        LIMIT 5;
    ''',
    "Περιοχές με τις περισσότερες πωλήσεις": '''
        SELECT Region, SUM(Sales) AS Total_Sales 
        FROM superstore 
        GROUP BY Region 
        ORDER BY Total_Sales DESC;
    ''',
    "Top 10 πόλεις με τις υψηλότερες πωλήσεις": '''
        SELECT City, SUM(Sales) AS Total_Sales 
        FROM superstore 
        GROUP BY City 
        ORDER BY Total_Sales DESC 
        LIMIT 10;
    ''',
    "Top 5 κατηγορίες βάσει ποσότητας": '''
        SELECT Category, SUM(Quantity) AS Total_Quantity 
        FROM superstore 
        GROUP BY Category 
        ORDER BY Total_Quantity DESC 
        LIMIT 5;
    ''',
    "Top 5 πόλεις με τα περισσότερα κέρδη": '''
        SELECT City, SUM(Profit) AS Total_Profit 
        FROM superstore 
        GROUP BY City 
        ORDER BY Total_Profit DESC 
        LIMIT 5;
    ''',
    "Top 5 παραγγελίες με τη μεγαλύτερη έκπτωση": '''
        SELECT OrderID, Discount, Sales, Profit 
        FROM superstore 
        ORDER BY Discount DESC 
        LIMIT 5;
    '''
}

option = st.selectbox("🔎 Διάλεξε ανάλυση", list(query_options.keys()))
if st.button("📊 Εκτέλεση ανάλυσης"):
    query = query_options[option]
    result = pd.read_sql_query(query, conn)
    st.subheader(f"Αποτελέσματα: {option}")
    st.dataframe(result)

# Κλείσιμο σύνδεσης (μόνο όταν τελειώσει η εφαρμογή)
# conn.close()  # Δεν το κλείνουμε εδώ γιατί streamlit κάνει re-run κάθε φορά
