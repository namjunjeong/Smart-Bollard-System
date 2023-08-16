from flask import Flask

app = Flask(__name__)

@app.route('/finish')
def curl():
    print("finished")
    print("finished")
    print("finished")
    print("finished")
    return f'aaa'

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 8000)