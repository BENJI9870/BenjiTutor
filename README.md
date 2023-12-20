[My Site](http://ec2-54-234-135-128.compute-1.amazonaws.com)


My site is a forum of sorts. Just click on the link. Without an account, you can look at both questions and comments. Everything is dated, and in chronological order. if you want to like, comment, or ask a question, first register as a user. Once done, you will be automatically logged in, and can do as you please. I used Python (flask), HTML, CSS, JavaScript, and as a database SQLAlchamy. Bootstrap was used to make a cleaner look. Unfortunately I was not able to make it as colorful as I would have liked. Even still, it is fully functional and up and running on an amazon Linux server as we speak. 

There were 5 tables used to make the database:

users: id, email, password, first_name, last_name

comment: id, commentor (linked to users.id), question_id (linked to question.id), main_text, datetime

question: id, asker_id (linked to users.id), title, main_text, datetime, subject

likes_questions: id, liker_id (linked to users.id), question_id (linked to question.id)

likes_comment: id, liker_id (linked to user.id), comment_id (linked to commentn.id)







## To run this after disconnecting from ssh:
```bash
tmux new -s flask_session

# run the app
sudo python3 -m AskTheTutor

# detach tmux session
ctrl B + D
```
