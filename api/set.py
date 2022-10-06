from flask import Blueprint, request
import json


bp = Blueprint('set', __name__)

@bp.route("/", methods=["POST"])
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