
import dash_core_components as dcc
import plotly.graph_objs as go
import dash
import dash_html_components as html
import base64
import datetime
from dash.dependencies import Input, Output, State
import dash_table
import dash_auth
import plotly

from flask import Flask, jsonify
from flask import Flask, send_file, make_response, send_from_directory
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import seaborn as sns
import numpy as np
import pandas as pd

from matplotlib.figure import Figure
import io

df_jan = pd.ExcelFile(r'ENE - 02.- MONTHLY INCIDENTS Real Time.xlsx')
dfs_jan = {sheet_name: df_jan.parse(sheet_name) 
          for sheet_name in df_jan.sheet_names}

jan_mir = dfs_jan.get('MONTHLY INCIDENTS RAISED')
jan_mir1 = jan_mir.drop([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16], axis= 0)
jan_mir2 = jan_mir1.reset_index().drop(["index"], axis = 1)
jan_mir2.columns = jan_mir2.iloc[0]
jan_mir3 = jan_mir2.drop([0], axis = 0)

jan_mic = dfs_jan.get('MONTHLY INCIDENTS CLOSED')
jan_mic1 = jan_mic.drop([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16], axis= 0)
jan_mic2 = jan_mic1.reset_index().drop(["index"], axis = 1)
jan_mic2.columns = jan_mic2.iloc[0]
jan_mic3 = jan_mic2.drop([0], axis = 0)

jan_mib = dfs_jan.get('MONTHLY INCIDENTS BACKLOG')
jan_mib1 = jan_mib.drop([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16], axis= 0)
jan_mib2 = jan_mib1.reset_index().drop(["index"], axis = 1)
jan_mib2.columns = jan_mib2.iloc[0]
jan_mib3 = jan_mib2.drop([0], axis = 0)

df_feb = pd.ExcelFile(r'FEB - 02.- MONTHLY INCIDENTS Real Time.xlsx')
dfs_feb = {sheet_name: df_feb.parse(sheet_name) 
          for sheet_name in df_feb.sheet_names}

feb_mir = dfs_feb.get('MONTHLY INCIDENTS RAISED')
feb_mir1 = feb_mir.drop([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16], axis= 0)
feb_mir2 = feb_mir1.reset_index().drop(["index"], axis = 1)
feb_mir2.columns = feb_mir2.iloc[0]
feb_mir3 = feb_mir2.drop([0], axis = 0)

feb_mic = dfs_feb.get('MONTHLY INCIDENTS CLOSED')
feb_mic1 = feb_mic.drop([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16], axis= 0)
feb_mic2 = feb_mic1.reset_index().drop(["index"], axis = 1)
feb_mic2.columns = feb_mic2.iloc[0]
feb_mic3 = feb_mic2.drop([0], axis = 0)

feb_mib = dfs_feb.get('MONTHLY INCIDENTS BACKLOG')
feb_mib1 = feb_mib.drop([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16], axis= 0)
feb_mib2 = feb_mib1.reset_index().drop(["index"], axis = 1)
feb_mib2.columns = feb_mib2.iloc[0]
feb_mib3 = feb_mib2.drop([0], axis = 0)

df_all_mic = pd.concat([jan_mic3, feb_mic3], axis=0)
#%%

serv = pd.ExcelFile(r"Incidents by service and applications JAN-JUN2018.xls")
serv1 = {sheet_name: serv.parse(sheet_name) 
          for sheet_name in serv.sheet_names}
serv_data = serv1.get('Data')


inc_data = serv_data.fillna("App not found")
#critical_inc= inc_app[inc_app["Priority"] == "Critical"]
#crit_count = critical_inc.groupby(['CI Name'])[['Incident ID']].nunique()
#crit_count["CI Name"]= crit_count.index
#%%
ava_pd = pd.ExcelFile(r'Incidents by service and applications JAN-JUN2018.xls')
Ava_df = {sheet_name: ava_pd.parse(sheet_name) 
          for sheet_name in ava_pd.sheet_names}
Availability_DF = Ava_df.get('Data')
Availability_DF=Availability_DF.fillna("Application not found")

Availability_critical= Availability_DF[Availability_DF["Priority"] == "Critical"]

#%%

serv2 = pd.ExcelFile(r'20190125 Critical services - application.xls')
serv2 = {sheet_name: serv2.parse(sheet_name) 
          for sheet_name in serv2.sheet_names}
