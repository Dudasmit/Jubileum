from dash import Dash, dash, dcc, dash_table
#from dash.dependencies import Input, Output, State
from dash import Input, Output, State, html
import pandas as pd
import dash_bootstrap_components as dbc
import base64
import plotly.graph_objects as go
import plotly.express as px
import json
from datetime import datetime, date, time
from csv import DictWriter

from dateutil.relativedelta import relativedelta




app = Dash(__name__, meta_tags=[
        {
            "name": "viewport",
            "content": "width=device-width, initial-scale=1, maximum-scale=1.0, user-scalable=no",
        }
    ], external_stylesheets=[dbc.themes.SLATE], suppress_callback_exceptions=True)



PLOTLY_LOGO = "pngwing.png"

threshold = 1

def Read_update_DF():
    global Input_columns
    df_Company = pd.read_csv('Companies Data_.csv')

    df_Company['Registration Date'] = pd.to_datetime(df_Company['Registration Date'], format='%d/%m/%Y', errors='coerce').dt.date
    df_Company.dropna(subset=['Registration Date'], inplace=True)
    df_Company.fillna(0, inplace=True)
    df_Company.reset_index(drop= True , inplace= True )
    Input_columns= df_Company.columns
    df_Company['Anniversary Day'] = date(1, 1, 1)

    return df_Company
'''
df_Company = pd.read_csv('Companies Data_.csv')

df_Company['Registration Date'] = pd.to_datetime(df_Company['Registration Date'], format='%d/%m/%Y', errors='coerce').dt.date
df_Company.dropna(subset=['Registration Date'], inplace=True)
df_Company.fillna(0, inplace=True)
df_Company.reset_index(drop= True , inplace= True )
'''
df_Company = Read_update_DF()


list_years=[1,2, 5,10,15,20,25]

List_of_columns = ['KvK Number', 'Company Name', 'Street',
       'House Number', 'Postal Code', 'City', 'Phone Number', 'Employee Count',
       'Registration Date', 'Branche Type', 'Branche Code',
       'Branche Description', 'Status Company','Anniversary Day']

#df_Company = df_Company[List_of_columns]

#print(['information_{}'.format(_) for _ in Input_columns])

Company_Desc = df_Company[List_of_columns].columns
#print(type(List_of_columns.append('Anniversary Day')))
color = 'rgb(40, 43, 48)'



def Convert(a):
    it = iter(a)
    res_dct = dict(zip(it, it))
    return res_dct

def Insert_Company(row):
    print(row)
    try:
        with open('Companies Data_.csv', 'a', newline='') as f_object:
    # Pass the CSV  file object to the Dictwriter() function
    # Result - a DictWriter object
            ListofCol = Input_columns.values.tolist()
            Company_dict = dict(zip(ListofCol, row))
            Registration_Date = datetime.strptime(Company_dict['Registration Date'], '%Y-%m-%d').date()
            Company_dict['Registration Date'] = Registration_Date .strftime("%d/%m/%Y")
            dictwriter_object = DictWriter(f_object, fieldnames=ListofCol)
    # Pass the data in the dictionary as an argument into the writerow() function
            dictwriter_object.writerow(Company_dict)
    # Close the file object
            f_object.close()
            return True
    except Exception as e:
        print(str(e))
        return False
    



def Anniversaries_date(engine, an__filter = []):

    an__filter = list(dict.fromkeys(an__filter))
    filter_ = ''
    if an__filter:
        filter_ = ' where ' 
    
        for item in an__filter:
            if Straat_filter.index(item) > 0:
                filter_ = filter_ + ' or '

            filter_ = filter_ + 'Anniversaries.Anniversary = \'' + str(item) + '\' '

    df_Straat = pd.read_sql_query(
        sql = '''Select  * FROM  Anniversaries''' ,
        con = engine
    )

    df_Straat.sort_values(by='year', ascending=True, inplace=True)

    return df_Straat


def days_until_anniversary(registration_date,value):
    #print(registration_date)
    today = pd.Timestamp('today')
    anniversary_date = pd.Timestamp(registration_date.year + value, registration_date.month, registration_date.day)
    if anniversary_date < today:
        return date(1, 1, 1)
        while anniversary_date < today:
            anniversary_date = pd.Timestamp(anniversary_date.year + value, anniversary_date.month, anniversary_date.day)
    delta = anniversary_date - today
    return datetime.date(anniversary_date)



def generate_table(dataframe, max_rows=3):
    
    
    return dash_table.DataTable(
        id='tbl',
        columns=[
            {'name': i, 'id': i, 'deletable': False} for i in dataframe.columns
        ],
        data=dataframe.to_dict('records'),
       # style table
        fixed_rows={'headers': True},
        style_table={
                'maxHeight': '100ex',
                #'overflowY': 'scroll',
                'width': '100%',
                'minWidth': '100%',
                'maxWidth': 0,
            },
            # style cell
        style_cell={
                'fontFamily': 'Open Sans',
                'textAlign': 'center',
                #'height': '60px',
                'padding': '2px 22px',
                'whiteSpace': 'inherit',
                'overflow': 'hidden',
                'textOverflow': 'string',
                'backgroundColor':  color,
                'maxWidth': 0,
            },
        
            # style header
        style_header={
                'fontWeight': 'bold',
                'backgroundColor':  color,
                'maxWidth': 0,

            },
       
        selected_rows=[],
        page_action='native',
        page_current= 0,
        page_size= 10,
    )
         
    

