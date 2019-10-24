from flask import Flask, render_template, request, url_for
from ltlf2dfa.Translator import Translator
from ltlf2dfa.DotHandler import DotHandler
import subprocess
import random
import os, datetime, uuid

app = Flask (__name__)

@app.route ('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        params = request.form
        declare_assumption = False
        if request.form.get('declare'):
            declare_assumption = True
        if params['formula']:
            try:
                ## TRANSLATOR ##
                translator = Translator(params['formula'])
                translator.formula_parser()
                translator.translate()
                translator.createMonafile(declare_assumption)
                translator.invoke_mona()

                dot_handler = DotHandler()
                dot_handler.modify_dot()

                # random_number = random.randrange(0, 9999)
                automa_name = str(datetime.datetime.now()).replace(" ", "_") + "_" + str(uuid.uuid4())

                dot_handler.output_dot('/var/www/ltlf2dfa_web/static/dot/'+automa_name+'.dot')
                subprocess.call('dot -Tsvg /var/www/ltlf2dfa_web/static/dot/'+ automa_name +'.dot -o /var/www/ltlf2dfa_web/static/tmp/'+automa_name+'.svg', shell=True)
                os.unlink('/var/www/ltlf2dfa_web/static/dot/'+automa_name+'.dot')

                return render_template('result.html', automa_name=automa_name, formula=params['formula'], flag=declare_assumption)

            except Exception as e:
                return str(e)
        else:
            return render_template("index.html")

    else:
        return render_template("index.html")


if __name__== "__main__":
    app.run()
