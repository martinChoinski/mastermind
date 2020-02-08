from . import app, db    
from . import views  # For import side-effects of setting up routes.
from .db import init_db

init_db()            # Create initial games table 
