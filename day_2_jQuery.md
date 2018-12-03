#### jQuery

jQuery这么流行，肯定是因为它解决了一些很重要的问题。实际上，jQuery能帮我们干这些事情：

- 消除浏览器差异：你不需要自己写冗长的代码来针对不同的浏览器来绑定事件，编写AJAX等代码；
- 简洁的操作DOM的方法：写`$('#test')`肯定比`document.getElementById('test')`来得简洁；
- 轻松实现动画、修改CSS等各种操作。

jQuery的理念“Write Less, Do More“，让你写更少的代码，完成更多的工作！



* **$符号**

  `$`是著名的jQuery符号。实际上，jQuery把所有功能全部封装在一个全局变量`jQuery`中，而`$`也是一个合法的变量名，它是变量`jQuery`的别名：

  ```js
  window.jQuery; // jQuery(selector, context)
  window.$; // jQuery(selector, context)
  $ === jQuery; // true
  typeof($); // 'function'
  ```

  ​

* **选择器**

  选择器是jQuery的核心。一个选择器写出来类似`$('#dom-id')`。

  jQuery的选择器就是帮助我们快速定位到一个或多个DOM节点。

  * 按ID查找

    如果某个DOM节点有`id`属性，利用jQuery查找如下：

    ```js
    // 查找<div id="abc">:
    var div = $('#abc'); //返回的对象是jQuery对象。jQuery对象类似数组，它的每个元素都是一个引用了DOM节点的对象。
    ```

  * 按tag查找

    ```js
    var ps = $('p'); // 返回所有<p>节点
    ps.length; // 数一数页面有多少个<p>节点
    ```

  * 按class查找

    ```js
    var a = $('.red'); // 所有节点包含`class="red"`都将返回
    ```

    通常很多节点有多个class，我们可以查找同时包含`red`和`green`的节点：

    ```js
    var a = $('.red.green'); // 注意没有空格！
    // 符合条件的节点：
    // <div class="red green">...</div>
    // <div class="blue green red">...</div>
    ```

  * 按属性查找

    ```js
    var email = $('[name=email]'); // 找出<??? name="email">
    var passwordInput = $('[type=password]'); // 找出<??? type="password">
    var a = $('[items="A B"]'); // 找出<??? items="A B">
    ```

    当属性的值包含空格等特殊字符时，需要用双引号括起来。

    按属性查找还可以使用前缀查找或者后缀查找：

    ```js
    var icons = $('[name^=icon]'); // 找出所有name属性值以icon开头的DOM
    // 例如: name="icon-1", name="icon-2"
    var names = $('[name$=with]'); // 找出所有name属性值以with结尾的DOM
    // 例如: name="startswith", name="endswith"
    ```

  * 组合查找

    如果我们查找`$('[name=email]')`，很可能把表单外的`<div name="email">`也找出来，但我们只希望查找`<input>`，就可以这么写：

    ```js
    var emailInput = $('input[name=email]'); // 不会找出<div name="email">
    ```

    同样的，根据tag和class来组合查找也很常见：

    ```js
    var tr = $('tr.red'); // 找出<tr class="red ...">...</tr>
    ```

  * 多项选择器

    ```js
    //多项选择器就是把多个选择器用,组合起来一块选：
    $('p,div'); // 把<p>和<div>都选出来
    $('p.red,p.green'); // 把<p class="red">和<p class="green">都选出来
    ```

    要注意的是，选出来的元素是按照它们在HTML中出现的顺序排列的，而且不会有重复元素。例如，`<p class="red green">`不会被上面的`$('p.red,p.green')`选择两次。