def CreateInput_():
    return [ dbc.Col([  dbc.Row(html.P("{}".format(_))), dbc.Row(dcc.Input(id="input_1{}".format(_),placeholder="input type {}".format(_)))], width=3)  for _ in Company_Desc]

def CreateInput__():
    return [ dbc.Row([  dbc.Col(html.P("{}".format(_)), width=3), dbc.Col(dcc.Input(id="input_{}".format(_),
            placeholder="input type {}".format(_), style={'width': '100%', 'textAlign': 'center'}), width=9)]) 
            if _ != 'Registration Date' 
            else dbc.Row([  dbc.Col(html.P("{}".format(_)), width=3), dbc.Col(
            dcc.DatePickerSingle(
                id="input_{}".format(_),
                
                date=pd.Timestamp('today').date(),  style={ 'width': '100%', 'textAlign': 'center'}
                    )
                , width=9)])   for _ in Input_columns]


def CreateIinformation():
    return [ dbc.Row([  dbc.Col(html.P("{}".format(_))), dbc.Col(html.P(id="information_{}".format(_),children ="{}".format(_)))]) for _ in Company_Desc]

def drawInput():
    return  html.Div([
        dbc.Row(CreateInput__()
        ),  
    ])



def drawIinformation():
    return  html.Div([
        dbc.Card(
            dbc.CardBody(dbc.Row(CreateIinformation()))
        ),  
    ])

def GetMap(City_Company):
    City_Company.reset_index(drop= True , inplace= True )
    mapbox_access_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNrOWJqb2F4djBnMjEzbG50amg0dnJieG4ifQ.Zme1-Uzoi75IaFbieBDl3A"

    fig = px.scatter_mapbox(City_Company, lat="lat", lon="lon", hover_name="Company Name", hover_data=["KvK Number", "Phone Number", "Street","House Number"],
                  color_continuous_scale=px.colors.cyclical.IceFire,  size_max=25, zoom=10,)
    fig.update_layout(mapbox_style="open-street-map", hovermode='closest',
    clickmode='event+select',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=go.layout.mapbox.Center(
            lat=City_Company['lat'].iloc[0],
            lon=City_Company['lon'].iloc[0]
        ),
        pitch=0,
        zoom=10
    ))
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig


def FILTERS():
    return dbc.CardBody([

                            #dbc.Col(html.P("Filters:"), md=12),
                            dbc.Row([
                                dbc.Col([
                                    dcc.Dropdown(
                                        id="choose_city",
                                        style={'color': color},
                                        options=[{"label": i, "value": i} for i in df_Company.City.unique()],
                                        value='',
                                        clearable = True,
                                                ),
                                        ],md=3),
                             
                                dbc.Col([
                                    dcc.Dropdown(
                                        id="choose_yaer",
                                        style={'color': color},
                                        options=[{"label": i, "value": i} for i in list_years],
                                        value='',
                                        clearable = True,
                                                ),
                                        ], md=3), 
                                    ], align='center'),

                            dbc.Col([html.Div(id="active_table")])

                            ])

def drawFiguremap():
    return  html.Div([
        dbc.Card(
                [

                    dcc.Loading(
                            id="loading-map_company",
                            children=  [dcc.Graph(id="map_company")],
                            type="default",
                                )
                ]
        ),  
    ])





with open(PLOTLY_LOGO, "rb") as image_file:
    img_data = base64.b64encode(image_file.read())
    img_data = img_data.decode()
    img_data = "{}{}".format("data:image/png;base64, ", img_data)

NAVBAR = dbc.Navbar(
    children=[
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col([
                           html.Img(src=img_data, height="60px"), dbc.NavbarBrand("Company anniversaries", className="ml-2")
                        ], width=8),
                    dbc.Col([dbc.Button(
                        "Add company",
                        id="Add_company",
                        className="ms-auto",
                        n_clicks=0,
                    )
                    ], width=4),
                
                   
                ],
                align="center",
                #no_gutters=True,
            ),
           
        )
    ],
    color="dark",
    dark=True,
    sticky="top",
)

FILTERS = html.Div(children=[FILTERS()], id = 'hide_filters')

BODY = html.Div(
                dbc.CardBody([
                        #dbc.Row([dbc.Col([drawInput()], width=12),], align='center'),
                        dbc.Row([dbc.Col([FILTERS], width=12),], align='center'),
                        html.Br(),
                        #dbc.Row([dbc.Col([dcc.Loading(id="loading-table")], width=12),], align='center'), 
                        dbc.Row([
                            dbc.Col([], width=12),
                                ], align='center'), 
                            ])
                        

                )
