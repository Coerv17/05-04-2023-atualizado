from tkinter import *
import random
from tkinter import Tk, StringVar, ttk
from PIL import Image, ImageTk
from tkcalendar import Calendar, DateEntry
from datetime import date
from datetime import datetime
import sqlite3
from tkinter import messagebox
from tkinter import filedialog
import cx_Oracle
# from tela import img
conn = cx_Oracle.connect('COMAL/COMAL@SRVORACLE/WINT')


# from view import atualizar_formu
################# cores ###############
co0 = "#f0f3f5"  # Preta
co1 = "#feffff"  # branca
co2 = "#4fa882"  # verde
co3 = "#38576b"  # valor
co4 = "#403d3d"   # letra
co5 = "#e06636"   # - profit
co6 = "#038cfc"   # azul
co7 = "#ef5350"   # vermelha
co8 = "#263238"   # + verde
co9 = "#e9edf5"   # sky blue

################# janela ###############

janela = Tk()
janela.title('')
janela.geometry('1170x600')
# janela.geometry('1170x410')
janela.iconbitmap("logo.ico")
janela.configure(background=co9)
janela.resizable(False,False)
style = ttk.Style(janela)
style.theme_use("clam")

################# FRAMES ###############

frame_cima = Frame(janela, width=1043, height=100, bg=co1, relief="flat")
frame_cima.grid(row=0, column=0)


frame_Meio = Frame(janela, width=1043, height=400, bg=co1, pady=20, relief="flat")
frame_Meio.grid(row=1, column=0, padx=1, pady=0, sticky=NSEW)


frame_Baixo = Frame(janela, width=1043, height=7000, bg=co1, relief="flat")
frame_Baixo.grid(row=4, column=0, padx=5, pady=0,sticky=NSEW)

