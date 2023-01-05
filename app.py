from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#  Flask環境準備
app = Flask(__name__)

# SQL設定
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

# クラスでテーブルを定義
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    detail = db.Column(db.String(100))
    due = db.Column(db.DateTime, nullable=False)

# タスク一覧の表示とDB保存を行う
@app.route("/", methods=['GET', 'POST'])
def index():
    # GETリクエストだった場合はDBのタスク一覧を返す
    if request.method == 'GET':
        posts = Post.query.all()
        return render_template('index.html', posts=posts)
    # POSTリクエストの場合はデータをDBに保存する
    else:
        title = request.form.get('title')
        detail = request.form.get('detail')
        due = request.form.get('due')
        limit = datetime.strptime(due, '%Y-%m-%d')
        
        # データをDBに保存する
        new_post = Post(title=title, detail=detail, due=limit)
        db.session.add(new_post)
        db.session.commit()
        
        return redirect('/')
        
# 投稿フォーム
@app.route("/create")
def create():
    return render_template('create.html')

# 投稿を削除する
@app.route('/delete/<int:id>')
def delete(id):
    post = Post.query.get(id)
    
    # データを削除する
    db.session.delete(post)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)