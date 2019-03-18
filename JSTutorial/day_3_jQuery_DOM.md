### jQuery DOM

当使用jQuery的选择器拿到了jQuery对象后就可以操作对应的DOM节点了。



* 修改Text和HTML

  jQuery对象的`text()`和`html()`方法分别获取节点的文本和原始HTML文本，例如，如下的HTML结构：

  ```html
  <ul id="test-ul">
      <li class="js">JavaScript</li>
      <li name="book">Java &amp; JavaScript</li>
  </ul>
  ```

  ```js
  var j1 = $('#test-ul li[name=book]').text(); // 'Java & JavaScript'
  $('#test-ul li[name=book]').html(); // 'Java &amp; JavaScript'
  ```

  如何设置文本或HTML？jQuery的API设计非常巧妙：无参数调用`text()`是获取文本，传入参数就变成设置文本，HTML也是类似操作。

  ```js
  $('#not-exist').text('Hello'); // 如果#**存在，则将其text设置为'Hello',若不存在，代码也不报错，没有节点被设置为'Hello'
  ```

  一个jQuery对象可以包含0个或任意个DOM对象，它的方法实际上会作用在对应的`每个DOM节点`上。

  ​

* 修改CSS: `css('name', 'value')`方法

  *注意*，jQuery对象的所有方法都返回一个jQuery对象（可能是新的也可能是自身），这样我们可以进行链式调用:

  ```js
  var div = $('#test-div');
  div.css('color'); // '#000033', 获取CSS属性
  div.css('color', '#336699'); // 设置CSS属性
  div.css('color', ''); // 清除CSS属性
  ```



* 显示和隐藏DOM

  要隐藏一个DOM，我们可以设置CSS的`display`属性为`none`，利用`css()`方法就可以实现。不过，要显示这个DOM就需要恢复原有的`display`属性，这就得先记下来原有的`display`属性到底是`block`还是`inline`还是别的值。

  而jQuery直接提供`show()`和`hide()`方法，我们不用关心它是如何修改`display`属性的。



* 获取DOM信息

  `attr()`和`removeAttr()`方法用于操作DOM节点的属性：

  ```js
  // <div id="test-div" name="Test" start="1">...</div>
  var div = $('#test-div');
  div.attr('data'); // undefined, 属性不存在
  div.attr('name'); // 'Test'
  div.attr('name', 'Hello'); // div的name属性变为'Hello'
  div.removeAttr('name'); // 删除name属性
  ```

  `prop()`方法和`attr()`类似，但是HTML5规定有一种属性在DOM节点中可以没有值，只有出现与不出现两种，例如：

  ```html
  <input id="test-radio" type="radio" name="test" checked value="1">
  ```

  等价于:

  ```html
  <input id="test-radio" type="radio" name="test" checked="checked" value="1">
  ```

  `attr()`和`prop()`对于属性`checked`处理有所不同：

  ```js
  var radio = $('#test-radio');
  radio.attr('checked'); // 'checked'
  radio.prop('checked'); // true
  ```

  不过，用`is()`方法判断更好：

  ```js
  var radio = $('#test-radio');
  radio.is(':checked'); // true
  ```

  类似的属性还有`selected`，处理时最好用`is(':selected')`。

  ​



* 操作表单

  对于表单元素，jQuery对象统一提供`val()`方法获取和设置对应的`value`属性：其统一了各种输入框的取值和赋值的问题。

  ````js
  /*
      <input id="test-input" name="email" value="">
      <select id="test-select" name="city">
          <option value="BJ" selected>Beijing</option>
          <option value="SH">Shanghai</option>
          <option value="SZ">Shenzhen</option>
      </select>
      <textarea id="test-textarea">Hello</textarea>
  */
  var
      input = $('#test-input'),
      select = $('#test-select'),
      textarea = $('#test-textarea');

  input.val(); // 'test'
  input.val('abc@example.com'); // 文本框的内容已变为abc@example.com

  select.val(); // 'BJ'
  select.val('SH'); // 选择框已变为Shanghai

  textarea.val(); // 'Hello'
  textarea.val('Hi'); // 文本区域已更新为'Hi'
  ````

  ​

* 添加DOM

  要添加新的DOM节点，除了通过jQuery的`html()`这种暴力方法外，还可以用`append()`方法(`prepend()`则把DOM添加到最前。)：

  ```js
  $('#test-div>ul').append('<li><span>Haskell</span></li>');
  ```

  除了接受字符串，`append()`还可以传入原始的DOM对象，jQuery对象和函数对象。

  另外，同级节点可以用`after()`或者`before()`方法。

  ​

* 删除节点

  要删除DOM节点，拿到jQuery对象后直接调用`remove()`方法就可以了。

  ```js
  var li = $('#test-div>ul>li');
  li.remove(); // 所有<li>全被删除
  ```

  ​