from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
import logging
logger=logging.getLogger(__name__)
SECRET_KEY = "SECRET_KEY"
ALGORITHM = "HS256"

security_scheme = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security_scheme)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            logger.warning(f"auth failed token has not subject")
            raise HTTPException(status_code=401, detail="invalid token")
        return email
    except JWTError:
        logger.warning(f"auth failed inavlid or expired token")
        raise HTTPException(status_code=401, detail="invalid token")