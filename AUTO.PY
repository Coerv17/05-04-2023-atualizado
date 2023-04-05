import pandas as pd
import cx_Oracle
import os
import numpy as np

# Conectar ao banco de dados Oracle
con = cx_Oracle.connect('COMAL/COMAL@SRVORACLE/WINT')
cursor = con.cursor()

# Define o caminho do arquivo
caminho_arquivo = 'C:/Users/administrador/Desktop/hoje/tela/TESTE.csv'

if os.path.exists(caminho_arquivo):
    print('Caminho do arquivo:', caminho_arquivo)
    df = pd.read_csv(caminho_arquivo, dtype={'CODPROD': int, 'QUANTIDADE': int})
else:
    print('Arquivo não encontrado')


# Diminuir o estoque para cada produto no arquivo CSV
for index, row in df.iterrows():
    if 'CODPROD' not in row or 'QUANTIDADE' not in row:
        print("Column not found in row: ", row)
        continue
    
    produto_id = int(row['CODPROD'])   
    quantidade = int(row['QUANTIDADE'])


    cursor.execute('SELECT DTVALIDADE, QT FROM PCVALIDADE WHERE CODPROD = :1 AND QT > 0 ORDER BY DTVALIDADE ASC', [produto_id])
    dados = cursor.fetchall()
    if not dados:
        print("Estoque do produto {} indisponível.".format(produto_id))
        continue
    estoque_total = sum(float(d[1]) for d in dados)

    # Verifique se a quantidade solicitada pode ser removida do estoque
    if estoque_total < quantidade:
        print("Quantidade solicitada excede o estoque disponível para o produto {}.".format(produto_id))
        nova_quantidade = 0
    else:
        estoque_restante = quantidade
        for data, qt in dados:
            if estoque_restante <= 0:
                break
            qt = float(qt)
            if qt >= estoque_restante:
                nova_quantidade = qt - estoque_restante
                estoque_restante = 0
            else:
                nova_quantidade = 0
                estoque_restante -= qt
            if qt > 0:
                qt_reservado = min(qt, quantidade)
                cursor.execute('UPDATE PCVALIDADE SET QT = :1, QTRESERV = QTRESERV + :2 WHERE CODPROD = :3 AND DTVALIDADE = :4', [nova_quantidade, qt_reservado, produto_id, data])
                con.commit()

    print("Estoque do produto {} atualizado.".format(produto_id))

# Fechar conexão com o banco de dados
cursor.close()
con.close()
