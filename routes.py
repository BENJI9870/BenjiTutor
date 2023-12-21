# flask routes
from flask import jsonify, request, redirect
from AskTheTutor import app, db, render_template, session
from AskTheTutor.models import User, Question, LikesQuestion, Comment, LikesComment
from werkzeug.security import generate_password_hash, check_password_hash
import re
from sqlalchemy import func



#################### UI ROUTES ####################

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')

@app.route('/example')
def example():
    return render_template('example.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/question/<int:question_id>')
def question(question_id):

    question = Question.query \
    .join(User, Question.asker_id == User.id) \
    .outerjoin(LikesQuestion, Question.id == LikesQuestion.question_id) \
    .add_columns(
        Question.id, Question.title, Question.main_text, Question.asker_id,
        Question.datetime, Question.subject, User.email,
        func.count(LikesQuestion.id).label('likes_count')
    ) \
    .filter(Question.id == question_id) \
    .group_by(Question.id, User.email) \
    .first()    

    print(question.email.split('@')[0])
    if question is None:
        return render_template('404.html'), 404
    else:
        return render_template('question.html', question=question)

@app.route('/write_question')
def write_question():
    if 'user_id' not in session:
        # redirect to login page
        return redirect('/login')
        
    return render_template('write_question.html')

@app.route('/question_list')
def question_list():
    return render_template('question_list.html')




@app.route('/edit_question/<int:question_id>')
def edit_question(question_id):
    if 'user_id' not in session:
        # redirect to login page
        return redirect('/login')
    

    question = Question.query.filter_by(id=question_id).first()
    if question is None:
        return render_template('404.html'), 404
    

    # now, check if user is the asker of the question
    if question.asker_id != session['user_id']:
        return "You are not the asker of this question. You cannot edit it.", 403
    
    return render_template('edit_question.html', question=question)
    

#################### API ROUTES ####################

@app.route('/api/login', methods=['POST'])
def api_login():
    # get data from post data (json)
    data = request.get_json()
    try:
        email = data['email']
        password = data['password']

        if (email == "" or password == ""):
            return jsonify({
                "success": False,
                "message": "Something is empty"
            })
        exists = db.session.query(User).filter_by(email=email).first()
      
        if (not exists):
            return jsonify({
                "success": False,
                "message": "Email doesn't exist"
            })
        
        if exists.email == email.lower() and check_password_hash(exists.password, password):
            session['user_id'] = exists.id
            return jsonify({
                'success': True,
            })
        else:
            return jsonify({
                "success": False,
                "message": "Email or Password is incorrect"
        })
        

    except KeyError:
        return jsonify({
            "success": False,
            "message": "Missing required field"
        })

    # TODO: do some stuff with the data to log the user in
    # for now, just return an error message.
    return jsonify({
        "success": False,
       "message": "Not yet implemented"
    })

@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json()
    try:
        first_name = data['firstName']
        last_name = data['lastName']
        email = data['email']
        password = data['password']
        confirm_password = data['confirmPassword']


        if (first_name == "" or last_name == "" or email == "" or password == "" or confirm_password == ""):
            return jsonify({
                "success": False,
                "message": "Something is empty"
            })
        
        if (password != confirm_password):
            return jsonify({
                "success": False,
                "message": "Passwords don't match"
            })
        

        exists = db.session.query(User.id).filter_by(email=email.lower()).first() is not None

        if (exists):
            return jsonify({
                "success": False,
                "message": "Email already exists"
            })
        
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if (not re.search(email_regex, email)):
            return jsonify({
                "success": False,
                "message": "Invalid email"
            })
        if (len(password) < 8):
            return jsonify({
                "success": False,
                "message": "Password must be at least 8 characters"
            })
        if (not any(char.isdigit() for char in password)):
            return jsonify({
                "success": False,
                "message": "Password must contain a number"
            })
        if (not any(char.isupper() for char in password)):
            return jsonify({
                "success": False,
                "message": "Password must contain an uppercase letter"
            })

        hashed_pass = generate_password_hash(password)

        new_user = User(first_name=first_name,
                    last_name=last_name,
                    email=email.lower(),
                    password=hashed_pass)
        db.session.add(new_user)
        db.session.commit()
        #created new user, tells frontend
        session['user_id'] = new_user.id
        return jsonify({
            "success": True
    
        })

    except KeyError:
        return jsonify({
            "success": False,
            "message": "Missing required field"
        })




