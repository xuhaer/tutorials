function hello(name) {
    // body...
    console.log('Hello' + name + '!')
}

// 要在模块中对外输出变量，用：
// module.exports = variable;
// 输出的变量可以是任意对象、函数、数组等等。
module.exports = hello