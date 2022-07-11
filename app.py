from flask import Flask, request, render_template, redirect, url_for
import os, shutil, json, re, random

app = Flask(__name__)

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


# ---------------- APIs ----------------

@app.route("/check", methods=["GET"])
def check():
  try:
    with open("appData/paths.json", "r", encoding="utf-8") as f:
      data = f.read()
      return data
  except:
    pass


@app.route("/createClass", methods=["POST"])
def createClass():
  if os.path.exists(f"{request.form['cssPath']}/props.json"):
    with open(f"{request.form['cssPath']}/props.json", "r", encoding="utf-8") as f:
      props = json.load(f)
    if props[f"#{request.form['id']}"]:
      props[f".{request.form['class']}"] = props[f"#{request.form['id']}"]
      rule = "\n" + f".{request.form['class']}" + json.dumps(props[f"#{request.form['id']}"]).replace("{", "{\n\t")\
        .replace('"', "").replace(",", ";\n\t").replace("}", ';\n}')
      with open(f"{request.form['cssPath']}/props.json", "w", encoding="utf-8") as f:
        json.dump(props, f)
      with open(f"{request.form['cssFile']}", "a", encoding="utf-8") as f:
        f.write(rule)


@app.route("/discard", methods=["POST"])
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


@app.route("/finish", methods=["POST"])
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


@app.route("/getClasses", methods=["POST"])
def getClasses():
  if os.path.exists(f"{request.form['cssFile']}"):
    with open(f"{request.form['cssFile']}", "r", encoding="utf-8") as f:
      try:
        classes = []
        classes = sorted(re.findall("[.][A-z0-9-_\n]*[ ]{|[.][A-z0-9-_]*{", f.read()))
        for i in range(0, len(classes)):
          classes[i] = classes[i].replace("{", "", 1).replace(" ", "").replace(".")
        
        for i in range(0, len(classes)):
          if classes[i] == classes[i+1]:
            del classes[i]
        
        return classes
      except:
        return ""


