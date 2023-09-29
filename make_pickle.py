import sqlite3
import pickle
import pandas as pd
import streamlit as st

if __name__ == '__main__':
    print("Hello World!")
    # Connect to SQLite database and query table
    conn = sqlite3.connect('genomes.db')
    df = pd.read_sql_query('SELECT accession, genome_size FROM refseq', conn)
    print(df)
    # Create dictionary with accession as key, genome_size as value
    genome_dict = df.set_index('accession')['genome_size'].to_dict() 
    print(genome_dict)
    # Save dictionary to a pickle file
    with open('refseq.pkl', 'wb') as f:
        pickle.dump(genome_dict, f)