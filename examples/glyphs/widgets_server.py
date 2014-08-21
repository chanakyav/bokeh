from __future__ import print_function

from datetime import date

from bokeh.document import Document
from bokeh.glyphs import Line, Circle
from bokeh.objects import (
    Plot, ColumnDataSource, DataRange1d, Glyph,
    LinearAxis, DatetimeAxis, Grid, HoverTool
)
from bokeh.session import Session
from bokeh.widgetobjects import VBox, TableColumn, HandsonTable

document = Document()
session = Session()
session.use_doc('widgets_server')
session.load_document(document)

def make_plot():
    source = ColumnDataSource(
        dict(
            dates=[ date(2014, 3, i) for i in [1, 2, 3, 4, 5] ],
            downloads=[100, 27, 54, 64, 75],
        )
    )

    xdr = DataRange1d(sources=[source.columns("dates")])
    ydr = DataRange1d(sources=[source.columns("downloads")])

    plot = Plot(title="Product downloads", data_sources=[source], x_range=xdr, y_range=ydr, plot_width=400, plot_height=400)

    line = Line(x="dates", y="downloads", line_color="blue")
    line_glyph = Glyph(data_source=source, xdata_range=xdr, ydata_range=ydr, glyph=line)
    plot.add_obj(line_glyph)

    circle = Circle(x="dates", y="downloads", fill_color="red")
    circle_glyph = Glyph(data_source=source, xdata_range=xdr, ydata_range=ydr, glyph=circle)
    plot.add_obj(circle_glyph)

    xaxis = DatetimeAxis()
    plot.add_obj(xaxis, 'below')

    yaxis = LinearAxis()
    plot.add_obj(yaxis, 'left')

    plot.add_obj(Grid(dimension=0, ticker=xaxis.ticker))
    plot.add_obj(Grid(dimension=1, ticker=yaxis.ticker))

    hover = HoverTool(plot=plot, tooltips=dict(downloads="@downloads"))
    plot.tools.append(hover)

    return plot, source

def make_ui():
    plot, source = make_plot()
    columns = [
        TableColumn(data="dates", type="date", header="Date"),
        TableColumn(data="downloads", type="numeric", header="Downloads"),
    ]
    data_table = HandsonTable(source=source, columns=columns)
    vbox = VBox(children=[plot, data_table])
    return vbox

document.add(make_ui())
session.store_document(document)

if __name__ == "__main__":
    link = session.object_link(document._plotcontext)
    print("Please visit %s to see the plots" % link)
