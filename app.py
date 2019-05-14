import os

from flask import render_template, Flask
import tapingo

app = Flask(__name__)


@app.route('/')
def home():
    food = tapingo.current_wait_times()
    for i in range(0, len(food)):
        food[i].append("style" + str((i % 6) + 1))

    return render_template("tapingoTemplate.html", food=food)


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))