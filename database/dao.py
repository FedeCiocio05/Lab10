from database.DB_connect import DBConnect
from model.compagnia import Compagnia
from model.hub import Hub
from model.tratta import Tratta

class DAO:
    """
    Implementare tutte le funzioni necessarie a interrogare il database.
    """

    @staticmethod
    def get_compagnia() -> list[Compagnia] | None:

        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("❌ Errore di connessione al database.")
            return None
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT * FROM compagnia"""
        try:
            cursor.execute(query)
            for row in cursor:
                compagnia = Compagnia(
                    id=row["id"],
                    codice=row["codice"],
                    nome=row["nome"],
                )
                result.append(compagnia)
        except Exception as e:
            print(f"Errore durante la query get_compagnia: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()

        return result


    @staticmethod
    def get_hub() -> list[Hub] | None:

        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("❌ Errore di connessione al database.")
            return None
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT * FROM hub"""
        try:
            cursor.execute(query)
            for row in cursor:
                hub = Hub(
                    id=row["id"],
                    codice=row["codice"],
                    nome=row["nome"],
                    citta=row["città"],
                    stato=row["stato"],
                    latitudine=row["latitudine"],
                    longitudine=row["longitudine"]
                )
                result.append(hub)
        except Exception as e:
            print(f"Errore durante la query get_hub: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()

        return result

    @staticmethod
    def get_tratta() -> list[Tratta] | None:

        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("❌ Errore di connessione al database.")
            return None
        cursor = cnx.cursor(dictionary=True)
        query = """ SELECT  LEAST(id_hub_origine,id_hub_destinazione) AS h1,
                            GREATEST(id_hub_origine,id_hub_destinazione) AS h2, 
                            SUM(valore_merce) AS valore_totale,
                            COUNT(*) AS n_spedizioni
                    FROM spedizione
                    GROUP BY h1,h2 """
        try:
            cursor.execute(query)
            for row in cursor:
                tratta = Tratta(
                    h1=row["h1"],
                    h2=row["h2"],
                    valore_totale=row["valore_totale"],
                    n_spedizioni=row["n_spedizioni"]
                )
                result.append(tratta)
        except Exception as e:
            print(f"Errore durante la query get_tratta: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()

        return result

    # TODO
