function func1(a){
    return function(b){
        return a+b
    }
}

decFunc = func1(1);
console.log(decFunc(4))