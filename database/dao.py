from database.DB_connect import DBConnect
from model.artist import Artist


class DAO:

    @staticmethod
    def read_role():
        conn = DBConnect.get_connection()
        result = []
        if conn is None:
            print("❌ Errore di connessione al database.")
            return None

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT DISTINCT(role) FROM authorship """
        try:
            cursor.execute(query)
            for row in cursor:
                result.append(row["role"])
        except Exception as e:
            print(f"Errore durante la query read_role: {e}")
            result = None
        finally:
            cursor.close()
            conn.close()

        return result

    @staticmethod
    def read_names():
        conn = DBConnect.get_connection()
        result = {}
        if conn is None:
            print("❌ Errore di connessione al database.")
            return None

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * FROM artists """
        try:
            cursor.execute(query)
            for row in cursor:
                result[row["artist_id"]] = row["name"]
        except Exception as e:
            print(f"Errore durante la query read_names: {e}")
            result = None
        finally:
            cursor.close()
            conn.close()

        return result

    @staticmethod
    def read_connections(role):
        conn = DBConnect.get_connection()
        result = {}
        if conn is None:
            print("❌ Errore di connessione al database.")
            return None

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT artist_id, COUNT(artist_id) 
                    FROM authorship au, objects o 
                    WHERE o.object_id = au.object_id AND o.curator_approved = 1 AND au.role = %s 
                    GROUP BY au.artist_id """
        try:
            cursor.execute(query, (role,))
            for row in cursor:
                artist = Artist(row["artist_id"],row["COUNT(artist_id)"])
                result[row['artist_id']] = artist


        except Exception as e:
            print(f"Errore durante la query read_connections: {e}")
            result = None
        finally:
            cursor.close()
            conn.close()

        return result