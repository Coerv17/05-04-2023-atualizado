import pandas as pd
import tkinter as tk
import cx_Oracle
from tkinter import messagebox

# Conectar ao banco de dados Oracle
con = cx_Oracle.connect('COMAL/COMAL@SRVORACLE/WINT')
cursor = con.cursor()

# Definir função para diminuir o estoque
def diminuir_estoque():
    # Obter o ID do produto e a quantidade a ser removida a partir das caixas de entrada
    produto_id = float(produto_id_entry.get())
    quantidade = float(quantidade_entry.get())

    cursor.execute('SELECT DTVALIDADE, QTBLOQUEADA, QTRESERV FROM PCVALIDADE WHERE CODPROD = :1 AND QTBLOQUEADA > 0 ORDER BY DTVALIDADE ASC', [produto_id])
    dados = cursor.fetchall()

    if not dados:
        messagebox.showerror('ERROR',"Estoque do produto {:.0f} indisponível.".format(produto_id))
        return

    estoque_total = sum(float(d[1]) for d in dados)

    if estoque_total < quantidade:
        messagebox.showinfo("Quantidade solicitada excede o estoque disponível.")
        return

    estoque_restante = quantidade

    for data, qt_bloqueada, qt_reserv in dados:
        if estoque_restante <= 0:
            break

        qt_bloqueada = float(qt_bloqueada)
        qt_reserv = float(qt_reserv)

        if qt_bloqueada == 0:
            continue

        qt_a_ser_desbloqueada = min(qt_bloqueada, estoque_restante)

        nova_quantidade_bloqueada = qt_bloqueada - qt_a_ser_desbloqueada
        nova_quantidade_reservada = qt_reserv + qt_a_ser_desbloqueada

        cursor.execute('UPDATE PCVALIDADE SET QTBLOQUEADA = :1, QTRESERV =  :2 WHERE CODPROD = :3 AND DTVALIDADE = :4', [nova_quantidade_bloqueada, nova_quantidade_reservada, produto_id, data])
        con.commit()

        estoque_restante -= qt_a_ser_desbloqueada

    if estoque_restante > 0:
        messagebox.showinfo('Aviso', "Estoque do produto {:.0f} atualizado, mas ainda restam {:.2f} unidades a serem removidas.".format(produto_id, estoque_restante))
    else:
        messagebox.showinfo('Sucesso', "Estoque do produto {:.0f} atualizado.".format(produto_id))

    root.destroy()

# Criação da janela principal
root = tk.Tk()
root.title("Diminuir estoque")

# Criação de caixas de entrada para o ID do produto e quantidade a ser removida
produto_id_label = tk.Label(root, text="ID do produto:")
produto_id_label.pack()
produto_id_entry = tk.Entry(root)
produto_id_entry.pack()

quantidade_label = tk.Label(root, text="Quantidade a ser removida:")
quantidade_label.pack()
quantidade_entry = tk.Entry(root)
quantidade_entry.pack()

# Criação do botão para diminuir o estoque
diminuir_estoque_button = tk.Button(root, text="Diminuir estoque", command=diminuir_estoque)
diminuir_estoque_button.pack()

# Executar o loop principal do tkinter

root.mainloop()



