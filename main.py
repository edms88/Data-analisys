import streamlit as st
import pandas as pd
from io import StringIO
import pygwalker as pyg
import os
from pygwalker.api.streamlit import StreamlitRenderer
from pathlib import Path

#path & settings
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()





st.set_page_config(
    page_title='Data Analsys',
    layout='wide'   
)

st.title('Projeto de analise de dados')

st.write("""Este projeto tem como objetivo fornecer
         uma análise rápida aos usuários, utilizando
         três bibliotecas em Python que facilitam
         a leitura de dados e a extração de insights valiosos.
         """)


col1, col2,col3 = st.columns(3)

with col1:
    st.subheader('PygWalker')
    st.write()

### Body Functional ### 



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
    
    return df


@st.cache_resource
def get_pyg_renderer(df: pd.DataFrame) -> "StreamlitRenderer":
    
    return StreamlitRenderer(df, spec_io_mode="rw")

# Carregamento de arquivos
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

            # Obter o renderizador do PyGWalker com cache
            renderer = get_pyg_renderer(df)
            
            # Exibir a visualização interativa com PyGWalker
            renderer.explorer()

        except Exception as e:
            st.error(f"Erro ao processar o arquivo {uploaded_file.name}: {e}")


