## jQuery ajax、扩展

用jQuery的相关对象来处理AJAX的优势:

1. 不需要考虑浏览器问题
2. 代码能大大简化



* ajax

  jQuery在全局对象`jQuery`（也就是`$`）绑定了`ajax()`函数，可以处理AJAX请求。`ajax(url, settings)`函数需要接收一个URL和一个可选的`settings`对象，常用的选项如下：

  - async：是否异步执行AJAX请求，默认为`true`，千万不要指定为`false`；
  - method：发送的Method，缺省为`'GET'`，可指定为`'POST'`、`'PUT'`等；
  - contentType：发送POST请求的格式，默认值为`'application/x-www-form-urlencoded; charset=UTF-8'`，也可以指定为`text/plain`、`application/json`；
  - data：发送的数据，可以是字符串、数组或object。如果是GET请求，data将被转换成query附加到URL上，如果是POST请求，根据contentType把data序列化成合适的格式；
  - headers：发送的额外的HTTP头，必须是一个object；
  - dataType：接收的数据格式，可以指定为`'html'`、`'xml'`、`'json'`、`'text'`等，缺省情况下根据响应的`Content-Type`猜测。

  jQuery的jqXHR对象类似一个Promise对象，我们可以用链式写法来处理各种回调：

  ```js
  var jqxhr = $.ajax('/api/categories', {
      dataType: 'json'
  }).done(function (data) {
      ajaxLog('成功, 收到的数据: ' + JSON.stringify(data));
  }).fail(function (xhr, status) {
      ajaxLog('失败: ' + xhr.status + ', 原因: ' + status);
  }).always(function () {
      ajaxLog('请求完成: 无论成功或失败都会调用');
  });
  ```

  ​

* get

  对常用的AJAX操作，jQuery提供了一些辅助方法。由于GET请求最常见，所以jQuery提供了`get()`方法，可以这么写：

  ```js
  var jqxhr = $.get('/path/to/resource', {
      name: 'Bob Lee',
      check: 1
  }); //实际url是/path/to/resource?name=Bob%20Lee&check=1
  ```

  ​

* post

  `post()`和`get()`类似，但是传入的第二个参数默认被序列化为`application/x-www-form-urlencoded`：

  ```js
  var jqxhr = $.post('/path/to/resource', {
      name: 'Bob Lee',
      check: 1
  });
  ```

  实际构造的数据`name=Bob%20Lee&check=1`作为POST的`body`被发送。

  ​

* getJSON

  jQuery也提供了`getJSON()`方法来快速通过GET获取一个JSON对象：

  ```js
  var jqxhr = $.getJSON('/path/to/resource', {
      name: 'Bob Lee',
      check: 1
  }).done(function (data) {
      // data已经被解析为JSON对象了
  });
  ```



* 安全限制

  jQuery的AJAX完全封装的是JavaScript的AJAX操作，所以它的安全限制和前面讲的用JavaScript写AJAX完全一样。

  如果需要使用JSONP，可以在`ajax()`中设置`jsonp: 'callback'`，让jQuery实现JSONP跨域加载数据。



* jQuery 插件

  可以扩展jQuery来实现自定义方法，这种方式也称为编写jQuery插件。

  给jQuery对象绑定一个新方法是通过扩展`$.fn`对象实现的。举例：`highlight1()`：

  ```js
  $.fn.my_highlight = function () {
      // this已绑定为当前jQuery对象:
      this.css('backgroundColor', '#fffceb').css('color', '#d85030');
      return this;
  }
  $('#test-highlight span').my_highlight();
  ```

  也可以给方法加个参数，让用户自己把参数用对象传进去:

  ```js
  $.fn.highlight2 = function (options) {
      // 要考虑到各种情况:
      // options为undefined
      // options只有部分key
      var bgcolor = options && options.backgroundColor || '#fffceb';
      var color = options && options.color || '#d85030';
      this.css('backgroundColor', bgcolor).css('color', color);
      return this;
  }
  //调用
  $('#test-highlight2 span').highlight2({
      backgroundColor: '#00a8e6',
      color: '#ffffff'
  });
  ```

  另一种方法是使用jQuery提供的辅助方法`$.extend(target, obj1, obj2, ...)`，它把多个object对象的属性合并到第一个target对象中，遇到同名属性，总是使用靠后的对象的值，也就是越往后优先级越高：

  ```js
  // 把默认值和用户传入的options合并到对象{}中并返回:
  var opts = $.extend({}, {
      backgroundColor: '#00a8e6',
      color: '#ffffff'
  }, options);
  ```

  highlight2也可以自己设定一个缺省值：

  ```js
  $.fn.my_highlight2 = function (options) {
      // 合并默认值和用户设定值:
      var opts = $.extend({}, $.fn.my_highlight2.defaults, options);
      this.css('backgroundColor', opts.backgroundColor).css('color', opts.color);
      return this;
  }

  // 设定默认值:
  $.fn.my_highlight2.defaults = {
      color: '#d85030',
      backgroundColor: '#fff8de'
  }
  ```

  现在，用户使用时，只需一次性设定默认值，然后就可以非常简单地调用my_highlight2`()`了。

  ​

  最终，我们得出编写一个jQuery插件的原则：

  1. 给`$.fn`绑定函数，实现插件的代码逻辑；
  2. 插件函数最后要`return this;`以支持链式调用；
  3. 插件函数要有默认值，绑定在`$.fn.<pluginName>.defaults`上；
  4. 用户在调用时可传入设定值以便覆盖默认值。

