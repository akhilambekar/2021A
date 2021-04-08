import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_core_components as dcc
from bs4 import BeautifulSoup
from flask import render_template
import requests
import json
import base64
import pymysql
from pymysql.converters import escape_string

from stanfordcorenlp import StanfordCoreNLP
import json
from json2html import *

from collections import defaultdict

from nltk.tree import ParentedTree
from nltk.treeprettyprinter import TreePrettyPrinter
import re

import pandas as pd
from tabulate import tabulate



app = dash.Dash(__name__)   #external_stylesheets=[dbc.themes.SUPERHERO]

appserver = app.server

graph_card = dbc.Card([
    
                    dbc.CardBody([
                        
                        dbc.Textarea(id='textzone', value='',bs_size="lg",
            className="mb-3", placeholder="Please inter a statement in proper grammar with all implied clauses."),
                            ])
                    ])


app.layout = html.Div([
    
    
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    
    dbc.Row([html.H1('Machine Learning & Ontology Software')], justify="around"),
    
    
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    
    dbc.Row(dcc.Input(id='name', placeholder='Enter Complete Name...', type='text'), style={"height": "auto", "margin-left": 314}),
    
    html.Br(),
    
    html.Div(dcc.Input(id='email', placeholder='Enter Email Address...', type='text'),style={"height": "auto", "margin-left": 314} ),
    
    html.Br(),
    
    html.Div(dcc.Input(id='phone', placeholder='Enter Phone Number...', type='text') ,style={"height": "auto", "margin-left": 314}),
    
    html.Br(),
    
    
    dbc.Row([dbc.Col(graph_card, width=8)], justify="around"),
    
    dcc.ConfirmDialogProvider( html.Button('Submit to sNLP', style={"height": "auto", "margin-left": 314}),id='submit_button'), #message='Danger danger! Are you sure you want to continue?'
   # dbc.Row([html.Div(id='textoutput', style={'whiteSpace': 'pre-line','margin-left': 320, 'width': '1000px', 'display' : "inline-block !important"})])
    html.Br(),
    
    html.Div(id='textoutput', style={'whiteSpace': 'pre', 'margin-left': 320, 'width': '1000px', "font-family": "monospace"})

])


@app.callback(
                Output('textoutput', 'children'),
                [Input('submit_button', 'submit_n_clicks'),
                 Input('textzone', 'value'),
                 Input("name", "value"),
                 Input("email", "value"),
                 Input("phone", "value"),]
)

