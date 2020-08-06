from flask import Flask, render_template, url_for
from flask_bootstrap import Bootstrap


app = Flask(__name__)
Bootstrap(app)


@app.route('/', methods=['GET','POST'])
def home():
    return render_template('exp.html')


@app.route('/exp', methods=['GET','POST'])
def exp():
    return render_template('exp.html')


@app.route('/edu', methods=['GET','POST'])
def edu():
    return render_template('edu.html')


@app.route('/skills', methods=['GET','POST'])
def skills():
    return render_template('skills.html')


@app.route('/proj', methods=['GET','POST'])
def proj():
    return render_template('exp.html')




if __name__=='__main__':
    app.run(debug='True',
            port=2000)