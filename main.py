from flask import Flask, render_template

from plagBetweenFiles import *
from plagBetweenInputQueryAndDatabaseFile import *
from plagBetweenQueryAndEnteredFile import *
import os

app = Flask("__name__")

app.config["UPLOAD_PATH"] = os.getcwd()




@app.route("/upload_file", methods=["GET", "POST"])
def upload_file():
    if request.method == 'POST' and request.form.get('action1') == 'Show Results':
        plagiarismRes = solve()
        if plagiarismRes == 0:
            return render_template("uploadFiles.html", msg="There are no files chosen.")
        return render_template('resultsPage.html', plagiarismRes=plagiarismRes)
    if request.method == 'POST':
        for f in request.files.getlist('file_name'):
            f.save(os.path.join(app.config["UPLOAD_PATH"], f.filename))
        return render_template("uploadFiles.html", msg="Files have been uploaded successfully.")
    return render_template("uploadFiles.html", msg="Please, Choose the files.")


@app.route("/")
def Home():
    deleteFiles()
    deleteTxtFiles()
    return render_template("homePage.html")


@app.route("/loadPage")
def loadPage():
    return render_template('queryAndDatabasePage.html', query="")


@app.route("/", methods=['POST'])
def plagBetweenInputQueryAndDatabaseFile():
    d = calcSimilarity()
    if d == 0:
        return render_template("queryAndDatabasePage.html", msg="There is no query entered.")
    return render_template('queryAndDatabasePage.html', query=d['inputQuery'], output=d['output'])


@app.route("/QueryAndEnteredFile", methods=["GET", "POST"])
def plagBetweenQueryAndEnteredFile():
    if request.method == 'POST' and request.form.get('action2') == 'Show Results':
        plagiarismRes = calcSimilarity2()
        if plagiarismRes == 0:
            return render_template("plagBetweenQueryAndEnteredFile.html", msg="There is no files chosen.")
        if plagiarismRes == -1:
            return render_template("plagBetweenQueryAndEnteredFile.html", msg="There is no query entered.")
        return render_template('plagBetweenQueryAndEnteredFile.html', query=plagiarismRes['inputQuery'],
                               output=plagiarismRes['output'])
    if request.method == 'POST':
        f = request.files['file']
        f.save(os.path.join(app.config["UPLOAD_PATH"], f.filename))
        return render_template('plagBetweenQueryAndEnteredFile.html', msg="File has been uploaded successfully.")
    return render_template('plagBetweenQueryAndEnteredFile.html', msg="Please, Choose a file.")


@app.route("/about")
def about():
    return render_template("aboutUs.html")


app.run()