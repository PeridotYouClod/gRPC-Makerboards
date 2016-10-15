import plotly
from plotly.graph_objs import Scatter, Layout

from pylibs.Database import Mongo

def GenScatterData(colname, size=None):
  x_axis = []
  y_axis = []
  mongo = Mongo()
  mongo.GetClient()
  prev = 0
  for data in mongo.Find(colname, size):
    x_axis.append(data['date'])
    y_axis.append(data[colname])
  print('Got %d datapoints' % len(y_axis))
  return(x_axis, y_axis)

def GenScatter(data):
  return Scatter(x=data[0], y=data[1])

def createGraph(num_points, colname):
  sensor_data = GenScatterData(colname, num_points)
  plotly.offline.plot({
    'data': [
        GenScatter(sensor_data),
    ],
    'layout': Layout(title='Data for %s' % colname)
  })

if __name__ == '__main__':
  num_points = 1000
  colname = 'lux'
  createGraph(num_points, colname)
