function sleep(waitSec, callbackFunc) {
    var spanedSec = 0;
    var id = setInterval(function () {
        spanedSec++;
        if (spanedSec >= waitSec) {
            clearInterval(id);
            if (callbackFunc) callbackFunc();
        }
    }, 1000);
}

function clearNode(elem){
    var clone = elem.cloneNode(false);
    elem.parentNode.replaceChild(clone, elem);
    return clone;
}

function hide(target){
    var elem = document.getElementById(target);
    if(elem.classList.contains('visible')){
        elem.classList.remove('visible')
    }
}

function show(target){
    document.getElementById(target).classList.add("visible");
}

function scrollTop(){
    document.body.scrollTop = 0;
}

function __fetch(method, url, params, callback) {
    try {
        let xhr = new XMLHttpRequest();
        xhr.onload = function(){
              if (xhr.readyState === 4 && xhr.status === 200) {
                  callback(xhr.responseText);
              } else {
                  console.log(xhr.statusText);
              }
          };
        xhr.onerror = () => {
            console.log(xhr.statusText);
        };
        xhr.open(method, url, true);
        if(params != null){
            xhr.setRequestHeader("Content-Type", "application/json");
            params = JSON.stringify(params);
        }
        xhr.send(params);
    } catch(error){
        console.log(error);
    }
}

function post(url,params,callback){
    __fetch('POST',url, params, function(response){callback(JSON.parse(response));});
}

function get(url, callback){
    __fetch('GET', url, null, function(response){ return callback(JSON.parse(response));});
}
function layer_init(){
    Array.prototype.forEach.call(document.querySelectorAll(".layer-control"), function(item){
        item.addEventListener("click",function(e){
            var data = e.currentTarget.dataset;
            var action = data.action;
            if(action == "hide"){
                hide(data.for);
            }
            if(action == "show"){
                show(data.for);
            }
        });
    });
}
