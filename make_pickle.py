import sqlite3
import pickle
import pandas as pd
import streamlit as st

if __name__ == '__main__':
    print("Hello World!")
    # Connect to SQLite database and query table
    conn = sqlite3.connect('genomes.db')
    df = pd.read_sql_query('SELECT accession, description, genome_size FROM refseq', conn)
    print(df)
    # Create dictionary with accession as key, genome_size as value
    genome_dict = {}
    for _, row in df.iterrows():
        genome_dict[row['accession']] = {
            'description': row['description'],
            'genome_size': row['genome_size']
        }
    print(genome_dict)
    # Save dictionary to a pickle file
    with open('refseq_v2.pkl', 'wb') as f:
        pickle.dump(genome_dict, f)