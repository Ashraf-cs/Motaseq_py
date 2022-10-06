from flask import Blueprint, redirect, url_for
import os, shutil, json
from . import init, ids, classes, set, finish

bp = Blueprint('api', __name__)

bp.register_blueprint(init.bp, url_prefix='/init')
bp.register_blueprint(ids.bp, url_prefix='/ids')
bp.register_blueprint(classes.bp, url_prefix='/classes')
bp.register_blueprint(set.bp, url_prefix='/set')
bp.register_blueprint(finish.bp, url_prefix='/finish')


@bp.route("/check", methods=["GET"])
def check():
  try:
    with open("appData/paths.json", "r", encoding="utf-8") as f:
      data = f.read()
      return data
  except:
    pass


@bp.route("/discard", methods=["POST"])
def discard():
    with open("appData/paths.json", "r", encoding="utf-8") as f:
      paths = json.load(f)
    shutil.copytree("appData/backup", f"{paths['htmlPath']}", dirs_exist_ok=True)
    with open(f"{paths['cssFile']}", "r", encoding="utf-8") as f:
      cssFile = f.read()
    with open(f"{paths['cssFile']}", "w", encoding="utf-8") as f:
      f.write(cssFile[0:cssFile.find("*:hover{border: 1px solid black;}")])
    
    os.remove(f"{paths['cssPath']}/props.json")
    os.remove("appData/paths.json")
    shutil.rmtree("appData/backup")

    return redirect(url_for("index"))