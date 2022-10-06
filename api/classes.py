from flask import Blueprint, request, make_response
import os, json, re


bp = Blueprint('classes', __name__)

@bp.route("/createClass", methods=["POST"])
def createClass():
  if os.path.exists(f"{request.form['cssPath']}/props.json"):
    with open(f"{request.form['cssPath']}/props.json", "r", encoding="utf-8") as f:
      props = json.load(f)
    if props.get(f"#{request.form['id']}"):
      props[f".{request.form['class']}"] = props[f"#{request.form['id']}"]
      rule = "\n" + f".{request.form['class']}" + json.dumps(props[f"#{request.form['id']}"]).replace("{", "{\n\t")\
        .replace('"', "").replace(",", ";\n\t").replace("}", ';\n}')
      with open(f"{request.form['cssPath']}/props.json", "w", encoding="utf-8") as f:
        json.dump(props, f)
      with open(f"{request.form['cssFile']}", "a", encoding="utf-8") as f:
        f.write(rule)
        
        return " "


@bp.route("/getClasses", methods=["POST"])
def getClasses():
  if os.path.exists(f"{request.form['cssFile']}"):
    with open(f"{request.form['cssFile']}", "r", encoding="utf-8") as f:
      try:
        classes = []
        classes = sorted(re.findall("[.][A-z0-9-_\n]*[ ]{|[.][A-z0-9-_]*{", f.read()))
        for i in range(0, len(classes)):
          classes[i] = classes[i].replace("{", "", 1).replace(" ", "").replace(".", "")
        
        for i in range(0, len(classes)-1):
          if classes[i] == classes[i+1]:
            classes[i] = ''

        return make_response({'classes': classes})
      except:
        return ""


@bp.route("/setClass", methods=["POST"])
def setClass():
    print('type of request form=>>>', type(request.form))
    for file in os.scandir(request.form['htmlPath']):
      if file.name.endswith("js") or file.name.endswith("jsx"):
        request.form['element'] = (request.form['element']).replace("class", "className")
        with open(f"{request.form['htmlPath']}/{file.name}", "r", encoding="utf-8") as f:
          reactNextFile = f.read()

          element = re.findall("data-id=[0-9\"']*", request.form['element'])[0]
          if reactNextFile.find(element) != -1 and (request.form['element']).find("className") != -1:
            index = reactNextFile.find("class", reactNextFile.find(element)) 
            index = reactNextFile.find("=", index)+2
            part1 = reactNextFile[0:index] + f"{request.form['class']} "
            part2 = reactNextFile[index:len(reactNextFile)]
            part1 = part1 + part2
            
            with open(f"{request.form['htmlPath']}/{file.name}", "w", encoding="utf-8") as f:
              f.write(part1)
          else:
            setClass = reactNextFile.replace(f"id=\"{request.form['id']}\"", f"id=\"{request.form['id']}\" className=\"{request.form['class']}\"")
            with open(f"{request.form['htmlPath']}/{file.name}", ) as f:
              f.write(setClass)

      elif file.name.endswith("html"):
        with open(f"{request.form['htmlPath']}/{file.name}", "r", encoding="utf-8") as f:
          htmlFile = f.read()

        element = re.findall("data-id=[0-9\"']*", request.form['element'])[0]
        if htmlFile.find(element) != -1 and (request.form['element']).find("class") != -1:
          index = htmlFile.find("class", htmlFile.find(element)) 
          index = htmlFile.find("=", index)+2
          part1 = htmlFile[0:index] + f"{request.form['class']} "
          part2 = htmlFile[index:len(htmlFile)]
          part1 = part1 + part2
          with open(f"{request.form['htmlPath']}/{file.name}", "w", encoding="utf-8") as f:
            f.write(part1)

          setClass = htmlFile.replace(f"id=\"{request.form['id']}\"", f"id=\"{request.form['id']}\" class=\"{request.form['class']}\"")
          with open(f"{request.form['htmlPath']}/{file.name}", "w", encoding="utf-8") as f:
            f.write(setClass)
    
    return " "
                