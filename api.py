from flask import Flask

app = Flask(__name__)

@app.route("/")
def welcome():
    return "<p>Welcome to my collection of api tools :)</p>"

@app.route('/print_arg/<arf>', methods=['GET'])
def do_arg_stuff(arf):
    return f"<p>{arf}</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)