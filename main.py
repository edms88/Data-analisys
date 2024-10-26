import streamlit as st
import pandas as pd
from io import StringIO
import pygwalker as pyg
import os
import webbrowser
from pathlib import Path
import openpyxl

# Path & settings
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
bio_pyg = current_dir / "Text" / "pyg.txt"

st.set_page_config(
    page_title='Data Analysis',
    layout='wide'
)

st.title('**Projeto de análise de dados**')

st.markdown("""
        Este projeto tem como objetivo fornecer
        uma análise rápida aos usuários, utilizando
        três bibliotecas em Python que facilitam
        a leitura de dados e a extração de insights valiosos.
""")

col1, col2 = st.columns(2)

with col1:
    st.subheader('PygWalker')
    with open(bio_pyg, 'r', encoding='utf-8') as bio_label_pyg:
        bio_label = bio_label_pyg.read()
        
    st.write(bio_label)


def read_file(uploaded_file):
    file_extension = os.path.splitext(uploaded_file.name)[1].lower()

    if file_extension == '.csv':
        df = pd.read_csv(StringIO(uploaded_file.getvalue().decode('utf-8')))
        st.write(f'Leitura do arquivo CSV: {uploaded_file.name}')
    elif file_extension in ['.xls', '.xlsx']:
        df = pd.read_excel(uploaded_file)
        st.write(f'Leitura do arquivo Excel: {uploaded_file.name}')
    else:
        raise ValueError(f'Formato não reconhecido: {file_extension}')
    return df.head(10)


def open_pyg_in_browser(df: pd.DataFrame):
    # Cria a visualização do PyGWalker e salva como HTML
    output_path = current_dir / "pygwalker_output.html"
    pyg.walk(df, out_path=output_path)

    # Abre o arquivo HTML no navegador padrão do sistema
    webbrowser.get().open_new_tab(f"file://{output_path}")

# Carregamento de arquivos
with col2:
    uploaded_files = st.file_uploader('File Upload', accept_multiple_files=True)

# Processar os arquivos enviados
if uploaded_files:
    for uploaded_file in uploaded_files:
        st.write(f'Nome do arquivo: {uploaded_file.name}')
        st.write('Upload bem-sucedido!')

        try:
            # Ler o arquivo usando a função read_file
            df = read_file(uploaded_file)
            st.write(df.head())  # Verifique os dados do DataFrame

            # Abre a visualização do PyGWalker em uma nova aba
            open_pyg_in_browser(df)

        except Exception as e:
            st.error(f"Erro ao processar o arquivo {uploaded_file.name}: {e}")
