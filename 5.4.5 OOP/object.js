function GetKeyObjectHasOwnProperty(obj){
    for (let key in obj){
        if (obj.hasOwnProperty(key)){
            console.log(key)
        }
    }
}

function IfKeyObject(str, obj){
    for (let key in obj){
        if (key==str){
            return true
        }
    }
    return false
}

function CreateObject(){
    return new Object();
}

const objPerson = {
    contry: 'Russian'
}
const objPeople = Object.create(objPerson);
objPeople.name = 'Ivan'
objPeople.age = '18'
GetKeyObjectHasOwnProperty(objPeople);
console.log(IfKeyObject('contry',objPeople))
const testObj = CreateObject();
console.log(testObj)
