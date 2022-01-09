import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from random import randint
from db import select, select old

sql = '''
select id from bulletins
    '''
result_sql = select_old(sql)['id']

sql = f'''
select sum* from bulletins 
where id not in [{result_sql}]
'''
result_sql = select(sql)['id']

graph = {
}

delta = 0
for row in result_sql:
    qty = graph.get(row['date_time']) or 0
    qty += 1
    graph[row['date_time']] = qty

fig, ax = plt.subplots()


ax.plot(graph.keys(), graph.values(), 'o-b')
ax.set_xlabel('Время',
              fontsize=15
              )
ax.set_ylabel('Количество принятых бюллетеней',
              fontsize=15)

plt.grid(True)
