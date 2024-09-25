function checkFormat(){
    var answer = [];
    Array.prototype.some.call(document.querySelectorAll(".answer-column"), function(item){
        var dataType = item.dataset.type;
        if(item.validity.patternMismatch || item.validity.valueMissing){
            return [];
        }
        answer.push(item.value);
    });
    return answer;
}

function createQuestion(q){
    function createInput(q){
        var iType = q.type == "num" ? "number" : "text";
        var pattern = "";
        var placeholder = "";
        var errorMsg = "";
        var id = q.id;
        if(q.type == "num"){
            placeholder = ' required placeholder="数字"';
            errorMsg = '数字で回答してください';
        }
        if(q.type == "any"){
            pattern = ' pattern="^.+$" required';
            placeholder = ' placeholder="文章"';
            errorMsg = '回答が不正です'
        }
        var html = '<div class="input-column">'
                 +     '<div class="input-group">'
                 +         '<label>' + q.label + '</label>'
                 +         '<input type="' + iType + '" class="input-answer answer-column" name="'+ id +'"'
                 +            pattern + placeholder +'/>'
                 +         '<span class="input-error">'+ errorMsg +'</span>'
                 +     '</div>'
                 + '</div>';
        return html;
    }
    function makeQuestion(q){
        var inputs = "";
        for(var i =0, m=q.columns.length; i<m; i++){
            inputs += createInput(q.columns[i])
        }
        var context = q.context ? '<div class="context">' +context + '</div>' : "";
        var html = '<div class="content content-default" id="BLOCK_'+ q.id +'">'
                 +      '<h3 class="quiz-title">'+ q.title + '</h3>'
                 +      '<div class="answer-area">'
                 +        inputs
                 +      '</div>'
                 +      context
                 + '</div>';
        return html;
    }
    return makeQuestion(q);
}

function createResult(data){
    var color = data.result ? "red" : "blue";
    var title = data.result ? "《正解》" : "《不正解》";
    var symbol = data.result ? "correct" : "incorrect";
    var answer = data.text;
    var html = '<div class="content content-'+ color +'">'
             +     '<h3 class="content-h">'+ title +'</h3>'
             +     '<div class="symbol"><img src="/resources/blob/symbol.svg#' + symbol + '" width="100%"/></div>'
             +     '<div class="content-text">答: '+ answer +'</div>'
             + '</div>'
    return html
}

function createMessage(m){
    var html = '<div class="content content-default">'
             +   '<div class="title">' + m.title + '</div>'
             +   '<div class="message">' + m.message + '</div>'
             + '</div>'
    return html;
}

function updateDisplay(msg, container){
    //container.insertAdjacentHTML();
    var content = "";
    hide("bt-area");
    if(msg.type == "QUESTION"){
        content = createQuestion(msg.data)
        show("bt-area");
    }
    if(msg.type == "ANSWER"){
        content = createResult(msg.data)
    }
    if(msg.type == "MESSAGE"){
        content = createMessage(msg.data)
    }
    container.innerHTML = content;
}

function init(){
    //var Result = {save : save_storage, restore : load_storage }
    const QUIZ_NS = '/quiz'; 
    //var socket = io.connect('https://' + document.domain + ':' + location.port + QUIZ_NS);
    var socket = io.connect('https://' + document.domain + QUIZ_NS);
    var container = document.getElementById("playground");
    socket.on('response', function(data){
        console.log("response")
        console.log(data);
        updateDisplay(data , container)
    });
    socket.on('connect', function(){
        console.log("connected");
        socket.emit('ready', {});
    });
    var submit = function(e){
        var data = e.target.dataset;
        var answer = checkFormat();
        if(answer.length > 0){
            console.log("submit");
            socket.emit('answer', {"answer": answer});
            socket.emit('ready', {});
        }
        return false;
    };
    document.getElementById("submit-question").addEventListener("click", submit);
}
