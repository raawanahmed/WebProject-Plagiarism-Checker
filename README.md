### 📜 Description:

Project contains two types of plagiarism checkers

1) Plagiarism Checker system that is used to detect plagiarism in files using cosine similarity. To compute the
   similarity between all files on project directory , the raw data is transformed into vectors, and then to arrays of
   numbers and then used vectors to compute the similarity between the files and prints the value in Decimals
   where `1.0` indicates `100%`.
2) Web application of Plagiarism Checker using Python-Flask. TF-IDF and cosine similarity. It checks for how similar the
   query is to the existing database file.

### Steps for first plagiarism
1. User enters the files.
2. Files are processed
3. Calculations are done (Term Frequency, Cosine Similarity)
4. The Plagiarism Percentage is returned on the web page

### Steps for second plagiarism
1. User enters a query
2. Query gets processed (Uppercase to lowercase, Removal of punctuationmarks, etc.)
3. Calculations are done (Term Frequency, Cosine Similarity)
4. The Plagiarism Percentage is returned on the web page

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
