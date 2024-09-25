function getColor(i){
    return 'c-' + (i+1).toString().padStart(2, '0');
}
function createTitle(data){
    var html = '<div class="start">' + data + '</div>';
    return html;
}
function createSelector(list){
    var columns = '';
    for(var i=0,m=list.length; i<m; i++){
        if(i % 4 == 0){
            columns += '<div class="selector-row">';
        }
        var title = list[i].title;
        var color = list[i].enable ? getColor(i) : 'c-disabled';
        var valid = list[i].enable ? 1 : 0
        columns += '<div class="selector-column"><div class="panel '+ color +'" data-i="'+ i +'" data-valid="'+ valid+'">'+ title +'</div></div>'
        if(i % 4 == 3){
            columns += '</div>';
        }
    }
    var html = '<div class="selector">'
             +     '<div class="selector-table">'
             +       columns
             +     '</div>'
             + '</div>'
    return html;
}
function createQuestion(q){
    var html = '<div class="question">'
             +     '<div class="text-area">'
             +         '<div class="category ' + getColor(q.index) +'">'+ q.title +'</div>'
             +         '<div class="text">' + q.question + '</div>'
             +     '</div>'
             + '</div>';
    return html;
}
function createAnswer(answer){
    var html = '<div class="result">'
             +     '<div class="result-header">正解は...</div>'
             +     '<div class="result-body">'
             +         '<div class="answer-text">'+ answer.text +'</div>'
             +     '</div>'
             + '</div>'
    return html;
}
function createMessage(data){
    var html = '<div class="message">'
             +     '<div class="message-header">' + data.title + '</div>'
             +     '<div class="message-body">' + data.message + '</div>'
             + '</div>'
    return html;
}

function updateDisplay(msg, container){
    //container.insertAdjacentHTML();
    var content = "";
    if(msg.type == "START"){
        content = createTitle(msg.data);
    }
    if(msg.type == "SELECT"){
        content = createSelector(msg.data);
    }
    if(msg.type == "QUESTION"){
        content = createQuestion(msg.data);
    }
    if(msg.type == "ANSWER"){
        content = createAnswer(msg.data);
    }
    if(msg.type == "MESSAGE"){
        content = createMessage(msg.data);
    }
    container.innerHTML = content;
}

function init(){
    //var Result = {save : save_storage, restore : load_storage }
    const QUIZ_NS = '/quiz_master'; 
    console.log(location.port);
    //var socket = io.connect('https://' + document.domain + ':' + location.port + QUIZ_NS);
    var socket = io.connect('https://' + document.domain + QUIZ_NS);
    var container = document.getElementById("playground");
    var state;

    socket.on('master_response', function(data){
        console.log(data);
        state = data.type;
        updateDisplay(data , container)
        if(state == "SELECT"){
            Array.prototype.forEach.call(document.querySelectorAll(".panel"), function(item){
                if(item.dataset.valid == 1){
                    var q_id = item.dataset.i;
                    item.addEventListener("click",function(e){
                        console.log("click panel");
                        socket.emit('master_select', {"id": q_id});
                    });
                }
            });
        }
    });
    socket.on('connect', function(){
        console.log("connected");
        socket.emit('master_ready', {});
    });
    var next = function(e){
        var btn = e.currentTarget;
        btn.disabled = true;
        console.log(state);
        if(state !== "SELECT"){
            socket.emit('master_next', {});
        }
        setTimeout(function(){ btn.disabled = false; }, 2000);
    }
    document.getElementById("quiz-next").addEventListener("click", next);
}
