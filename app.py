from flask import Flask,render_template
app = Flask(__name__)

@app.route('/')
def Hello_World():
    return render_template('index.html')
    # return 'Hello, World!'

@app.route('/products')
def Products():
    return 'This is products page'

if __name__ == "__main__":
    app.run(debug = True)
    # app.run(debug = True, port=8000)


    