from flask import Blueprint, request
import os, re


bp = Blueprint('ids', __name__)

@bp.route("/setID", methods=["POST"])
def setID():
    for file in os.scandir(request.form['htmlPath']):
        if file.name.endswith("js") or file.name.endswith("jsx") or file.name.endswith("html"):
            with open(f"{request.form['htmlPath']}\\{file.name}", "r", encoding="utf-8") as f:
                pageFile = f.read()

            match = ""
            try:
              match = re.findall("data-id=[0-9\'\"]*", request.form['element'])[0]
              # match = match.replace(/"/g, "'")
              setId = pageFile.replace(match, match + f' id="{request.form["id"]}"')
              with open(f"{request.form['htmlPath']}\\{file.name}", "w", encoding="utf-8") as f:
                  f.write(setId)
            except:
                pass
    return ""