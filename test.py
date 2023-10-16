import os
import sys
from dotenv import load_dotenv, find_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
import pinecone
import streamlit as st
import pandas as pd

# Add the sifter_support_shared directory to the system path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'sifter_support_shared'))
from functions.doc_loader import insert_or_fetch_embeddings
from functions.q_and_a import ask_with_memory, ask_and_get_answer


def clear_history():
    if 'history' in st.session_state:
        del st.session_state['history']


load_dotenv(find_dotenv(), override=True)
api_key = os.environ['OPENAI_API_KEY']
index_name = 'garmin'
vector_store = insert_or_fetch_embeddings(index_name)


def load_headers():
    st.title("Sifter: Intelligent Search Tools")
    ""
    st.subheader("Test: Garmin wearables")
    if 'vs' not in st.session_state:
        st.session_state.vs = vector_store


def create_selector_dropdown():
    df = pd.read_csv('data/current_wearables.csv')
    df['product_id'] = df['product_id'].astype(str)
    label = "Select the model you need to ask about:"
    with st.sidebar:
        st.image('sifter_support_shared/images/Garmin.png')
        option = st.selectbox(label=label, options=df)
        if option:
            # Add a loading bar here?
            temp_df = df[df['product_name'] == option]
            st.write("**Currently viewing:**", option)
            st.write('**Category:**', temp_df['product_category'].values[0])
            st.write('**Sub-category:**', temp_df['product_subcategory'].values[0])
            st.write('**Product ID:**', temp_df['product_id'].values[0])
            st.write('**Part Number:**', temp_df['part_number'].values[0])
            st.write('**Listing URL:**', temp_df['product_url'].values[0])
            st.write('**Manual URL:**', temp_df['product_manual_url'].values[0])


def allow_input():
    q = st.text_input('Ask a question about Garmin wearables:')
    if q:
        if 'vs' in st.session_state:
            vector_store = st.session_state.vs
            st.write(f"k: {vector_store}")  # debugging only
            answer = ask_and_get_answer(vector_store, q)
            st.text_area("LLM Answer:", value=answer, height=200)

            st.divider()

            if 'history' not in st.session_state:
                st.session_state.history = ''
            value = f'Q: {q} \nA: {answer}'
            st.session_state.history = f'{value} \n{"-" * 100} \n {st.session_state.history}'
            h = st.session_state.history
            st.text_area(label='Chat History', value=h,
                         key='history', height=400)


if __name__ == "__main__":
    load_headers()
    create_selector_dropdown()
    # allow_input()
