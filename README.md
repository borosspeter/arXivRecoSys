# arXivRecoSys
Recommendation system for arXiv manuscripts

## Description
The main aim of project arXivRecoSys is to predict relevance of recent arXiv manuscripts for a research group. Prediction is based on arXiv manuscripts of the group and that manuscripts arXiv citations. Predicative model learns from authors lists, titles and abstracts.

## Dataset
[Kaggle arXiv Dataset](https://www.kaggle.com/Cornell-University/arxiv) is used for model building. After downloading and unzipping the dataset, you can put it in the folder `data/`.

## Files
- arXivRecoSys.ipynb - ipython notebook for raw data preprocessing, model fitting and prediction (standalone)
- PredictSavedb.py - python code for prediction and save prediction into SQL database (request data/model.sav)
- data/arxiv-metadata-oai-snapshot.json - Kaggle arXiv Dataset (raw data) 
- data/traindataset.csv - Training dataset processed from Kaggle arXiv dataset (not synced)
- data/model.sav - Trained model for prediction (synced)
- data/manuscripts.db - SQL database contains recent manuscripts with predicted relevance

## Usage
Funcionality of `arXivRecoSys.ipynb`:
- Training data preparation
- Model training 
- Making a query through arXiv API
- Predicting relevance of recent maunuscipts
- Exporting results into SQL database