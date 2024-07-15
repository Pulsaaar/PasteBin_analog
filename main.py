from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles
import models, schemas, database

app = FastAPI()

# Подключение статики
app.mount("/static", StaticFiles(directory="static"), name="static")

# Инициализация шаблонов
templates = Jinja2Templates(directory="templates")

# Создание таблиц
models.Base.metadata.create_all(bind=database.engine)

# Приветственное сообщение на домашней странице
@app.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(database.get_db)):
    # Получаем последние добавленные пасты для отображения на домашней странице
    db_pastes = db.query(models.Paste).order_by(models.Paste.id.desc()).limit(5).all()
    return templates.TemplateResponse("home.html", {"request": request, "pastes": db_pastes})

@app.get("/create", response_class=HTMLResponse)
def create_paste_form(request: Request):
    return templates.TemplateResponse("create_paste.html", {"request": request})

@app.post("/pastes/", response_class=HTMLResponse)
def create_paste(request: Request, title: str = Form(...), content: str = Form(...), db: Session = Depends(database.get_db)):
    db_paste = models.Paste(title=title, content=content)
    db.add(db_paste)
    db.commit()
    db.refresh(db_paste)
    return templates.TemplateResponse("view_paste.html", {"request": request, "paste": db_paste})

@app.get("/pastes/{paste_id}", response_class=HTMLResponse)
def read_paste(request: Request, paste_id: int, db: Session = Depends(database.get_db)):
    db_paste = db.query(models.Paste).filter(models.Paste.id == paste_id).first()
    if db_paste is None:
        raise HTTPException(status_code=404, detail="Paste not found")
    return templates.TemplateResponse("view_paste.html", {"request": request, "paste": db_paste})

@app.get("/pastes", response_class=HTMLResponse)
def list_pastes(request: Request, db: Session = Depends(database.get_db)):
    db_pastes = db.query(models.Paste).all()
    return templates.TemplateResponse("list_pastes.html", {"request": request, "pastes": db_pastes})
