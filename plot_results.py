import simplejson
import numpy as np
import plotly
import plotly.plotly as py
from plotly.graph_objs import *

def load_files(avg_file, std_file):

    # load files
    with open(avg_file) as f:
        avg = simplejson.load(f)

    with open(std_file) as f:
        std = simplejson.load(f)

    std = np.array(std)
    print std
    std = np.true_divide(std, 2.)
    print std

    avg = np.array(avg)

    avg_upper = avg + std
    avg_lower = avg - std

    return avg, avg_upper, avg_lower

def plot_results(avg, avg_upper, avg_lower):

    n = len(avg)
    x =[i+1 for i in range(n+1)]
    x_rev = x[::-1]

    y1 = list(avg)
    y_upper = list(avg_upper)
    y_lower = list(avg_lower)
    y_lower = [0,0] + y_lower[::-1]

    trace1 = Scatter(
        x=x+x_rev,
        y=y_upper+y_lower,
        fill='tozerox',
        fillcolor='rgba(0,100,80,0.2)',
        line=Line(color='transparent'),
        showlegend=False,
        name='Fair'
    )

    trace2 = Scatter(
        x=x,
        y=y1,
        line=Line(color='rgb(0,100,80)'),
        mode='lines',
        name='Fair'
    )

    data = Data([trace1, trace2])

    layout = Layout(
        paper_bgcolor='rgb(255,255,255)',
        plot_bgcolor='rgb(229,229,229)',
        xaxis=XAxis(
            gridcolor='rgb(255,255,255)',
            range=[1,n+1],
            showgrid=True,
            showline=False,
            showticklabels=True,
            tickcolor='rgb(127,127,127)',
            ticks='outside',
            zeroline=False
        ),
        yaxis=YAxis(
            gridcolor='rgb(255,255,255)',
            showgrid=True,
            showline=False,
            showticklabels=True,
            tickcolor='rgb(127,127,127)',
            ticks='outside',
            zeroline=False
        )
    )

    plotly.offline.plot({"data": data, "layout": layout})


if __name__ == '__main__':

    avg_file1 = 'avg1.txt'
    avg_file2 = 'avg2.txt'
    std_file1 = 'std1.txt'
    std_file2 = 'std2.txt'

    avg, avg_upper, avg_lower = load_files(avg_file1, std_file1)
    plot_results(avg, avg_upper, avg_lower)

    # avg, avg_upper, avg_lower = load_files(avg_file2, std_file2)
    # plot_results(avg, avg_upper, avg_lower)
