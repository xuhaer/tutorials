* JavaScript 能够改变任意 HTML 元素的大多数属性,如:

```js
x=document.getElementById("demo")
x.style.color='red'
```



* JavaScript 函数和事件

  通常，我们需要在某个事件发生时执行代码，比如当用户点击按钮时。

  如果我们把 JavaScript 代码放入函数中，就可以在事件发生时调用该函数。

  ```html
  <button onclick="myFunction()">点击这里</button>
  <script>
  function myFunction(){
      //使用 document.write() 仅仅向文档输出写内容,如果在文档已完成加载后执行 document.write，整个 HTML 页面将被覆盖
      document.write("糟糕！文档消失了。");
  }
  </script>
  ```

  ​

* 比较运算符

  ```js
  x = 5
  == #等于 x==5 为true, x=='5'为true
  === #全等(值、类型) x===5为true, x==='5'为fals
  ```
  ​

* 逻辑运算符

  ```js
  && #and
  || #or
  ! #not
  ```



* 条件运算符

  ```js
  variablename=(condition)?value1:value2 
  greeting=(time=="morning")?"good moring ":"afternoon ";
  ```

  ​

* Switch 语句

  ```js
  var day=new Date().getDay();
  switch (day)
  {
  case 0: # if day === 0
    x="Today it's Sunday";
    break;
  case 6:
    x="Today it's Saturday";
    break
  default:
    //case 0 和 case 1 均不满足时执行的代码
    x = "Today it's weekday"
  }
  ```

  ​

* JavaScript 错误

  ```js
  try 语句测试代码块的错误。
  catch 语句处理错误。
  throw 语句创建自定义错误。
  ```

  ​

* JavaScript 表单验证

  JavaScript 可用来在数据被送往服务器前对 HTML 表单中的这些输入数据进行验证。

  被 JavaScript 验证的这些典型的表单数据有：

  - 用户是否已填写表单中的必填项目？
  - 用户输入的邮件地址是否合法？
  - 用户是否已输入合法的日期？
  - 用户是否在数据域 (numeric field) 中输入了文本？

  ​

* onload 和 onunload 事件

  onload 和 onunload 事件会在用户进入或离开页面时被触发。

  onload 事件可用于检测访问者的浏览器类型和浏览器版本，并基于这些信息来加载网页的正确版本。

  ​

* onchange 事件

  当离开输入字段时，触发

  onchange 事件常结合对输入字段的验证来使用。

  ​



* onmouseover 和 onmouseout 事件

  onmouseover 和 onmouseout 事件可用于在用户的鼠标移至 HTML 元素上方或移出元素时触发函数。

  ​



* onmousedown、onmouseup 以及 onclick 事件

  onmousedown, onmouseup 以及 onclick 构成了鼠标点击事件的所有部分。首先当点击鼠标按钮时，会触发 onmousedown 事件，当释放鼠标按钮时，会触发 onmouseup 事件，最后，当完成鼠标点击时，会触发 onclick 事件。



* onfocus

  当输入字段获得焦点时，触发onfocus事件。



* JavaScript 是面向对象的语言，但 JavaScript 不使用类。在 JavaScript 中，不会创建类，也不会通过类来创建对象



* JavaScript 只有一种数字类型。JavaScript 中的所有数字都存储为根为 10 的 64 位（8 比特），浮点数。

  所以浮点运算并不总是 100% 准确:

  ```js
  x = 0.2+0.1; # 0.30000000000000004
  ```

  ​

* 八进制和十六进制

  如果前缀为 0，则 JavaScript 会把数值常量解释为八进制数，如果前缀为 0 和 "x"，则解释为十六进制数。

  **提示：绝不要在数字前面写零，除非您需要进行八进制转换。**



* 在JavaScript的世界中，所有代码都是单线程执行的。

  由于这个“缺陷”，导致JavaScript的所有网络操作，浏览器事件，都必须是异步执行。异步执行可以用回调函数实现：

  ```js
  function callback() {
      console.log('Done');
  }
  console.log('before setTimeout()');
  setTimeout(callback, 1000); // 1秒钟后调用callback函数
  console.log('after setTimeout()');

  /* 结果：
  before setTimeout()
  after setTimeout()
  (等待1秒后)
  Done
  */
  ```

  ​



