from database.DB_connect import DBConnect
from model.state import State


class DAO():
    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT DISTINCT Year(s.`datetime`) as year
                    FROM sighting s  """

        cursor.execute(query)

        for row in cursor:
            result.append(row["year"])

        cursor.close()
        conn.close()
        return result



    @staticmethod
    def getShapesByYear(anno):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT DISTINCT s.shape 
                    FROM sighting s 
                    WHERE Year(s.`datetime`) = %s and s.shape != ""  """

        cursor.execute(query, (anno,))

        for row in cursor:
            result.append(row["shape"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllStates():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT * FROM state s """

        cursor.execute(query)

        for row in cursor:
            result.append(State(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllNeighbors():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT *
                    FROM neighbor n 
                    WHERE state1<state2 """

        cursor.execute(query)

        for row in cursor:
            result.append((row["state1"], row["state2"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getWeightNeighbors(s1,s2,year,shape):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT t1.N1 + t2.N2 as somma
                    FROM (SELECT count(*) as N1
                    from sighting s 
                    WHERE s.state = %s and Year(s.`datetime`) = %s and s.shape = %s) as t1,
                    (SELECT count(*) as N2
                    from sighting s 
                    WHERE s.state = %s and Year(s.`datetime`) = %s and s.shape = %s) as t2 """

        cursor.execute(query, (s1,year,shape,s2,year,shape,))

        for row in cursor:
            result.append(row["somma"])

        cursor.close()
        conn.close()
        return result