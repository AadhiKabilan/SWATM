import pyodbc
try:
    connection = pyodbc.connect(
        'DSN=OracleDSN1;'
        'UID=Aadhi;'
        'PWD=123;'
    )
    print("Connection successful!")
except pyodbc.Error as e:
    print("Error:", e)
