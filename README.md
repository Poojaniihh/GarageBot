# 🏎️ AutoGarage Chatbot

[![Python](https://img.shields.io/badge/python-3.11-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-v0.111.0-green)](https://fastapi.tiangolo.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT-5-purple)](https://platform.openai.com/)
[![License](https://img.shields.io/badge/license-MIT-orange)](LICENSE)

A **LangChain-powered AI chatbot** that lets users check **vehicle status** by license number. The chatbot uses a **database-first approach** to fetch accurate vehicle details and **LangChain + OpenAI LLM** to generate friendly, human-readable responses.

---

## 📌 Features

- Fetch vehicle details from MySQL by license number  
- Show repair status, overall progress, and owner info  
- Friendly AI responses using **LangChain + GPT-5**  
- Supports Sri Lankan license formats like `ABC-1234` or `CA-1010`  
- Modular and easy to extend with memory or historical vehicle logs  

---

## 🛠️ Tech Stack

| Layer          | Technology |
|----------------|------------|
| Backend        | Python 3.11, FastAPI |
| Database       | MySQL (XAMPP / phpMyAdmin) |
| AI / LLM       | LangChain + OpenAI GPT-5 |
| Environment    | python-dotenv for config |
| HTTP Server    | uvicorn |
| SQL Connector  | mysql-connector-python |

---

## ⚡ Project Flow

1. **User sends a license number** to the `/chat` API endpoint.  
2. **Extract license number** using regex.  
3. **Fetch vehicle data** from MySQL database.  
4. **Generate a friendly AI response** via LangChain + GPT-5.  
5. **Return the response** to the user in JSON format.  

---
