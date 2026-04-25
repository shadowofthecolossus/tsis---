import psycopg2

moy_parol = "12345678" #password 

try:
    baza = psycopg2.connect(
        host="localhost",
        database="phonebooktest",
        user="postgres",
        password=moy_parol
    )
    
    print("work")
    baza.close()
    
except Exception as i:
    print("not working", i)