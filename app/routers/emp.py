from app.services import emp as em
from app.schemas.emp import requestedemp,requestedtask
from fastapi import APIRouter,Depends
from app.dependencies.auth import get_current_user

router=APIRouter(
    prefix='/emp',
    tags=['Employee'],
    dependencies=[Depends(get_current_user)]
)

@router.get('/')
def get_all_employees():
    return em.get_all_emp()

@router.get('/{emp_id}')
def get_employee_by_id(emp_id:int):
    return em.get_emp_id(emp_id)

@router.post('/')
def create_employee(new:requestedemp):
    return em.create_emp(new)

@router.put('/')
def update_employees(emp_id:int,update:requestedemp,current_user:str=Depends(get_current_user)):
    return em.upd_emp(emp_id,update)

@router.delete('/{emp_id}')
def delete_employee(emp_id:int,current_user:str=Depends(get_current_user)):
    return em.del_emp(emp_id)