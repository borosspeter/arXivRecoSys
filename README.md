# arXivRecoSys
Recommendation system for arXiv manuscripts

## About arXivRecoSys
The main aim of project arXivRecoSys is to predict relevance of recent arXiv manuscripts for a research group. Prediction is based on arXiv manuscripts of the group and arXiv references of that manuscripts. Predicative model learns from authors lists, titles and abstracts.

## Dataset
Raw [Kaggle arXiv Dataset](https://www.kaggle.com/Cornell-University/arxiv) is used for model building. After downloading and unzipping the dataset, you can put it in the folder `data/`.

## Files
- `arXivRecoSys.ipynb` : ipython notebook for raw data preprocessing, model fitting and prediction (cover all functionality of the project)
- `PredictSavedb.py` : python code for prediction and save prediction into SQL database (standalone but requests `data/model.sav`)
- `data/arxiv-metadata-oai-snapshot.json` : Kaggle arXiv Dataset (raw data, not synced by github) 
- `data/traindataset.csv` : Training dataset processed from Kaggle arXiv dataset (not synced by github)
- `data/model.sav` : Trained model for prediction (synced by github)
- `data/manuscripts.db` : SQL database contains recent manuscripts with predicted relevance (not synced by github)

## Usage
Functionality of `arXivRecoSys.ipynb` (cover all functionality of the project):
- Training data preparation
- Model training 
- Making a query through arXiv API
- Predicting relevance of recent manuscripts
- Exporting results into SQL database

Functionality of `PredictSavedb.py` (standalone but requests `data/model.sav`):
- Making a query through arXiv API
- Predicting relevance of recent manuscripts
- Exporting results into SQL database

## Output
Main output is `data/manuscripts.db` which is a SQL database with table `manuscripts`, its columns are: 
- `id` : Full arXiv link (**TEXT**)
- `published` : Published date (**TIMESTAMP**)
- `authors` : List of authors in the format `F1. (F2., ...) Last` with comma separation (**TEXT**)
- `title` : Title (**TEXT**)
- `abstract` : Abstract (**TEXT**)
- `relevance` : Predicted relevance of the manuscript between 0 (not relevant) and 1 (relevant) (**REAL**) 

## Used packages and web services
- [Python wrapper for the arXiv](https://pypi.org/project/arxiv/)
- [Prophy Science](https://www.prophy.science/)
