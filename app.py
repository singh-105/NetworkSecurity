import sys
import os

import certifi
ca = certifi.where()

from dotenv import load_dotenv
load_dotenv()
mongo_db_url = os.getenv("MONGODB_URL_KEY")
print(mongo_db_url)
import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.pipeline.training_pipeline import TrainingPipeline

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Request, Form
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd

from networksecurity.utils.main_utils.utils import load_object

from networksecurity.utils.ml_utils.model.estimator import NetworkModel


if mongo_db_url:
    client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
    database = client[DATA_INGESTION_DATABASE_NAME]
    collection = database[DATA_INGESTION_COLLECTION_NAME]
else:
    print("Warning: MONGODB_URL_KEY is None. Database connection skipped.")
    client = None
    database = None
    collection = None

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="./templates")

@app.get("/", tags=["authentication"])
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/check_url")
async def check_url(request: Request, url: str = Form(...)):
    # Dummy verification logic
    # In a real scenario, this would call a model or an API
    
    classification = "Safe"
    result_class = "safe"
    
    # Simple rule-based dummy check for demonstration
    unsafe_keywords = ["malware", "phishing", "virus", "attack", "suspicious"]
    
    if any(keyword in url.lower() for keyword in unsafe_keywords):
        classification = "Unsafe"
        result_class = "unsafe"
    
    from urllib.parse import urlparse
    parsed_url = urlparse(url)
    
    details = {
        "Domain": parsed_url.netloc,
        "Scheme": parsed_url.scheme,
        "Path Length": len(parsed_url.path),
        "Total Length": len(url),
        "Risk Score": "85/100" if classification == "Unsafe" else "10/100" # Dummy score
    }

    return templates.TemplateResponse("index.html", {
        "request": request, 
        "url": url, 
        "result": classification,
        "result_class": result_class,
        "details": details
    })

@app.get("/train")
async def train_route():
    try:
        train_pipeline=TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training is successful")
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
@app.post("/predict")
async def predict_route(request: Request,file: UploadFile = File(...)):
    try:
        df=pd.read_csv(file.file)
        #print(df)
        preprocesor=load_object("final_model/preprocessor.pkl")
        final_model=load_object("final_model/model.pkl")
        network_model = NetworkModel(preprocessor=preprocesor,model=final_model)
        print(df.iloc[0])
        y_pred = network_model.predict(df)
        print(y_pred)
        df['predicted_column'] = y_pred
        print(df['predicted_column'])
        #df['predicted_column'].replace(-1, 0)
        #return df.to_json()
        df.to_csv('prediction_output/output.csv')
        table_html = df.to_html(classes='table table-striped')
        #print(table_html)
        return templates.TemplateResponse("table.html", {"request": request, "table": table_html})
        
    except Exception as e:
            raise NetworkSecurityException(e,sys)

    
if __name__=="__main__":
    app_run(app,host="127.0.0.1",port=8000)
