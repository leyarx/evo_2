from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    
    def __init__(self, name):
        self.name = name
        
    def __repr__(self):
        return '<User %r>' % self.name

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/users', methods=['POST', 'GET'])
def handle_users():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            if 'name' in data:
                name = data['name']
                if db.session.query(User.id).filter_by(name=name).first() is not None:
                    return {"user": name}
                new_user = User(name)
                db.session.add(new_user)
                db.session.commit()
                return {"user": new_user.name}, 201
            else:
                return {"error": "Key 'name' is not found"}
        else:
            return {"error": "The request payload is not in JSON format"}

    elif request.method == 'GET':
        users = User.query.all()
        result = [
            {
                "name": user.name,
            } for user in users]

        return {"count": len(result), "users": result}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port = port)