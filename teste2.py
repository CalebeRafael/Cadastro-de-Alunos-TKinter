

import sqlite3
import datetime


conexao = sqlite3.connect('dados.db')
c = conexao.cursor()      
c.execute("SELECT SUM(soma) FROM alunos") 
total = (c.fetchall()[0][0])
conexao.close()


print("{:.2f}".format(total))