@app.route('/test/loggedin')
def api_loggedIn():
    if 'user_id' in session:
      user = db.session.query(User).filter_by(id=session['user_id']).first()
      return jsonify({
        'user':{
            'id': user.id,
            'firstName': user.first_name,
            'lastName': user.last_name,
            'email': user.email
            },
        }
      )
    else:
        return jsonify({
            'user': None
        })
@app.route('/api/home')
def api_home():
    if 'user_id' in session:
        user = db.session.query(User).filter_by(id=session['user_id']).first()
        return jsonify({
            'user':{
                'id': user.id,
                'firstName': user.first_name,
                'lastName': user.last_name,
                'email': user.email
                },
            }
        )
    else:
        return jsonify({
            'user': None
        })

@app.route('/api/write_question', methods=['POST'])
def api_question():
    if 'user_id' in session:
        data = request.get_json()
        try:
            title = data['title']
            main_text = data['main_text']
            subject = data['subject']

            if (title == "" or subject == ""):
                return jsonify({
                    "success": False,
                    "message": "Something is empty"
                })
            new_question = Question(title=title, main_text=main_text, subject=subject, asker_id=session['user_id'])
            db.session.add(new_question)
            db.session.commit()
            return jsonify({
                'success': True
            })
        except KeyError:
            return jsonify({
                "success": False,
                "message": "Missing required field"
            })
        
    else:
        return jsonify({
            "success": False,
            'message': "Not logged in"
        })

@app.route('/api/question_list')
def api_question_list():

    data = Question.query \
    .join(User, Question.asker_id == User.id) \
    .outerjoin(LikesQuestion, Question.id == LikesQuestion.question_id) \
    .add_columns(
        Question.id, Question.title, Question.main_text, Question.asker_id,
        Question.datetime, Question.subject, User.email,
        func.count(LikesQuestion.id).label('likes_count')
    ) \
    .group_by(Question.id, User.email) \
    .order_by(Question.datetime.desc()) \
    .all()

# Convert data to json
    json_data = []
    for row in data:
        json_data.append({
            'id': row.id,
            'title': row.title,
            'mainText': row.main_text,
            'askerID': row.asker_id,
            'datetime': row.datetime,
            'subject': row.subject,
            'username': row.email.split('@')[0],
            'likesCount': row.likes_count
        })

    return jsonify(json_data)

@app.route('/api/like_question', methods=['POST'])
def api_like_question():
    if 'user_id' in session:
        data = request.get_json()
        try:
            question_id = data['question_id']
            exists = db.session.query(LikesQuestion.id).filter_by(question_id=question_id, liker_id=session['user_id']).first() is not None
            if (exists):
                # delete like
                like = db.session.query(LikesQuestion).filter_by(question_id=question_id, liker_id=session['user_id']).first()
                if like:
                    db.session.delete(like)
                    db.session.commit()                
                    return jsonify({
                    "success": True,
                    "action": "unlike"
                })
            new_like = LikesQuestion(question_id=question_id, liker_id=session['user_id'])
            db.session.add(new_like)
            db.session.commit()
            return jsonify({
                'success': True,
                'action': 'like'
            })
        except KeyError:
            return jsonify({
                "success": False,
                "message": "Missing required field"
            })
        
    else:
        return jsonify({
            "success": False,
            'message': "Not logged in"
        })



@app.route('/api/like_comment', methods=['POST'])
def api_like_comment():
    if 'user_id' in session:
        data = request.get_json()
        try:
            comment_id = data['comment_id']
            exists = db.session.query(LikesComment.id).filter_by(comment_id=comment_id, liker_id=session['user_id']).first() is not None
            if (exists):
                # delete like
                like = db.session.query(LikesComment).filter_by(comment_id=comment_id, liker_id=session['user_id']).first()
                if like:
                    db.session.delete(like)
                    db.session.commit()                
                    return jsonify({
                    "success": True,
                    "action": "unlike"
                })
            new_like = LikesComment(comment_id=comment_id, liker_id=session['user_id'])
            db.session.add(new_like)
            db.session.commit()
            return jsonify({
                'success': True,
                'action': 'like'
            })
        except KeyError:
            return jsonify({
                "success": False,
                "message": "Missing required field"
            })
        
    else:
        return jsonify({
            "success": False,
            'message': "Not logged in"
        })
    

