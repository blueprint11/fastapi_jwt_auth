from fastapi import FastAPI 
from pydantic import BaseModel
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from fastapi import security

app=FastAPI()
oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/token")

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Uthui(BaseModel):
    username: str
    password: str

fake_user_db = {
    "akshat": {
        "username": "akshat",
        "password": "test123"
    }
}

def authenticate_user(db,username: str, password: str):
    user=db.get(username)
    if not user or user["password"]!=password:
        return False
    return user

def jwt_token(data:dict, expires_delta:timedelta | None = None):
    copy_for_encode=data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc)+ timedelta(minutes=15)
    copy_for_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(copy_for_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

#creation of jwt token 
@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user=authenticate_user(fake_user_db,form_data.username,form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="incorrect username or password",
            headers={"WWW-Authenticate":"Bearer"},
              )
    access_token_expires=timedelta(minutes=30)
    access_token=jwt_token(
        data={"sub":user["username"]},
        expires_delta=access_token_expires
    )
    return {"access_token":access_token, "token_type":"bearer"}


#verifiction of jwt token :helper function
def authenticate_token(token: str):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except JWTError:
         raise HTTPException(status_code=401, detail="Invalid token")

#getting user from input token :dependency for routes tht need authorization   
def get_current_user(token: str = Depends(oauth2_scheme)):
    username = authenticate_token(token)
    return username

@app.get("/me")
def read_me(current_user: str = Depends(get_current_user)):
    return {"user": current_user}

@app.get("/health", tags=["Health check"])
def health_check():
    return {"status":"ok","message":"service up and running"}