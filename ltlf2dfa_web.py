from flask import Flask, render_template, request, jsonify
from ltlf2dfa.parser.ltlf import LTLfParser
from ltlf2dfa.parser.pltlf import PLTLfParser
import subprocess
import os
import datetime
import uuid
import base64
import json

app = Flask(__name__)


def encode_svg(file):
    with open(file, "r") as image_file:
        encoded_string = base64.b64encode(image_file.read().encode("utf-8"))
    return encoded_string


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/ltlf_syntax')
def ltlf_syntax():
    return render_template("ltlf_syntax.html")


@app.route('/pltlf_syntax')
def pltlf_syntax():
    return render_template("pltlf_syntax.html")

@app.route('/dfa')
def dfa():
    return render_template("dfa.html")

# @app.route('/dfa', methods=['POST'])
# def dfa():
#     formula = request.form['formula']
#     if formula:
#         try:
#             ## TRANSLATOR ##
#             translator = Translator(formula)
#             translator.formula_parser()
#             translator.translate()
#             translator.createMonafile(declare_assumption)
#             translator.invoke_mona()
#
#             dot_handler = DotHandler()
#             dot_handler.modify_dot()
#
#             automa_name = str(datetime.datetime.now()).replace(" ", "_") + "_" + str(uuid.uuid4())
#
#             dot_handler.output_dot('/var/www/ltlf2dfa_web/static/dot/'+automa_name+'.dot')
#             subprocess.call('dot -Tsvg /var/www/ltlf2dfa_web/static/dot/'+ automa_name +'.dot -o /var/www/ltlf2dfa_web/static/tmp/'+automa_name+'.svg', shell=True)
#
#             # automa_name = "declare-img1"
#
#             encoding = encode_svg('/var/www/ltlf2dfa_web/static/tmp/{}.svg'.format(automa_name)).decode("utf-8")
#             data = {'code': "SUCCESS", 'formula': formula, 'flag': declare_assumption, 'svg': encoding}
#             json_data = json.dumps(data)
#
#             os.unlink('/var/www/ltlf2dfa_web/static/dot/'+automa_name+'.dot')
#             os.unlink('/var/www/ltlf2dfa_web/static/tmp/{}.svg'.format(automa_name))
#
#             return json_data
#
#             # return render_template('dfa.html', automa_name=automa_name, formula=params['formula'], encoding=encoding, flag=declare_assumption)
#
#         except Exception as e:
#             data = {'code': "FAIL", 'formula': formula, 'flag': declare_assumption, 'error': str(e)}
#             return json.dumps(data)
#             # return str(e)
#     else:
#         return render_template("index.html")

if __name__== "__main__":
    app.run(debug=True)
