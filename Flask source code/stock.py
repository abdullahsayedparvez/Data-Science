from flask import Flask , render_template , request , redirect , url_for
app = Flask(__name__)
@app.route('/')   # Variable rule--> <int:score>
def homepage():
    return render_template('stock_market_frontend_main.html')

if __name__ == '__main__':
    app.run(debug=True,port=8000)  