from datetime import datetime, timedelta
from fastapi import HTTPException
from jose import JWTError, jwt

SECRET_KEY = "<s^t@>5rPi9(N^qzG=t1M:;N&uP?/f:#j&:QcIMO{)Q3daAXW=E&2+wIsHJs8ly"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 960

def create_token(data: dict):
    try:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)        
        return encoded_jwt
    except JWTError as e:  
        raise HTTPException(status_code=500, detail="Error interno al generar el token")


def validate_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None