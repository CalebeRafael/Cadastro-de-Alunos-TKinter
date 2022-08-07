

import sqlite3
import datetime


conexao = sqlite3.connect('dados.db')
c = conexao.cursor()      
c.execute("SELECT time(sum(strftime('%s', soma) - strftime('%s', '00:00')), 'unixepoch') FROM alunos") 
total = (c.fetchall()[0][0])
conexao.close()


print(total)

