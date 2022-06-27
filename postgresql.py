import psycopg2


def create_db(conn):
    conn.execute("""
                DROP TABLE IF EXISTS phone;
                DROP TABLE IF EXISTS client;
            """)
    conn.execute("""
                CREATE TABLE IF NOT EXISTS client(
                            id SERIAL PRIMARY KEY,
                    first_name VARCHAR(60) NOT NULL,
                     last_name VARCHAR(60) NOT NULL,
                         email VARCHAR(60) NOT NULL UNIQUE
                );
                CREATE TABLE IF NOT EXISTS phone(
                              id SERIAL PRIMARY KEY,
                       client_id INTEGER REFERENCES client(id),
                    number_phone VARCHAR(18) NOT NULL
                );
            """)


def add_client(conn, first_name, last_name, email, phone=None):
    conn.execute("""
           INSERT INTO client(first_name, last_name, email) 
           VALUES (%s, %s, %s);            
       """, (first_name, last_name, email))
    if phone != None:
        conn.execute("""
                   SELECT c.id 
                     FROM client c
                    WHERE c.email = %s;                          
           """, (email,))
        client_id = conn.fetchone()[0]
        conn.execute("""
               INSERT INTO phone(client_id, number_phone)
               VALUES (%s, %s);
           """, (client_id, phone))


def add_phone(conn, client_id, number_phone):
    conn.execute("""
        INSERT INTO phone( client_id, number_phone) 
        VALUES (%s, %s);            
    """, (client_id, number_phone))


def change_client(conn, client_id, first_name=None, last_name=None, email=None, phone=None):
    conn.execute("""
        UPDATE client
           SET first_name = %s      
         WHERE id = %s;                 
        UPDATE client
           SET last_name = %s      
         WHERE id = %s;                 
        UPDATE client
           SET email = %s      
         WHERE id = %s;                 
    """, (first_name, client_id, last_name, client_id, email, client_id,))
    if phone != None:
        conn.execute("""
                   SELECT c.id 
                     FROM client c
                    WHERE c.email = %s;                          
           """, (email,))
        client_id = conn.fetchone()[0]
        conn.execute("""
               INSERT INTO phone(client_id, number_phone)
               VALUES (%s, %s);
           """, (client_id, phone))


def delete_phone(conn, client_id, phone):
    conn.execute("""
        DELETE FROM phone      
         WHERE client_id=%s and  number_phone=%s;                 
    """, (client_id, phone))


def delete_client(conn, client_id):
    conn.execute("""
        DELETE FROM phone      
         WHERE client_id=%s;
        DELETE FROM client      
         WHERE id=%s;                 
    """, (client_id, client_id))


def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    conn.execute("""
        SELECT c.first_name, c.last_name, c.email, p.number_phone 
          FROM client c
          JOIN phone p on c.id = p.client_id
         WHERE first_name=%s OR last_name = %s OR email = %s OR number_phone = %s
    """, (first_name, last_name, email, phone))
    return conn.fetchall()


with psycopg2.connect(database="python_client_db", user="postgres", password="123456") as conn:
    with conn.cursor() as cur:
        create_db(cur)
        add_client(cur, "John", "Smith", "smit@mail.ru","+99999999999")
        add_client(cur, "Mikchael", "Jordan", "mimimiska@mail.ru")
        add_client(cur, "Michael", "Tyson", "mimimiska2@mail.ru","+54384958122")
        add_phone(cur, 1, "+78945642113")
        add_phone(cur, 2, "+78945648913")
        add_phone(cur, 2, "+83883456201")
        change_client(cur, 1, "James", "Bond", "bond@mail.ru")
        delete_phone(cur, 1, "+78945648913")
        delete_client(cur, 1)
        print(find_client(cur, "Mikchael"))
    conn.commit()
conn.close()
