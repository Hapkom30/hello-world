function EvenArray(arr=[]){

    let i = 0
    let notEven = 0
    let even = 0

    if (arr!=[]){

        while (i < arr.length){
            even = (arr[i]%2==0 && typeof(arr[i])=='number')? even + 1: even
            notEven = (arr[i]%2!=0 && typeof(arr[i])=='number')? notEven + 1: notEven
            if (arr[i]==null || arr[i]=='' || arr[i]==NaN || typeof(arr[i])=='undefined'){
                console.log(`${arr[i]} - ${typeof(arr[i])} is null object`)
            }
            i++
        }

        console.log(`${even} Even and ${notEven} NotEven`)

    } else{

        console.log("Your's array is null")

    }
}



ars = [1,2,3,4,5,6,7,8,'!','4','str','',null]
EvenArray(ars);
