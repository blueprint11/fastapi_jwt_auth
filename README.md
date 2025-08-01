# FastAPI JWT Authentication Example

This is a simple FastAPI project demonstrating user authentication using JWT (JSON Web Tokens).

## 🔧 Features

- "/token" – Login endpoint to generate JWT access token
- "/health" – Health check endpoint
- "/me" – Protected endpoint that requires a valid token

## 🚀 How to Run

1. **Create virtual environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # on Windows use venv\Scripts\activate
    

2. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    

3. **Start FastAPI server**
    ```bash
    uvicorn main:app --reload
    

4. **Visit Swagger docs**:  
    [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## 🔐 Authentication

1. Use "/token" to log in using valid credentials.
2. login using username password in authenticate.
