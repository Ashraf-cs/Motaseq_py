window.addEventListener("message", (event) => {
    if(event.data[0] == "element"){
        if(!event.data[1] && event.data[2]) {
            try{
                
                let set_id;
                set_id = (event.data[5]) ? event.data[5] : `id${Math.random().toString().slice(2,8)}`
                document.getElementById("id").value = set_id
                fetch('/api/ids/setID', {method: "POST", headers: {"Accept": "appliceation/x-www-form-urlencoded", 
                "content-type": "application/x-www-form-urlencoded"}, 
                body: `htmlPath=${localStorage.getItem("htmlPath")}&element=${event.data[3]}&id=${set_id}`})
                let ClassName = document.getElementsByClassName("id");
                for(let i=0; i<ClassName.length; i++){
                    ClassName[i].value = set_id
                }
                
                let match = (event.data[3]).match(/data-id=[0-9\'\"]*/g)[0]
                let setId = (event.data[3]).replace(match, match + ` id="${set_id}"`)
                localStorage.setItem("element", setId)

            }catch{}
        }else if(event.data[0] == "updatedOuter"){

            localStorage.setItem("element", event.data[3])

        }else{

            document.getElementById("id").value = (event.data[1]);
            let ClassName = document.getElementsByClassName("id");
            for(let i=0; i<ClassName.length; i++){
                ClassName[i].value = event.data[1]
                localStorage.setItem("element", event.data[3])
            }

        }
        
        document.getElementById("tag").value = String((event.data[2])).toLowerCase(); 
    
        let TagName = document.getElementsByClassName("TagName");  
        for(let i=0; i<TagName.length; i++){
          TagName[i].value = String((event.data[2])).toLowerCase();
        }  
    
        for(let x in event.data[4]){
            if(event.data[4][x].search("px") != -1){
                try{
                    document.getElementById(`${x}`).value = Number(event.data[4][x].replace("px",""))
                }catch{}
            }else{
                try{
                    document.getElementById(`${x}`).value = event.data[4][x]
                }catch{}
            }
        }
    }
    else if(event.data[0] == "updatedOuter"){
        localStorage.setItem("element", event.data[1])
    }
    
})

let cssPath = document.getElementsByClassName("cssPath");
for(let i=0; i<cssPath.length; i++){
    cssPath[i].value = localStorage.getItem("cssPath")
}

let cssFile = document.getElementsByClassName("cssFile");
for(let i=0; i<cssFile.length; i++){
cssFile[i].value = localStorage.getItem("cssFile")
}

document.getElementById("server").innerHTML = "localhost:" + localStorage.getItem('port')
document.getElementById("iframe").src = "http://localhost:" + localStorage.getItem('port');
document.body.style.overflow = "hidden";


// margins direction
if(document.getElementById("margin-all").checked){
    document.getElementById("margin-c-field").setAttribute("disabled", "true")
    document.getElementById("margin-c-field").setAttribute("hidden", "true")
}
document.getElementById("margin-all").addEventListener("click", () => {
    document.getElementById("margin-all-field").removeAttribute("disabled")
    document.getElementById("margin-all-field").removeAttribute("hidden")
    document.getElementById("margin-c-field").setAttribute("disabled", "true")
    document.getElementById("margin-c-field").setAttribute("hidden", "true")
    document.getElementById("margin-c").removeAttribute("checked")
})
document.getElementById("margin-c").addEventListener("click", () => {
    document.getElementById("margin-all-field").setAttribute("disabled", "true")
    document.getElementById("margin-all-field").setAttribute("hidden", "true")
    document.getElementById("margin-c-field").removeAttribute("disabled")
    document.getElementById("margin-c-field").removeAttribute("hidden")
    document.getElementById("margin-all").removeAttribute("checked")
})


// padding direction
if(document.getElementById("padding-all").checked){
    document.getElementById("padding-c-field").setAttribute("disabled", "true")
    document.getElementById("padding-c-field").setAttribute("hidden", "true")
}
document.getElementById("padding-all").addEventListener("click", () => {
    document.getElementById("padding-all-field").removeAttribute("disabled")
    document.getElementById("padding-all-field").removeAttribute("hidden")
    document.getElementById("padding-c-field").setAttribute("disabled", "true")
    document.getElementById("padding-c-field").setAttribute("hidden", "true")
    document.getElementById("padding-c").removeAttribute("checked")
})
document.getElementById("padding-c").addEventListener("click", () => {
    document.getElementById("padding-all-field").setAttribute("disabled", "true")
    document.getElementById("padding-all-field").setAttribute("hidden", "true")
    document.getElementById("padding-c-field").removeAttribute("disabled")
    document.getElementById("padding-c-field").removeAttribute("hidden")
    document.getElementById("padding-all").removeAttribute("checked")
})


// font size types
if(document.getElementById("fs-type-c").checked){
    document.getElementById("font-size-pre").setAttribute("disabled", "true")
}
document.getElementById("fs-type-pre").addEventListener("click", () => {
    document.getElementById("font-size-pre").removeAttribute("disabled")
    document.getElementById("font-unit").setAttribute("disabled", "true")
    document.getElementById("font-size").setAttribute("disabled", "true")
})
document.getElementById("fs-type-c").addEventListener("click", () => {
    document.getElementById("font-unit").removeAttribute("disabled")
    document.getElementById("font-size").removeAttribute("disabled")
    document.getElementById("font-size-pre").setAttribute("disabled", "true")
})


// background size types
if(document.getElementById("background-size-type-pre").checked){
    document.getElementById("background-size-c-field").setAttribute("disabled", "true")
    document.getElementById("background-size-c-field").setAttribute("hidden", "true")
}
document.getElementById("background-size-type-pre").addEventListener("click", () => {
    document.getElementById("background-size-pre-field").removeAttribute("disabled")
    document.getElementById("background-size-pre-field").removeAttribute("hidden")
    document.getElementById("background-size-c-field").setAttribute("disabled", "true")
    document.getElementById("background-size-c-field").setAttribute("hidden", "true")
})
document.getElementById("background-size-type-c").addEventListener("click", () => {
    document.getElementById("background-size-pre-field").setAttribute("disabled", "true")
    document.getElementById("background-size-pre-field").setAttribute("hidden", "true")
    document.getElementById("background-size-c-field").removeAttribute("disabled")
    document.getElementById("background-size-c-field").removeAttribute("hidden")
})


// outline width type
if(document.getElementById("outline-width-type-pre").checked){
    document.getElementById("outline-width-c-field").setAttribute("disabled", "true");
    document.getElementById("outline-width-c-field").setAttribute("hidden", "true");
}
document.getElementById("outline-width-type-pre").addEventListener("click", () => {
    document.getElementById("outline-width-pre-field").removeAttribute("disabled");
    document.getElementById("outline-width-pre-field").removeAttribute("hidden");
    document.getElementById("outline-width-c-field").setAttribute("disabled", "true");
    document.getElementById("outline-width-c-field").setAttribute("hidden", "true");
})
document.getElementById("outline-width-type-c").addEventListener("click", () => {
    document.getElementById("outline-width-c-field").removeAttribute("disabled");
    document.getElementById("outline-width-c-field").removeAttribute("hidden");
    document.getElementById("outline-width-pre-field").setAttribute("disabled", "true");
    document.getElementById("outline-width-pre-field").setAttribute("hidden", "true");
})

////////////////////////////////////////////////////////////////////////////

function setAllBorder(){
    toTargetFrame(document.getElementById("id").value,"border", document.getElementById("border").value + document.getElementById("borders-unit").value)
    toTargetFrame(document.getElementById("id").value,"border-style", document.getElementById("border-style").value);
    toTargetFrame(document.getElementById("id").value,"border-color", document.getElementById("border-color").value);
    fetch('/api/set', {method: "POST", headers: {'Accept': 'application/x-www-form-urlencoded',
    'Content-Type': 'application/x-www-form-urlencoded'}, body: `catg=border-all&id=${document.getElementById("id").value}&` +
    `cssFile=${localStorage.getItem("cssFile")}&cssPath=${localStorage.getItem("cssPath")}&border=${document.getElementById("border").value}&` +
    `border-style=${document.getElementById("border-style").value}&borders-unit=${document.getElementById("borders-unit").value}&border-color=${document.getElementById("border-color").value}`})
}


function setClass(name){
    name = name.replace(".", "")
    fetch('/api/classes/setClass', {method: "POST", headers: {'Accept': 'application/x-www-form-urlencoded',
    'Content-Type': 'application/x-www-form-urlencoded'},
     body: `htmlPath=${localStorage.getItem('htmlPath')}&id=${document.getElementById("id").value}&class=${name}&element=${localStorage.getItem("element")}`})
  }


function updateOuter(id){

    if((localStorage.getItem("element")).indexOf("class") != -1){
        try{let element = localStorage.getItem("element")
            element = element.match(/<[A-z0-9\.\-\#\_\n\t\(\)\+\;\@\{\}\:\'\"\=\,\!\$\%\^\&\*\?\|\/\\ ]*[^\/]>/g)[0]
            let addClass = element.replace('class="', `class="${id} `)
            let setClass = element.replace(element, addClass)
            localStorage.setItem("element", setClass)
        }catch{}
    }
    else{
        let element = localStorage.getItem("element")
        element = element.match(/<[A-z0-9\.\-\#\_\n\t\(\)\+\;\@\{\}\:\'\"\=\,\!\$\%\^\&\*\?\|\/\\ ]*[^\/]>/g)[0]
        let addClass = element.replace(`id="${document.getElementById("id").value}"`, `id="${document.getElementById("id").value}" class="${id}"`)
        let setClass = element.replace(element, addClass)
        localStorage.setItem("element", setClass)
    }
}


function getClasses(){
    fetch('/api/classes/getClasses', {method: "POST", headers: {'Accept': 'application/x-www-form-urlencoded',
      'Content-Type': 'application/x-www-form-urlencoded'}, body: `cssFile=${localStorage.getItem('cssFile')}`})
    .then(res => res.json())
    .then(data => {
        
        let classes = ""
        data.classes.map((class_name, index) => {
            if(class_name != ""){
                classes += `<span class="badge bg-light text-dark me-1" 
                onclick="setClass(event.target.textContent); updateOuter(event.target)">${class_name}</span>` 
            }
        })
        
        document.getElementById("classes").innerHTML = classes
    })
}


function toTargetFrame(id, prop, value ){
    let frameWindow = window.frames[0]
    frameWindow.postMessage(["style",id, prop, value ], "*")
}