################# CRIANDO FUNCOES ###############
global tree 
global imagem, imagem_sting, l_imagem, pyimage1
###############
def inserir_form():
    DTREGISTRO = e_registro.get_date()
    NUMBONUS = e_bonus.get()
    DTENTRADA = e_entrada.get_date()
    NUMNOTAENT = e_num.get()
    NUMLOTE = e_lote.get()
    CODPROD = e_cod.get()
    FABRICANTE = e_fabricante.get()
    DTFABRICACAO = e_dtfabi.get_date()
    DTVALIDADE = e_dtvali.get_date()
    QT = e_qt.get()
    lista_inserir = [NUMNOTAENT, NUMBONUS, DTENTRADA, DTREGISTRO, NUMLOTE, CODPROD, FABRICANTE, DTFABRICACAO, DTVALIDADE, QT]
    for i in lista_inserir:
        if i == '':
            messagebox.showerror('Erro', 'Preencha todos os campos')
            return

    dtRegistro_str = datetime.strftime(DTREGISTRO, '%d/%m/%Y')
    dtEntrada_str = datetime.strftime(DTENTRADA, '%d/%m/%Y')
    dtFabricacao_str = datetime.strftime(DTFABRICACAO, '%d/%m/%Y')
    dtValidade_str = datetime.strftime(DTVALIDADE, '%d/%m/%Y')
    novo_id = gerar_id()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO PCVALIDADE (ID, DTREGISTRO, NUMBONUS, DTENTRADA, NUMNOTAENT, NUMLOTE, CODPROD, FABRICANTE, DTFABRICACAO, DTVALIDADE, QT, QTBLOQUEADA) 
                      VALUES (:1, TO_DATE(:2, 'DD/MM/YYYY'), :3, TO_DATE(:4, 'DD/MM/YYYY'), :5, :6, :7, :8, TO_DATE(:9, 'DD/MM/YYYY'), TO_DATE(:10, 'DD/MM/YYYY'), :11, :11)''',
                   (novo_id, dtRegistro_str, NUMBONUS, dtEntrada_str, NUMNOTAENT, NUMLOTE, CODPROD, FABRICANTE, dtFabricacao_str, dtValidade_str, QT))

    conn.commit()
    cursor.close()
    messagebox.showinfo('Sucesso', 'Dados inseridos com sucesso!')
    mostar()
    
    #############################           DELETAR DADOS APÓS INSERIR                #############################  
    e_registro.delete(0, 'end')
    e_bonus.delete(0, 'end')
    e_entrada.delete(0, 'end')
    e_num.delete(0, 'end')
    e_lote.delete(0, 'end')
    e_cod.delete(0, 'end')
    e_fabricante.delete(0, 'end')
    e_dtfabi.delete(0, 'end')
    e_dtvali.delete(0, 'end')
    e_qt.delete(0, 'end')

def gerar_id():
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(ID) FROM PCVALIDADE")
    ultimo_id = cursor.fetchone()[0]
    if ultimo_id is None:
        novo_id = 1
    else:
        novo_id = ultimo_id + 1
    return novo_id


                

def atualizar_formu():
    try:
        treev_dados = tree.focus()
        treev_dic = tree.item(treev_dados)
        trev_lista = treev_dic['values']

        # valor = trev_lista[1]

        e_registro.delete(0,'end')
        e_bonus.delete(0,'end')
        e_entrada.delete(0,'end')
        e_num.delete(0,'end')
        e_lote.delete(0,'end')
        e_cod.delete(0,'end')
        e_fabricante.delete(0,'end')
        e_dtfabi.delete(0,'end')
        e_dtvali.delete(0,'end')
        e_qt.delete(0,'end')

        e_registro.insert(0,trev_lista[0]) 
        e_bonus.insert(0,trev_lista[1])
        e_entrada.insert(0,trev_lista[2])
        e_num.insert(0,trev_lista[3])
        e_lote.insert(0,trev_lista[4])
        e_cod.insert(0,trev_lista[5])
        e_fabricante.insert(0,trev_lista[6])
        e_dtfabi.insert(0,trev_lista[7])
        e_dtvali.insert(0,trev_lista[8])
        e_qt.insert(0,trev_lista[9])
        ID = int(trev_lista[10])
        
        


        def update():
            
            DTREGISTRO = e_registro.get_date()
            NUMBONUS = e_bonus.get()
            DTENTRADA = e_entrada.get_date()
            NUMNOTAENT = e_num.get()
            NUMLOTE = e_lote.get()
            CODPROD = e_cod.get()
            FABRICANTE = e_fabricante.get()
            DTFABRICACAO = e_dtfabi.get_date()
            DTVALIDADE = e_dtvali.get_date()
            QT = e_qt.get()
            # novo_id = gerar_id()
            lista_atualizar = [DTREGISTRO,NUMBONUS,DTENTRADA,NUMNOTAENT,NUMLOTE,CODPROD,FABRICANTE,DTFABRICACAO,DTVALIDADE,QT,str(ID)]

            for i in lista_atualizar:
                if i=='':
                    messagebox.showerror('Erro','Preencha todos os campos')
                    return
            conn = cx_Oracle.connect('COMAL/COMAL@SRVORACLE/WINT')
            cursor = conn.cursor()
            cursor.execute('''UPDATE PCVALIDADE SET DTREGISTRO=:1, NUMBONUS=:2, DTENTRADA=:3, NUMNOTAENT=:4, NUMLOTE=:5, CODPROD=:6, FABRICANTE=:7, DTFABRICACAO=:8, DTVALIDADE=:9, QT=:10 WHERE ID=:11''',
                            (DTREGISTRO, NUMBONUS, DTENTRADA, NUMNOTAENT, NUMLOTE, CODPROD, FABRICANTE, DTFABRICACAO, DTVALIDADE, QT,ID))


            conn.commit()
            cursor.close()


            # Clear the entry fields and show success message
            e_registro.delete(0,'end')
            e_bonus.delete(0,'end')
            e_entrada.delete(0,'end')
            e_num.delete(0,'end')
            e_lote.delete(0,'end')
            e_cod.delete(0,'end')
            e_fabricante.delete(0,'end')
            e_dtfabi.delete(0,'end')
            e_dtvali.delete(0,'end')
            e_qt.delete(0,'end')

            messagebox.showinfo('Sucesso','Os dados foram atualizados com sucesso')


            b_confirmar.destroy()
            mostar()
          
        b_confirmar = Button(frame_Meio,command=update, text='confirmar'.upper(), overrelief=RIDGE,font=('Ivy 10 bold'),bg=co1, fg=co4) 
        b_confirmar.grid(row=4, column=3, padx=0, pady=0)       

    except IndexError:
        messagebox.showerror('Erro','Seleciona um dados da tabela')


  # Definindo a função a ser chamada no double click




################# IMAGEM ###############
# app_img = Image.open('inv.png')
# app_img = app_img.resize((45,45))
# app_img = ImageTk.PhotoImage(app_img)

app_logo = Label(frame_cima, text="CONTROLE DE VALIDADE", width=1240, compound=LEFT,relief=RAISED, anchor=NW,font=('Verdana 20 bold'),bg=co1,fg=co4)
app_logo.grid(row=1, column=1, padx=1, pady=0)
# ta dando erro

################# ENTRADAS DE DADOS  ###############

l_registro = Label(frame_Meio,text='DTREGISTRO * ', height=1, anchor=NW,font=('Ivy 10 bold'), bg=co1, fg=co4)
l_registro.grid(row=1, column=1, padx=1, pady=0)
e_registro= DateEntry(frame_Meio, width=12, background='darkblue',bordewidth=2, year=2023)
e_registro.grid(row=2, column=1, padx=1, pady=0)


l_bonus = Label(frame_Meio,text='NUMBONUS *', height=1, anchor=NW,font=('Ivy 10 bold'), bg=co1, fg=co4)
l_bonus.grid(row=1, column=2, padx=2, pady=0)
e_bonus= Entry(frame_Meio, width=16, justify='left', relief=SOLID)
e_bonus.grid(row=2, column=2, padx=2, pady=0)



l_entrada = Label(frame_Meio,text='DTENTRADA *', height=1, anchor=NW,font=('Ivy 10 bold'), bg=co1, fg=co4)
l_entrada.grid(row=1, column=3, padx=3, pady=0)
e_entrada= DateEntry(frame_Meio, width=12, background='darkblue',bordewidth=2, year=2023)
e_entrada.grid(row=2, column=3, padx=3, pady=0)


l_num = Label(frame_Meio,text='NUMNOTAENT*', height=1, anchor=NW,font=('Ivy 10 bold'), bg=co1, fg=co4)
l_num.grid(row=1, column=4, padx=4, pady=0)
e_num= Entry(frame_Meio, width=16, justify='left', relief=SOLID)
e_num.grid(row=2, column=4, padx=4, pady=0)


l_lote = Label(frame_Meio,text='NUMLOTE*', height=1, anchor=NW,font=('Ivy 10 bold'), bg=co1, fg=co4)
l_lote.grid(row=1, column=5, padx=5, pady=0)
e_lote= Entry(frame_Meio, width=16, justify='left', relief=SOLID)
e_lote.grid(row=2, column=5, padx=5, pady=0)

l_cod = Label(frame_Meio,text='CODPROD *', height=1, anchor=NW,font=('Ivy 10 bold'), bg=co1, fg=co4)
l_cod.grid(row=1, column=6, padx=6, pady=0)
e_cod= Entry(frame_Meio, width=16, justify='left', relief=SOLID)
e_cod.grid(row=2, column=6, padx=6, pady=0)

l_fabricante = Label(frame_Meio,text='FABRICANTE *', height=1, anchor=NW,font=('Ivy 10 bold'), bg=co1, fg=co4)
l_fabricante.grid(row=1, column=7, padx=7, pady=0)
e_fabricante= Entry(frame_Meio, width=16, justify='left', relief=SOLID)
e_fabricante.grid(row=2, column=7, padx=7, pady=0)

l_dtfabri = Label(frame_Meio,text='DTFABRICACAO *', height=1, anchor=NW,font=('Ivy 10 bold'), bg=co1, fg=co4)
l_dtfabri.grid(row=1, column=8, padx=8, pady=0)
e_dtfabi= DateEntry(frame_Meio, width=12, background='darkblue',bordewidth=2, year=2023)
e_dtfabi.grid(row=2, column=8, padx=7, pady=0)

l_dtvali = Label(frame_Meio,text='DTVALIDADE *', height=1, anchor=NW,font=('Ivy 10 bold'), bg=co1, fg=co4)
l_dtvali.grid(row=1, column=9, padx=9, pady=0)
e_dtvali= DateEntry(frame_Meio, width=12, background='darkblue',bordewidth=2, year=2023)
e_dtvali.grid(row=2, column=9, padx=9, pady=1)

l_qt = Label(frame_Meio,text='QT *', height=1, anchor=NW,font=('Ivy 10 bold'), bg=co1, fg=co4)
l_qt.grid(row=1, column=10, padx=10, pady=0)
e_qt= Entry(frame_Meio, width=16, justify='left', relief=SOLID)
e_qt.grid(row=2, column=10, padx=10, pady=0)


################# BOTOES  ###############
entrada_pesquisa = Entry(janela)
entrada_pesquisa.grid(row=4, column=4, padx=0, pady=0)
botao_pesquisa = Button(janela, text="Pesquisar")
botao_pesquisa.grid(row=4, column=3, padx=0, pady=0)
# img_add = Image.open('adicionar.png')
# img_add = img_add.resize((20,20))
# img_add = ImageTk.PhotoImage(img_add)
img = PhotoImage(file="verde.png")

# configurar o botão com a imagem
btn = Button(frame_Meio, image=img)
adicinocar = Button(frame_Meio,image=img, command=inserir_form, text='Adicionar'.upper(), compound=LEFT, anchor=NW, overrelief=RIDGE,font=('Ivy 10 bold'),bg=co1, fg=co4) 
adicinocar.grid(row=4, column=1, padx=0, pady=0)

# img_delete = Image.open('botao-atualizar.png')
# img_delete = img_delete.resize((20,20))
# img_delete = ImageTk.PhotoImage(img_delete)
deletar = Button(frame_Meio, command=atualizar_formu, text='Atualizar'.upper(), compound=LEFT, anchor=NW, overrelief=RIDGE,font=('Ivy 10 bold'),bg=co1, fg=co4) 
deletar.grid(row=4, column=2, padx=0, pady=0)
# img_delete2 = Image.open('update.png')
# img_delete2 = img_delete2.resize((20,20))
# img_delete2 = ImageTk.PhotoImage(img_delete2)
# att = Button(frame_Meio,command=att.attDiminuir,text='chamar outra fun'.upper(), compound=LEFT, anchor=NW, overrelief=RIDGE,font=('Ivy 10 bold'),bg=co1, fg=co4) 
# att.grid(row=4, column=6, padx=0, pady=0)



#######################################################################################################################################
#######################################################################################################################################
#######################################################################################################################################
#######################################################################################################################################
#########################################################E##############################################################################




import tkinter.messagebox as messagebox

def pesquisar2():
    # Conectando ao banco de dados Oracle
    connection = cx_Oracle.connect('COMAL/COMAL@SRVORACLE/WINT')
    cursor = connection.cursor()
    # Limpar a treeview antes de adicionar os resultados

    codigo = deletar2.get()
    # Verificar se o código de produto foi informado antes de executar a consulta
    if codigo:
        cursor.execute("SELECT DTREGISTRO, NUMBONUS, DTENTRADA, NUMNOTAENT, NUMLOTE, CODPROD, FABRICANTE, DTFABRICACAO, DTVALIDADE, QT,ID FROM PCVALIDADE WHERE CODPROD = :1", (codigo,))
        resultados = cursor.fetchall()

        if resultados:
            tree.delete(*tree.get_children())
            # atualizar a treeview com os resultados
            for resultado in resultados:
                tree.insert("", "end", values=resultado)
        else:
            # mostrar uma mensagem de erro se não houver resultados
            messagebox.showerror("Erro", "Nenhum resultado encontrado.")
    else:
        # mostrar uma mensagem de erro se o campo estiver em branco
        messagebox.showerror("Erro", "Por favor, informe o código do produto.") 

def mostrar_todos():
    # Conectando ao banco de dados Oracle
    connection = cx_Oracle.connect('COMAL/COMAL@SRVORACLE/WINT')
    cursor = connection.cursor()
    # Limpar a treeview antes de adicionar os resultados
    tree.delete(*tree.get_children())
    cursor.execute("SELECT DTREGISTRO, NUMBONUS, DTENTRADA, NUMNOTAENT, NUMLOTE, CODPROD, FABRICANTE, DTFABRICACAO, DTVALIDADE, QT FROM PCVALIDADE")
    resultados = cursor.fetchall()

    if resultados:
        # atualizar a treeview com os resultados
        for resultado in resultados:
            tree.insert("", "end", values=resultado)
    else:
        # mostrar uma mensagem de erro se não houver resultados
        messagebox.showerror("Erro", "Nenhum resultado encontrado.")





deletar2 = Entry(frame_Meio, text='QT 999*', font=('Ivy 10 bold'), bg=co1, fg=co4, highlightthickness=2, highlightbackground='black')
deletar2.grid(row=4, column=7, padx=0, pady=0)
deletar = Button(frame_Meio, command=pesquisar2, text='Buscar'.upper(), compound=LEFT, anchor=NW, overrelief=RIDGE,font=('Ivy 10 bold'),bg=co1, fg=co4) 
deletar.grid(row=4, column=6, padx=0, pady=0)

deletar6 = Button(frame_Meio, command=mostrar_todos, text='MOSTRAR TODOS'.upper(), compound=LEFT, anchor=NW, overrelief=RIDGE,font=('Ivy 10 bold'),bg=co1, fg=co4) 
deletar6.grid(row=4, column=8, padx=0, pady=0)

# img_deletar = Image.open('bloquear.png')
# img_deletar = img_deletar.resize((20,20))
# img_deletar = ImageTk.PhotoImage(img_deletar)

# deletar = Button(frame_Meio, image=img_deletar, command=deletar3,width=95, text='Deletar'.upper(), compound=LEFT, anchor=NW, overrelief=RIDGE,font=('Ivy 10 bold'),bg=co1, fg=co4) 
# deletar.grid(row=4, column=3, padx=0, pady=0)


def ver_formu():
    con = cx_Oracle.connect('COMAL/COMAL@SRVORACLE/WINT')
    ver_dados = []
    with con:
        cur = con.cursor()
        query = 'SELECT DTREGISTRO, NUMBONUS, DTENTRADA, NUMNOTAENT, NUMLOTE, CODPROD, FABRICANTE, DTFABRICACAO, DTVALIDADE, QT , ID FROM PCVALIDADE ORDER BY CODPROD'
        cur.execute(query)
        rows = cur.fetchall()
        for row in rows:
            ver_dados.append(row)
    return ver_dados

    
################################################
def mostar():
    global tree
    tabela_head = ['IDTREGISTRO'.upper(),'NUMBONUS'.upper(),  'DTENTRADA'.upper(),'NUMNOTAENT'.upper(), 'NUMLOTE'.upper(), 'CODPROD'.upper(),'FABRICANTE'.upper(), 'DTFABRICACAO'.upper(),'DTVALIDADE'.upper(),'QT'.upper()]
    
    lista_itens = ver_formu()



    tree = ttk.Treeview(frame_Baixo, selectmode="extended",columns=tabela_head, show="headings")

    # vertical scrollbar
    vsb = ttk.Scrollbar(frame_Baixo, orient="vertical", command=tree.yview)

    # horizontal scrollbar
    hsb = ttk.Scrollbar(frame_Baixo, orient="horizontal", command=tree.xview)
    

    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    tree.grid(column=0, row=0, sticky='nsew')
    vsb.grid(column=1, row=0, sticky='ns')
    hsb.grid(column=0, row=1, sticky='ew')
    frame_Baixo.grid_rowconfigure(0, weight=120)

    hd=["center","center","center","center","center","center","center", 'center','center','center']
    h=[100,150,100,160,130,100,100, 100,100,100]
    n=0
    

    for col in tabela_head:
        tree.heading(col, text=col.upper(), anchor=CENTER)
        # adjust the column's width to the header string
        tree.column(col, width=h[n],anchor=hd[n])
        n+=1

    
    # inserindo os itens dentro da tabela
    for item in lista_itens:
        tree.insert('', 'end', values=item)
    

        


mostar() 


# Define a flag para verificar se a função on_double_click() está em execução
is_double_click_running = False

def on_double_click(event):
    # Declarar a variável como global antes de usá-la
    global is_double_click_running
    
    # Verifica se a função já está em execução
    if is_double_click_running:
        return
    
    # Define a flag como True para indicar que a função está em execução
    is_double_click_running = True
    
    # Executa a função atualizar_formu()
    atualizar_formu()
    
    # Define a flag como False para indicar que a função terminou de executar
    is_double_click_running = False

# Declara a variável globalmente fora da função
is_double_click_running = False

# Associa a função ao evento de double click da TreeList
tree.bind('<Double-1>', on_double_click)


janela.mainloop()


