import streamlit as st
import pandas as pd
from io import StringIO
import pygwalker as pyg
import os
from pygwalker.api.streamlit import StreamlitRenderer
from pathlib import Path

#path & settings
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
bio_pyg = current_dir / "Text" / "pyg.txt"



st.set_page_config(
    page_title='Data Analsys',
    layout='wide'   
)

st.title('**Projeto de analise de dados**')

st.markdown("""
        Este projeto tem como objetivo fornecer
        uma análise rápida aos usuários, utilizando
        três bibliotecas em Python que facilitam
        a leitura de dados e a extração de insights valiosos.
         """)


col1, col2 = st.columns(2)

with col1:
    st.subheader('PygWalker')
    with open(bio_pyg,'r', encoding='utf-8') as bio_label_pyg:
        bio_label = bio_label_pyg.read()
        
    st.write(bio_label)

### Body Functional ### 



def read_file(uploaded_file):
    file_extension = os.path.splitext(uploaded_file.name)[1].lower()

    if file_extension == '.csv':
        df = pd.read_csv(StringIO(uploaded_file.getvalue().decode('utf-8')))
        st.write(f'Leitura do arquivo CSV: {uploaded_file.name}')
    elif file_extension in ['.xls', '.xlsx']:
        # Lê o arquivo Excel com openpyxl
        excel_file = pd.ExcelFile(uploaded_file, engine='openpyxl')

        # Verifica se há tabelas nomeadas no arquivo
        table_names = [name for name in excel_file.sheet_names]
        
        if table_names:
            st.write(f"Planilhas encontradas: {', '.join(table_names)}")
            # Você pode adicionar um seletor para o usuário escolher uma tabela, mas aqui vamos pegar a primeira
            df = pd.read_excel(uploaded_file, sheet_name=table_names[0])
            st.write(f'Leitura da planilha: {table_names[0]}')
        else:
            # Caso não haja tabelas nomeadas, lê a primeira planilha normalmente
            df = pd.read_excel(uploaded_file)
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
        st.write(f'Nome do arquivo: {uploaded_file.name}',type=['csv', 'xls', 'xlsx'])
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