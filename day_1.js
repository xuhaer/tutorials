'use strict';

//function (x) { ... }是一个匿名函数,赋值给了abs,末尾需要在函数体尾加一个';',表示赋值语句结束。
//rest参数只能写在最后，前面用...标识
var abs = function (num, ...rest) {
    //关键字arguments，它只在函数内部起作用，并且永远指向当前函数的调用者传入的所有参数。
    if (arguments.length === 0) {
        return 0;
    }
    else if (arguments.length >= 2) {
        console.log('rest: ' + rest);
    }
    var x = arguments[0];
    return x >= 0 ? x : -x; //x >=0 取x, 否则取 -x
};
// 由于JavaScript允许传入任意个参数而不影响调用，因此传入的参数比定义的参数多也没有问题，虽然函数内部并不需要这些参数；传入的参数比定义的少也没有问题。
console.log('abs: ' + abs(1,2,3)); 


// JavaScript的函数定义有个特点，它会先扫描整个函数体的语句，把所有申明的变量“提升”到函数顶部, 但不会提升变量y的赋值:
//所以，请严格遵守“在函数内部首先申明所有变量”这一规则
function foo() {
    var x = '变量提升: Hello, ' + y;
    console.log(x);//Hello, undefined
    var y = 'Bob';
}
// var y = 'Bob'; //如果放在这，注释掉上面 y的赋值，foo()不会报错
foo();

/*
作用域:
由于JavaScript的变量作用域实际上是函数内部，我们在for循环等语句块中是无法定义具有局部作用域的变量的。
为了解决块级作用域，ES6引入了新的关键字let，用let替代var可以申明一个块级作用域的变量。
ES6标准引入了新的关键字const来定义常量，const与let都具有块级作用域。
没有var 定义的变量JavaScript会将其当做全局变量
*/


