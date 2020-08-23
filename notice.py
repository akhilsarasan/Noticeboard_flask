from flask import Flask,render_template,redirect,request
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
app =Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db=SQLAlchemy(app)

class Message(db.Model):
    mid = db.Column(db.Integer,primary_key=True)
    content = db.Column(db.String(200), nullable =False)
    date_created = db.Column(db.DateTime,default=datetime.utcnow)
    def __repr__(self):
        return '<Message %r>'%self.id
db.create_all()


@app.route("/")
def base():
    return render_template('base.html')

@app.route("/home/",methods= ['POST','GET'])
def index():

    if request.method =='POST':
        mesge_content = request.form['content']
        new_mesge =Message(content= mesge_content)
        try:
            db.session.add(new_mesge)
            db.session.commit()
            return redirect("/home")
        except :
            return "error"
    else:
        messages=Message.query.order_by(Message.date_created).all()
        return render_template("index.html",messages=messages)


@app.route('/delete/<int:mid>')
def delete(mid):
    message_to_delete = Message.query.get_or_404(mid)
    try:
        db.session.delete(message_to_delete)
        db.session.commit()
        return redirect("/home/")
    except:
        return "error"



@app.route('/update/<int:mid>',methods=['POST','GET'])
def update(mid):

    msge = Message.query.get_or_404(mid)
    if request.method == 'POST':
        msge.content = request.form['content']
        try:
            db.session.commit()
            return redirect("/home/")
        except:
            return "error"
    else:
        return render_template('edit.html',msge=msge)


@app.route('/draft/<int:mid>',methods=['POST','GET'])
def saved():
    if request.method =='POST':
        mesge_content = request.form['con']
        new_mesge =Message(content= mesge_content)
        try:
            db.session.add(new_mesge)
            db.session.commit()
            return redirect("/home")
        except :
            return "error"
    else:
        messages=Message.query.order_by(Message.date_created).all()
        return render_template("draft.html",messages=messages)



if __name__ == "__main__":
    app.debug =True
    app.run()
