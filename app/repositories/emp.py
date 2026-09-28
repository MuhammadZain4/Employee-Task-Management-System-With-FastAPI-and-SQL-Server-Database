from sqlalchemy import text
from app.core.database import engine
from app.schemas.emp import requestedemp,requestedtask,requestedAssigned
def get_emp():
    with engine.connect() as conn:
        result=conn.execute(text("""exec sp_get_all_employee
                                """
                                ),
                            )
        res=result.mappings().all()
    return res

def get_emp_by_id(emp_id:int):
    with engine.connect() as conn:
        result=conn.execute(text("""exec sp_get_employee_by_id
                                    @emp_id=:emp_id
                                """),
                                {
                                    'emp_id':emp_id
                                }
                            )
        res=result.mappings().all()
    return res

def update_emp(emp_id:int,updated:requestedemp):
    with engine.connect() as conn:
        result=conn.execute(text("""exec sp_update_employee
                                    @emp_id=:emp_id,
                                    @emp_name=:emp_name,
                                    @emp_department=:emp_department,
                                    @emp_salary=:emp_salary
                                    """
                                ),
                                {
                                    "emp_id":emp_id,
                                    "emp_name":updated.emp_name,
                                    "emp_department":updated.emp_department,
                                    "emp_salary":updated.emp_salary
                                }
        )
        conn.commit()
        return{"message":"updated employee successfully"}

def delete_emp(emp_id:int):
    with engine.connect() as conn:
        result=conn.execute(text("""exec sp_delete_empl
                                    @emp_id=:emp_id
                                """),
                                {
                                    "emp_id":emp_id
                                }
        )
        conn.commit()
        return{"message":"employe deleted successfully"}

def create_new_emp(new:requestedemp):
    with engine.connect() as conn:
        result=conn.execute(text("""exec sp_create_employee
                                    @emp_name=:emp_name,
                                    @emp_department=:emp_department,
                                    @emp_salary=:emp_salary
                                    """
                                ),
                                {
                                    "emp_name":new.emp_name,
                                    "emp_department":new.emp_department,
                                    "emp_salary":new.emp_salary
                                })
        conn.commit()
        return {"message":"created employee successfully"}

def get_tasks():
    with engine.connect() as conn:
        result=conn.execute(text("""exec sp_get_all_task""")
        )
        re=result.mappings().all()
    return re

def get_id(task_id:int):
    with engine.connect() as conn:
        result=conn.execute(text("""exec sp_get_by_id
                                    @task_id=:task_id
                                """),
                                {
                                    "task_id":task_id
                                }
        )
        re=result.mappings().all()
    return re

def upd_task(task_id:int,update:requestedtask):
    with engine.connect() as conn:
        result=conn.execute(text("""exec sp_update_task
                                    @task_id=:task_id,
                                    @task_name=:task_name,
                                    @emp_id=:emp_id
                                """
                                ),
                                {
                                    "task_id":task_id,
                                    "task_name":update.task_name,
                                    "emp_id":update.emp_id
                                }
        )
        conn.commit()
        return{"message":"update task successfully"}

def create_new_task(emp_id:int,new:requestedtask):
    with engine.connect() as conn:
        result=conn.execute(text("""exec sp_create_task
                                    @emp_id=:emp_id,
                                    @task_name=:task_name
                                """
                                ),
                                {
                                    "emp_id":emp_id,
                                    "task_name":new.task_name
                                }
        )
        conn.commit()
        return{"message":"task created successfully"}


def delet_task(task_id:int):
    with engine.connect() as conn:
        result=conn.execute(text("""exec sp_delete_task
                                    @task_id=:task_id
                                """),
                                {
                                    "task_id":task_id
                                }
        )
        conn.commit()
        return{"message":"delete task successfully"}



def assign_task(new:requestedAssigned):
    with engine.connect() as conn:
        conn.execute(text("""exec sp_assign_task_to_emp
                                    @emp_id=:emp_id,
                                    @task_name=:task_name
                                """
                                ),
                                {
                                    "emp_id":new.emp_id,
                                    "task_name":new.task_name
                                }
        )
        conn.commit()
        return{"message":"assigned task to employee successfully"}