serv2_data = serv2.get('Dominio-ser-aplic')

appl= inc_data ["CI Name"].tolist()
crit_app= serv2_data ["Application"].tolist()

critic_appl=[]

for i in appl:
    if i in crit_app:
        critic_appl.append(i)
    else:
        critic_appl.append("False")
            
inc_data.insert(loc=0, column='Critical_app', value=critic_appl)
   

#critical_inc= inc_data[inc_data["Priority"] == "Critical"]
critical_inc= inc_data[inc_data["Critical_app"] != "False"]

#critical_inc = inc_data["Incident ID"].unique()
crit_count = critical_inc.groupby(['CI Name'])[['Incident ID']].nunique()
#crit_app_count= critical_applications.groupby(['CI Name'])[['Incident ID']].nunique()
crit_count["CI Name"]= crit_count.index

#%%
critical_inc['date'] = pd.DatetimeIndex(critical_inc['Date raised']).date
critical_inc['month'] = pd.DatetimeIndex(critical_inc['Date raised']).month
critical_inc['month'] = critical_inc['month'].map(lambda x: 'January' if x == 1 else x) 
critical_inc['month'] = critical_inc['month'].map(lambda x: 'February' if x == 2 else x) 
critical_inc['month'] = critical_inc['month'].map(lambda x: 'March' if x == 3 else x) 
critical_inc['month'] = critical_inc['month'].map(lambda x: 'April' if x == 4 else x) 
critical_inc['month'] = critical_inc['month'].map(lambda x: 'May' if x == 5 else x) 
critical_inc['month'] = critical_inc['month'].map(lambda x: 'June' if x == 6 else x)

#%%
jan_inc= critical_inc[critical_inc["month"] == "January"]
jan_inc['date'] = pd.DatetimeIndex(jan_inc['Date raised']).date
jan_count = jan_inc.groupby(['CI Name'])[['Incident ID']].nunique()
jan_count["CI Name"]= jan_count.index

feb_inc= critical_inc[critical_inc["month"] == "February"]
feb_inc['date'] = pd.DatetimeIndex(feb_inc['Date raised']).date

feb_count = feb_inc.groupby(['CI Name'])[['Incident ID']].nunique()
feb_count["CI Name"]= feb_count.index

mar_inc= critical_inc[critical_inc["month"] == "March"]
mar_inc['date'] = pd.DatetimeIndex(mar_inc['Date raised']).date

mar_count = mar_inc.groupby(['CI Name'])[['Incident ID']].nunique()
mar_count["CI Name"]= mar_count.index

apr_inc= critical_inc[critical_inc["month"] == "April"]
apr_inc['date'] = pd.DatetimeIndex(apr_inc['Date raised']).date

apr_count = apr_inc.groupby(['CI Name'])[['Incident ID']].nunique()
apr_count["CI Name"]= apr_count.index

may_inc= critical_inc[critical_inc["month"] == "May"]
may_inc['date'] = pd.DatetimeIndex(may_inc['Date raised']).date

may_count = may_inc.groupby(['CI Name'])[['Incident ID']].nunique()
may_count["CI Name"]= may_count.index

jun_inc= critical_inc[critical_inc["month"] == "June"]
jun_inc['date'] = pd.DatetimeIndex(jun_inc['Date raised']).date

jun_count = jun_inc.groupby(['CI Name'])[['Incident ID']].nunique()
jun_count["CI Name"]= jun_count.index


