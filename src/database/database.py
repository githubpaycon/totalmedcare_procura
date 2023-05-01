from funcsforspo_l.fpython.functions_for_py import *
from funcsforspo_l.fselenium.functions_selenium import *
from funcsforspo_l.fsqlite.sqlite_functions import *
from funcsforspo_l.fpysimplegui.functions_for_sg import *
import pandas as pd

# GLOBAL
DATABASE_PATH = arquivo_com_caminho_absoluto('bin', 'database.db')
RESULTADO = cria_dir_no_dir_de_trabalho_atual('Resultados')
# GLOBAL

# BACKUP
def faz_backup_do_banco_de_dados():
    json_config = read_json(arquivo_com_caminho_absoluto('bin', 'config.json'))

    # cria os dirs
    cria_dir_no_dir_de_trabalho_atual(arquivo_com_caminho_absoluto('bin', 'backup'))
    
    path_database_copy = arquivo_com_caminho_absoluto(['bin', 'backup'], f'database_{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}.db')
    shutil.copy2(DATABASE_PATH, path_database_copy)
    return path_database_copy
# BACKUP


# EXPORT
def exportar_database():
    cur, con =  connect_db(DATABASE_PATH)
    arquivos = pd.read_sql('SELECT * FROM arquivos', con)
    arquivos_com_ocr = pd.read_sql('SELECT * FROM arquivos_com_ocr', con)
    # TRATAMENTOS
    arquivos_com_ocr['data_adicao'] = arquivos_com_ocr['data_adicao'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S.%f'))
    
    arquivos_com_ocr.rename(columns={'caminho_arquivo': 'Caminho do Arquivo'}, inplace=True)
    arquivos_com_ocr.rename(columns={'nome_do_arquivo': 'Nome do Arquivo'}, inplace=True)
    arquivos_com_ocr.rename(columns={'ocr': 'OCR do Arquivo'}, inplace=True)
    arquivos_com_ocr.rename(columns={'data_adicao': 'Data de Envio no Database'}, inplace=True)


    arquivos.rename(columns={'caminho_arquivo': 'Caminho do Arquivo'}, inplace=True)
    arquivos.rename(columns={'nome_do_arquivo': 'Nome do Arquivo'}, inplace=True)
    # TRATAMENTOS
    
    try:
        with pd.ExcelWriter(os.path.join(RESULTADO, 'DATABASE.xlsx')) as writer:
            arquivos_com_ocr.to_excel(writer, sheet_name="Arquivos Com OCR", index=False)
            arquivos.to_excel(writer, sheet_name="PDFs Recuperados da Máquina", index=False)
    except PermissionError:
        sleep(10)
        try:
            with pd.ExcelWriter(os.path.join(RESULTADO, 'DATABASE.xlsx')) as writer:
                arquivos_com_ocr.to_excel(writer, sheet_name="Arquivos Com OCR", index=False)
                arquivos.to_excel(writer, sheet_name="PDFs Recuperados da Máquina", index=False)
        except PermissionError:
            faz_log('O Arquivo está aberto, não foi possível exportar...')
    except OSError:
        popup_erro('Sem espaço em disco para fazer o arquivo...', 'Sem espaço...')
        pass
# EXPORT

# DELETE
def delete(table):
    # Apaga todos os dados da tabela enviada
    cur, con =  connect_db(DATABASE_PATH)
    query = f'DELETE FROM {table};'
    cur.execute(query)
    con.commit()
# DELETE

# SELECT
def select(table:str, col: str='*', data_from_line: bool=False):
    cur, con =  connect_db(DATABASE_PATH)
    cur.execute(f'SELECT {col} FROM {table}')
    faz_log(f'SELECT {col} FROM {table}', 'i*')
    data = []
    if data_from_line:
        for line in cur.fetchall():
            for i in line:
                data.append(i)
        return tuple(data)
    else:
        for line in cur.fetchall():
            data.append(line)
        return tuple(data)
# SELECT

