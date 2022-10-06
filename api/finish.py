from flask import Blueprint, render_template
import os, shutil, json, re


bp = Blueprint('finish', __name__)

@bp.route("/", methods=["POST"])
def finish():
  inject1 ='<script>function selector(e){const cssObj = window.getComputedStyle(e.target, null);\
    let style = {};for (let x in cssObj) {let cssObjProp = cssObj.item(x);\
    style[cssObjProp] = cssObj.getPropertyValue(cssObjProp);}let createdId = "";\
    if(!e.target.id){createdId = "id"+Math.random().toString().slice(2,10);let parentWindow =\
    window.parent;parentWindow.postMessage(["element",e.target.id, e.target.tagName, \
    e.target.outerHTML, style, createdId], "*");e.target.setAttribute("id", createdId);}\
    else{let parentWindow = window.parent;parentWindow.postMessage(["element",e.target.id, \
    e.target.tagName, e.target.outerHTML, style], "*");}}document.body.addEventListener(\'click\',\
    selector);window.addEventListener("message", (event) => {if(event.data[0] == "style")\
    {try{document.querySelector("#"+event.data[1]).style[(event.data[2])] = (event.data[3])}catch{}}\
    else if(event.data[0] == "outerHTML"){try{let outer = document.getElementById(event.data[1]).outerHTML;\
    let parentWindow = window.parent;parentWindow.postMessage(["updatedOuter", outer], "*")}catch{}}})</script></body>'

  inject2 = ' onClick={(e)=>{const cssObj = window.getComputedStyle(e.target, null);let style = {};\
    for (let x in cssObj) {let cssObjProp = cssObj.item(x);style[cssObjProp] = cssObj.getPropertyValue(cssObjProp);}\
    let parentWindow = window.parent;parentWindow.postMessage(["element",e.target.id, e.target.tagName, \
    e.target.outerHTML, style], "*");}}'
  
  inject3 = '{window.addEventListener("message", (event) => {if(event.data[0] == "style")\
    {try{document.querySelector("#"+event.data[1]).style[(event.data[2])] = (event.data[3])}catch{}}\
    else if(event.data[0] == "outerHTML"){try{let outer = document.getElementById(event.data[1]).outerHTML;\
    let parentWindow = window.parent;parentWindow.postMessage(["updatedOuter", outer], "*")}catch{}}})}'

  inject4 = ' onClick={(e)=>{const cssObj = window.getComputedStyle(e.target, null);let style = {};\
    for (let x in cssObj) {let cssObjProp = cssObj.item(x);style[cssObjProp] = cssObj.getPropertyValue(cssObjProp);}\
      let parentWindow = window.parent;parentWindow.postMessage(["element",e.target.id, e.target.tagName, \
      e.target.outerHTML, style], "*");}}'

  inject5 = "<Script>{`"+'window.addEventListener("message", (event) => {if(event.data[0] == "style")\
    {try{document.querySelector("#"+event.data[1]).style[(event.data[2])] = (event.data[3])}catch{}}\
    else if(event.data[0] == "outerHTML"){try{let outer = document.getElementById(event.data[1]).outerHTML;\
    let parentWindow = window.parent;parentWindow.postMessage(["updatedOuter", outer], "*")}catch{}}});'+"`}</Script>"
  
  with open("appData/paths.json", "r", encoding="utf-8") as f:
    paths = json.load(f)

  for file in os.scandir(paths['htmlPath']):
    if file.name.endswith("js") or file.name.endswith("jsx") or file.name.endswith("html") or file.name.endswith("hbs"):
      with open(f"{paths['htmlPath']}/{file.name}", "r", encoding="utf-8") as f:
        htmlFile = f.read()
      
      htmlFile = re.sub("[ ]data-id=[0-9\"']*", "", htmlFile).replace(inject1, "").replace(inject2, "")\
        .replace(inject3, "").replace(inject4, "").replace(inject5, "")

      with open(f"{paths['htmlPath']}/{file.name}", "w", encoding="utf-8") as f:
        f.write(htmlFile)

  with open(f"{paths['cssFile']}", "r", encoding="utf-8") as f:
    cssFile = f.read()
  with open(f"{paths['cssFile']}", "w", encoding="utf-8") as f:
    f.write(cssFile[0: cssFile.find("*:hover{border: 1px solid black;}")])

  with open(f"{paths['cssPath']}/props.json", "r", encoding="utf-8") as f:
    props = json.load(f)
    style = ""

  for selector in props:
    if selector != "#" and selector != ".":
        style += "\n{0}{1}".format(selector, "{")
        for prop in props[selector]:
          style +=f"\n\t{prop}:{props[selector][prop]};"
        style += "\n}"
      
  with open(f"{paths['cssFile']}", "a", encoding="utf-8") as f:
    f.write(style)

  os.remove(f"{paths['cssPath']}/props.json")
  os.remove("appData/paths.json")
  shutil.rmtree("appData/backup")

  return render_template("done.html")