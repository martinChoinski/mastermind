# print("run app.py")
# Entry point for the application.
from . import app    # For application discovery by the 'flask' command.
# print(f'__name__ = ({__name__})')
from . import views  # For import side-effects of setting up routes.

