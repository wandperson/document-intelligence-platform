# Backend
from fastapi.templating import Jinja2Templates

# Custom
from app.core.config import MAIN_DIR


templates = Jinja2Templates(directory=MAIN_DIR / "templates")
