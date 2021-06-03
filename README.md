# arXivRecoSys
Recommendation system for arXiv manuscripts

## About arXivRecoSys
The main aim of project arXivRecoSys is to predict relevance of recent arXiv manuscripts for a research group. Prediction is based on arXiv manuscripts of the group and arXiv references of that manuscripts. Predicative model learns from authors lists, titles and abstracts.

## Dataset
Raw [Kaggle arXiv Dataset](https://www.kaggle.com/Cornell-University/arxiv) is used for model building. After downloading and unzipping the dataset, you can put it in the folder `data/`.

## Files
- `arXivRecoSys.ipynb` : ipython notebook for raw data preprocessing, model fitting and prediction (standalone)
- `PredictSavedb.py` : python code for prediction and save prediction into SQL database (request `data/model.sav`)
- `data/arxiv-metadata-oai-snapshot.json` : Kaggle arXiv Dataset (raw data, not synced by github) 
- `data/traindataset.csv` : Training dataset processed from Kaggle arXiv dataset (not synced by github)
- `data/model.sav` : Trained model for prediction (synced by github)
- `data/manuscripts.db` : SQL database contains recent manuscripts with predicted relevance (not synced by github)

## Usage
Funcionality of `arXivRecoSys.ipynb`:
- Training data preparation
- Model training 
- Making a query through arXiv API
- Predicting relevance of recent maunuscipts
- Exporting results into SQL database

## Used packages
- [Python wrapper for the arXiv](https://pypi.org/project/arxiv/)