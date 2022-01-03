from flask import Flask, render_template
from helperFunctions import CHOOSE_FILE_AND_INPUT_TEXT, CHOOSE_FILES_TO_BE_SUBMITTED, FILES_SUCCESSFULLY_UPLOADED, NO_FILES_CHOSEN, NO_INPUT_SUBMITTED, clearAllPreExistingFiles, deleteUserInputFiles

from plagBetweenFiles import *
from plagBetweenQueryAndEnteredFile import *
from plagBetweenTwoInputQueries import *

app = Flask("__name__")

app.config["UPLOAD_PATH"] = os.getcwd() + "/files"


@app.route("/upload_file", methods=["GET", "POST"])
def plagBetweenFiles():        
    if request.method == 'POST':
        for f in request.files.getlist('file_name'):
            try:
                f.save(os.path.join(app.config["UPLOAD_PATH"], f.filename))
            except:
                return render_template("uploadFilesPage.html", warningMessage=NO_FILES_CHOSEN, greetingMessage="")
        percentageOfPlagiarism = calcSimilarityBetweenFiles()
        if percentageOfPlagiarism == -1:
            return render_template("uploadFilesPage.html", warningMessage=NO_FILES_CHOSEN, greetingMessage="")
        return render_template('resultsOfPlagBetweenFilesPage.html', results=percentageOfPlagiarism)

    return render_template("uploadFilesPage.html", warningMessage="", greetingMessage=CHOOSE_FILES_TO_BE_SUBMITTED)


@app.route("/")
def Home():
    clearAllPreExistingFiles()
    return render_template("homePage.html")


@app.route("/TwoInputFiles", methods=['GET'])
def loadTwoInputFilesPage():
    return render_template('twoQueriesPage.html', query1="", query2="")


@app.route("/TwoInputQueries", methods=['POST'])
def plagBetweenTwoInputQueries():
    percentageOfPlagiarism = calcSimilarityBetweenTwoQueries()
    if percentageOfPlagiarism == -1:
        return render_template("twoQueriesPage.html", warningMessage=NO_INPUT_SUBMITTED, greetingMessage="")
    return render_template('twoQueriesPage.html', query1=percentageOfPlagiarism['inputQuery1'],
                           query2=percentageOfPlagiarism['inputQuery2'], output=percentageOfPlagiarism['output'])



app.config["UPLOAD_PATH2"] = os.getcwd()

@app.route("/QueryAndEnteredFile", methods=["GET", "POST"])
def plagBetweenQueryAndEnteredFile():       
    if request.method == 'POST':

        f = request.files['file']
        try:
            f.save(os.path.join(app.config["UPLOAD_PATH2"], f.filename))
        except:
            return render_template("queryAndEnteredFilePage.html", warningMessage=NO_FILES_CHOSEN, greetingMessage="", query = request.form['query'])


        percentageOfPlagiarism = calcSimilarityBetweenQueryAndFile()
        if percentageOfPlagiarism == 0:
            # clearAllPreExistingFiles()
            return render_template("queryAndEnteredFilePage.html", warningMessage=NO_FILES_CHOSEN, greetingMessage="", query = request.form['query'])
        if percentageOfPlagiarism == -1:
            # clearAllPreExistingFiles()
            return render_template("queryAndEnteredFilePage.html", warningMessage=NO_INPUT_SUBMITTED,  greetingMessage="",)

        # clearAllPreExistingFiles()
        return render_template('queryAndEnteredFilePage.html', query=request.form['query'],
                               output=percentageOfPlagiarism['output'])

    # clearAllPreExistingFiles()
    return render_template('queryAndEnteredFilePage.html', warningMessage="", greetingMessage=CHOOSE_FILE_AND_INPUT_TEXT)


@app.route("/about")
def about():
    # clearAllPreExistingFiles()
    return render_template("aboutUsPage.html")


app.run()
