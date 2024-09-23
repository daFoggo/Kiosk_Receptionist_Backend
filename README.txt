# How to install 

## 1. Active venv 
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   .\.venv\Scripts\Activate  # Windows

## 2. Install requirement
   pip install -r requirements.txt

## 3. Create secret key for jwt
- Navigate to app/key.py
- Run debug
- Copy the key that was generated in terminal
- Create an .env file
- Copy to .env file :
   SECRET_KEY = "your secret key"

# 4. Build script :
   uvicorn app.main:app --reload 

