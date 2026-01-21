from importlib import reload
from fastapi import FastAPI, UploadFile, File, HTTPException
import pandas as pd
from model import JsonModel
from adding_columns import add_columns
import requests
import uvicorn


app = FastAPI(
    title="SERVER-www",
    version="1.0.0",
)
SERVICE_C_URL = "http://service-c:8000/records"


@app.post("/clean")
def clean_data(data:list[JsonModel]):
    if not data:
        raise HTTPException(status_code=400, detail="No data provided")

    try:
        df = pd.DataFrame([item.model_dump() for item in data])
        cleaned_data = add_columns(df)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid data file")

    # response = requests.post(SERVICE_C_URL, json=cleaned_data)
    # if response.status_code != 200:
    #     raise HTTPException(
    #         status_code=500,
    #         detail="Failed to send data to Service C"
    #     )

    return {
        "status": "success",
        "records_sent": "lll"
    }

# if __name__ =="__main__":
#     uvicorn.run("main2:app",host="localhost",port=8888,reload=True)




