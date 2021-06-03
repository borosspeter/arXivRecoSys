# arXivRecoSys
Recommendation system for arXiv manuscripts

## About arXivRecoSys
The main aim of project arXivRecoSys is to predict relevance of recent arXiv manuscripts for a research group. Prediction is based on arXiv manuscripts of the group and arXiv references of that manuscripts. Predicative model learns from authors lists, titles and abstracts.

## Dataset
Raw [Kaggle arXiv Dataset](https://www.kaggle.com/Cornell-University/arxiv) is used for model building. After downloading and unzipping the dataset, you can put it in the folder `data/`.

## Files
- `arXivRecoSys.ipynb` : ipython notebook for raw data preprocessing, model fitting and prediction
- `PredictSavedb.py` : python code for prediction and save prediction into SQL database (standalone but requests `data/model.sav`)
- `data/arxiv-metadata-oai-snapshot.json` : Kaggle arXiv Dataset (raw data, not synced by github) 
- `data/traindataset.csv` : Training dataset processed from Kaggle arXiv dataset (not synced by github)
- `data/model.sav` : Trained model for prediction (synced by github)
- `data/manuscripts.db` : SQL database contains recent manuscripts with predicted relevance (not synced by github)

## Usage
Funcionality of `arXivRecoSys.ipynb`:
- Training data preparation
- Model training 
- Making a query through arXiv API
- Predicting relevance of recent manuscripts
- Exporting results into SQL database

Funcionality of `PredictSavedb.py` (standalone but requests `data/model.sav`) :
- Making a query through arXiv API
- Predicting relevance of recent manuscripts
- Exporting results into SQL database

## Output
Main output is `data/manuscripts.db` that is a SQL database, columns of `manuscripts` table:
- `id` : full arXiv link (TEXT)
- `published` : published date (TIMESTAMP)
- `authors` : list of authors in the format F1. (F2.) Last with comma separation (TEXT)
- `title` : title (TEXT)
- `abstract` : abstract (TEXT)
- `relevance` :  relevance of the manuscript between 0 and 1 (REAL) 

## Used packages
- [Python wrapper for the arXiv](https://pypi.org/project/arxiv/)
