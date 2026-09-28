from pydantic import BaseModel

class requestedemp(BaseModel):
    emp_name:str
    emp_department:str
    emp_salary:float

class requestedtask(BaseModel):
    emp_id:int
    task_name:str
    


class requesteduser(BaseModel):
    username:str
    email:str
    password:str

class LoginRequest(BaseModel):
    email:str
    password:str


class requestedAssigned(BaseModel):
    emp_id:int
    task_name:str
