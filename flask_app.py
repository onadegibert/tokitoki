"""
Author: Ona de Gibert
"""
# https://realpython.com/python-web-applications/#build-a-basic-python-web-application
# https://dev.to/dcodeyt/creating-beautiful-html-tables-with-css-428l
from flask import Flask
from flask import request, escape
from main import *

app = Flask(__name__)


def return_results(results):
    return (
        """<head>
              <title>Toki Toki!</title>
           </head>
           <p class=page_title>TOKI TOKI, per aprendre Toki Pona</p>
           <body>
              <form action="/" method="get">
                Introdueix una frase: <br> <input type="text" name="sentence">
                <br> <input type="submit" value="Analitza" style="background-color:#c9f6d2;">
              </form>
             <form action="button">
                <br> O genera una de forma aleatòria:
                <br> <button name="randoam" style="background-color:#c9f6d2;">Frase aleatòria</button>
              </form>
           </body>
           <style>
           .page_title {
                font-family:"sans-serif";
                font-size:20px;
           }
            body {background-color: white;}
            h1   {color: white;font-family: sans-serif}}
            p    {font-family: sans-serif;font-size: 20px;background-color:black;color:white           
        </style>
        """
        + results
    )

# Decorator Flask uses to connect URL endpoints with code contained in functions.
@app.route("/")
# Create a form element on the landing page
def index():
    sentence = str(escape(request.args.get("sentence", ""))) #use escape to make sure no html tags can be introduced
    if sentence:
        results = """<p>La teva frase era... </p>""" + analyze(sentence)
    else:
        results = ""
    return return_results(results)


def get_pretty_print(results_dirty):
    table_entries = str()
    for entry in results_dirty:
        table_entries=table_entries+"""<tr class="active-row">
                <td>"""+entry.split('\t')[0]+"""</td>
                <td>"""+entry.split('\t')[1]+"""</td>
                <td>"""+entry.split('\t')[2]+"""</td>
            </tr>"""

    final_table = """<table class="styled-table">
        <thead>
            <tr>
                <th>Paraula</th>
                <th>Categoria</th>
                <th>Significat</th>
            </tr>
        </thead>
        <tbody>"""+table_entries+"""
            <!-- and so on... -->
        </tbody>
    </table>
    
    
    <style>
    .styled-table {
    border-collapse: collapse;
    margin: 25px 0;
    font-size: 0.9em;
    font-family: sans-serif;
    min-width: 400px;
    }
    
    .styled-table thead tr {
    background-color: #009879;
    color: #ffffff;
    text-align: left;
    }
    .styled-table th,
    .styled-table td {
    padding: 12px 15px;
    }
    .styled-table tbody tr {
        border-bottom: 1px solid #dddddd;
    }
    .styled-table tbody tr:nth-of-type(even) {
        background-color: #f3f3f3;
    }
    .styled-table tbody tr:last-of-type {
        border-bottom: 2px solid #009879;
    }
    </style>    
    """
    return final_table


def analyze(sentence):
    words, meanings_dict, nouns, adjs, vts, vis, poss = load_dict()
    sentence, words_meanings = analyse_sentence(sentence, meanings_dict, '')
    pretty_print = ' <p>' + sentence + '</p>' + get_pretty_print(words_meanings)
    return pretty_print

@app.route("/button")
def get_random_sentence():
    words, meanings_dict, nouns, adjs, vts, vis, poss = load_dict()
    sentence_syntax = get_sentence_syntax()
    sentence, pos = get_sentence(sentence_syntax, nouns, vis, vts, adjs, poss)
    sentence, words_meanings = analyse_sentence(sentence, meanings_dict, pos)
    pretty_print = ' <p>' + sentence + '</p>' + get_pretty_print(words_meanings)
    return return_results(pretty_print)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)

