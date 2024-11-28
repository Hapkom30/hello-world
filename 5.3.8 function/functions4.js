function Iteratioins(start, exit) {
    let num = start;

    let timerId = setInterval(function() {
        console.log(num);
        if (num == exit) {
            clearInterval(timerId);
        }
        num++;
    }, 1000);
}

Iteratioins(5, 17);