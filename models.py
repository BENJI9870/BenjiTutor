from AskTheTutor import db 
from sqlalchemy.dialects.postgresql import ENUM

class User(db.Model):

    # By default, SQLAlchemy assumes that the table name is the lowercase version of the class name. But this is not always the case.
    # if tablename is not lowercase version of class name, specify tablename like so:
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.VARCHAR(100), nullable=False)
    email = db.Column(db.VARCHAR(100), unique=True, nullable=False)
    last_name = db.Column(db.VARCHAR(100), nullable=False)
    password = db.Column(db.VARCHAR(250), nullable=False)

    # this is a method that will be called when we print a User object
    # it's here so that we can see the contents of the object. It's not necessary and not meant to be used in the frontend
    def __repr__(self):
        return f"User('{self.first_name}', '{self.last_name}', '{self.email}')"
    

class Question(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.VARCHAR(250), nullable=False)
    main_text = db.Column(db.Text, nullable=False)
    asker_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    datetime = db.Column(db.TIMESTAMP, nullable=False, default=db.func.current_timestamp())
    subject = db.Column(ENUM("history", "math", "science", "english", "other", name="subject"), nullable=False)

    

    def __repr__(self):
        return f"Question('{self.title}', '{self.body}', '{self.user_id}')"


class LikesQuestion(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    liker_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"LikesQuestion('{self.question_id}', '{self.liker_id}')"

class Comment(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    commentor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    main_text = db.Column(db.Text, nullable=False)
    datetime = db.Column(db.TIMESTAMP, nullable=False, default=db.func.current_timestamp())

    def __repr__(self):
        return f"Comment('{self.question_id}', '{self.commenter_id}', '{self.main_text}')"

class LikesComment(db.Model):
    
        id = db.Column(db.Integer, primary_key=True)
        comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=False)
        liker_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
        def __repr__(self):
            return f"LikesComment('{self.comment_id}', '{self.liker_id}')"