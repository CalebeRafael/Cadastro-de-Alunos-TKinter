import tkinter as tk
import sqlite3
import pandas as pd
 
# conexao = sqlite3.connect('banco_alunos.db')

# c = conexao.cursor()

# c.execute('''CREATE TABLE alunos (
#     nome text,
#     dia text,
#     horas text
# )
# ''')

# conexao.commit()
# conexao.close()

def cadastrar_aluno():
    conexao = sqlite3.connect('banco_alunos.db')

    c = conexao.cursor()

    c.execute('INSERT INTO alunos VALUES (:nome, :dia, :horas)', 
    {
        'nome': entry_nome.get(),
        'dia': entry_dia.get(), 
        'horas': entry_horas.get()
    }
    )

    conexao.commit()
    conexao.close()
    entry_nome.delete(0, "end")
    entry_dia.delete(0, "end")
    entry_horas.delete(0, "end")


def exportar_alunos():
    conexao = sqlite3.connect('banco_alunos.db')

    c = conexao.cursor()

    c.execute("SELECT *, oid FROM alunos")
    alunos_cadastrados = c.fetchall()
    alunos_cadastrados = pd.DataFrame(alunos_cadastrados, columns=["nome", 'dia', "horas", "Id_banco"])
    alunos_cadastrados.to_excel("banco_alunos.xlsx")
    conexao.commit()
    conexao.close()


janela = tk.Tk()
janela.title('Cadastro de Alunos')

#Labels

label_nome = tk.Label(janela, text= 'Nome') 
label_nome.grid(row=0, column=0, padx=10, pady=10)

label_dia = tk.Label(janela, text= 'Dia') 
label_dia.grid(row=1, column=0, padx=10, pady=10)

label_horas = tk.Label(janela, text= 'Horas') 
label_horas.grid(row=2, column=0, padx=10, pady=10)


#Entrys

entry_nome = tk.Entry(janela, text= 'Nome', width=30) 
entry_nome.grid(row=0, column=1, padx=10, pady=10)

entry_dia = tk.Entry(janela, text= 'Dia', width=30) 
entry_dia.grid(row=1, column=1, padx=10, pady=10)

entry_horas = tk.Entry(janela, text= 'Horas', width=30) 
entry_horas.grid(row=2, column=1, padx=10, pady=10)

#Botão

botao_cadastrar = tk.Button(janela, text='Cadastar Aluno', command= cadastrar_aluno)
botao_cadastrar.grid(row=4, column=0, padx=10, pady=10, columnspan=2, ipadx=103)

botao_exportar = tk.Button(janela, text='Exportar Base de Alunos', command= exportar_alunos)
botao_exportar.grid(row=5, column=0, padx=10, pady=10, columnspan=2, ipadx=80)


janela.mainloop()