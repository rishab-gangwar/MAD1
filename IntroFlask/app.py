from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def hello_world():
    if request.method == "GET":
        return render_template("get_info.html")
    else:
        name = request.form["name"]
        return render_template("display_info.html", display_name=name)


if __name__ == '__main__':
    app.debug = True
    app.run()
