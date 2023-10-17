import os
import sys
from dotenv import load_dotenv, find_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
import pinecone
import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import yaml
from yaml.loader import SafeLoader

# Add the sifter_support_shared directory to the system path
sys.path.insert(0, os.path.join(os.path.dirname(__file__),
                                'sifter_support_shared'))
from functions.doc_loader import insert_or_fetch_embeddings
from functions.q_and_a import ask_with_memory, ask_and_get_answer


def load_yaml(file='credentials.yaml'):
    with open('credentials.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)
    return config


config = load_yaml()


def update_yaml(file='credentials.yaml'):
    with open('credentials.yaml', 'w') as file:
        yaml.dump(config, file, default_flow_style=False)


authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

load_dotenv(find_dotenv(), override=True)
api_key = os.environ['OPENAI_API_KEY']
index_name = 'garmin'


def clear_history():
    if 'history' in st.session_state:
        del st.session_state['history']


def load_headers():
    st.title("Sifter: Intelligent Search Tools")
    ""
    st.subheader("Context: Garmin wearables")
    if 'vs' not in st.session_state:
        vector_store = insert_or_fetch_embeddings(index_name)
        st.session_state.vs = vector_store


def select_and_ask():
    df = pd.read_csv('data/current_wearables.csv')
    df['product_id'] = df['product_id'].astype(str)
    label = "Select the model you need to ask about:"
    with st.sidebar:
        st.image('sifter_support_shared/images/Garmin.png')
        option = st.selectbox(label=label, options=df)
        if option:
            # Add a loading bar here?
            temp_df = df[df['product_name'] == option]
            product = temp_df['product_name'].values[0]
            st.write("**Currently viewing:**", option)
            st.write('**Category:**', temp_df['product_category'].values[0])
            st.write('**Sub-category:**', temp_df['product_subcategory'].values[0])
            st.write('**Product ID:**', temp_df['product_id'].values[0])
            st.write('**Part Number:**', temp_df['part_number'].values[0])
            st.write('**Listing URL:**', temp_df['product_url'].values[0])
            st.write('**Manual URL:**', temp_df['product_manual_url'].values[0])
            st.session_state.product = product
            filter = {'product_name': {'$eq': st.session_state.product}}
        else:
            st.write("Please select a product to ask about.")
    q = st.text_input('Ask a question about Garmin wearables:')
    if q:
        if 'vs' in st.session_state:
            vector_store = insert_or_fetch_embeddings(index_name)
            # Add a loading bar or something here
            if 'product' not in st.session_state:
                st.write("You must select a product from the lefthand side!")
            else:
                answer = ask_and_get_answer(vector_store, q,
                                            filter_args=filter)
            st.text_area("LLM Answer:", value=answer, height=200)

            st.divider()

            if 'history' not in st.session_state:
                st.session_state.history = ''
            value = f'Q: {q} \nA: {answer}'
            st.session_state.history = f'{value} \n{"-" * 100} \n {st.session_state.history}'
            h = st.session_state.history
            st.text_area(label='Chat History', value=h,
                         key='history', height=400)


def register_user():
    "First time? Register below:"
    try:
        if authenticator.register_user('New user', preauthorization=True):
            st.success('User registered successfully')
            update_yaml()
    except Exception as e:
        st.error(e)


def login():
    st.image('sifter_support_shared/images/Sifter.png')
    "Returning visitors can log in with their username and password:"
    name, authentication_status, username = authenticator.login('Login', 'main')
    if st.session_state['authentication_status']:
        authenticator.logout('Logout', 'sidebar')
        st.write(f'Welcome *{st.session_state["name"]}*')
        load_headers()
        select_and_ask()
        try:
            if authenticator.reset_password(st.session_state["username"],
                                            'Reset password', 'sidebar'):
                st.success("Password modified successfully")
        except Exception as e:
            st.error(e)
    elif st.session_state['authentication_status'] is False:
        register_user()
        st.error('Username/password is incorrect')
    elif st.session_state['authentication_status'] is None:
        register_user()
        st.warning("Please enter your username/password")


if __name__ == "__main__":
    login()
    # load_headers()
    # select_and_ask()
