function IfSimpleNumber(num=0){
    if (num <=1000 && num > 1) {
        let b = 2
        for (let i = 2; i < num; i++) {
    
            if (num % i != 0){
               b++
            }
            if (b==num){
                return true
            }
        }
        return false
    } else{
        return 'Error, the number cannot exceed 1000 or be equal to 1 or 0, and must be a natural number'
    }


}

console.log(IfSimpleNumber(11))