from app import create_app, db, celery
from app.models import User, Question, Video, Submission


app = create_app()
app.app_context().push()


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db, 
        'User': User, 
        'Question': Question, 
        'Video': Video, 
        'Submission': Submission,
        }
