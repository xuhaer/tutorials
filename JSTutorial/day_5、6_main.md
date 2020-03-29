*  要引入其他模块输出的对象，用：

  ```js
  var foo = require('./day_5_hello');

  foo('许某')
  // node.js的import不会搞，算了
  ```



因为Node.js是运行在服务区端的JavaScript环境，服务器程序和浏览器程序相比，最大的特点是没有浏览器的安全限制了，而且，服务器程序必须能接收网络请求，读写文件，处理二进制内容，所以，Node.js内置的常用模块就是为了实现基本的服务器功能。这些模块在浏览器环境中是无法被执行的，因为它们的底层代码是用C/C++在Node.js运行环境中实现的。

* global

   JavaScript有且仅有一个全局对象，在浏览器中，叫window对象。而在Node.js环境中，也有唯一的全局对象，但不叫window，而叫global。

  ```bash
  > global.console
  Console {
    log: [Function: bound consoleCall],
    debug: [Function: bound consoleCall],
    info: [Function: bound consoleCall],
    dirxml: [Function: bound consoleCall],
    warn: [Function: bound consoleCall],
    error: [Function: bound consoleCall],
    dir: [Function: bound consoleCall],
    time: [Function: bound consoleCall],
    timeEnd: [Function: bound consoleCall],
    trace: [Function: bound consoleCall],
    assert: [Function: bound consoleCall],
    clear: [Function: bound consoleCall],
    count: [Function: bound consoleCall],
    ...
  ```



* process

  `process`也是Node.js提供的一个对象，它代表当前Node.js进程:

  ```bash
  > process === global.process;
  true
  > process.version;
  'v10.1.0'
  > process.platform;
  'darwin'
  > process.arch;
  'x64'
  > process.cwd(); //返回当前工作目录
  '/Users/har/git/node_js_tutorial'
  > process.chdir('/private/tmp'); // 切换当前工作目录
  undefined
  > process.cwd();
  '/private/tmp'
  ```



* 判断js执行环境

  有很多JavaScript代码既能在浏览器中执行，也能在Node环境执行，常用的方式就是根据浏览器和Node环境提供的全局变量名称来判断：

  ```js
  if (typeof(window) === 'undefined') {
      console.log('node.js');
  } else {
      console.log('browser');
  }
  ```



* fs模块

  Node.js内置的`fs`模块就是文件系统模块，负责读写文件。

  和所有其它JavaScript模块不同的是，`fs`模块同时提供了异步和同步的方法。

  * 异步读取文件

    ```js
    'use strict';

    var fs = require('fs');

    fs.readFile('sample.txt', 'utf-8', function (err, data) {
        if (err) {
            console.log('fail');
        } else {
            console.log('success');
        }
    });
    ```

    异步读取时，传入的回调函数接收两个参数，当正常读取时，`err`参数为`null`，`data`参数为读取到的String。当读取发生错误时，`err`参数代表一个错误对象，`data`为`undefined`。这也是Node.js标准的回调函数：第一个参数代表错误信息，第二个参数代表结果。

    ​

    当读取二进制文件时，不传入文件编码时，回调函数的`data`参数将返回一个`Buffer`对象。

    `Buffer`对象可以和String作转换，例如，把一个`Buffer`对象转换成String：

    ```js
    var text = data.toString('utf-8');
    console.log(text);
    ```

    或者把一个String转换成`Buffer`：

    ```js
    var buf = Buffer.from(text, 'utf-8');
    console.log(buf);
    ```

    ​

  * 同步读取文件

    同步读取的函数和异步函数相比，多了一个Sync后缀，并且不接收回调函数，函数直接返回结果(需要用`try...catch`捕获该错误)

    ```js
    'use strict';

    var fs = require('fs');

    var data = fs.readFileSync('sample.txt', 'utf-8');
    console.log(data);
    ```

    ​

  * 写文件: fs.writeFile()

    ```js
    'use strict';

    var fs = require('fs');

    var data = 'Hello, Node.js';
    fs.writeFile('output.txt', data, function (err) {
        if (err) {
            console.log(err);
        } else {
            console.log('ok.');
        }
    });
    ```

    `writeFile()`的参数依次为文件名、数据和回调函数。如果传入的数据是String，默认按UTF-8编码写入文本文件，如果传入的参数是`Buffer`，则写入的是二进制文件。回调函数由于只关心成功与否，因此只需要一个`err`参数。

    和`readFile()`类似，`writeFile()`也有一个同步方法，叫`writeFileSync()`：

    ```js
    'use strict';

    var fs = require('fs');

    var data = 'Hello, Node.js';
    fs.writeFileSync('output.txt', data);
    ```

    ​

  * stat

    获取文件大小，创建时间等信息，可以使用`fs.stat()`，它返回一个`Stat`对象，能告诉我们文件或目录的详细信息。

    ​

  * 异步还是同步

    fs模块中，提供同步方法是为了方便使用。

    由于Node环境执行的JavaScript代码是服务器端代码，所以，绝大部分需要在服务器运行期反复执行业务逻辑的代码，*必须使用异步代码*，否则，同步代码在执行时期，服务器将停止响应，因为JavaScript只有一个执行线程。

    ​