import pickle
from fastapi import APIRouter, FastAPI, HTTPException
from service.predict import Predict
import logging


class App:
    """
    Controller Class for all the api endpoints for App resource.
    """
    def __init__(self, prefix: str):
        print("App")
        self.model = pickle.load(open('backend/option_predictor_model.pkl', 'rb'))
        self.router = APIRouter(prefix=prefix)

        # Define routes within the APIRouter
        self.router.post("/app/predict")(self.predict)
        self.router.get("/app/")(self.home)

    def predict(self, data: dict):
        # "/app/predict" API entrypoint
        predict = Predict(data=data, model=self.model)
        status, response = predict.process_request()
        logging.debug(status, response)
        if status:
            return {"status_code": 200, "message": response }
        raise HTTPException(status_code=500, detail=f"Predictor Model Failed, Error: {response}")

    def home(self):
        return {"status_code": 200, "message": "Received."}


# Initialize App controller with APIRouter
app_controller = App(prefix="/v1")

app = FastAPI()


# Include the APIRouter within FastAPI
app.include_router(app_controller.router)


