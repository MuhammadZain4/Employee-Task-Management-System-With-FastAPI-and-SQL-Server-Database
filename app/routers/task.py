from app.services import emp as em
from app.schemas.emp import requestedemp,requestedtask,requestedAssigned
from fastapi import APIRouter,Depends
from app.dependencies.auth import get_current_user
router=APIRouter(
    prefix='/task',
    tags=['Tasks'],
    dependencies=[Depends(get_current_user)]
)

@router.get('/')
def get_every_task():
    return em.get_al_task()

@router.get('/{task_id}')
def get_task_by_ids(task_id:int,current_user:str=Depends(get_current_user)):
    return em.get_tsk_by_id(task_id)

@router.post('/')
def create_newly_task(new:requestedtask,current_user:str=Depends(get_current_user)):
    return em.create_neww_task(new,current_user)

@router.put('/{task_id}')
def update_task_detail(task_id:int,updated:requestedtask,current_user:str=Depends(get_current_user)):
    return em.updte_task(task_id,updated)

@router.delete('/{task_id}')
def delete_tasks(task_id:int,current_user:str=Depends(get_current_user)):
    return em.deletee_task(task_id)

@router.post('/assign')
def assigned_tasks(new:requestedAssigned,current_user:str=Depends(get_current_user)):
    return em.ass_task(new) 