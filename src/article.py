from src.database import connectDatabase


def getSources():
    connection = connectDatabase()
    cursor = connection.cursor()
    
    source_id = 1
    query = "SELECT * FROM sources"
    
    cursor.execute(query)
    sources = []
    results = cursor.fetchall()
    for row in results:
        sources.append({"id": row[0], "nom": row[1], "lien": row[2]})
        print(f"ID: {row[0]}, Nom: {row[1]}, Lien: {row[2]}")
    cursor.close()
    connection.close()
    return sources
