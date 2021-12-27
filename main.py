from flask import Flask, request, render_template

from plagBetweenFiles import *
from plagBetweenInputQueryAndDatabaseFile import *

app = Flask("__name__")

app.config["UPLOAD_PATH"] = "D:\My projects\WebProject-Plagiarism-Checker"


@app.route("/upload_file", methods=["GET", "POST"])
def upload_file():
    if request.method == 'POST' and request.form.get('action1') == 'Show Results':
        plagiarismRes = solve()  # try catch
        return render_template('resultsPage.html', plagiarismRes=plagiarismRes)
    if request.method == 'POST':
        for f in request.files.getlist('file_name'):
            f.save(os.path.join(app.config["UPLOAD_PATH"], f.filename))
        return render_template("uploadFiles.html", msg="Files has been uploaded successfully")
    return render_template("uploadFiles.html", msg="Please Choose a file")


@app.route("/")
def Home():
    deleteFiles()
    return render_template("homePage.html")


@app.route("/loadPage")
def loadPage():
    return render_template('queryAndDatabasePage.html', query="")


@app.route("/", methods=['POST'])
def plagBetweenInputQueryAndDatabaseFile():
    d = calcSimilarity()
    return render_template('queryAndDatabasePage.html', query=d['inputQuery'], output=d['output'])


app.run()
