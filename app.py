import re
import sqlite3
import tkinter as tk
import tkinter.ttk as tkk
from tkinter import RIGHT, messagebox
import datetime as dt
from datetime import datetime
from turtle import left, right
import databases as db
import pandas as pd
from termcolor import colored


data_criacao =  dt.datetime.now()  

# CRIA E CONECTA NO DB

class ConectarDB:
    def __init__(self):
        self.con = sqlite3.connect('dados.db')
        self.cur = self.con.cursor()
        self.criar_tabela()


    def criar_tabela(self):
        
        try:
            self.cur.execute('''CREATE TABLE IF NOT EXISTS alunos (
                aluno TEXT,
                inicio TIME,
                fim TIME,
                soma TIME,
                data TEXT,
                total TIME)''')
        except Exception as e:
            print('[x] Falha ao criar tabela: %s [x]' % e)
        else:
            print('\n[!] Tabela criada com sucesso [!]\n')


    def inserir_registro(self, aluno, inicio, fim, soma, data, total):
        try:
            self.cur.execute(
                '''INSERT INTO alunos VALUES (?, ?, ?, ?, ?, ?)''', (aluno, inicio, fim, soma, data, total))
        except Exception as e:
            print('\n[x] Falha ao inserir registro [x]\n')
            print('[x] Revertendo operação (rollback) %s [x]\n' % e)
            self.con.rollback()
        else:
            self.con.commit()
            print('\n[!] Registro inserido com sucesso [!]\n')


    def consultar_registros(self):
        return self.cur.execute('SELECT rowid, * FROM alunos').fetchall()


    def consultar_ultimo_rowid(self):
        return self.cur.execute('SELECT MAX(rowid) FROM alunos').fetchone()


    def remover_registro(self, rowid):
        try:
            self.cur.execute("DELETE FROM alunos WHERE rowid=?", (rowid,))
        except Exception as e:
            print('\n[x] Falha ao remover registro [x]\n')
            print('[x] Revertendo operação (rollback) %s [x]\n' % e)
            self.con.rollback()
        else:
            self.con.commit()
            print('\n[!] Registro removido com sucesso [!]\n')


    def total(self):
        self.cur.execute("SELECT time(sum(strftime('%s', soma) - strftime('%s', '00:00:00')), 'unixepoch') FROM alunos")  
        return (self.cur.fetchall()[0][0])        
        

#INTERFACE

