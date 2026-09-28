from app.repositories import emp as e
from app.repositories import users as u
from app.schemas.emp import requestedemp,requestedtask,requestedAssigned
from fastapi import HTTPException
from app.repositories.users import get_email
def get_all_emp():
    return e.get_emp()

def get_emp_id(emp_id:int):
    exist=e.get_emp_by_id(emp_id)
    if not exist:
        raise HTTPException(status_code=404,detail="id not found")
    return exist

def upd_emp(emp_id:int,updated:requestedemp):
    exist=e.get_emp_by_id(emp_id)
    if not exist:
        raise HTTPException(status_code=404,detail="employee not found")
    return e.update_emp(emp_id,updated)


def create_emp(new:requestedemp):
    return e.create_new_emp(new)


def del_emp(emp_id:int):
    exist=e.get_emp_by_id(emp_id)
    if not exist:
        raise HTTPException(status_code=404,detail="employee not found")
    return e.delete_emp(emp_id)


def create_neww_task(new: requestedtask, current_user_email: str):
    user = u.get_email(current_user_email)
    if not user:
        raise HTTPException(status_code=404, detail="employee not found")
    return e.create_new_task(user['emp_id'], new)

def get_al_task():
    return e.get_tasks()

def get_tsk_by_id(task_id:int):
    res=e.get_id(task_id)
    if not res:
        raise HTTPException(status_code=404,detail="id not found")
    return res

def updte_task(task_id:int,update:requestedtask):
    existed=e.get_id(task_id)
    if not existed:
            raise HTTPException(status_code=404,detail="task not found")
    return e.upd_task(task_id,update)

def deletee_task(task_id):
    result=e.get_id(task_id)
    if not result:
        raise HTTPException(status_code=404,detail="task not found")
    return e.delet_task(task_id)


def ass_task(new:requestedAssigned):
    user=e.get_emp_by_id(new.emp_id)
    if not user:
        raise HTTPException(status_code=404,detail="employee not found")
    return e.assign_task(new)