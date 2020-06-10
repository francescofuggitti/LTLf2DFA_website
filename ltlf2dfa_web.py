from flask import Flask, render_template, request, url_for
from ltlf2dfa.parser.ltlf import LTLfParser
from ltlf2dfa.parser.pltlf import PLTLfParser
import subprocess
import os
import datetime
import uuid
import base64


PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
FUTURE_OPS = {"X", "F", "U", "G", "WX", "R"}
PAST_OPS = {"Y", "O", "S", "H"}

app = Flask(__name__)


def encode_svg(file):
    """Encode file to base64."""
    with open(file, "r") as image_file:
        encoded_string = base64.b64encode(image_file.read().encode("utf-8"))
    return encoded_string


def write_dot_file(dfa, name):
    """Write DOT file."""
    with open("{}/static/dot/{}.dot".format(PACKAGE_DIR, name), 'w') as fout:
        fout.write(str(dfa).replace(" size = \"7.5,10.5\";", "").replace("LR", "TB"))


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/ltlf_syntax')
def ltlf_syntax():
    return render_template("ltlf_syntax.html")


@app.route('/pltlf_syntax')
def pltlf_syntax():
    return render_template("pltlf_syntax.html")


@app.route('/dfa', methods=["POST"])
def dfa():
    formula_string = request.form["inputFormula"]
    assert formula_string
    automa_name = "dfa_" + str(datetime.datetime.now()).replace(" ", "_") + "_" + str(uuid.uuid4())

    if all(c in FUTURE_OPS for c in formula_string if c.isupper()):
        f_parser = LTLfParser()
        try:
            formula = f_parser(formula_string)
        except Exception as e:
            if request.form.get("exampleCheck1"):
                return render_template("dfa.html", error=str(e).encode("utf-8"))
            return render_template("index.html", error=str(e).encode("utf-8"))
    else:
        assert all(c in PAST_OPS for c in formula_string if c.isupper())
        p_parser = PLTLfParser()
        try:
            formula = p_parser(formula_string)
        except Exception as e:
            if request.form.get("exampleCheck1"):
                return render_template("dfa.html", error=str(e).encode("utf-8"))
            return render_template("index.html", error=str(e).encode("utf-8"))

    dfa = formula.to_dfa()
    write_dot_file(str(dfa), automa_name)
    subprocess.call('dot -Tsvg {} -o {}'.format("{}/static/dot/{}.dot".format(PACKAGE_DIR, automa_name),
                                                "{}/static/tmp/{}.svg".format(PACKAGE_DIR, automa_name)), shell=True)

    encoding = encode_svg("{}/static/tmp/{}.svg".format(PACKAGE_DIR, automa_name)).decode("utf-8")

    os.unlink("{}/static/dot/{}.dot".format(PACKAGE_DIR, automa_name))
    os.unlink("{}/static/tmp/{}.svg".format(PACKAGE_DIR, automa_name))

    return render_template("dfa.html",
                           formula=formula,
                           output=encoding)

if __name__== "__main__":
    app.run(debug=True)