#%%
trace1 = go.Bar(
    x=jan_count['CI Name'], 
    y=jan_count['Incident ID'],
    name = 'Jan',
    marker=dict(color='#8A0808')
)
trace2 = go.Bar(
    x=feb_count['CI Name'],
    y=feb_count['Incident ID'],
    name='Feb',
    marker=dict(color='#FFBF00')
)
trace3 = go.Bar(
    x=mar_count['CI Name'],
    y=mar_count['Incident ID'],
    name='March',
    marker=dict(color='#F7D358')
)
trace4 = go.Bar(
    x=apr_count['CI Name'],  
    y=apr_count['Incident ID'],
    name = 'Apr',
    marker=dict(color='#F5A9A9')
)
trace5 = go.Bar(
    x=may_count['CI Name'],
    y=may_count['Incident ID'],
    name='May',
    marker=dict(color='#D8D8D8')
)
trace6 = go.Bar(
    x=jun_count['CI Name'],
    y=jun_count['Incident ID'],
    name='June',
    marker=dict(color='#F6CECE')
)
data = [trace1, trace2, trace3, trace4, trace5, trace6]
#%%
#traceline1 = go.Scatter(
#    y=jan_inc['Incident ID'], 
#    x=jan_inc['date'],
#    name = 'Jan',
#    mode='markers',
#    marker=dict(color='#8A0808')
#)
#traceline2 = go.Scatter(
#    y=feb_inc['Incident ID'],
#    x=feb_inc['date'],
#    name='Feb',
#    mode='markers',
#    marker=dict(color='#FFBF00') 
#)
#traceline3 = go.Scatter(
#    y=mar_inc['Incident ID'],
#    x=mar_inc['date'],
#    name='March',
#    mode='markers',
#    marker=dict(color='#F7D358')
#)
#traceline4 = go.Scatter(
#    y=apr_inc['Incident ID'],
#    x=apr_inc['date'],
#    name = 'Apr',
#    mode='markers',
#    marker=dict(color='#F5A9A9')
#)
#traceline5 = go.Scatter(
#    y=may_inc['Incident ID'],
#    x=may_inc['date'],
#    name='May',
#    mode='markers',
#    marker=dict(color='#D8D8D8')
#)
#traceline6 = go.Scatter(
#    y=jun_inc['Incident ID'],
#    x=jun_inc['date'],
#    name='June',
#    mode='markers',
#    marker=dict(color='#F6CECE')
#)
#dataline = [traceline1, traceline2, traceline3, traceline4, traceline5, traceline6]

#%%

critical_inc['Date closed'].apply (str)

critical_inc['Date closed'] = pd.to_datetime(critical_inc['Date closed'], errors= "coerce")


critical_inc['Date closed'] = critical_inc['Date closed'].astype('datetime64[ns]')

critical_inc['MTTR general'] = (critical_inc['Date closed'] - critical_inc['Date raised'])
critical_inc['MTTR days'] = (critical_inc['Date closed'] - critical_inc['Date raised']) / pd.Timedelta('1 day')
critical_inc['MTTR hours'] = (critical_inc['Date closed'] - critical_inc['Date raised']) / pd.Timedelta('1 hour')
critical_inc['MTTR minutes'] = (critical_inc['Date closed'] - critical_inc['Date raised']) / pd.Timedelta('1 minute')

Av_min = critical_inc.groupby(['CI Name'])[['MTTR minutes']].agg("mean")
Av_days= critical_inc.groupby(['CI Name'])[['MTTR days']].agg("mean")
Av_hour= critical_inc.groupby(['CI Name'])[['MTTR hours']].agg("mean")
#%%
Av_min["Applications"]= Av_min.index
Av_days["Applications"]= Av_days.index
Av_hour["Applications"]= Av_hour.index
av_min_sorted = Av_min.sort_values(by='MTTR minutes', ascending=False)
av_hour_sorted = Av_hour.sort_values(by='MTTR hours', ascending=False)
av_days_sorted = Av_days.sort_values(by='MTTR days', ascending=False)
final_min = av_min_sorted.head(10)
final_hour = av_hour_sorted.head(10)
final_days = av_days_sorted.head(10)

#%% Availability time per Application per month

Availability_critical['month'] = pd.DatetimeIndex(Availability_critical['Date raised']).month
Availability_critical['month'] = Availability_critical['month'].map(lambda x: 'January' if x == 1 else x) 
Availability_critical['month'] = Availability_critical['month'].map(lambda x: 'February' if x == 2 else x) 
Availability_critical['month'] = Availability_critical['month'].map(lambda x: 'March' if x == 3 else x) 
Availability_critical['month'] = Availability_critical['month'].map(lambda x: 'April' if x == 4 else x) 
Availability_critical['month'] = Availability_critical['month'].map(lambda x: 'May' if x == 5 else x) 
Availability_critical['month'] = Availability_critical['month'].map(lambda x: 'June' if x == 6 else x)

jan_inc1= Availability_critical[Availability_critical["month"] == "January"]

feb_inc1= Availability_critical[Availability_critical["month"] == "February"]

mar_inc1= Availability_critical[Availability_critical["month"] == "March"]

apr_inc1= Availability_critical[Availability_critical["month"] == "April"]

