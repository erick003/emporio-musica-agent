import os
import glob
import sqlite3
import pandas as pd

DB_PATH = "emporio_musica.db"

def init_database(data_dir: str = "data") -> sqlite3.Connection:
    """Carrega os arquivos CSV da pasta data/ para o banco SQLite."""
    conn = sqlite3.connect(DB_PATH)
    csv_files = glob.glob(os.path.join(data_dir, "*.csv"))
    
    for file in csv_files:
        table_name = os.path.basename(file).replace(".csv", "").lower()
        df = pd.read_csv(file)
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        
    return conn

def execute_sql_query(query: str) -> str:
    """Executa consultas SQL de leitura e retorna o resultado formatado."""
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query(query, conn)
        conn.close()
        if df.empty:
            return "No records found matching the query."
        return df.to_string(index=False)
    except Exception as e:
        return f"Error executing database query: {str(e)}"