def text_output(submit_n_clicks,value, name, email, phone):
    
    if not submit_n_clicks:
        return ''
    
    else:
        host='http://66.76.242.198'
        port=9888
        
        nlp = StanfordCoreNLP(host, port=port,timeout=30000) 
        
        props = {
             'annotators': 'tokenize,ssplit,pos,lemma,ner,parse,depparse,dcoref,relation',
            'pipelineLanguage': 'en',
             'outputFormat': 'json'}
        
        tokn=nlp.word_tokenize(value)
        
        Pos=nlp.pos_tag(value)
        Ner=nlp.ner(value)
        Parse=nlp.parse(value)
        Dep_parse=nlp.dependency_parse(value)
        Json_data=json.loads(nlp.annotate(value, properties=props))

        # Connect to the Database server and save the required information
        #Password encryption/decryption for accessing Database server
        #------------Generate encrypted password---------------------------
        #EncodedServerPass = base64.b64encode("ServerPass".encode("utf-8"))
        #EncodedMySQLPass = base64.b64encode("MySQLPass".encode("utf-8"))
        #------------------------------------------------------------------

        with open("EncodedPasswords.txt", "r") as filestream:
            for line in filestream:
                EncServerPass, EncMySQLPass = line.split(",")


        ServerPass = base64.b64decode(EncServerPass)
        MySQLPass = base64.b64decode(EncMySQLPass)

        # Initializing required variables
        ServerAdress = '66.76.242.194'
        ServerUserName = 'ambekarakhil'
        MySQLUserName = 'ambekarakhil'
        DatabaseName = 'ambekarakhil'


        #Make a database connection
        cnx = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user= MySQLUserName,
            password= MySQLPass,
            db = DatabaseName
        )

        print("Connected to the following MySQL Server: " + cnx.get_server_info())

        # Add escape string (\\") for double quotes present in the json data, removes any conflict with insert statement
        json_data_sql = json.dumps(Json_data)

        CountVal = 3
        TeacherVal = name
        AssertionVal= "dummyAssertion"
        LinkageVal = "dummyLinkage"
        InputSentence = value

        #Execute SQL Commands
        with cnx.cursor() as cur:
    
            cur.execute('use ambekarakhil;')
            sql_command = """INSERT INTO verus0302c(count, teacher, assertion, nlp, linkages, inputSen) VALUES (%s, %s, %s, %s, %s, %s)""" 
            cur.execute(sql_command, (CountVal, TeacherVal, AssertionVal, json_data_sql, LinkageVal, InputSentence))

        cnx.commit()

        """
        #Retrieve data from MySQL
        with cnx.cursor() as cur:
    
            cur.execute('use ambekarakhil;')
            cur.execute('Select * from verus0302c;')
            rows = cur.fetchall()
            for row in rows:
                print(f'{row[0]} {row[1]} {row[2]} {row[3]} {row[4]}')

        """
        # Close all connections
        cnx.close()

        # # Convert the JSON result in a tabular format with HTML tags
        # jsontohtml = json2html.convert(json = Json_data);

        # #---------------Will expand this code to add more complex tasks --------------------
        # # Display the HTML code in a new browser
        # import webbrowser
        # f = open('JSONResult.html','w')
        # f.write(jsontohtml)
        # f.close()

        # webbrowser.open_new_tab('JSONResult.html')
        # #---------------Will expand this code to add more complex tasks --------------------

        # Flatten nested JSON data and convert the resultant into a dataframe.
        # This dataframe will be displayed on the web page.
        
        df_nested_list = pd.json_normalize(Json_data)
        df_nested_Sen = pd.json_normalize(Json_data, record_path = ["sentences"])
        df_nested_3 = df_nested_Sen.iloc[:, 0:2]
        df_nested_basic = df_nested_Sen.iloc[:, 2:3]
        df_nested_enhanced = df_nested_Sen.iloc[:, 3:4]
        df_nested_enhancedPP = df_nested_Sen.iloc[:, 4:5]
        df_nested_entity = df_nested_Sen.iloc[:, 5:6]
        df_nested_tokens = df_nested_Sen.iloc[:, 6:7]
        df_nested_basic['basicDependencies'] = df_nested_basic['basicDependencies'].astype('str').str.replace('},','}\n')
        df_nested_enhanced['enhancedDependencies'] = df_nested_enhanced['enhancedDependencies'].astype('str').str.replace('},','}\n')
        df_nested_enhancedPP['enhancedPlusPlusDependencies'] = df_nested_enhancedPP['enhancedPlusPlusDependencies'].astype('str').str.replace('},','}\n')
        df_nested_entity['entitymentions'] = df_nested_entity['entitymentions'].astype('str').str.replace('},','}\n')
        df_nested_tokens['tokens'] = df_nested_tokens['tokens'].astype('str').str.replace('},','}\n')
        
        return [output_nlp(Json_data, tokn, Pos, Ner, Parse, Dep_parse), tabulate(df_nested_3, headers='keys', tablefmt='psql'),
                tabulate(df_nested_basic, headers='keys', tablefmt='psql'), tabulate(df_nested_enhanced, headers='keys', tablefmt='psql'),
                tabulate(df_nested_enhancedPP, headers='keys', tablefmt='psql'),
                tabulate(df_nested_entity, headers='keys', tablefmt='psql'), tabulate(df_nested_tokens, headers='keys', tablefmt='psql')]
"""
                tabulate(df_nested_Sen["basicDependencies"], headers='keys', tablefmt='psql'),
                tabulate(df_nested_Sen["enhancedDependencies"], headers='keys', tablefmt='psql'),
                tabulate(df_nested_Sen["enhancedPlusPlusDependencies"], headers='keys', tablefmt='psql'),
                tabulate(df_nested_Sen["entitymentions"], headers='keys', tablefmt='psql'),
                tabulate(df_nested_Sen["tokens"], headers='keys', tablefmt='psql')]
"""        

# def output_nlp(Json_data, tokn, Pos, Ner, Parse, Dep_parse):
#     parse_tree = ParentedTree.fromstring(Parse)
#     parse_tree.pretty_print()
#     return "NLP Parse: \n {}".format(Parse)

def output_nlp(Json_data, tokn, Pos, Ner, Parse, Dep_parse):
    parse_tree = ParentedTree.fromstring(Parse)
    pretty_tree = TreePrettyPrinter(parse_tree).text()
    tree = pretty_tree.split("\n")
    tree.reverse()
    parse_print = '\n'.join(tree)
    parse_print = re.sub("_", "-", parse_print)
    return "NLP Parse(sentence structure): \n{}".format(parse_print)

    
if __name__ == "__main__":

    app.run_server(debug=False)
