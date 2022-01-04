from flask import Flask
from Constants import CHOOSE_FILE_AND_INPUT_TEXT, CHOOSE_FILES_TO_BE_SUBMITTED, EMPTY_FILE_SUBMITTED, ERROR_ONE_FILE_ONLY, FILES_SUCCESSFULLY_UPLOADED, NO_FILES_CHOSEN, NO_INPUT_SUBMITTED, ONLY_ONE_FILE_CHOSEN
from helperFunctions import deleteUserInputFiles, renderPage

from plagBetweenFiles import *
from plagBetweenQueryAndEnteredFile import *
from plagBetweenTwoInputQueries import *

app = Flask("__name__")

app.config["filesDirectory"] = os.getcwd() + "/files"


@app.route("/upload_file", methods=["GET", "POST"])
def plagBetweenFiles():        
    if request.method == 'POST': 
        for f in request.files.getlist('file_name'):
            try:
                if not os.path.exists(app.config["filesDirectory"] ):
                    os.makedirs(app.config["filesDirectory"] )
                f.save(os.path.join(app.config["filesDirectory"], f.filename))
            except:
                return renderPage(fileName="uploadFilesPage.html", warningMessage=NO_FILES_CHOSEN, greetingMessage="")
        percentageOfPlagiarism = calcSimilarityBetweenFiles()
        if percentageOfPlagiarism == ERROR_NO_FILES:
            return renderPage(fileName="uploadFilesPage.html", warningMessage=NO_FILES_CHOSEN, greetingMessage="")
        if percentageOfPlagiarism == ERROR_ONE_FILE_ONLY:
            return renderPage(fileName="uploadFilesPage.html", warningMessage=ONLY_ONE_FILE_CHOSEN, greetingMessage="")
        if percentageOfPlagiarism == ERROR_EMPTY_FILE:
            return renderPage(fileName="uploadFilesPage.html", warningMessage=EMPTY_FILE_SUBMITTED, greetingMessage="")
        return renderPage(fileName='resultsOfPlagBetweenFilesPage.html', results=percentageOfPlagiarism)
    # Get
    return renderPage(fileName="uploadFilesPage.html", warningMessage="", greetingMessage=CHOOSE_FILES_TO_BE_SUBMITTED)


@app.route("/")
def Home():
    return renderPage(fileName="homePage.html")


@app.route("/TwoInputFiles", methods=['GET'])
def loadTwoInputFilesPage():
    return renderPage(fileName='twoQueriesPage.html', query1="", query2="")


@app.route("/TwoInputQueries", methods=['POST'])
def plagBetweenTwoInputQueries():
    percentageOfPlagiarism, inputText1, inputText2 = calcSimilarityBetweenTwoQueries()
    if percentageOfPlagiarism == ERROR_NO_INPUT:
        return renderPage(fileName="twoQueriesPage.html", warningMessage=NO_INPUT_SUBMITTED, greetingMessage="")
    return renderPage(fileName='twoQueriesPage.html', query1=inputText1,
                           query2=inputText2, output=percentageOfPlagiarism)



app.config["projectDirectory"] = os.getcwd()

@app.route("/QueryAndEnteredFile", methods=["GET", "POST"])
def plagBetweenQueryAndEnteredFile():       
    if request.method == 'POST':

        f = request.files['file']
        try:
            f.save(os.path.join(app.config["projectDirectory"], f.filename))
        except:
            return renderPage(fileName="queryAndEnteredFilePage.html", warningMessage=NO_FILES_CHOSEN, greetingMessage="", query = request.form['query'])


        percentageOfPlagiarism = calcSimilarityBetweenQueryAndFile()
        if percentageOfPlagiarism == ERROR_NO_FILES:
            return renderPage(fileName="queryAndEnteredFilePage.html", warningMessage=NO_FILES_CHOSEN, greetingMessage="", query = request.form['query'])
        if percentageOfPlagiarism == ERROR_EMPTY_FILE:
            return renderPage(fileName="queryAndEnteredFilePage.html", warningMessage=EMPTY_FILE_SUBMITTED, greetingMessage="", query = request.form['query'])
        if percentageOfPlagiarism == ERROR_NO_INPUT:
            return renderPage(fileName="queryAndEnteredFilePage.html", warningMessage=NO_INPUT_SUBMITTED,  greetingMessage="")

        return renderPage(fileName='queryAndEnteredFilePage.html', query=request.form['query'],
                               output=percentageOfPlagiarism)
    return renderPage(fileName='queryAndEnteredFilePage.html', warningMessage="", greetingMessage=CHOOSE_FILE_AND_INPUT_TEXT)


@app.route("/about")
def about():
    return renderPage(fileName="aboutUsPage.html")

if __name__ == "__main__":
    app.run()



# Rawan      calcSimilarityBetweenTwoQueries, calcSimilarityBetweenQueryandFile
#Agina       first 4 functions Helper function
#Salma       HTML, CSS
#Bedo        last 6 functions Helper function  
#Moataz      app.py           
#kareem      plagbetweenFiles