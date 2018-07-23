from app import db
from models import Question


objects = [
    Question(text="Tell me something about yourself."),
    Question(text="Explain how you interact with colleagues."),
    Question(text="Describe a conflict resolution situation you experienced."),
    Question(text="How do you face a situation requiring skills you don’t have?"),
    Question(text="Do you do anything for fun?"),
    Question(text="Describe your working habits.")
]
db.session.add_all(objects)
db.session.commit()