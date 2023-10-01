import pandas as pd
import streamlit as st
import pickle
# db = "refseq.pkl"
db = "refseq_v2.pkl"

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
        _uploaded_file_name = uploaded_file.filename
        df = pd.read_csv(uploaded_file)
        df['taxid'] = df['taxid'].astype(str)
        df = sum_read_lengths_by_reference_and_taxid(df)
        # Load genome size dict
        with open(db, 'rb') as f:
            genome_dict = pickle.load(f)
            
        # Create new column using dict
        for col in ['genome_size', 'description']:
            df[col] = df['closet_reference'].map(genome_dict).map(lambda x: x[col])
        
        # df['genome_size'] = df['closet_reference'].map(genome_dict).map(lambda x: x['genome_size'])
        # df['description'] = df['closet_reference'].map(genome_dict).map(lambda x: x['description'])
        
    
        # Calculate estimated genome coverage
        df['coverage'] = estimate_coverage(df['genome_size'], df['read_length_sum'])
        
        # Display table
        st.markdown('### Table with Estimated Genome Coverage by Reference')
        st.write(df)
        # Download button for updated CSV file
        st.markdown('### File with New Genome Size and Coverage Columns')
        st.download_button(
            label='Download CSV',
            data=df.to_csv().encode('utf-8'),
            file_name=f'{_uploaded_file_name}_by_reference.csv',
            mime='text/csv',
        )
        # Coverage by taxid
        new_df = df.copy()
        # Calculate the new coverage for each row based on the genome size and coverage, and sum it by taxid
        new_df['new_coverage'] = new_df.apply(lambda row: row['genome_size'] / new_df[new_df['taxid'] == row['taxid']]['genome_size'].sum() * row['coverage'], axis=1)
        new_df = new_df.groupby('taxid').agg({'new_coverage': 'sum', 'read_length_sum': 'sum'}).reset_index()
        st.markdown('### Table with Estimated Genome New Coverage by TaxID ###')
        st.write(new_df)
        st.download_button(
            label='Download CSV',
            data=new_df.to_csv().encode('utf-8'),
            file_name=f'{_uploaded_file_name}_by_taxid.csv',
            mime='text/csv',
        )