import mysql.connector
import pprint as p
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np


cnx = mysql.connector.connect(user='username', password='password',
                              host='192.168.1.2',
                              database='database')
cursor = cnx.cursor()

query = ("""select hour(insert_time) as hour,
         date_format(insert_time, '%m/%d') as date,
         avg(humidity) as humidity
         FROM homedb.RP_DHT11_v2
         group by hour(insert_time),
         date_format(insert_time, '%m/%d')
         limit 10000"""
        )

cursor.execute(query)

# empty data structures
data = [];
humidity = [];
hour = [];
date = [];

for q in cursor:
    data.append((q))

cnx.close()

#parse results of query into separate lists
for q in range(len(data)):
    hour.append(data[q][0]);
    date.append(data[q][1]);
    humidity.append(data[q][2]);

#build plot.ly data structures
data = [
    go.Heatmap(
        z = humidity,
        x = date,
        y = hour,
        colorscale = 'Viridis'
    )
]

layout = go.Layout(
    title = 'Humidity Per Hour',
    xaxis = dict(ticks = '', nticks = 15),
    yaxis = dict(ticks = '')
)
fig = go.Figure(data = data, layout = layout)

#push to plot.ly
url = py.plot(fig, filename='datetime-heatmap2')
