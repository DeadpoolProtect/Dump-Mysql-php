import os
import mysql.connector


mysql_connection_string = {
    'host': '',
    'database': '',
    'user': '',
    'password': ''
}

# Créer un dossier pour les fichiers SQL s'il n'existe pas
output_folder = "tables_sql"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Se connecter à la base de données
try:
    connection = mysql.connector.connect(**mysql_connection_string)
    print("Connexion réussie à la base de données MySQL!")
except mysql.connector.Error as error:
    print("Échec de la connexion à la base de données MySQL: {}".format(error))
    exit(1)


cursor = connection.cursor()

# Récupérer les noms des tables dans la base de données
cursor.execute("SHOW TABLES")
tables = cursor.fetchall()
table_names = [table[0] for table in tables]


for table_name in table_names:
    sql_file_path = os.path.join(output_folder, f"{table_name}.sql")
    with open(sql_file_path, 'w', encoding='utf-8') as sql_file:
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        for row in rows:
            values = ', '.join([f"'{str(value)}'" for value in row])
            insert_statement = f"INSERT INTO {table_name} VALUES ({values});\n"
            sql_file.write(insert_statement)

    print(f"Données de la table '{table_name}' exportées dans le fichier '{sql_file_path}'")

# Fermer la connexion et le curseur
cursor.close()
connection.close()
