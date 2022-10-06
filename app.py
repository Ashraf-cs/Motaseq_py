from flask import Flask, render_template
import json

from api.api import bp

app = Flask(__name__)

# ---------------- APIs ----------------

app.register_blueprint(bp, url_prefix='/api')


# ---------------- Pages ----------------

@app.route("/", methods=["GET"])
def index():
  try:
    with open("appData/paths.json", "r", encoding="utf-8") as f:
      paths = json.load(f)
      if paths['htmlPath']:
        return render_template("index.html", file=True)
  except:
    return render_template("index.html", file=False)


@app.route("/styler", methods=["GET"])
def styler():
  return render_template("styler.html")
