import re
from db import get_connection

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain


llm = ChatOpenAI(
    model_name="gpt-5-chat-latest",
    temperature=0
)


def extract_license(text: str):
    pattern = r"[A-Z]{2,3}-\d{4}"
    match = re.search(pattern, text.upper())
    return match.group() if match else None


def get_vehicle_data(license_number: str):
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
        "owner_name": result[2]
    }


def generate_response(data: dict):
    if not data:
        prompt_text = "No vehicle found. Ask the user politely to check the license number."
    else:
        prompt_text = f"""
        You are an AutoGarage assistant who provides vehicle status.

        Vehicle Data:
        License: {data['license']}
        Status: {data['overall_status']}
        Owner: {data['owner_name']}

        Provide a simple answer whether the owner can pick up the vehicle or not.
        If done, say 'ready to pick up', if in progress, provide a simple progress statement,
        and if upcoming, say 'not even started to repair yet'.

        Explain clearly in a friendly way.
        """


    prompt = ChatPromptTemplate.from_template("{user_input}")
    chain = LLMChain(llm=llm, prompt=prompt)
    response = chain.run(user_input=prompt_text)
    return response