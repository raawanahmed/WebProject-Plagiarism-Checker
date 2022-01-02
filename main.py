from flask import Flask, render_template

from plagBetweenFiles import *
from plagBetweenQueryAndEnteredFile import *
from plagBetweenTwoInputQueries import *

app = Flask("__name__")

app.config["UPLOAD_PATH"] = os.getcwd() + "/files"


@app.route("/upload_file", methods=["GET", "POST"])
def plagBetweenFiles():
    if request.method == 'POST' and request.form.get('action1') == 'Show Results':
        percentageOfPlagiarism = calcSimilarityBetweenFiles()
        if percentageOfPlagiarism == -1:
            return render_template("uploadFilesPage.html", msg="There are no files chosen.")
        return render_template('resultsOfPlagBetweenFilesPage.html', results=percentageOfPlagiarism)
    if request.method == 'POST':
        for f in request.files.getlist('file_name'):
            f.save(os.path.join(app.config["UPLOAD_PATH"], f.filename))
        return render_template("uploadFilesPage.html", msg="Files have been uploaded successfully.")
    return render_template("uploadFilesPage.html", msg="Please, Choose the files.")


@app.route("/")
def Home():
    deleteFilesInFolderFiles()  # delete uploaded files to be able to upload new files
    deleteTxtFiles()
    return render_template("homePage.html")


@app.route("/loadPage")
def loadPage():
    return render_template('twoQueriesPage.html', query1="", query2="")


@app.route("/TwoInputQueries", methods=['POST'])
def plagBetweenTwoInputQueries():
    percentageOfPlagiarism = calcSimilarityBetweenTwoQueries()
    if percentageOfPlagiarism == -1:
        return render_template("twoQueriesPage.html", msg="There is no query entered.")
    return render_template('twoQueriesPage.html', query1=percentageOfPlagiarism['inputQuery1'],
                           query2=percentageOfPlagiarism['inputQuery2'], output=percentageOfPlagiarism['output'])


app.config["UPLOAD_PATH2"] = os.getcwd()


@app.route("/QueryAndEnteredFile", methods=["GET", "POST"])
def plagBetweenQueryAndEnteredFile():
    if request.method == 'POST' and request.form.get('action2') == 'Show Results':
        percentageOfPlagiarism = calcSimilarityBetweenQueryAndFile()
        if percentageOfPlagiarism == 0:
            return render_template("queryAndEnteredFilePage.html", msg="There is no files chosen.")
        if percentageOfPlagiarism == -1:
            return render_template("queryAndEnteredFilePage.html", msg="There is no query entered.")
        return render_template('queryAndEnteredFilePage.html', query=percentageOfPlagiarism['inputQuery'],
                               output=percentageOfPlagiarism['output'])
    if request.method == 'POST':
        f = request.files['file']
        f.save(os.path.join(app.config["UPLOAD_PATH2"], f.filename))
        return render_template('queryAndEnteredFilePage.html', msg="File has been uploaded successfully.")
    return render_template('queryAndEnteredFilePage.html', msg="Please, Choose a file.")


@app.route("/about")
def about():
    return render_template("aboutUsPage.html")


app.run()
