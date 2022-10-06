from flask import Blueprint, request, redirect, url_for
import os, shutil, json, re, random


bp = Blueprint('init', __name__)

@bp.route("/", methods=["POST"])
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
              let style = {};for (let x in cssObj) {let cssObjProp = cssObj.item(x);style[cssObjProp] =\
              cssObj.getPropertyValue(cssObjProp);}let createdId = "";if(!e.target.id)\
              {createdId = "id"+Math.random().toString().slice(2,10);let parentWindow = window.parent;\
              parentWindow.postMessage(["element",e.target.id, e.target.tagName, e.target.outerHTML,\
              style, createdId], "*");e.target.setAttribute("id", createdId);}else{let parentWindow =\
              window.parent;parentWindow.postMessage(["element",e.target.id, e.target.tagName,\
              e.target.outerHTML, style], "*");}};document.body.addEventListener(\'click\', selector);\
              window.addEventListener("message", (event) => {if(event.data[0] == "style")\
              {try{document.querySelector("#"+event.data[1]).style[(event.data[2])] = (event.data[3])}catch{}}else if\
              (event.data[0] == "outerHTML"){try{let outer = document.getElementById(event.data[1]).outerHTML;\
              let parentWindow = window.parent;parentWindow.postMessage(["updatedOuter", outer], "*")}catch{}}})\
              </script></body>'

              # '<script>function selector(e){const cssObj = window.getComputedStyle(e.target, null);'+\
              # 'let style = {};for (let x in cssObj) {let cssObjProp = cssObj.item(x);style[cssObjProp] ='+\
              # 'cssObj.getPropertyValue(cssObjProp);}let createdId = "";if(!e.target.id)'+\
              # '{createdId = "id"+Math.random().toString().slice(2,10);let parentWindow = window.parent;'+\
              # 'parentWindow.postMessage(["element",e.target.id, e.target.tagName, e.target.outerHTML,'+\
              # 'style, createdId], "*");e.target.setAttribute("id", createdId);}else{let parentWindow ='+\
              # 'window.parent;parentWindow.postMessage(["element",e.target.id, e.target.tagName,'+\
              # 'e.target.outerHTML, style], "*");}};document.body.addEventListener(\'click\', selector);'+\
              # 'window.addEventListener("message", (event) => {if(event.data[0] == "style")'+\
              # '{try{document.querySelector("#"+event.data[1]).style[(event.data[2])] = (event.data[3])}catch{}}else if'+\
              # '(event.data[0] == "outerHTML"){try{let outer = document.getElementById(event.data[1]).outerHTML;'+\
              # 'let parentWindow = window.parent;parentWindow.postMessage(["updatedOuter", outer], "*")}catch{}}})'+\
              # '</script></body>'

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