TABLE = html.Div(dbc.CardBody([dbc.Row([dbc.Col([dcc.Loading(id="loading-table1", children = generate_table(df_Company[List_of_columns]), type="default")], width=12)], align='center',)
]))


modal_show = html.Div(
    [
        dbc.Modal(
            [   
                dbc.ModalHeader(dbc.ModalTitle(html.P(id="company_name",children =[]))),
                dbc.ModalBody(dbc.Row([dbc.Col([drawIinformation()], width=6), dbc.Col(drawFiguremap(), width=6)], align='center')),

                dbc.ModalFooter(
                    dbc.Button(
                        "Close",
                        id="close-show",
                        className="ms-auto",
                        n_clicks=0,
                    )
                ),
            ],
            id="modal-show",
            size="lg",
            scrollable=True,
            is_open=False,
        ),
    ]
)

modal_inp = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("New company")),
                
                dbc.ModalBody(dbc.Row([dbc.Col([drawInput()])], align='center')),
                dbc.ModalFooter(
                    dbc.Row([
                        
                        dbc.Col([
                            dbc.Button("Save", id="Save", className="ms-auto", n_clicks=0)
                                ])
                            ], align='center')
                                ),
            ],
            id="modal_inp",
            scrollable=True,
            size="lg",
            is_open=False,
        ),
    ]
)

modal_Save = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle(html.P(id="save_information",children =[]))),
                
            ],
            id="modal_Save",
            is_open=False,
        ),
    ]
)



app.layout = html.Div(children=[modal_show, modal_inp, modal_Save, NAVBAR, BODY, TABLE]) 



@app.callback(
    Output("loading-table1", "children"),

    [Input("choose_city", "value"),Input("choose_yaer", "value")],

)
def update_table(value, value_yaer):
   
    today6 = datetime.date(datetime.now()) + relativedelta(months=+6)
    today18 = datetime.date(datetime.now()) + relativedelta(months=+18)
    

    if value_yaer:
            
       
        df_Company['Anniversary Day'] = df_Company['Registration Date'].apply(days_until_anniversary,args = ([value_yaer]))
        df_Company1 = df_Company.loc[(df_Company['Anniversary Day'] >=  today6) & (df_Company['Anniversary Day'] <=  today18)]

        if value:
            table = generate_table(df_Company1.loc[df_Company1['City'] == value][List_of_columns])
        else:
            table = generate_table(df_Company1[List_of_columns])

    else:
        if value:
            #table = dbc.Table.from_dataframe(df_Company.loc[df_Company['City'] == value][List_of_columns], striped=True, bordered=True, hover=True, index=True)
            table = generate_table(df_Company.loc[df_Company['City'] == value][List_of_columns])
        else:
            table = generate_table(df_Company[List_of_columns])

            #table = dbc.Table.from_dataframe(df_Company[List_of_columns], striped=True, bordered=True, hover=True, index=True)
 
    return table

@app.callback(
    [[Output('information_{}'.format(_), 'children') for _ in Company_Desc], 
    Output("modal-show", "is_open"),
    Output("company_name", "children"),
    Output("map_company", "figure"),

    ],
    [Input('tbl', 'active_cell'),Input("close-show", "n_clicks")],
    [State('tbl', 'data'),
    State("modal-show", "is_open")],
)
def update_output(active_cell, n2, data, is_open):
    open = is_open
    Company_name = ''
    #print(active_cell)
    

    if active_cell is None:
        return ['{}'.format(_) for _ in Company_Desc], open,Company_name , GetMap(df_Company)
        
    if active_cell or n2:
        open = not is_open
    

    if active_cell:
        
        col = active_cell['column_id']
        row = active_cell['row']
        cellData = data[row][col]
        fig = GetMap(df_Company.loc[df_Company['KvK Number'] == data[row]['KvK Number']])

        return [data[row]['{}'.format(i)] for i in Company_Desc], open, str(data[row]['Company Name']), fig
    return ['{}'.format(_) for _ in Company_Desc], open, Company_name, GetMap(df_Company)




@app.callback(
    [ Output("modal_inp", "is_open"), 
    Output("modal_Save", "is_open"),
    Output("save_information", "children"),
    Output("Save", "n_clicks"),
    ],
    [Input("Add_company", "n_clicks"), Input("Save", "n_clicks")], 
    [State("modal_inp", "is_open"),State("modal_Save", "is_open"), [State('input_{}'.format(_), 'value') if _ != 'Registration Date'  else State('input_{}'.format(_), 'date') for _ in Input_columns]]
)
def Add_company_modal(n1, n2, is_open_inp, is_open_Save, row_company):
    print(n1)
    if n1 or n2:
        if n2 & n2 != 0:
            print(n2)
            if Insert_Company(row_company):
                global df_Company
                df_Company = Read_update_DF()

                return not is_open_inp, not is_open_Save,  "Saved", 0
            else:
                return is_open_inp, not is_open_Save, "Not saved", 0
        else:
            return not is_open_inp, is_open_Save, "Not saved", 0
    else:
        return is_open_inp, is_open_Save, "Not saved", 0





if __name__ == "__main__":
    app.run_server()