@app.route("/init", methods=["POST"])
def init():
  try:
    shutil.rmtree("appData/backup")
  except:
    pass
  
  try:
    os.makedirs("appData/backup")
  except:
    pass

  path = f"{request.form['htmlPath']}".replace("\\", "/")
  cssPath = (f"{request.form['cssFile']}").replace("\\", "/")
  cssPath = cssPath.replace(re.findall("/[^/]*.css", cssPath)[0], "")

  def cssFile(path):
    if os.path.exists(path):
      selector = "\n*:hover{border: 1px solid black;}"
      with open(path, "a", encoding="utf-8") as f:
        f.write(selector)    

  if f"{request.form['type']}" == "html":
    if os.path.exists(path):
      for file in os.scandir(path):
        if file.name.endswith("htm") or file.name.endswith("html") or file.name.endswith("hbs"):

          shutil.copy2(f"{path}/{file.name}", f"appData/backup/{file.name}")

          with open(f"{path}/{file.name}", "r", encoding="utf-8") as f:
            htmlFile = f.read()

          if re.search("data-id=[0-9\"']*", htmlFile) is None:
            e = []
            slice = ""
            Res = htmlFile
            while re.search(f"<[A-z0-9 ]*", htmlFile):
              slice = htmlFile[re.search("<[A-z0-9 ]*", htmlFile).start():
              re.search("[A-z0-9\"\>\/{} ]>", htmlFile).start()+2]
              e.append(slice)
              htmlFile = htmlFile.replace(slice, "", 1)
              htmlFile = htmlFile.replace("/>","", 1)
            
            ee = e[0:len(e)]
            arr = []
            for i in ee:
              for j in re.findall("<[A-z0-9<>\/\"'={}\n ]*", i):
                arr.append(j)

            arr2= arr[0:len(arr)]
            for i in range(len(arr2)):
              if arr2[i].find(" ") != -1 and not arr2[i].startswith("</") and \
                re.search("data-id=[0-9{0}']*".format('"'), arr2[i]) is None:
                arr2[i] = arr2[i].replace("='", '="').replace("' ", '" ').replace("'>", '">')\
                  .replace(" ", f' data-id="{random.randint(1, 1e8)}" ', 1)
              
              elif arr2[i].find(" ") == -1 and not arr2[i].startswith("</") and \
                re.search("data-id=[0-9{0}']*".format('"'), arr2[i]) is None:
                arr2[i] = arr2[i].replace("='", '="').replace("' ", '" ').replace("'>", '">')\
                  .replace(">", f' data-id="{random.randint(1, 1e8)}">', 1)
              
              else:
                arr2[i] = arr2[i].replace("='", '="').replace("' ", '" ').replace("'>", '">')\
                  .replace(arr2[i], arr2[i], 1)
                
            for i in range(len(arr)):
              Res = Res.replace(arr[i], arr2[i], 1)

            selector = '<script>function selector(e){const cssObj = window.getComputedStyle(e.target, null);\
              let style = {};for (let x in cssObj) {let cssObjProp = cssObj.item(x);style[cssObjProp] = \
              cssObj.getPropertyValue(cssObjProp);}let createdId = "";if(!e.target.id)\
              {createdId = "id"+Math.random().toString().slice(2,10);let parentWindow = window.parent;\
              parentWindow.postMessage(["element",e.target.id, e.target.tagName, e.target.outerHTML, \
              style, createdId], "*");e.target.setAttribute("id", createdId);}else{let parentWindow = \
              window.parent;parentWindow.postMessage(["element",e.target.id, e.target.tagName, \
              e.target.outerHTML, style], "*");}}document.body.addEventListener(\'click\', selector);\
              window.addEventListener("message", (event) => {if(event.data[0] == "style"){try{document.\
              querySelector("#"+event.data[1]).style[(event.data[2])] = (event.data[3])}catch{}}else if\
              (event.data[0] == "outerHTML"){try{let outer = document.getElementById(event.data[1]).outerHTML;\
              let parentWindow = window.parent;parentWindow.postMessage(["updatedOuter", outer], "*")}catch{}}})\
              </script></body>'

            inject = Res.replace("</body>", selector, 1)
            with open(f"{path}/{file.name}", "w", encoding="utf-8") as f:
              f.write(inject)
                  
    cssFile(f"{request.form['cssFile']}")
    with open(f"{cssPath}/props.json", "w", encoding="utf-8") as f:
      f.write("{}")
    paths = {
      "htmlPath": f"{request.form['htmlPath']}",
      "cssFile": f"{request.form['cssFile']}",
      "cssPath": cssPath
    }

    with open("appData/paths.json", "w", encoding="utf-8") as f:
      json.dump(paths, f)
    return redirect(url_for("styler"))
      
  elif f"{request.form['type']}" == "react":
    if os.path.exists(path):
      for file in os.scandir(path):
        if file.name.endswith("js") or file.name.endswith("jsx"):

          shutil.copy2(f"{path}/{file.name}", f"appData/backup/{file.name}")
          
          with open(f"{path}/{file.name}", "r", encoding="utf-8") as f:
            reactFile = f.read()
          
          if re.search("<[A-z0-9\.\-\#\_\n\t\(\)\+\;\@\{\}\:\'\"\=\,\!\$\%\^\&\*\?\|\/\\ ]*[^\/]>", reactFile)\
            and re.search("data-id=[0-9\"']*", reactFile) is None:
            e = []
            slice = ""
            Res = reactFile
            while re.search("<[A-z0-9 ]*", reactFile):
              slice = reactFile[re.search("<[A-z0-9 ]*", reactFile).start():
              re.search("[A-z0-9\"\>\/{} ]>", reactFile).start()+2]
              e.append(slice)
              reactFile = reactFile.replace(slice, "", 1)
              reactFile = reactFile.replace("/>","", 1)
            
            ee = e[0:len(e)]
            arr = []
            for i in range(len(ee)):
              for j in re.findall("<[A-z0-9<>\/\"'={}\n ]*", ee[i]):
                arr.append(j)

            arr2= arr[0:len(arr)]
            for i in range(len(arr2)):
              if arr2[i].find(" ") != -1 and not arr2[i].startswith("</") and \
                re.search("data-id=[0-9{0}']*".format('"'), arr2[i]) is None:
                arr2[i] = arr2[i].replace("='", '="').replace("' ", '" ').replace("'>", '">')\
                .replace(" ", f' data-id="{random.randint(1, 1e8)}" ', 1)
              
              elif arr2[i].find(" ") == -1 and  not arr2[i].startswith("</") and \
                re.search("data-id=[0-9{0}']*".format('"'), arr2[i]) is None:
                arr2[i] = arr2[i].replace("='", '="').replace("' ", '" ').replace("'>", '">')\
                .replace(">", f' data-id="{random.randint(1, 1e8)}">', 1)
              
              else:
                arr2[i] = arr2[i].replace("='", '="').replace("' ", '" ').replace("'>", '">').replace(arr2[i], arr2[i], 1)
                
            

            for i in range(len(arr)):
              Res = Res.replace(arr[i], arr2[i], 1)
            
            
            selector = ' onClick={(e)=>{const cssObj = window.getComputedStyle(e.target, null);let style = {};\
              for (let x in cssObj) {let cssObjProp = cssObj.item(x);style[cssObjProp] = \
              cssObj.getPropertyValue(cssObjProp);}let parentWindow = window.parent;\
              parentWindow.postMessage(["element",e.target.id, e.target.tagName, e.target.outerHTML, style], "*");}}'

            script = '{window.addEventListener("message", (event) => {if(event.data[0] == "style")\
              {try{document.querySelector("#"+event.data[1]).style[(event.data[2])] = (event.data[3])}catch{}}\
              else if(event.data[0] == "outerHTML"){try{let outer = document.getElementById(event.data[1]).outerHTML;\
              let parentWindow = window.parent;parentWindow.postMessage(["updatedOuter", outer], "*")}catch{}}})}'

            match = re.findall("<[A-z0-9\.\-\#\_\n\t\(\)\+\;\@\{\}\:\'\"\=\,\!\$\%\^\&\*\?\|\/\\ ]*[^\/]>", Res)[0]
            match2 = match[0:len(match) - 1]
            inject = Res.replace(match, match + f'\n{script}\n', 1)
            inject2 = inject.replace(match2, match2 + selector, 1)
            
            with open(f"{path}/{file.name}", "w", encoding="utf-8") as f:
              f.write(inject2)
                    
    cssFile(f"{request.form['cssFile']}")
    with open(f"{cssPath}/props.json", "w", encoding="utf-8") as f:
      f.write("{}")
    paths = {
      "htmlPath": f"{request.form['htmlPath']}",
      "cssFile": f"{request.form['cssFile']}",
      "cssPath": cssPath
    }
    with open("appData/paths.json", "w", encoding="utf-8") as f:
      json.dump(paths, f)
    return redirect(url_for("styler"))
  
  elif f"{request.form['type']}" == "nextjs":
    if os.path.exists(path):
      for file in os.scandir(path):
        if file.name.endswith("js"):

          shutil.copy2(f"{path}/{file.name}", f"appData/backup/{file.name}")

          with open(f"{path}/{file.name}", "r", encoding="utf-8") as f:
            nextjsFile = f.read()

          if re.search("<[A-z0-9\.\-\#\_\n\t\(\)\+\;\@\{\}\:\'\"\=\,\!\$\%\^\&\*\?\|\/\\ ]*[^\/]>", nextjsFile)\
            and re.search("data-id=[0-9\"']*", nextjsFile) is None:
            e = []
            slice = ""
            Res = nextjsFile
            while re.search("<[A-z0-9 ]*", nextjsFile):
              slice = nextjsFile[re.search("<[A-z0-9 ]*", nextjsFile).start(): 
                re.search("[A-z0-9\"\>\/{} ]>", nextjsFile).start()+2]
              e.append(slice)
              nextjsFile = nextjsFile.replace(slice, "", 1)
              nextjsFile = nextjsFile.replace("/>","", 1)
            
            ee = e[0:len(e)]
            arr = []
            for i in range(len(ee)):
              for j in re.findall("<[A-z0-9<>\/\"'={}\n ]*", ee[i]):
                arr.append(j)


            arr2= arr[0:len(arr)]
            for i in range(len(arr2)):
              if arr2[i].find(" ") != -1 and not arr2[i].startswith("</"):
                arr2[i] = arr2[i].replace("='", '="').replace("' ", '" ').replace("'>", '">')\
                .replace(" ", f' data-id="{random.randint(1, 1e8)}" ', 1)
              
              elif arr2[i].find(" ") == -1 and not arr2[i].startswith("</"):
                arr2[i] = arr2[i].replace("='", '="').replace("' ", '" ').replace("'>", '">')\
                .replace(">", f' data-id="{random.randint(1, 1e8)}">', 1)
              
              else:
                arr2[i] = arr2[i].replace("='", '="').replace("' ", '" ').replace("'>", '">').replace(arr2[i], arr2[i], 1)
                
            
            for i in range(len(arr)):
              Res = Res.replace(arr[i], arr2[i], 1)
            
            selector = ' onClick={(e)=>{const cssObj = window.getComputedStyle(e.target, null);\
              let style = {};for (let x in cssObj) {let cssObjProp = cssObj.item(x);style[cssObjProp] = \
              cssObj.getPropertyValue(cssObjProp);}let parentWindow = window.parent;\
              parentWindow.postMessage(["element",e.target.id, e.target.tagName, e.target.outerHTML, style], "*");}}'

            script = "<Script>{`"+'window.addEventListener("message", (event) => {if(event.data[0] == "style")\
              {try{document.querySelector("#"+event.data[1]).style[(event.data[2])] = (event.data[3])}catch{}}else if\
              (event.data[0] == "outerHTML"){try{let outer = document.getElementById(event.data[1]).outerHTML;\
              let parentWindow = window.parent;parentWindow.postMessage(["updatedOuter", outer], "*")}catch{}}});'+\
              "`}</Script>"
            
            firstChar = re.findall(".", Res)[0]
            match = re.findall("<[A-z0-9\.\-\#\_\n\t\(\)\+\;\@\{\}\:\'\"\=\,\!\$\%\^\&\*\?\|\/\\ ]*[^\/]>", Res)[0]
            match2 = match[0:len(match) - 1]
            inject = Res.replace(match, match + f"\n{script}\n", 1)
            inject2 = inject.replace(match2, match2 + selector, 1)
            if inject2.find("import Script from") == -1:
              inject3 =  inject2.replace(firstChar, f"import Script from 'next/script'\n{firstChar}", 1)
              with open(f"{path}/{file.name}", "w", encoding="utf-8") as f:
                f.write(inject3)                        
            else:
              with open(f"{path}/{file.name}", "w", encoding="utf-8") as f:
                f.write(inject2)  

    cssFile(f"{request.form['cssFile']}")
    with open(f"{cssPath}/props.json", "w", encoding="utf-8") as f:
      f.write("{}")
    paths = {
      "htmlPath": f"{request.form['htmlPath']}",
      "cssFile": f"{request.form['cssFile']}",
      "cssPath": cssPath
    }
    with open("appData/paths.json", "w", encoding="utf-8") as f:
      json.dump(paths, f)
    return redirect(url_for("styler"))
    