may_inc1= Availability_critical[Availability_critical["month"] == "May"]

jun_inc1= Availability_critical[Availability_critical["month"] == "June"]

jan_inc1['Resolution Time'] = ((pd.to_datetime(jan_inc1['Date closed']) - pd.to_datetime(jan_inc1['Date raised'])).dt.total_seconds() / 60)
feb_inc1['Resolution Time'] = ((pd.to_datetime(feb_inc1['Date closed']) - pd.to_datetime(feb_inc1['Date raised'])).dt.total_seconds() / 60)
mar_inc1['Resolution Time'] = ((pd.to_datetime(mar_inc1['Date closed']) - pd.to_datetime(mar_inc1['Date raised'])).dt.total_seconds() / 60)
apr_inc1['Resolution Time'] = ((pd.to_datetime(apr_inc1['Date closed']) - pd.to_datetime(apr_inc1['Date raised'])).dt.total_seconds() / 60)
may_inc1['Resolution Time'] = ((pd.to_datetime(may_inc1['Date closed']) - pd.to_datetime(may_inc1['Date raised'])).dt.total_seconds() / 60)
jun_inc1['Resolution Time'] = ((pd.to_datetime(jun_inc1['Date closed']) - pd.to_datetime(jun_inc1['Date raised'])).dt.total_seconds() / 60)

jan_availability = jan_inc1.groupby(['CI Name'])[['Resolution Time']].sum()
jan_availability["Uptime %"] = (43800- jan_availability ['Resolution Time'])/43800*100
#
feb_availability = feb_inc1.groupby(['CI Name'])[['Resolution Time']].sum()
feb_availability["Uptime %"] = (40320- feb_availability ['Resolution Time'])/40320*100

mar_availability = mar_inc1.groupby(['CI Name'])[['Resolution Time']].sum()
mar_availability["Uptime %"] = (43800- mar_availability ['Resolution Time'])/43800*100

apr_availability = apr_inc1.groupby(['CI Name'])[['Resolution Time']].sum()
apr_availability["Uptime %"] = (43800- apr_availability ['Resolution Time'])/43800*100

may_availability = may_inc1.groupby(['CI Name'])[['Resolution Time']].sum()
may_availability["Uptime %"] = (43800- may_availability ['Resolution Time'])/43800*100

jun_availability = jun_inc1.groupby(['CI Name'])[['Resolution Time']].sum()
jun_availability["Uptime %"] = (43800- jun_availability ['Resolution Time'])/43800*100


#%% Avialability time per Application cumulative 6 months
Availability_critical['Resolution Time'] = ((pd.to_datetime(Availability_critical['Date closed']) - pd.to_datetime(Availability_critical['Date raised'])).dt.total_seconds() / 60)
total_av = Availability_critical.groupby(['CI Name'])[['Resolution Time']].sum()
total_av ["Uptime %"]= (259320-total_av['Resolution Time'])/259320*100

high_10_av=total_av.nlargest(10, "Uptime %") # this is top 5 by availability
bottom_10_av=total_av.nsmallest(10, "Uptime %")# this is bottom 5 by availability
high_10_av["Applications"]= high_10_av.index
bottom_10_av["Applications"]= bottom_10_av.index

#%%

jan_sum = jan_count.sum()
jan_sum= pd.DataFrame (jan_sum)
feb_sum = feb_count.sum()
mar_sum = mar_count.sum()
apr_sum = apr_count.sum()
may_sum = may_count.sum()
jun_sum = jun_count.sum()

jan_sum = jan_sum.drop('CI Name')
feb_sum = feb_sum.drop('CI Name')
mar_sum = mar_sum.drop('CI Name')
apr_sum = apr_sum.drop('CI Name')
may_sum = may_sum.drop('CI Name')
jun_sum = jun_sum.drop('CI Name')

frames = [jan_sum, feb_sum, mar_sum, apr_sum, may_sum, jun_sum]


incidents_overtime = pd.concat([jan_sum, feb_sum,mar_sum,apr_sum,may_sum,jun_sum ], axis=0)
incidents_overtime = pd.DataFrame (incidents_overtime)
months=["january", "February","March2", "April", "May", "June"]

incidents_overtime.insert(loc=0, column="Month", value=months)
#%% Trends of incidents overtime, number of incidents raised per day of each month

