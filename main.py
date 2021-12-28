from flask import Flask, render_template

from plagBetweenFiles import *
from plagBetweenInputQueryAndDatabaseFile import *
from plagBetweenQueryAndEnteredFile import *

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
        return render_template("uploadFiles.html", msg="Files have been uploaded successfully")
    return render_template("uploadFiles.html", msg="Please, Choose the files")


@app.route("/")
def Home():
    deleteFiles()
    deleteFileInDatabaseFolder()
    return render_template("homePage.html")


@app.route("/loadPage")
def loadPage():
    return render_template('queryAndDatabasePage.html', query="")


@app.route("/", methods=['POST'])
def plagBetweenInputQueryAndDatabaseFile():
    d = calcSimilarity()
    return render_template('queryAndDatabasePage.html', query=d['inputQuery'], output=d['output'])


app.config["PATH2"] = "D:\My projects\WebProject-Plagiarism-Checker\database"


@app.route("/QueryAndEnteredFile", methods=["GET", "POST"])
def plagBetweenQueryAndEnteredFile():
    if request.method == 'POST' and request.form.get('action2') == 'Show Results':
        plagiarismRes = calcSimilarity()
        return render_template('plagBetweenQueryAndEnteredFile.html', query=plagiarismRes['inputQuery'],
                               output=plagiarismRes['output'])
    if request.method == 'POST':
        f = request.files['file']
        f.save(os.path.join(app.config["PATH2"], f.filename))
        return render_template('plagBetweenQueryAndEnteredFile.html', msg="File has been uploaded successfully")
    return render_template('plagBetweenQueryAndEnteredFile.html', msg="Please, Choose a file")


app.run()
