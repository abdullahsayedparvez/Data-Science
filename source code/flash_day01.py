import flask
from flask import Flask
app = Flask(__name__)  # it return  <Flask '__main__'>



# what you want to show on website
@app.route("/")
def welcome():
    return "<h1>Welcome to Stock Prediction</h2>"
# print(app.route("/hello"))


# what you want to show on website
@app.route("/home")
def home():
    return "<h1>Home page hai bhai</h2>"
# print(app.route("/hello"))



# what you want to show on website
@app.route("/about")
def about():
    return "<h1>Aspiring Data Scienece</h2>"
# print(app.route("/hello"))


# it is use when you refresh the page it will show the new website look
if __name__ == "__main__":
    app.run(debug=True)