incident_trend_jan= []
incident_trend_jan= pd.DataFrame(incident_trend_jan)
incident_trend_jan["Incident ID"]= jan_inc ["Incident ID"]
incident_trend_jan ["Date"] = jan_inc["Date raised"]
incident_trend_jan ["Date"] = pd.DatetimeIndex(incident_trend_jan ["Date"]).day
counts_jan = incident_trend_jan.groupby(["Date"]).size().reset_index(name="january")
#incident_trend_jan_trend= incident_trend_jan.groupby ["Date"]

incident_trend_feb= []
incident_trend_feb= pd.DataFrame(incident_trend_feb)
incident_trend_feb["Incident ID"]= feb_inc ["Incident ID"]
incident_trend_feb ["Date"] = feb_inc["Date raised"]
incident_trend_feb ["Date"] = pd.DatetimeIndex(incident_trend_feb ["Date"]).day
counts_feb = incident_trend_feb.groupby(["Date"]).size().reset_index(name="february")


incident_trend_mar= []
incident_trend_mar= pd.DataFrame(incident_trend_mar)
incident_trend_mar["Incident ID"]= mar_inc ["Incident ID"]
incident_trend_mar ["Date"] = mar_inc["Date raised"]
incident_trend_mar ["Date"] = pd.DatetimeIndex(incident_trend_mar ["Date"]).day
counts_mar = incident_trend_mar.groupby(["Date"]).size().reset_index(name="march")

incident_trend_apr= []
incident_trend_apr= pd.DataFrame(incident_trend_apr)
incident_trend_apr["Incident ID"]= apr_inc ["Incident ID"]
incident_trend_apr ["Date"] = apr_inc["Date raised"]
incident_trend_apr ["Date"] = pd.DatetimeIndex(incident_trend_apr ["Date"]).day
counts_apr = incident_trend_apr.groupby(["Date"]).size().reset_index(name="april")

incident_trend_may= []
incident_trend_may= pd.DataFrame(incident_trend_may)
incident_trend_may["Incident ID"]= may_inc ["Incident ID"]
incident_trend_may ["Date"] = may_inc["Date raised"]
incident_trend_may ["Date"] = pd.DatetimeIndex(incident_trend_may ["Date"]).day
counts_may = incident_trend_may.groupby(["Date"]).size().reset_index(name="may")

incident_trend_jun= []
incident_trend_jun= pd.DataFrame(incident_trend_jun)
incident_trend_jun["Incident ID"]= jun_inc ["Incident ID"]
incident_trend_jun  ["Date"] = jun_inc["Date raised"]
incident_trend_jun ["Date"] = pd.DatetimeIndex(incident_trend_jun ["Date"]).day
counts_jun = incident_trend_jun.groupby(["Date"]).size().reset_index(name="june")
#%% putting it in one dataframe
total_counts= counts_jan["Date"]
total_counts = pd.DataFrame(total_counts)

total_counts ["January"]= counts_jan["january"]
total_counts ["Febryary"]= counts_feb["february"]
total_counts ["March"]= counts_mar["march"]
total_counts ["April"]= counts_apr["april"]
total_counts ["May"]= counts_may["may"]
total_counts ["June"]= counts_jun["june"]
#%%
traceTotal = go.Scatter(
    y=total_counts['January'],  # NOC stands for National Olympic Committee
    x=total_counts['Date'],
    name = 'Jan',
    fill='tonexty',
    mode='lines',
    marker=dict(color='#8A0808') # set the marker color to gold
)
traceTotal2 = go.Scatter(
    y=total_counts['Febryary'],
    x=total_counts['Date'],
    name='Feb',
    fill='tonexty',
    mode='lines',
    marker=dict(color='#FFBF00') # set the marker color to silver
)
traceTotal3 = go.Scatter(
    y=total_counts['March'],
    x=total_counts['Date'],
    name='March',
    fill='tonexty',
    mode='lines',
    marker=dict(color='#F7D358') # set the marker color to bronze
)
traceTotal4 = go.Scatter(
    y=total_counts['April'],  # NOC stands for National Olympic Committee
    x=total_counts['Date'],
    name = 'Apr',
    fill='tonexty',
    mode='lines',
    marker=dict(color='#F5A9A9') # set the marker color to gold
)
traceTotal5 = go.Scatter(
    y=total_counts['May'],
    x=total_counts['Date'],
    name='May',
    fill='tonexty',
    mode='lines',
    marker=dict(color='#D8D8D8') # set the marker color to silver
)
traceTotal6 = go.Scatter(
    y=total_counts['June'],
    x=total_counts['Date'],
    name='June',
    fill='tonexty',
    mode='lines',
    marker=dict(color='#F6CECE') # set the marker color to bronze
)
dataTotal = [traceTotal, traceTotal2, traceTotal3, traceTotal4, traceTotal5, traceTotal6]