class Janela(tk.Frame):
    """Janela principal"""

    def __init__(self, master=None):
        """Construtor"""
        super().__init__(master)
        # Coletando informações do monitor
        largura = round(self.winfo_screenwidth() / 1.1)
        altura = round(self.winfo_screenheight() / 2)
        tamanho = ('%sx%s' % (largura, altura))

        # Título da janela principal.
        master.title('Cadastro de Horas')

        # Tamanho da janela principal.
        master.geometry(tamanho)

        # Instanciando a conexão com o banco.
        self.banco = ConectarDB()

        # Gerenciador de layout da janela principal.
        self.pack()

        # Criando os widgets da interface.
        self.criar_widgets()


    def criar_widgets(self):
        # Containers.
        frame1 = tk.Frame(self)
        frame1.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)

        frame2 = tk.Frame(self)
        frame2.pack(fill=tk.BOTH, expand=True)

        frame3 = tk.Frame(self)
        frame3.pack(side=tk.BOTTOM, padx=10)

        # Labels.
        label_aluno = tk.Label(frame1, text='Nome do Aluno', font="ComicSans 12 bold", fg="black")
        label_aluno.grid(row=0, column=0)

        label_inicio = tk.Label(frame1, text='Início', font="ComicSans 12 bold", fg="black")
        label_inicio.grid(row=0, column=1)

        label_fim = tk.Label(frame1, text='Fim', font="ComicSans 12 bold", fg="black")
        label_fim.grid(row=0, column=2)         
        
        label_total = tk.Label(frame1, text=self.banco.total(), font="ComicSans 10")
        label_total.grid(row=1, column=5)

        label_total = tk.Label(frame1, text='Total', font="ComicSans 12 bold", fg="black")
        label_total.grid(row=0, column=5)
        
        label_data = tk.Label(frame1, text= 'Data', font="ComicSans 12 bold", fg="black")
        label_data.grid(row=0, column=3)

        data = data_criacao.strftime("%d/%m/%Y")
        label_data = tk.Label(frame1, text= data, font="ComicSans 10")
        label_data.grid(row=1, column=3)

        # Entrada de texto.
        self.entry_aluno = tk.Entry(frame1)
        self.entry_aluno.grid(row=1, column=0)

        self.entry_inicio = tk.Entry(frame1)
        self.entry_inicio.grid(row=1, column=1, padx=10)

        self.entry_fim = tk.Entry(frame1)
        self.entry_fim.grid(row=1, column=2, padx=10)            
        
        # Treeview.
        self.treeview = tkk.Treeview(frame2, columns=('Nome do Aluno', 'Início', 'Fim', 'Soma', 'Data'))
        self.treeview.heading('#0', text= "ID")
        self.treeview.heading('#1', text= f"{'Aluno': <60}")        
        self.treeview.heading('#2', text=f"{'Início': <60}")
        self.treeview.heading('#3', text=f"{'Fim': <60}")
        self.treeview.heading('#4', text=f"{'Soma': <60}")
        self.treeview.heading('#5', text=f"{'Data': <60}")

        # Inserindo os dados do banco no treeview.
        for row in self.banco.consultar_registros():
            self.treeview.insert('', 'end', text=row[0], values=(row[1], row[2], row[3], row[4], row[5]))

        self.treeview.pack(fill=tk.BOTH, expand=True)

        # Botão para adicionar um novo registro.
        button_adicionar = tk.Button(frame1, text='Adicionar', bg='blue', fg='white', font="ComicSans 12 bold")
        # Método que é chamado quando o botão é clicado.
        button_adicionar['command'] = self.adicionar_registro
        button_adicionar.grid(row=0, column=6, rowspan=4, ipadx=10, padx=50)

        # Botão para remover um item.
        button_excluir = tk.Button(frame3, text='Excluir', bg='red', fg='white', font="ComicSans 12 bold")
        # Método que é chamado quando o botão é clicado.
        button_excluir['command'] = self.excluir_registro
        button_excluir.pack(pady=30)

        # Botão para exportar planilha do Excel.
        button_exportar = tk.Button(frame1, text='Exportar Tabela',  bg='black', fg='white', font="ComicSans 12 bold")
        # Método que é chamado quando o botão é clicado.
        button_exportar['command'] = self.exportar_alunos
        button_exportar.grid(row=0, column=7, rowspan=2, ipadx=1)


    def adicionar_registro(self):

        # Coletando os valores.    
        aluno = self.entry_aluno.get()
        
        while True:
            try:
                inicio =self.entry_inicio.get()
                break
            except ValueError:
                print('\n[!] Digitar no formato hh:mm [!]\n')

        while True:
            try:
                fim = self.entry_fim.get()
                break
            except ValueError:
                print('\n[!] Digitar no formato hh:mm [!]\n')

        #SOMA
        hora_entrada = inicio        
        hora_saida = fim
        entrada = datetime.strptime(hora_entrada, '%H:%M')
        saida = datetime.strptime(hora_saida, '%H:%M')        
        diff = saida - entrada        
        minutes = int(diff.total_seconds()) // 60
        soma = f'{minutes // 60:02}:{minutes % 60:02}'

        #TOTAL
        total = self.banco.total()
            
        #DATA DA CRIAÇÃO
        data = data_criacao.strftime("%d/%m/%Y %H:%M")
        self.entry_aluno.delete(0, "end")
        self.entry_inicio.delete(0, "end")
        self.entry_fim.delete(0, "end")
       
        # Validação simples (utilizar datetime deve ser melhor para validar).
        validar_data = re.search(r'(..)/(..)/(....)', data)

        # Se a data digitada passar na validação
        if validar_data:
            # Dados digitando são inseridos no banco de dados
            self.banco.inserir_registro(aluno=aluno, inicio=inicio, fim=fim, soma=soma, data=data, total=total)

            # Coletando a ultima rowid que foi inserida no banco.
            rowid = self.banco.consultar_ultimo_rowid()[0]

            # Adicionando os novos dados no treeview.
            self.treeview.insert('', 'end', text=rowid, values=(aluno, inicio, fim, soma, data))
        else:
            # Caso a data não passe na validação é exibido um alerta.
            messagebox.showerror('Erro', 'Padrão de data incorreto, utilize dd/mm/yyyy')


    def excluir_registro(self):
        # Verificando se algum item está selecionado.
        if not self.treeview.focus():
            messagebox.showerror('Erro', 'Nenhum item selecionado')
        else:
            # Coletando qual item está selecionado.
            item_selecionado = self.treeview.focus()

            # Coletando os dados do item selecionado (dicionário).
            rowid = self.treeview.item(item_selecionado)

            # Removendo o item com base no valor do rowid (argumento text do treeview).
            # Removendo valor da tabela.
            self.banco.remover_registro(rowid['text'])

            # Removendo valor do treeview.
            self.treeview.delete(item_selecionado)


    def exportar_alunos(self):
    
        conexao = sqlite3.connect('dados.db')
        c = conexao.cursor()   

        c.execute("SELECT *, oid FROM alunos")
        alunos_cadastrados = c.fetchall()
        alunos_cadastrados = pd.DataFrame(alunos_cadastrados, columns=["aluno", 'inicio', "fim", "soma", "data", "total", "ID"])
        alunos_cadastrados.to_excel("banco_alunos.xlsx")
        conexao.commit()
        conexao.close()  


root = tk.Tk()
app = Janela(master=root)
app.mainloop()