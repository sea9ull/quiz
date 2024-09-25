function check_v(val){
    return (val == 1) ? '●' : '';
}
function createScore(data){
    var records = "";
    for(var i=0,m=data.length; i<m; i++){
        records += '<tr>'
                 +   '<td>'+ data[i].name +'</td>'
                 +   '<td>'+ data[i].total +'</td>'
                 +   '<td>'+ check_v(data[i].q1)  +'</td>'
                 +   '<td>'+ check_v(data[i].q2)  +'</td>'
                 +   '<td>'+ check_v(data[i].q3)  +'</td>'
                 +   '<td>'+ check_v(data[i].q4)  +'</td>'
                 +   '<td>'+ check_v(data[i].q5)  +'</td>'
                 +   '<td>'+ check_v(data[i].q6)  +'</td>'
                 +   '<td>'+ check_v(data[i].q7)  +'</td>'
                 +   '<td>'+ check_v(data[i].q8)  +'</td>'
                 +   '<td>'+ check_v(data[i].q9)  +'</td>'
                 +   '<td>'+ check_v(data[i].q10) +'</td>'
                 +   '<td>'+ check_v(data[i].q11) +'</td>'
                 +   '<td>'+ check_v(data[i].q12) +'</td>'
                 + '</tr>';
    }
    var html = '<table class="score">'
             + '<tr>'
             +   '<th>名前</th>'
             +   '<th>計</ht>'
             +   '<th>①</th><th>②</th><th>③</th><th>④</th>'
             +   '<th>⑤</th><th>⑥</th><th>⑦</th><th>⑧</th>'
             +   '<th>⑨</th><th>⑩</th><th>⑪</th><th>⑫</th>'
             + '</tr>'
             +   records
             + '</div>'
    return html;
}

function updateDisplay(data, container){
    //container.insertAdjacentHTML();
    var content = createScore(data.score);
    container.innerHTML = content;
}

function init(){
    var container = document.getElementById("playground");

    document.getElementById("quiz-app-reset").addEventListener("click", function(e){
        post("/api/resetApp", {}, function(res){
            console.log(res);
        });
    });
    document.getElementById("quiz-user-reset").addEventListener("click", function(e){
        post("/api/resetUser", {}, function(res){
            console.log(res);
        });
    });
    document.getElementById("quiz-user-score").addEventListener("click", function(e){
        get("/api/score", function(res){
            console.log(res);
            updateDisplay(res, container);
        });
    });
}
