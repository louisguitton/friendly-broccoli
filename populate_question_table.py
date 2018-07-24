from app import db
from models import Question


objects = [
    Question(text="Tell me something about yourself.", order_pos=1),
    Question(text="Explain how you interact with colleagues.", order_pos=2),
    Question(text="Describe a conflict resolution situation you experienced.", order_pos=3),
    Question(text="How do you face a situation requiring skills you don’t have?", order_pos=4),
    Question(text="Do you do anything for fun?", order_pos=5),
    Question(text="Describe your working habits.", order_pos=6)
]
db.session.add_all(objects)
db.session.commit()