#%%


app = Flask("term-eduardo")

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

sns.set(style="whitegrid")

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server= app.server

app.scripts.config.serve_locally = True
app.config['suppress_callback_exceptions']=True

app.layout = html.Div([
        html.H1("IAG Incidence Metrics"),
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='Incidences', value='tab-1'),
        dcc.Tab(label='Availability', value='tab-2')


    ]),
    html.Div(id='tabs-content')
], 
            style={'text-align':'center',
                   'font-family':'Courier New'})

@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])

def render_content(tab):
    if tab == 'tab-1':
         return html.Div([
                html.Div([
            html.H2('Incidence Report')], 
            style={'text-align':'center'}),
                    
    dcc.Graph(
        figure=go.Figure(
            data=data,
            layout=go.Layout(
                title='Critical Incidences Per Month',
                barmode='stack',
                xaxis={'title':''},
                yaxis={'title':'Total Incidences'},
                showlegend=True,
                legend=go.layout.Legend(
                    x=0,
                    y=1.0
                ),
                margin=go.layout.Margin(l=100, r=0, t=100, b=100)
            )
        ),
        style={'height': 500,
               'width': '90%',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'},
        id='my-graph2'
    ) ,
                
    dcc.Graph(
        figure=go.Figure(
            data=[
                go.Bar(
                    x=crit_count['CI Name'],
                    y=crit_count['Incident ID'],
                    name='Total Critical Incidences per Application',
                    marker=go.bar.Marker(
                        color='#8A0808'
                    )
                )
            ],
            layout=go.Layout(
                title='Total Critical Incidences per Application',
                xaxis={'title':''},
                yaxis={'title':'Total Incidences'},
                showlegend=False,
                margin=go.layout.Margin(l=100, r=0, t=100, b=100)
            )
        ),
        style={'height': 500,
               'width': '90%',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'},
        id='my-graph'
    ),
                 
    dcc.Graph(
        figure=go.Figure(
            data=dataTotal,
            layout=go.Layout(
                title='Monthlhy Indicence Growth',
                xaxis={'title':'Date'},
                yaxis={'title':'Critical Incidences'},
                margin=go.layout.Margin(l=100, r=0, t=100, b=100)
            )
        ),
        style={'height': 500,
               'width': '90%',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'},
        id='my-graph10'  ),       

])
    elif tab == 'tab-2':
            return html.Div([
                html.Div([
            html.H2('Availability Report')], 
            style={'text-align':'center'}),
    dcc.Graph(
        figure=go.Figure(
            data=[
                go.Bar(
                    x=high_10_av['Applications'],
                    y=high_10_av['Uptime %'],
                    name='Most Available Applications',
                    marker=go.bar.Marker(
                        color='#8A0808'
                    )
                )
            ],
            layout=go.Layout(
                title='Most Available Applicatios',
                xaxis={'title':''},
                yaxis=dict(
            range=[99.90, 100]
        ),
                showlegend=False,
                margin=go.layout.Margin(l=100, r=0, t=100, b=100)
            )
        ),
        style={'height': 500,
               'width': '90%',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'},
        id='my-graph5'
    ),
             
   dcc.Graph(
        figure=go.Figure(
            data=[
                go.Bar(
                    x=bottom_10_av['Applications'],
                    y=bottom_10_av['Uptime %'],
                    name='Least Available Applications',
                    marker=go.bar.Marker(
                        color='#8A0808'
                    )
                )
            ],
            layout=go.Layout(
                title='Least Available Applications',
                xaxis={'title':''},
                yaxis=dict(
            range=[95, 100]
        ),
                showlegend=False,
                margin=go.layout.Margin(l=100, r=0, t=100, b=100)
            )
        ),
        style={'height': 500,
               'width': '90%',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'},
        id='my-graph6'
    )
])


if __name__ == '__main__':
    app.run_server(debug=True)
#    , use_reloader=False