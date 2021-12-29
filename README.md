### 📜 Description:

Project contains three types of plagiarism checkers:

1) Plagiarism Checker system that is used to detect plagiarism in files using cosine similarity. To compute the similarity between all files on project directory , the raw data is transformed into vectors, and then to arrays of numbers and then used vectors to compute the similarity between the files and prints the percentage. 

2) Plagiarism Checker using Python-Flask. TF-IDF and cosine similarity. It checks for how similar the query is to the existing database file.

3) Plagiarism Checker system that is used to detect plagiarism of the entered file with the given query.ase file.

### Steps for the first plagiarism
1. User enters the files.
2. Files are processed.
3. Calculations are done (Term Frequency, Cosine Similarity).
4. The Plagiarism Percentage is returned on the web page.

### Steps for the second plagiarism
1. User enters a query.
2. Query gets processed (Uppercase to lowercase, Removal of punctuationmarks, etc).
3. Calculations are done (Term Frequency, Cosine Similarity).
4. The Plagiarism Percentage is returned on the web page.

### Steps for the third plagiarism
1. User enters a query and a file.
2. Query gets processed (Uppercase to lowercase, Removal of punctuationmarks, etc.)
3. File is processed.
4. Calculations are done (Term Frequency, Cosine Similarity).
5. The Plagiarism Percentage is returned on the web page.

### Install required dependencies with:

```bash
pip install scikit-learn
```

### Built With:

- Python.
- Sklearn.
- TF_IDF_Vectorizer.
- Cosine_Similarity.
- Pycharm.
- Python-Flask : is a light-weight web framework for Python.
