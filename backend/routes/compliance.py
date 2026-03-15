from fastapi import APIRouter
from schemas.project_schema import ProjectCreate
from datetime import date
from services.compliance_engine import check_deadline_status
from services.report_generator import generate_report
from fastapi import UploadFile, File
import shutil
from ai_modules.regulation_parser import extract_compliance_rules
from ai_modules.risk_prediction import predict_risk
from database import SessionLocal
from models.project import Project
from models.task import Task
from schemas.task_schema import TaskCreate, TaskUpdate
from models.report import Report
from services.notification_services import send_email_alert
from fastapi.responses import FileResponse
from datetime import date, timedelta
import random




router = APIRouter()


# Create Project

@router.post("/create_project")
def create_project(project: ProjectCreate):

    db = SessionLocal()

    new_project = Project(
        #project_id=project.project_id,
        name=project.name,
        location=project.location,
        owner=project.owner,
        start_date=project.start_date
    )

    db.add(new_project)
    db.commit()
    db.close()

    return {"message": "Project stored in database"}




# View Projects

@router.get("/projects")
def get_projects():

    db = SessionLocal()

    data = db.query(Project).all()

    db.close()

    return data




# Create Compliance Task

@router.post("/create_task")
def create_task(task: TaskCreate):

    db = SessionLocal()

    new_task = Task(
        project_id=task.project_id,
        compliance_type=task.compliance_type,
        deadline=task.deadline,
        status=task.status
    )

    db.add(new_task)
    db.commit()
    db.close()

    return {"message": "Task created"}





# View All Compliance Tasks

@router.get("/tasks/{project_id}")
def get_tasks(project_id: int):

    db = SessionLocal()

    tasks = db.query(Task).filter(Task.project_id == project_id).all()

    db.close()

    return tasks



@router.get("/task_status")
def get_task_status():

    db = SessionLocal()

    tasks = db.query(Task).all()

    result = []
    overdue_tasks_list = []

    for task in tasks:

        status = check_deadline_status(task.deadline)

        result.append({
            "task_id": task.task_id,
            "project_id": task.project_id,
            "compliance_type": task.compliance_type,
            "deadline": task.deadline,
            "status": status
        })

        if status == "OVERDUE":
            overdue_tasks_list.append(task.compliance_type)

    # Send ONE summary email instead of multiple emails
    if overdue_tasks_list:

        message = "Compliance Alert\n\nThe following tasks are overdue:\n\n"

        for t in overdue_tasks_list:
            message += f"- {t}\n"

        send_email_alert(message)

    db.close()

    return result



@router.put("/update_task_status/{task_id}")
def update_task_status(task_id: int, data: TaskUpdate):

    db = SessionLocal()

    task = db.query(Task).filter(Task.task_id == task_id).first()

    if task:
        task.status = data.status # type: ignore
        db.commit()

    db.close()

    return {"message": "Task status updated"}




@router.get("/generate_report/{project_id}")
def generate_project_report(project_id: int):

    db = SessionLocal()

    project = db.query(Project).filter(Project.project_id == project_id).first()

    if not project:
      db.close()
      return {"error": "Project not found"}

    tasks = db.query(Task).filter(Task.project_id == project_id).all()

    task_list = []

    for task in tasks:

        status = check_deadline_status(task.deadline)

        task_list.append({
            "compliance_type": task.compliance_type,
            "deadline": task.deadline,
            "status": status
        })

    file_path = generate_report(project.name, task_list)

    report = Report(
        project_id = project_id,
        report_path = file_path
    )

    db.add(report)
    db.commit()
    db.close()

    return FileResponse(
        path=file_path,
        filename="compliance_report.pdf",
        media_type="application/pdf"
    )




@router.get("/reports/{project_id}")
def get_reports(project_id: int):

    db = SessionLocal()

    reports = db.query(Report).filter(Report.project_id == project_id).all()

    db.close()

    return reports





@router.post("/upload_regulation/{project_id}")
def upload_regulation(project_id: int, file: UploadFile = File(...)):

    db = SessionLocal()

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    rules = extract_compliance_rules(file_path)

    created_tasks = []

    for rule in rules:

        new_task = Task(
            project_id=project_id,
            compliance_type=rule,
            deadline = date.today() + timedelta(days=random.randint(-3,10)),
            status="Pending"
        )

        db.add(new_task)

        created_tasks.append(rule)

    db.commit()
    db.close()

    return {
        "message": "Regulation processed",
        "tasks_created": created_tasks
    }




@router.get("/risk_prediction/{project_id}")
def risk_prediction(project_id: int):

    db = SessionLocal()

    tasks = db.query(Task).filter(Task.project_id == project_id).all()

    total = 0
    overdue = 0
    due_soon = 0

    for task in tasks:

        total += 1

        status = check_deadline_status(task.deadline)

        if status == "OVERDUE":
            overdue += 1

        if status == "DUE_SOON":
            due_soon += 1

    risk = predict_risk(total, overdue, due_soon)

    db.close()

    return {
        "project_id": project_id,
        "total_tasks": total,
        "overdue": overdue,
        "due_soon": due_soon,
        "risk_level": risk
    }





@router.get("/dashboard")
def dashboard():

    db = SessionLocal()

    projects = db.query(Project).all()
    tasks = db.query(Task).all()

    dashboard_data = []

    for project in projects:

        total = 0
        overdue = 0
        due_soon = 0

        for task in tasks:

            if task.project_id == project.project_id:  # type: ignore

                total += 1

                status = check_deadline_status(task.deadline)

                if status == "OVERDUE":
                    overdue += 1

                if status == "DUE_SOON":
                    due_soon += 1

        risk = predict_risk(total, overdue, due_soon)

        dashboard_data.append({
            "project_id": project.project_id,
            "project_name": project.name,
            "location": project.location,
            "total_tasks": total,
            "overdue_tasks": overdue,
            "due_soon_tasks": due_soon,
            "risk_level": risk
        })

    db.close()

    return dashboard_data





@router.get("/bottleneck_analysis/{project_id}")
def bottleneck_analysis(project_id: int):

    db = SessionLocal()

    tasks = db.query(Task).filter(Task.project_id == project_id).all()

    total_tasks = len(tasks)

    overdue = 0
    due_soon = 0

    for task in tasks:

        status = check_deadline_status(task.deadline)

        if status == "OVERDUE":
            overdue += 1

        if status == "DUE_SOON":
            due_soon += 1

    # calculate delay ratio
    ratio = overdue / total_tasks if total_tasks > 0 else 0

    # determine bottleneck severity
    if ratio > 0.5:
        level = "CRITICAL BOTTLENECK"

    elif ratio > 0.2:
        level = "WARNING"

    else:
        level = "NORMAL"

    db.close()

    return {
        "project_id": project_id,
        "total_tasks": total_tasks,
        "overdue_tasks": overdue,
        "due_soon_tasks": due_soon,
        "delay_ratio": ratio,
        "bottleneck_level": level
    }




@router.get("/alerts")
def get_alerts():

    db = SessionLocal()

    tasks = db.query(Task).all()

    alerts = []

    for task in tasks:

        status = check_deadline_status(task.deadline)

        if status == "OVERDUE":

            alerts.append({
                "type": "OVERDUE",
                "task_id": task.task_id,
                "project_id": task.project_id,
                "message": f"Task '{task.compliance_type}' is overdue"
            })

        elif status == "DUE_SOON":

            alerts.append({
                "type": "DUE_SOON",
                "task_id": task.task_id,
                "project_id": task.project_id,
                "message": f"Task '{task.compliance_type}' is due soon"
            })

    db.close()

    return alerts