from flask import Flask, render_template, request, url_for
from tool.Translator import Translator
from tool.DotHandler import DotHandler
import subprocess
import random
import os

app = Flask (__name__)

@app.route ('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        params = request.form
        declare_assumption = False
        if request.form.get('declare', declare_assumption):
            declare_assumption = True
        else:
            if params['formula']:
                try:
                    ## TRANSLATOR ##
                    translator = Translator(params['formula'])
                    translator.formula_parser()
                    translator.translate()
                    translator.createMonafile(declare_assumption)

                    ## CALL MONA TOOL ##
                    if os.path.isfile("mona") and os.access("mona",
                                                            os.X_OK):  # check if mona exists and if it's executable
                        random_number = random.randrange(0,9999)
                        automa_name = 'automa-'+str(random_number)
                        subprocess.call('mona -u -gw automa.mona > static/tmp/'+automa_name+'.dot', shell=True)
                    else:
                        print('[ERROR] - MONA tool does not exist or it is not executable...')
                        exit()

                    ## POST-PROCESS MONA AUTOMATON ##
                    dot_handler = DotHandler('static/tmp/'+automa_name+'.dot')
                    dot_handler.modify_dot()
                    dot_handler.output_dot()

                    if os.path.isfile("mona"):  # check if automa exists
                        subprocess.call('dot -Tgif static/tmp/automa.dot -o static/tmp/'+automa_name+'.gif', shell=True)
                    else:
                        print('[ERROR] - MONA tool does not exist or it is not executable...')
                        exit()

                    return render_template('result.html', automa_name=automa_name)

                except Exception as e:
                    return str(e)
            else:
                return render_template("index.html")

    else:
        return render_template("index.html")


if __name__== "__main__":
    app.run(debug=True)