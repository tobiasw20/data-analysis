from pathlib import Path
import math
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Select, Div, CustomJS, HoverTool, NumeralTickFormatter
from bokeh.plotting import figure, output_file, save

ROOT = Path(__file__).resolve().parents[1]
months = [f'2025-{m:02d}' for m in range(1,13)]
categories = ['Alle Kategorien', 'Elektronik', 'Haushalt', 'Büro']
data = {}
for category, base, trend, phase in [('Elektronik', 5200, 155, 0), ('Haushalt', 3500, 85, 1), ('Büro', 2200, 110, 2)]:
    data[category] = [round(base + trend*i + 390*math.sin(i*0.85+phase) + (i%3)*110) for i in range(12)]
data['Alle Kategorien'] = [sum(data[c][i] for c in categories[1:]) for i in range(12)]
source = ColumnDataSource(data=dict(x=list(range(1,13)), month=months, revenue=data['Alle Kategorien']))
plot = figure(height=365, sizing_mode='stretch_width', title='Monatliche Umsätze 2025', x_range=(0.5,12.5), tools='pan,wheel_zoom,box_zoom,reset,save', toolbar_location='above')
plot.line('x','revenue',source=source,line_width=3,color='#2563eb')
plot.scatter('x','revenue',source=source,size=9,color='#2563eb')
plot.xaxis.axis_label = 'Monat (2025)'
plot.yaxis.axis_label = 'Umsatz (€)'
plot.yaxis.formatter = NumeralTickFormatter(format='0,0')
plot.add_tools(HoverTool(tooltips=[('Monat','@month'),('Umsatz','@revenue{0,0} €')],mode='vline'))
select = Select(title='Produktkategorie', value='Alle Kategorien', options=categories, width=260)
summary = Div(text='', sizing_mode='stretch_width')
callback = CustomJS(args=dict(source=source, summary=summary, select=select, dataset=data), code="""
const values = dataset[select.value];
source.data = {x: Array.from({length:12}, (_,i)=>i+1), month: source.data.month.slice(), revenue: values.slice()};
const total = values.reduce((a,b)=>a+b,0);
const change = (values[11]/values[0]-1)*100;
const euro = new Intl.NumberFormat('de-DE',{style:'currency',currency:'EUR',maximumFractionDigits:0});
summary.text = `<div style="display:flex;gap:24px;flex-wrap:wrap;font-family:Arial,sans-serif;padding:12px 0"><div><small>Jahresumsatz</small><h2 style="margin:5px 0;color:#172554">${euro.format(total)}</h2></div><div><small>Veränderung Januar–Dezember</small><h2 style="margin:5px 0;color:#172554">${change.toFixed(1).replace('.',',')} %</h2></div></div>`;
source.change.emit();
""")
select.js_on_change('value',callback)
initial_total=sum(data['Alle Kategorien'])
initial_change=(data['Alle Kategorien'][-1]/data['Alle Kategorien'][0]-1)*100
summary.text=f'<div style="display:flex;gap:24px;flex-wrap:wrap;font-family:Arial,sans-serif;padding:12px 0"><div><small>Jahresumsatz</small><h2 style="margin:5px 0;color:#172554">{initial_total:,.0f} €</h2></div><div><small>Veränderung Januar–Dezember</small><h2 style="margin:5px 0;color:#172554">{initial_change:.1f} %</h2></div></div>'.replace(',','.')
layout = column(Div(text='<h2 style="font-family:Arial,sans-serif;color:#172554">Interaktive Umsatzanalyse</h2><p style="font-family:Arial,sans-serif">Demodaten · Kategorie auswählen, Punkte untersuchen und Diagramm zoomen.</p>'),select,summary,plot,sizing_mode='stretch_width',width=900)
output_file(ROOT/'demos'/'umsatzanalyse.html',title='Interaktive Umsatzanalyse | Demo',mode='inline')
save(layout)
print('Dashboard erzeugt')
