import re
from typing import Optional, Dict, Any

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


from db import get_connection


llm = ChatOpenAI(
    model="gpt-5-chat-latest",
)

def extract_license(text: str) -> Optional[str]:
    """Extracts vehicle license plate from text using regex."""
    pattern = r"[A-Z]{2,3}-\d{4}"
    match = re.search(pattern, text.upper())
    return match.group() if match else None


def get_vehicle_data(license_number: str) -> Optional[Dict[str, Any]]:
    """Fetches vehicle details from the database."""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            query = """
                SELECT license_number, model, owner_name, overall_status
                FROM vehicles 
                WHERE license_number = %s;
            """
            cursor.execute(query, (license_number,))
            result = cursor.fetchone()

            if not result:
                return None

            return {
                "license": result[0],
                "owner_name": result[2],
                "overall_status": result[3]
            }
    finally:
        conn.close()


def generate_response(data: Optional[dict]) -> str:
    """Generates a friendly garage status update using LCEL."""

    if not data:

        system_prompt = "You are a polite AutoGarage assistant."
        user_content = "No vehicle found. Ask the user politely to check the license number."
    else:
        system_prompt = "You are an AutoGarage assistant who provides vehicle status."
        user_content = f"""
        Vehicle Data:
        - License: {data['license']}
        - Status: {data['overall_status']}
        - Owner: {data['owner_name']}

        Rules:
        1. If status is 'done', say 'ready to pick up'.
        2. If 'in progress', provide a simple progress statement.
        3. If 'upcoming', say 'not even started to repair yet'.

        Explain clearly and in a friendly way.
        """


    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}")
    ])


    chain = prompt | llm | StrOutputParser()


    response = chain.invoke({"input": user_content})
    return response

