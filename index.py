from flask import Flask,redirect,url_for,request,render_template
from wtforms import StringField,Form
import random,string
from wtforms import Form,StringField
from flask_mysqldb import MySQL

app=Flask(__name__)
app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]="root"
app.config["MYSQL_DB"]="urlshortner"
app.config["MYSQL_CURSOR"]="DictCursor"

url_mapper_list=[]
map={}
mysql=MySQL(app)



class UrlForm(Form):
    url=StringField('Enter URl')



@app.route('/')
def index():
    return "mohit"

@app.route('/shortner/',methods=['GET','POST'])
def shortner():
    form=UrlForm(request.form)
    if request.method=='POST' and form.validate():
        userurl=form.url.data
        final=""
        length=7
        char=string.digits+string.ascii_uppercase+string.ascii_lowercase
        for _ in range(length):
            final+=random.choice(char)
        map[final]=userurl
        cur=mysql.connection.cursor()
        result=cur.execute("SELECT * FROM shortner WHERE url='{0}'".format(userurl))
        if result>0:
            data=cur.fetchone()
            return "<h1> this  url already exist and url is <br><i style='color:red'>localhost:5000/url/"+str(data[1])+"</i></h1>"
        result=cur.execute("INSERT INTO shortner(compress,url) VALUE(%s,%s)",(final,userurl))
        mysql.connection.commit()
        cur.close()
        url_='localhost:5000/url/'+final
        return render_template("results.html",url=url_)
    return render_template("urlshortner.html",form=form)

@app.route('/url/<string:cid>')
def redirecturl(cid):
    cur=mysql.connection.cursor()
    result=cur.execute("SELECT url FROM shortner WHERE compress='{0}'".format(cid))
    if result>0:
        url=cur.fetchone()
        return redirect(url[0])
    else:
        return "NO SUCH link exists"



if __name__=='__main__':
    app.run(debug=True)







