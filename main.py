from fastapi import FastAPI
from service import extract_license, get_vehicle_data, generate_response

app = FastAPI()

@app.get("/chat")
def chat(message: str):
    license_number = extract_license(message)

    if not license_number:
        return {"response": "Please provide a valid vehicle license number."}

    data = get_vehicle_data(license_number)

    response = generate_response(data)

    return {"response": response}