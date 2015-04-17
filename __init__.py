from flask import Flask, render_template
import BDFuntions as bd

app = Flask(__name__, template_folder=".")

@app.route("/")
def mapview():
    # creating a map in the view
    print(bd.login('helmetk','topo'))
    print(bd.login('helmetk','sadf'))
    return render_template('templates/map.html')

if __name__ == "__main__":
    app.run(debug=True)
