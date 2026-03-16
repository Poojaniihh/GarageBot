import re
from db import get_connection
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def extract_license(text):
    pattern = r"[A-Z]{2,3}-\d{4}"
    match = re.search(pattern, text.upper())
    return match.group() if match else None



def get_vehicle_data(license_number):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT 
            v.license_number,
            v.model,
            v.owner_name,
            v.overall_status,
            v.completed_steps,
            v.total_steps
        FROM vehicles v
        WHERE v.license_number = %s;
    """

    cursor.execute(query, (license_number,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if not result:
        return None

    return {
        "license": result[0],
        "overall_status": result[3],
        "owner_name": result[2],
    }



def generate_response(data):
    if not data:
        prompt = "No vehicle found. Ask the user politely to check the license number."
    else:
        prompt = f"""
        You are an AutoGarage assistant who provides vehicle status.

        Vehicle Data:
        License: {data['license']}
        Status: {data['overall_status']}
        Hello: {data['owner_name']}
        Provide simple answer whether owner can pickup or not and if its done ready to pick up if its in progress 
        provide simple progress statement and if its upcoming say its not even started to repair yet  
    
        Explain this clearly and in a friendly way.
        """

    response = client.chat.completions.create(
        model="gpt-5-chat-latest",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content