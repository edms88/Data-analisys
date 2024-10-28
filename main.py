import streamlit as st
import pandas as pd
import os
from pygwalker.api.streamlit import StreamlitRenderer
from pathlib import Path
import chardet

# Path & settings
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
bio_pyg = current_dir / "Text" / "pyg.txt"

st.set_page_config(
    page_title='Data Analysis',
    layout='wide'
)

st.title('**Projeto de Análise de Dados**')

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

### Body Functional ###
def detecter_encodi(caminho_arquivo):
    with open(caminho_arquivo, 'rb') as f:
        resultado = chardet.detect(f.read)
    return resultado['encoding']
    
def read_file(uploaded_file):
    file_extension = os.path.splitext(uploaded_file.name)[1].lower()

    if file_extension == '.csv':
        encoding = detecter_encodi(uploaded_file)
        df = pd.read_csv(uploaded_file, encoding=encoding)
        st.write(f'Leitura do arquivo CSV: {uploaded_file.name} com o encoding {encoding}')
    elif file_extension in ['.xls', '.xlsx']:
        # Lê o arquivo Excel
        df = pd.read_excel(uploaded_file, engine='openpyxl')
        st.write(f'Leitura do arquivo Excel: {uploaded_file.name}')
    else:
        raise ValueError(f'Formato não reconhecido: {file_extension}')

    return df.head(10)

@st.cache_resource
def get_pyg_renderer(df: pd.DataFrame) -> "StreamlitRenderer":
    return StreamlitRenderer(df, spec_io_mode="rw")

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
            st.write(df)  # Exibe os dados do DataFrame

            # Obter o renderizador do PyGWalker com cache
            renderer = StreamlitRenderer(df)

            # Exibir a visualização interativa com PyGWalker
            renderer.explorer()

        except Exception as e:
            st.error(f"Erro ao processar o arquivo {uploaded_file.name}: {e}")
