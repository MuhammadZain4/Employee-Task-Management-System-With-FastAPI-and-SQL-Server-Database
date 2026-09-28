from app.core.database import engine
from sqlalchemy import text
from app.schemas.emp import requesteduser

def create_user(hashed_password:str,new:requesteduser):
    with engine.connect() as conn:
        result=conn.execute(text("""exec sp_create_user
                                    @username=:username,
                                    @email=:email,
                                    @hashed_password=:hashed_password
                                    """
                                ),
                                {
                                    "username":new.username,
                                    "email":new.email,
                                    "hashed_password":hashed_password
                                    
                                }
        )
        conn.commit()
        return {"message":"user created successfully"}

def get_email(email:str):
    with engine.connect() as conn:
        result=conn.execute(text("""exec sp_get_user_by_email
                                    @email=:email
                                """                                    ),
                                {
                                    "email":email
                                })
        res=result.mappings().first()
    return res