@app.route('/api/new_comment', methods=['POST'])
def api_comment():
    if 'user_id' in session:
        data = request.get_json()
        try:
            main_text = data['comment_text']
            question_id = data['question_id']

            if (main_text == "" or question_id == ""):
                return jsonify({
                    "success": False,
                    "message": "Something is empty"
                })
            new_comment = Comment(main_text=main_text, question_id=question_id, commentor_id=session['user_id'])
            db.session.add(new_comment)
            db.session.commit()
            return jsonify({
                'success': True
            })
        except KeyError:
            return jsonify({
                "success": False,
                "message": "Missing required field"
            })
        
    else:
        return jsonify({
            "success": False,
            'message': "Not logged in"
        })
    
@app.route('/api/get_comments', methods=['POST'])
def api_get_comments():
    data = request.get_json()
    try:
        question_id = data['question_id']
    except KeyError:
        return jsonify({
            "success": False,
            "message": "Missing required field"
        })
    

    data = Comment.query \
    .join(User, Comment.commentor_id == User.id) \
    .outerjoin(LikesComment, Comment.id == LikesComment.comment_id) \
    .filter(Comment.question_id == question_id) \
    .add_columns(
        Comment.id, Comment.main_text, Comment.commentor_id,
        Comment.datetime, User.email,
        func.count(LikesComment.id).label('likes_count')
    ) \
    .group_by(Comment.id, User.email) \
    .order_by(Comment.datetime.desc()) \
    .all()

# Convert data to json
    json_data = []
    for row in data:
        json_data.append({
            'id': row.id,
            'mainText': row.main_text,
            'commentorID': row.commentor_id,
            'datetime': row.datetime,
            'username': row.email.split('@')[0],
            'likesCount': row.likes_count
        })

    return jsonify(json_data)

@app.route('/api/is_logged_in', methods=['GET'])
def api_is_logged_in():
    if 'user_id' in session:
        return jsonify({
            'success': True
        })
    else:
        return jsonify({
            'success': False
        })
    
@app.route('/api/edit_question', methods=['POST'])
def api_edit_question():
    if 'user_id' in session:
        data = request.get_json()
        try:
            question_id = data.get('question_id')
            title = data['title']
            main_text = data['main_text']
            subject = data['subject']

            if (title == "" or subject == ""):
                return jsonify({
                    "success": False,
                    "message": "Something is empty"
                })
            if question_id:
                # Update existing question
                question = Question.query.get(question_id)
                if question and question.asker_id == session['user_id']:
                    question.title = title
                    question.main_text = main_text
                    question.subject = subject
                else:
                    return jsonify({"success": False, "message": "Question not found or unauthorized"})
            else:
                return jsonify({"success": False, "message": "Question ID not provided"})
                
            db.session.commit()
            return jsonify({
                'success': True
            })
        except KeyError:
            return jsonify({
                "success": False,
                "message": "Missing required field"
            })
        
    else:
        return jsonify({
            "success": False,
            'message': "Not logged in"
        })
    



@app.route('/api/delete_question', methods=['POST'])
def delete_question():
    if 'user_id' in session:
        data = request.get_json()
        try:
            question_id = data['question_id']
            question = Question.query.get(question_id)
            if question and question.asker_id == session['user_id']:

                # delete all likes on this question
                likes = LikesQuestion.query.filter_by(question_id=question_id).all()
                for like in likes:
                    db.session.delete(like)

                # delete all comments on this question
                comments = Comment.query.filter_by(question_id=question_id).all()
                for comment in comments:
                    # delete all likes on this comment
                    likes = LikesComment.query.filter_by(comment_id=comment.id).all()
                    for like in likes:
                        db.session.delete(like)
                    db.session.delete(comment)




                db.session.delete(question)
                db.session.commit()
                return jsonify({
                    'success': True
                })
            else:
                return jsonify({"success": False, "message": "Question not found or unauthorized"})
        except KeyError:
            return jsonify({
                "success": False,
                "message": "Missing required field"
            })
        
    else:
        return jsonify({
            "success": False,
            'message': "Not logged in"
        })