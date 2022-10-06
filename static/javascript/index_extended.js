setTimeout(loader, 1000)

function setParams(){
    let cssPath = document.getElementById("cssFile").value.replace(/\\/g, "/").replace(/\/[^/]*.css/, "")
    localStorage.setItem("port", document.getElementById("port").value);
    localStorage.setItem("htmlPath", document.getElementById("htmlPath").value);
    localStorage.setItem("cssPath", cssPath);
    localStorage.setItem("cssFile", document.getElementById("cssFile").value);
}


function loader(){
    document.getElementById("loader").style.display = "none";
    document.getElementById("main").style.display = "block";
}


function getPaths(){
    fetch('/api/check')
    .then(res => res.json())
    .then(paths => {
        localStorage.setItem("htmlPath", paths.htmlPath);
        localStorage.setItem("cssFile", paths.cssFile);
        localStorage.setItem("cssPath", paths.cssPath);
        document.getElementById("directory").textContent = paths.htmlPath;
    })
}