@app.route("/set", methods=["POST"])
def set():
  with open(f"{request.form['cssPath']}/props.json", "r", encoding="utf-8") as f:
      props = json.load(f)
  if request.form['catg'] == "margin-all":
    rule = (f"\n#{request.form['id']}""{"
          f"\n\tmargin:{request.form['margin']}{request.form['margins-unit']};"
        "\n}")
    if props.get(f"#{request.form['id']}") is None:
      props[f"#{request.form['id']}"] = {}
    
    props[f"#{request.form['id']}"]["margin"] = f"{request.form['margin']}{request.form['margins-unit']}"
    with open(f"{request.form['cssPath']}/props.json", "w", encoding="utf-8") as f:
        json.dump(props, f)
    with open(f"{request.form['cssFile']}", "a", encoding="utf-8") as f:
        f.write(rule)
  
  elif request.form['catg'] == "margin-c":
    rule = (f"\n#{request.form['id']}""{"
      f"\n\tmargin-top:{request.form['margin-top']}{request.form['margin-unit']};"
      f"\n\tmargin-right:{request.form['margin-right']}{request.form['margin-unit']};"
      f"\n\tmargin-bottom:{request.form['margin-bottom']}{request.form['margin-unit']};"
      f"\n\tmargin-left:{request.form['margin-left']}{request.form['margin-unit']};"
    "\n}")
    if props.get(f"#{request.form['id']}") is None:
      props[f"#{request.form['id']}"] = {}
    
    props[f"#{request.form['id']}"]['margin-top'] = f"{request.form['margin-top']}{request.form['margin-unit']}"
    props[f"#{request.form['id']}"]['margin-right'] = f"{request.form['margin-right']}{request.form['margin-unit']}"
    props[f"#{request.form['id']}"]['margin-bottom'] = f"{request.form['margin-bottom']}{request.form['margin-unit']}"
    props[f"#{request.form['id']}"]['margin-left'] = f"{request.form['margin-left']}{request.form['margin-unit']}"

    with open(f"{request.form['cssPath']}/props.json", "w", encoding="utf-8") as f:
        json.dump(props, f)
    with open(f"{request.form['cssFile']}", "a", encoding="utf-8") as f:
        f.write(rule)
  
  elif request.form['catg'] == "padding-all":
    rule = (f"\n#{request.form['id']}""{"
      f"\n\tpadding:{request.form['padding']}{request.form['paddings-unit']};"
    "\n}")
    if props.get(f"#{request.form['id']}") is None:
      props[f"#{request.form['id']}"] = {}
    
    props[f"#{request.form['id']}"]['padding'] = f"{request.form['padding']}{request.form['paddings-unit']}"
    with open(f"{request.form['cssPath']}/props.json", "w", encoding="utf-8") as f:
        json.dump(props, f)
    with open(f"{request.form['cssFile']}", "a", encoding="utf-8") as f:
        f.write(rule)
  
  elif request.form['catg'] == "padding-c":
    rule = (f"\n#{request.form['id']}""{"
      f"\n\tpadding-top:{request.form['padding-top']}{request.form['padding-unit']};"
      f"\n\tpadding-right:{request.form['padding-right']}{request.form['padding-unit']};"
      f"\n\tpadding-bottom:{request.form['padding-bottom']}{request.form['padding-unit']};"
      f"\n\tpadding-left:{request.form['padding-left']}{request.form['padding-unit']};"
    "\n}")
    if props.get(f"#{request.form['id']}") is None:
      props[f"#{request.form['id']}"] = {}
    
    props[f"#{request.form['id']}"]['padding-top'] = f"{request.form['padding-top']}{request.form['padding-unit']}"
    props[f"#{request.form['id']}"]['padding-right'] = f"{request.form['padding-right']}{request.form['padding-unit']}"
    props[f"#{request.form['id']}"]['padding-bottom'] = f"{request.form['padding-bottom']}{request.form['padding-unit']}"
    props[f"#{request.form['id']}"]['padding-left'] = f"{request.form['padding-left']}{request.form['padding-unit']}"
    with open(f"{request.form['cssPath']}/props.json", "w", encoding="utf-8") as f:
        json.dump(props, f)
    with open(f"{request.form['cssFile']}", "a", encoding="utf-8") as f:
        f.write(rule)
  
  elif request.form['catg'] == "font-style":
    rule = (f"\n#{request.form['id']}""{"
      f"\n\tfont-style:{request.form['font-style']};"
    "\n}")
    if props.get(f"#{request.form['id']}") is None:
      props[f"#{request.form['id']}"] = {}
    
    props[f"#{request.form['id']}"]['font-style'] = f"{request.form['font-style']}"
    with open(f"{request.form['cssPath']}/props.json", "w", encoding="utf-8") as f:
        json.dump(props, f)
    with open(f"{request.form['cssFile']}", "a", encoding="utf-8") as f:
        f.write(rule)
  
  elif request.form['catg'] == "font-weight":
    rule = (f"\n#{request.form['id']}""{"
      f"\n\tfont-weight:{request.form['font-weight']};"
    "\n}")
    if props.get(f"#{request.form['id']}") is None:
      props[f"#{request.form['id']}"] = {}
    
    props[f"#{request.form['id']}"]['font-weight'] = f"{request.form['font-weight']}"
    with open(f"{request.form['cssPath']}/props.json", "w", encoding="utf-8") as f:
        json.dump(props, f)
    with open(f"{request.form['cssFile']}", "a", encoding="utf-8") as f:
        f.write(rule)
  
  elif request.form['catg'] == "font-size":
    rule = (f"\n#{request.form['id']}""{"
      f"\n\tfont-size:{request.form['font-size']}{request.form['font-unit']};"
    "\n}")
    if props.get(f"#{request.form['id']}") is None:
      props[f"#{request.form['id']}"] = {}
    
    props[f"#{request.form['id']}"]['font-size'] = f"{request.form['font-size']}{request.form['font-unit']}"
    with open(f"{request.form['cssPath']}/props.json", "w", encoding="utf-8") as f:
        json.dump(props, f)
    with open(f"{request.form['cssFile']}", "a", encoding="utf-8") as f:
        f.write(rule)
  
  elif request.form['catg'] == "font-size-pre":
    rule = (f"\n#{request.form['id']}""{"
      f"\n\tfont-size:{request.form['font-size-pre']};"
    "\n}")
    if props.get(f"#{request.form['id']}") is None:
      props[f"#{request.form['id']}"] = {}
    
    props[f"#{request.form['id']}"]['font-size'] = f"{request.form['font-size-pre']}"
    with open(f"{request.form['cssPath']}/props.json", "w", encoding="utf-8") as f:
        json.dump(props, f)
    with open(f"{request.form['cssFile']}", "a", encoding="utf-8") as f:
        f.write(rule)
  
  elif request.form['catg'] == "font-family":
    rule = (f"\n#{request.form['id']}""{"
      f"\n\tfont-family:{request.form['font-family']};"
    "\n}")
    if props.get(f"#{request.form['id']}") is None:
      props[f"#{request.form['id']}"] = {}
    
    props[f"#{request.form['id']}"]['font-family'] = f"{request.form['font-family']}"
    with open(f"{request.form['cssPath']}/props.json", "w", encoding="utf-8") as f:
        json.dump(props, f)
    with open(f"{request.form['cssFile']}", "a", encoding="utf-8") as f:
        f.write(rule)
  
  elif request.form['catg'] == "font-color":
    rule = (f"\n#{request.form['id']}""{"
      f"\n\tcolor:{request.form['color']};"
    "\n}")
    if props.get(f"#{request.form['id']}") is None:
      props[f"#{request.form['id']}"] = {}
    
    props[f"#{request.form['id']}"]['color'] = f"{request.form['color']}"
    with open(f"{request.form['cssPath']}/props.json", "w", encoding="utf-8") as f:
        json.dump(props, f)
    with open(f"{request.form['cssFile']}", "a", encoding="utf-8") as f:
        f.write(rule)
  
  elif request.form['catg'] == "width":
    rule = (f"\n#{request.form['id']}""{"
      f"\n\twidth:{request.form['width']}{request.form['width-unit']};"
    "\n}")
    if props.get(f"#{request.form['id']}") is None:
      props[f"#{request.form['id']}"] = {}
    
    props[f"#{request.form['id']}"]['width'] = f"{request.form['width']}{request.form['width-unit']}"
    with open(f"{request.form['cssPath']}/props.json", "w", encoding="utf-8") as f:
        json.dump(props, f)
    with open(f"{request.form['cssFile']}", "a", encoding="utf-8") as f:
        f.write(rule)
  
  elif request.form['catg'] == "height":
    rule = (f"\n#{request.form['id']}""{"
      f"\n\theight:{request.form['height']}{request.form['height-unit']};"
    "\n}")
    if props.get(f"#{request.form['id']}") is None:
      props[f"#{request.form['id']}"] = {}
    
    props[f"#{request.form['id']}"]['height'] = f"{request.form['height']}{request.form['height-unit']}"
    with open(f"{request.form['cssPath']}/props.json", "w", encoding="utf-8") as f:
        json.dump(props, f)
    with open(f"{request.form['cssFile']}", "a", encoding="utf-8") as f:
        f.write(rule)
  
  elif request.form['catg'] == "background-color":
    rule = (f"\n#{request.form['id']}""{"
      f"\n\tbackground-color:{request.form['background-color']};"
    "\n}")
    if props.get(f"#{request.form['id']}") is None:
      props[f"#{request.form['id']}"] = {}
    
    props[f"#{request.form['id']}"]['background-color'] = f"{request.form['background-color']}"
    with open(f"{request.form['cssPath']}/props.json", "w", encoding="utf-8") as f:
        json.dump(props, f)
    with open(f"{request.form['cssFile']}", "a", encoding="utf-8") as f:
        f.write(rule)
  
  elif request.form['catg'] == "background-image":
    rule = (f"\n#{request.form['id']}""{"
      f"\n\tbackground-image:url('{request.form['background-image']}');"
    "\n}")
    if props.get(f"#{request.form['id']}") is None:
      props[f"#{request.form['id']}"] = {}
    
    props[f"#{request.form['id']}"]['background-image'] = f"url('{request.form['background-image']}')"
    with open(f"{request.form['cssPath']}/props.json", "w", encoding="utf-8") as f:
        json.dump(props, f)
    with open(f"{request.form['cssFile']}", "a", encoding="utf-8") as f:
        f.write(rule)
  
  elif request.form['catg'] == "background-position":
    rule = (f"\n#{request.form['id']}""{"
      f"\n\tbackground-position:{request.form['background-position']};"
    "\n}")
    if props.get(f"#{request.form['id']}") is None:
      props[f"#{request.form['id']}"] = {}
    
    props[f"#{request.form['id']}"]['background-position'] = f"{request.form['background-position']}"
    with open(f"{request.form['cssPath']}/props.json", "w", encoding="utf-8") as f:
        json.dump(props, f)
    with open(f"{request.form['cssFile']}", "a", encoding="utf-8") as f:
        f.write(rule)
  
  elif request.form['catg'] == "background-attachment":
    rule = (f"\n#{request.form['id']}""{"
      f"\n\tbackground-attachment:{request.form['background-attachment']};"
    "\n}")
    if props.get(f"#{request.form['id']}") is None:
      props[f"#{request.form['id']}"] = {}
    
    props[f"#{request.form['id']}"]['background-attachment'] = f"{request.form['background-attachment']}"
    with open(f"{request.form['cssPath']}/props.json", "w", encoding="utf-8")as f:
        json.dump(props, f)
    with open(f"{request.form['cssFile']}", "a", encoding="utf-8") as f:
        f.write(rule)
  
  elif request.form['catg'] == "background-clip":
    rule = (f"\n#{request.form['id']}""{"
      f"\n\tbackground-clip:{request.form['background-clip']};"
    "\n}")
    if props.get(f"#{request.form['id']}") is None:
      props[f"#{request.form['id']}"] = {}
    
    props[f"#{request.form['id']}"]['background-clip'] = f"{request.form['background-clip']}"
    with open(f"{request.form['cssPath']}/props.json", "w", encoding="utf-8") as f:
        json.dump(props, f)
    with open(f"{request.form['cssFile']}", "a", encoding="utf-8") as f:
        f.write(rule)
  
  elif request.form['catg'] == "background-repeat":
    rule = (f"\n#{request.form['id']}""{"
      f"\n\tbackground-repeat:{request.form['background-repeat']};"
    "\n}")
    if props.get(f"#{request.form['id']}") is None:
      props[f"#{request.form['id']}"] = {}
    
    props[f"#{request.form['id']}"]['background-repeat'] = f"{request.form['background-repeat']}"
    with open(f"{request.form['cssPath']}/props.json", "w", encoding="utf-8") as f:
        json.dump(props, f)
    with open(f"{request.form['cssFile']}", "a", encoding="utf-8") as f:
        f.write(rule)
  
  elif request.form['catg'] == "background-origin":
    rule = (f"\n#{request.form['id']}""{"
      f"\n\tbackground-origin:{request.form['background-origin']};"
    "\n}")
    if props.get(f"#{request.form['id']}") is None:
      props[f"#{request.form['id']}"] = {}
    
    props[f"#{request.form['id']}"]['background-origin'] = f"{request.form['background-origin']}"
    with open(f"{request.form['cssPath']}/props.json", "w", encoding="utf-8")as f:
        json.dump(props, f)
    with open(f"{request.form['cssFile']}", "a", encoding="utf-8") as f:
        f.write(rule)
  
  elif request.form['catg'] == "background-size-pre":
    rule = (f"\n#{request.form['id']}""{"
      f"\n\tbackground-size:{request.form['background-size']};"
    "\n}")
    if props.get(f"#{request.form['id']}") is None:
      props[f"#{request.form['id']}"] = {}
    
    props[f"#{request.form['id']}"]['background-size'] = f"{request.form['background-size']}"
    with open(f"{request.form['cssPath']}/props.json", "w", encoding="utf-8") as f:
        json.dump(props, f)
    with open(f"{request.form['cssFile']}", "a", encoding="utf-8") as f:
        f.write(rule)
  
  elif request.form['catg'] == "background-size-c":
    rule = (f"\n#{request.form['id']}""{"
      f"\n\tbackground-size:{request.form['background-size-c']}{request.form['background-size-c-unit']};"
    "\n}")
    if props.get(f"#{request.form['id']}") is None:
      props[f"#{request.form['id']}"] = {}
    
    props[f"#{request.form['id']}"]["background-size"] = f"{request.form['background-size-c']}{request.form['background-size-c-unit']}"
    with open(f"{request.form['cssPath']}/props.json", "w", encoding="utf-8") as f:
        json.dump(props, f)
    with open(f"{request.form['cssFile']}", "a", encoding="utf-8") as f:
        f.write(rule)
  
  elif request.form['catg'] == "border-all":
    rule = (f"\n#{request.form['id']}""{"
      f"\n\tborder:{request.form['border']}{request.form['borders-unit']} {request.form['border-style']} \
        {request.form['border-color']};"
    "\n}")
    if props.get(f"#{request.form['id']}") is None:
      props[f"#{request.form['id']}"] = {}
    
    props[f"#{request.form['id']}"]["border"] = f"{request.form['border']}{request.form['borders-unit']} \
    {request.form['border-style']} {request.form['border-color']}"
    with open(f"{request.form['cssPath']}/props.json", "w", encoding="utf-8") as f:
        json.dump(props, f)
    with open(f"{request.form['cssFile']}", "a", encoding="utf-8") as f:
        f.write(rule)
  
  elif request.form['catg'] == "border-c":
    rule = (f"\n#{request.form['id']}""{"
      f"\n\tborder-top-width:{request.form['border-top-width']}{request.form['border-unit']};"
      f"\n\tborder-right-width:{request.form['border-right-width']}{request.form['border-unit']};"
      f"\n\tborder-bottom-width:{request.form['border-bottom-width']}{request.form['border-unit']};"
      f"\n\tborder-left-width:{request.form['border-left-width']}{request.form['border-unit']};"
    "\n}")
    if props.get(f"#{request.form['id']}") is None:
      props[f"#{request.form['id']}"] = {}
    
    props[f"#{request.form['id']}"]["border-width"] = \
    (
      f"{request.form['border-top-width']}{request.form['border-unit']} " 
      f"{request.form['border-right-width']}{request.form['border-unit']} " 
      f"{request.form['border-bottom-width']}{request.form['border-unit']} " 
      f"{request.form['border-left-width']}{request.form['border-unit']}"
    )

    with open(f"{request.form['cssPath']}/props.json", "w", encoding="utf-8") as f:
        json.dump(props, f)
    with open(f"{request.form['cssFile']}", "a", encoding="utf-8") as f:
        f.write(rule)
  
  elif request.form['catg'] == "border-color":
    rule = (f"\n#{request.form['id']}""{"
      f"\n\tborder-color:{request.form['border-color']};"
    "\n}")
    if props.get(f"#{request.form['id']}") is None:
      props[f"#{request.form['id']}"] = {}
    
    props[f"#{request.form['id']}"]['border-color'] = f"{request.form['border-color']}"
    with open(f"{request.form['cssPath']}/props.json", "w", encoding="utf-8") as f:
        json.dump(props, f)
    with open(f"{request.form['cssFile']}", "a", encoding="utf-8") as f:
        f.write(rule)
  
  elif request.form['catg'] == "border-style":
    rule = (f"\n#{request.form['id']}""{"
      f"\n\tborder-style:{request.form['border-style']};"
    "\n}")
    if props.get(f"#{request.form['id']}") is None:
      props[f"#{request.form['id']}"] = {}
    
    props[f"#{request.form['id']}"]['border-style'] = f"{request.form['border-style']}"
    with open(f"{request.form['cssPath']}/props.json", "w", encoding="utf-8") as f:
        json.dump(props, f)
    with open(f"{request.form['cssFile']}", "a", encoding="utf-8") as f:
        f.write(rule)
  
  elif request.form['catg'] == "border-radius":
    rule = (f"\n#{request.form['id']}""{"
      f"\n\tborder-radius:{request.form['border-radius']}{request.form['border-raduis-unit']};"
    "\n}")
    if props.get(f"#{request.form['id']}") is None:
      props[f"#{request.form['id']}"] = {}
    
    props[f"#{request.form['id']}"]['border-radius'] = f"{request.form['border-radius']}{request.form['border-raduis-unit']}"
    with open(f"{request.form['cssPath']}/props.json", "w", encoding="utf-8") as f:
        json.dump(props, f)
    with open(f"{request.form['cssFile']}", "a", encoding="utf-8") as f:
        f.write(rule)
  
  elif request.form['catg'] == "border-spacing":
    rule = (f"\n#{request.form['id']}""{"
      f"\n\tborder-spacing:{request.form['border-spacing-x']}px {request.form['border-spacing-y']}px;"
    "\n}")
    if props.get(f"#{request.form['id']}") is None:
      props[f"#{request.form['id']}"] = {}
    
    props[f"#{request.form['id']}"]['border-spacing'] = f"{request.form['border-spacing-x']}px {request.form['border-spacing-y']}px"
    with open(f"{request.form['cssPath']}/props.json", "w", encoding="utf-8") as f:
        json.dump(props, f)
    with open(f"{request.form['cssFile']}", "a", encoding="utf-8") as f:
        f.write(rule)
  
  elif request.form['catg'] == "border-collapse":
    rule = (f"\n#{request.form['id']}""{"
      f"\n\tborder-collapse:{request.form['border-collapse']};"
    "\n}")
    if props.get(f"#{request.form['id']}") is None:
      props[f"#{request.form['id']}"] = {}
    
    props[f"#{request.form['id']}"]['border-collapse'] = f"{request.form['border-collapse']}"
    with open(f"{request.form['cssPath']}/props.json", "w", encoding="utf-8") as f:
        json.dump(props, f)
    with open(f"{request.form['cssFile']}", "a", encoding="utf-8") as f:
        f.write(rule)
  
  elif request.form['catg'] == "outline-width-pre":
    rule = (f"\n#{request.form['id']}""{"
      f"\n\toutline-width:{request.form['outline-width-pre']};"
    "\n}")
    if props.get(f"#{request.form['id']}") is None:
      props[f"#{request.form['id']}"] = {}
    
    props[f"#{request.form['id']}"]['outline-width'] = f"{request.form['outline-width-pre']}"
    with open(f"{request.form['cssPath']}/props.json", "w", encoding="utf-8") as f:
        json.dump(props, f)
    with open(f"{request.form['cssFile']}", "a", encoding="utf-8") as f:
        f.write(rule)
  
  elif request.form['catg'] == "outline-width-c":
    rule = (f"\n#{request.form['id']}""{"
      f"\n\toutline-width:{request.form['outline-width']}px;"
    "\n}")
    if props.get(f"#{request.form['id']}") is None:
      props[f"#{request.form['id']}"] = {}
    
    props[f"#{request.form['id']}"]['outline-width'] = f"{request.form['outline-width']}px"
    with open(f"{request.form['cssPath']}/props.json", "w", encoding="utf-8") as f:
        json.dump(props, f)
    with open(f"{request.form['cssFile']}", "a", encoding="utf-8") as f:
        f.write(rule)
  
  elif request.form['catg'] == "outline-color":
    rule = (f"\n#{request.form['id']}""{"
      f"\n\toutline-color:{request.form['outline-color']};"
    "\n}")
    if props.get(f"#{request.form['id']}") is None:
      props[f"#{request.form['id']}"] = {}
    
    props[f"#{request.form['id']}"]['outline-color'] = f"{request.form['outline-color']}"
    with open(f"{request.form['cssPath']}/props.json", "w", encoding="utf-8") as f:
        json.dump(props, f)
    with open(f"{request.form['cssFile']}", "a", encoding="utf-8") as f:
        f.write(rule)
  
  elif request.form['catg'] == "outline-style":
    rule = (f"\n#{request.form['id']}""{"
      f"\n\toutline-style:{request.form['outline-style']};"
    "\n}")
    if props.get(f"#{request.form['id']}") is None:
      props[f"#{request.form['id']}"] = {}
    
    props[f"#{request.form['id']}"]['outline-style'] = f"{request.form['outline-style']}"
    with open(f"{request.form['cssPath']}/props.json", "w", encoding="utf-8") as f:
        json.dump(props, f)
    with open(f"{request.form['cssFile']}", "a", encoding="utf-8") as f:
        f.write(rule)
  
  elif request.form['catg'] == "outline-offset":
    rule = (f"\n#{request.form['id']}""{"
      f"\n\toutline-offset:{request.form['outline-offset']}px;"
    "\n}")
    if props.get(f"#{request.form['id']}") is None:
      props[f"#{request.form['id']}"] = {}
    
    props[f"#{request.form['id']}"]['outline-offset'] = f"{request.form['outline-offset']}px"
    with open(f"{request.form['cssPath']}/props.json", "w", encoding="utf-8") as f:
        json.dump(props, f)
    with open(f"{request.form['cssFile']}", "a", encoding="utf-8") as f:
        f.write(rule)
  
  elif request.form['catg'] == "text-align":
    rule = (f"\n#{request.form['id']}""{"
      f"\n\ttext-align:{request.form['text-align']};"
    "\n}")
    if props.get(f"#{request.form['id']}") is None:
      props[f"#{request.form['id']}"] = {}
    
    props[f"#{request.form['id']}"]['text-align'] = f"{request.form['text-align']}"
    with open(f"{request.form['cssPath']}/props.json", "w", encoding="utf-8") as f:
        json.dump(props, f)
    with open(f"{request.form['cssFile']}", "a", encoding="utf-8") as f:
        f.write(rule)
  
  elif request.form['catg'] == "vertical-align":
    rule = (f"\n#{request.form['id']}""{"
      f"\n\tvertical-align:{request.form['vertical-align']};"
    "\n}")
    if props.get(f"#{request.form['id']}") is None:
      props[f"#{request.form['id']}"] = {}
    
    props[f"#{request.form['id']}"]['vertical-align'] = f"{request.form['vertical-align']}"
    with open(f"{request.form['cssPath']}/props.json", "w", encoding="utf-8") as f:
        json.dump(props, f)
    with open(f"{request.form['cssFile']}", "a", encoding="utf-8") as f:
        f.write(rule)
  
  elif request.form['catg'] == "text-align-last":
    rule = (f"\n#{request.form['id']}""{"
      f"\n\ttext-align-last:{request.form['text-align-last']};"
    "\n}")
    if props.get(f"#{request.form['id']}") is None:
      props[f"#{request.form['id']}"] = {}
    
    props[f"#{request.form['id']}"]['text-align-last'] = f"{request.form['text-align-last']}"
    with open(f"{request.form['cssPath']}/props.json", "w", encoding="utf-8") as f:
        json.dump(props, f)
    with open(f"{request.form['cssFile']}", "a", encoding="utf-8") as f:
        f.write(rule)
  
  elif request.form['catg'] == "text-decoration":
    rule = (f"\n#{request.form['id']}""{"
      f"\n\ttext-decoration:{request.form['text-decoration']};"
    "\n}")
    if props.get(f"#{request.form['id']}") is None:
      props[f"#{request.form['id']}"] = {}
    
    props[f"#{request.form['id']}"]['text-decoration'] = f"{request.form['text-decoration']}"
    with open(f"{request.form['cssPath']}/props.json", "w", encoding="utf-8") as f:
        json.dump(props, f)
    with open(f"{request.form['cssFile']}", "a", encoding="utf-8") as f:
        f.write(rule)
  
  elif request.form['catg'] == "text-decoration-color":
    rule = (f"\n#{request.form['id']}""{"
      f"\n\ttext-decoration-color:{request.form['text-decoration-color']};"
    "\n}")
    if props.get(f"#{request.form['id']}") is None:
      props[f"#{request.form['id']}"] = {}
    
    props[f"#{request.form['id']}"]['text-decoration-color'] = f"{request.form['text-decoration-color']}"
    with open(f"{request.form['cssPath']}/props.json", "w", encoding="utf-8") as f:
        json.dump(props, f)
    with open(f"{request.form['cssFile']}", "a", encoding="utf-8") as f:
        f.write(rule)
  
  elif request.form['catg'] == "text-decoration-style":
    rule = (f"\n#{request.form['id']}""{"
      f"\n\ttext-decoration-style:{request.form['text-decoration-style']};"
    "\n}")
    if props.get(f"#{request.form['id']}") is None:
      props[f"#{request.form['id']}"] = {}
    
    props[f"#{request.form['id']}"]['text-decoration-style'] = f"{request.form['text-decoration-style']}"
    with open(f"{request.form['cssPath']}/props.json", "w", encoding="utf-8") as f:
        json.dump(props, f)
    with open(f"{request.form['cssFile']}", "a", encoding="utf-8") as f:
        f.write(rule)
  
  elif request.form['catg'] == "text-indent":
    rule = (f"\n#{request.form['id']}""{"
      f"\n\ttext-indent:{request.form['text-indent']}px;"
    "\n}")
    if props.get(f"#{request.form['id']}") is None:
      props[f"#{request.form['id']}"] = {}
    
    props[f"#{request.form['id']}"]['text-indent'] = f"{request.form['text-indent']}px"
    with open(f"{request.form['cssPath']}/props.json", "w", encoding="utf-8") as f:
        json.dump(props, f)
    with open(f"{request.form['cssFile']}", "a", encoding="utf-8") as f:
        f.write(rule)
  
  elif request.form['catg'] == "text-overflow":
    rule = (f"\n#{request.form['id']}""{"
      f"\n\ttext-overflow:{request.form['text-overflow']};"
    "\n}")
    if props.get(f"#{request.form['id']}") is None:
      props[f"#{request.form['id']}"] = {}
    
    props[f"#{request.form['id']}"]['text-overflow'] = f"{request.form['text-overflow']}"
    with open(f"{request.form['cssPath']}/props.json", "w", encoding="utf-8") as f:
        json.dump(props, f)
    with open(f"{request.form['cssFile']}", "a", encoding="utf-8") as f:
        f.write(rule)
  
  elif request.form['catg'] == "text-transform":
    rule = (f"\n#{request.form['id']}""{"
      f"\n\ttext-transform:{request.form['text-transform']};"
    "\n}")
    if props.get(f"#{request.form['id']}") is None:
      props[f"#{request.form['id']}"] = {}
    
    props[f"#{request.form['id']}"]['text-transform'] = f"{request.form['text-transform']}"
    with open(f"{request.form['cssPath']}/props.json", "w", encoding="utf-8") as f:
        json.dump(props, f)
    with open(f"{request.form['cssFile']}", "a", encoding="utf-8") as f:
        f.write(rule)
  
  elif request.form['catg'] == "display":
    rule = (f"\n#{request.form['id']}""{"
      f"\n\tdisplay:{request.form['display']};"
    "\n}")
    if props.get(f"#{request.form['id']}") is None:
      props[f"#{request.form['id']}"] = {}
    
    props[f"#{request.form['id']}"]['display'] = f"{request.form['display']}"
    with open(f"{request.form['cssPath']}/props.json", "w", encoding="utf-8") as f:
        json.dump(props, f)
    with open(f"{request.form['cssFile']}", "a", encoding="utf-8") as f:
        f.write(rule)
  
  elif request.form['catg'] == "position":
    rule = (f"\n#{request.form['id']}""{"
      f"\n\tposition:{request.form['position']};"
    "\n}")
    if props.get(f"#{request.form['id']}") is None:
      props[f"#{request.form['id']}"] = {}
    
    props[f"#{request.form['id']}"]['position'] = f"{request.form['position']}"
    with open(f"{request.form['cssPath']}/props.json", "w", encoding="utf-8") as f:
        json.dump(props, f)
    with open(f"{request.form['cssFile']}", "a", encoding="utf-8") as f:
        f.write(rule)
  
  elif request.form['catg'] == "z-index":
    rule = (f"\n#{request.form['id']}""{"
      f"\n\tz-index:{request.form['z-index']};"
    "\n}")
    if props.get(f"#{request.form['id']}") is None:
      props[f"#{request.form['id']}"] = {}
    
    props[f"#{request.form['id']}"]['z-index'] = f"{request.form['z-index']}"
    with open(f"{request.form['cssPath']}/props.json", "w", encoding="utf-8") as f:
        json.dump(props, f)
    with open(f"{request.form['cssFile']}", "a", encoding="utf-8") as f:
        f.write(rule)
  
  elif request.form['catg'] == "overflow":
    rule = (f"\n#{request.form['id']}""{"
      f"\n\toverflow:{request.form['overflow']};"
    "\n}")
    if props.get(f"#{request.form['id']}") is None:
      props[f"#{request.form['id']}"] = {}
    
    props[f"#{request.form['id']}"]['overflow'] = f"{request.form['overflow']}"
    with open(f"{request.form['cssPath']}/props.json", "w", encoding="utf-8") as f:
        json.dump(props, f)
    with open(f"{request.form['cssFile']}", "a", encoding="utf-8") as f:
        f.write(rule)
  
  elif request.form['catg'] == "float":
    rule = (f"\n#{request.form['id']}""{"
      f"\n\tfloat:{request.form['float']};"
    "\n}")
    if props.get(f"#{request.form['id']}") is None:
      props[f"#{request.form['id']}"] = {}
    
    props[f"#{request.form['id']}"]['float'] = f"{request.form['float']}"
    with open(f"{request.form['cssPath']}/props.json", "w", encoding="utf-8") as f:
        json.dump(props, f)
    with open(f"{request.form['cssFile']}", "a", encoding="utf-8") as f:
        f.write(rule)
  
  elif request.form['catg'] == "opacity":
    rule = (f"\n#{request.form['id']}""{"
      f"\n\topacity:{request.form['opacity']};"
    "\n}")
    if props.get(f"#{request.form['id']}") is None:
      props[f"#{request.form['id']}"] = {}
    
    props[f"#{request.form['id']}"]['opacity'] = f"{request.form['opacity']}"
    with open(f"{request.form['cssPath']}/props.json", "w", encoding="utf-8") as f:
        json.dump(props, f)
    with open(f"{request.form['cssFile']}", "a", encoding="utf-8") as f:
        f.write(rule)
  
  return ""


@app.route("/setClass", methods=["POST"])
def setClass():
    
    request.form['element'] = (request.form['element']).replace("class", "className")
    for file in os.scandir(request.form['htmlPath']):
        if file.name.endswith("js") or file.name.endswith("jsx"):
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


@app.route("/setID", methods=["POST"])
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
