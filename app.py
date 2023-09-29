import pandas as pd
import streamlit as st
import pickle
db = "refseq.pkl"

def sum_read_lengths_by_reference_and_taxid(df):
    # Group DataFrame by closet_reference and taxid and sum read_length values
    read_length_sum = df.groupby(['closet_reference', 'taxid'])['read_length'].sum()
    print(read_length_sum.head())
    # Convert resulting Series to DataFrame and reset index
    read_length_df = read_length_sum.to_frame().reset_index()
    print(read_length_df.head())
    # Rename columns
    read_length_df.columns = ['closet_reference', 'taxid', 'read_length_sum']
    
    return read_length_df

# Function to estimate genome coverage
def estimate_coverage(genome_size, read_lengths):
    coverage = read_lengths / genome_size
    return coverage

if __name__ == '__main__':
    # Streamlit app
    st.title('Add Genome Size Column')

    uploaded_file = st.file_uploader('Upload CSV File')
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        df['taxid'] = df['taxid'].astype(str)
        df = sum_read_lengths_by_reference_and_taxid(df)
        # Load genome size dict
        with open(db, 'rb') as f:
            genome_dict = pickle.load(f)
            
        # Create new column using dict
        df['genome_size'] = df['closet_reference'].map(genome_dict)
        
        # Calculate estimated genome coverage
        df['coverage'] = estimate_coverage(df['genome_size'], df['read_length_sum'])
        
        # Display table
        st.markdown('### Table with Estimated Genome Coverage')
        st.write(df)
        
        # Download button for updated CSV file
        st.markdown('### File with New Genome Size and Coverage Columns')
        st.download_button(
            label='Download CSV',
            data=df.to_csv().encode('utf-8'),
            file_name='output.csv',
            mime='text/csv',
        )