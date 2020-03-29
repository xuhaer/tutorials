## jQuery

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

###选择器

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
    var email = $('[name=email]'); // 找出<xxx name="email">
    var passwordInput = $('[type=password]'); // 找出<xxx type="password">
    var a = $('[items="A B"]'); // 找出<xxx items="A B">
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
    $('p,div'); // 把<p>或<div>都选出来
    $('p.red,p.green'); // 把<p class="red">或<p class="green">都选出来
    ```

    要注意的是，选出来的元素是按照它们在HTML中出现的顺序排列的，而且不会有重复元素。例如，`<p class="red green">`不会被上面的`$('p.red,p.green')`选择两次。

    ​

    ​

* 层级选择器（Descendant Selector）

  如果两个DOM元素具有层级关系，就可以用`$('ancestor descendant')`来选择，层级之间用空格隔开，如：

  ```html
  <div class="testing">
    <ul class="lang">
        <li class="lang-javascript">JavaScript</li>
        <li class="lang-python">Python</li>
        <li class="lang-lua">Lua</li>
    </ul>
  </div>
  ```

  要选出JavaScript，可以用层级选择器：

  ```js
  $('ul.lang li.lang-javascript'); // [<li class="lang-javascript">JavaScript</li>]

  $('div.testing li.lang-javascript'); // [<li class="lang-javascript">JavaScript</li>]
  ```

  这种层级选择器相比单个的选择器好处在于，它缩小了选择范围。

  ​

* 子选择器（Child Selector）

  子选择器`$('parent>child')`类似层级选择器，但是限定了层级关系必须是父子关系，就是`<child>`节点必须是`<parent>`节点的直属子节点。还是以上面的例子：

  ```js
  $('ul.lang>li.lang-javascript'); // 可以选出[<li class="lang-javascript">JavaScript</li>]
  $('div.testing>li.lang-javascript'); // [], 无法选出，因为<div>和<li>不构成父子关系
  ```

  ​

* 过滤器（Filter）

  过滤器一般不单独使用，它通常附加在选择器上，帮助我们更精确地定位元素。

  ```js
  $('ul.lang li'); // 选出JavaScript、Python和Lua 3个节点

  $('ul.lang li:first-child'); // 仅选出JavaScript
  $('ul.lang li:nth-child(2)'); // 选出第N个元素，N从1开始
  $('ul.lang li:nth-child(odd)'); // 选出序号为奇数的元素
  ```

  ​

* 表单相关

  针对表单元素，jQuery还有一组特殊的选择器：

  - `:input`：可以选择`<input>`，`<textarea>`，`<select>`和`<button>`；
  - `:file`：可以选择`<input type="file">`，和`input[type=file]`一样；
  - `:checkbox`：可以选择复选框，和`input[type=checkbox]`一样；
  - `:radio`：可以选择单选框，和`input[type=radio]`一样；
  - `:focus`：可以选择当前输入焦点的元素，例如把光标放到一个`<input>`上，用`$('input:focus')`就可以选出；
  - `:checked`：选择当前勾选上的单选框和复选框，用这个选择器可以立刻获得用户选择的项目，如`$('input[type=radio]:checked')`；
  - `:enabled`：可以选择可以正常输入的`<input>`、`<select>`等，也就是没有灰掉的输入；
  - `:disabled`：和`:enabled`正好相反，选择那些不能输入的。

  此外，jQuery还有很多有用的选择器，例如，选出可见的或隐藏的元素:

  ```js
  $('div:visible'); // 所有可见的div
  $('div:hidden'); // 所有隐藏的div
  ```

  ​

### 查找和过滤

通常情况下选择器可以直接定位到我们想要的元素，但是，当我们拿到一个jQuery对象后，还可以以这个对象为基准，进行查找和过滤。

最常见的查找是在某个节点的所有子节点中查找，使用`find()`方法，它本身又接收一个任意的选择器。

```html
<ul class="lang">
    <li class="js dy">JavaScript</li>
    <li class="dy">Python</li>
    <li id="swift">Swift</li>
    <li class="dy">Scheme</li>
    <li name="haskell">Haskell</li>
</ul>
```

* 用`find()`查找：

  ```js
  var ul = $('ul.lang'); // 获得<ul>
  var dy = ul.find('.dy'); // 获得JavaScript, Python, Scheme
  var hsk = ul.find('[name=haskell]'); // 获得Haskell
  ```

  对于位于同一层级的节点，可以通过`next()`和`prev()`方法，例如:

  ```js
  var swift = $('#swift');

  swift.next(); // Scheme
  swift.next('[name=haskell]'); // 空的jQuery对象，因为Swift的下一个元素Scheme不符合条件[name=haskell]
  swift.prev('.dy'); // Python，因为Python同时符合过滤器条件.dy
  ```

  ​


* 用`filter()`过滤掉不符合选择器条件的节点

  类似于python中的filter

  ```js
  var langs = $('ul.lang li'); // 拿到JavaScript, Python, Swift, Scheme和Haskell
  var a = langs.filter('.dy'); // 拿到JavaScript, Python, Scheme
  ```

  或者传入一个函数，要特别注意函数内部的`this`被绑定为DOM对象，不是jQuery对象：

  ```js
  var langs = $('ul.lang li'); // 拿到JavaScript, Python, Swift, Scheme和Haskell
  langs.filter(function () {
      return this.innerHTML.indexOf('S') === 0; // 返回S开头的节点
  }); // 拿到Swift, Scheme
  ```

  ​

* `map()`方法把一个jQuery对象包含的若干DOM节点转化为其他对象

  类似于python中的map

  ```js
  var langs = $('ul.lang li'); // 拿到JavaScript, Python, Swift, Scheme和Haskell
  var arr = langs.map(function () {
      return this.innerHTML;
  }).get(); // 用get()拿到包含string的Array：['JavaScript', 'Python', 'Swift', 'Scheme', 'Haskell']
  ```



* 此外，一个jQuery对象如果包含了不止一个DOM节点，`first()`、`last()`和`slice()`方法可以返回一个新的jQuery对象，把不需要的DOM节点去掉：

  ```js
  var langs = $('ul.lang li'); // 拿到JavaScript, Python, Swift, Scheme和Haskell
  var js = langs.first(); // JavaScript，相当于$('ul.lang li:first-child')
  var haskell = langs.last(); // Haskell, 相当于$('ul.lang li:last-child')
  var sub = langs.slice(2, 4); // Swift, Scheme, 参数和数组的slice()方法一致
  ```

