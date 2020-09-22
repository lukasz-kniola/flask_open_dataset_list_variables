from flask import Flask, flash, render_template, request, redirect, Markup
from sas7bdat import SAS7BDAT
import csv

import pandas as pd
from werkzeug.utils import secure_filename

def step2(request, args, data):
    if 'file' not in request.files:
        flash('No file part')
        return render_template('step1.html')

    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file.filename.rsplit('.', 1)[1].lower() == 'csv':
        df = pd.read_csv(file)
        htm = Markup(df.to_html())

        file.stream.seek(0)
        f=file.read().decode("utf-8")
        reader = csv.DictReader(f.splitlines(), skipinitialspace=True)
        data.reset([row for row in reader])

        return render_template('step2.html', vars=reader.fieldnames, htm=htm)

    elif file.filename.rsplit('.', 1)[1].lower() == 'sas7bdat':
        file.save('./tmp/_')

        #Pandas
        df = pd.read_sas('./tmp/_', format = 'sas7bdat', encoding='iso-8859-1')
        htm = Markup(df.to_html())
        print(df.columns)

        #SAS7BDAT
        # with SAS7BDAT('./tmp/_', skip_header=True) as sasreader:
        #     for row in sasreader:
        #         print(row)
        #     for col in sasreader.columns:
        #         print(str(col.name))

        return render_template('step2.html', vars=list(df.columns), htm=htm)

    else:
        flash('Extension not recognized.')
        return redirect(request.url)


    return render_template('step2.html', vars=reader.fieldnames, htm=htm)


def step3(request, args, data):
    columns = {var:[row[var] for row in data] for var in data.vars if var in args['vars']}
    columns = {k:sorted(list(set(v))) for k,v in columns.items()}

    return render_template('step3.html', vars=columns.items())

