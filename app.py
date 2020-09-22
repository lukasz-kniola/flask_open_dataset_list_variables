from flask import Flask, flash, render_template, request

from service import *
from models import *

app = Flask(__name__)
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = '12345'

DATA = Dataset()

@app.route('/', methods=['GET', 'POST'])
def process_request():
    args = request.form.to_dict(flat=False)
    print("Request Arguments: " + str(args))

    if request.method == 'POST':
        return globals()[args['action'][0]](request, args, DATA)

    return render_template('step1.html')

app.run(host='127.0.0.1', port=8080)