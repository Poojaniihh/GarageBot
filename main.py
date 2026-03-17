from fastapi import FastAPI
from pydantic import BaseModel
from service import extract_license, get_vehicle_data, generate_response

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(request: ChatRequest):

    license_number = extract_license(request.message)

    if not license_number:
        return {"reply": "Please provide a valid vehicle license number."}

    data = get_vehicle_data(license_number)
    response = generate_response(data)


    return {"reply": response}