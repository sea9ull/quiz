function LocalStorage(){
    this.__storage = window.localStorage ? window.localStorage : null
}

LocalStorage.prototype.save = function(key, value){
    if(this.__storage){
        try{
            this.__storage.setItem(key, JSON.stringify(value));
        }catch(e){
            console.log(e);
        }
    }
}

LocalStorage.prototype.load = function(key){
    var response = {};
    if(this.__storage){
        var item = this.__storage.getItem(key);
        if(item != null){
            try{
                response = JSON.parse(item);
            }catch(e){
                console.log(e);
            }
        }
    }
    return response;
}

var storage = new LocalStorage();
var key = "quiz_game"
function save_storage(value){
    try{
        storage.save(key, value);
    }catch(error){
        console.log(error)
    }
}
function load_storage(){
    return storage.load(key);
}
