## jQuery 事件、动画

因为JavaScript在浏览器中以单线程模式运行，页面加载后，一旦页面上所有的JavaScript代码被执行完后，就只能依赖触发事件来执行JavaScript代码。

其能够绑定的事件主要包括：

* 鼠标事件

  * click: 鼠标单击时触发；

  * dblclick：鼠标双击时触发；

  * mouseenter：鼠标进入时触发；

  * mouseleave：鼠标移出时触发；

  * mousemove：鼠标在DOM内部移动时触发；

  * hover：鼠标进入和退出时触发两个函数，相当于mouseenter加上mouseleave。

    ​

* 键盘事件

  键盘事件仅作用在当前焦点的DOM上，通常是`<input>`和`<textarea>`。

  * keydown：键盘按下时触发；

  * keyup：键盘松开时触发；

  * keypress：按一次键后触发。

    ​

* 其它事件

  * focus：当DOM获得焦点时触发；
  * blur：当DOM失去焦点时触发；
  * change：当`<input>`、`<select>`或`<textarea>`的内容改变时触发；
  * submit：当`<form>`提交时触发；
  * ready：当页面被载入并且DOM树完成初始化后触发。

  其中，`ready`仅作用于`document`对象。由于`ready`事件在DOM完成初始化后触发，且只触发一次，所以非常适合用来写其他的初始化代码。

  ​

* 事件参数

  有些事件，如`mousemove`和`keypress`，我们需要获取鼠标位置和按键的值，所有事件都会传入`Event`对象作为参数，可以从`Event`对象上获取到更多的信息：

  ```js
  $(function () {
      $('#testMouseMoveDiv').mousemove(function (e) {
          $('#testMouseMoveSpan').text('pageX = ' + e.pageX + ', pageY = ' + e.pageY);
      });
  });
  ```

  ​

* 取消绑定

  一个已被绑定的事件可以解除绑定，通过`off('click', function)`实现：

  ```js
  function hello() {
      alert('hello!');
  }

  a.click(hello); // 绑定事件

  // 10秒钟后解除绑定:
  setTimeout(function () {
      a.off('click', hello);
  }, 10000);
  ```

  为了实现移除效果，可以使用`off('click')`一次性移除已绑定的`click`事件的所有处理函数。

  同理，无参数调用`off()`一次性移除已绑定的所有类型的事件处理函数。



* 事件触发条件

  事件的触发总是由用户操作引发的，如：

  ```js
  var input = $('#test-input');
  input.change(function () {
      console.log('changed...');
  })
  ```

  但是，如果用JavaScript代码去改动文本框的值，将**不会**触发：

  ```js
  var input = $('#test-input');
  input.val('change it!'); // 无法触发change事件
  ```

  ​

* 浏览器安全限制

  在浏览器中，有些JavaScript代码只有在用户触发下才能执行，例如，`window.open()`函数，这些“敏感代码”只能由用户操作来触发



jQuery内置的几种动画样式：

* show/hide

  直接以无参数形式调用`show()`和`hide()`，会显示和隐藏DOM元素。但是，只要传递一个时间参数进去，就变成了动画：

  ```js
  var div = $('#test-show-hide');
  div.hide(3000); // 在3秒钟内逐渐消失
  ```

  时间以毫秒为单位，但也可以是`'slow'`，`'fast'`这些字符串

  而`toggle()`方法则根据当前状态决定是`show()`还是`hide()`。

  ​

* slideUp/slideDown

  `show()`和`hide()`是从左上角逐渐展开或收缩的，而`slideUp()`和`slideDown()`则是在垂直方向逐渐展开或收缩的。

  `slideUp()`把一个可见的DOM元素收起来，效果跟拉上窗帘类似，`slideDown()`相反，而`slideToggle()`则根据元素是否可见来决定下一步动作。



* fadeIn/fadeOut

  `fadeIn()`和`fadeOut()`的动画效果是淡入淡出，也就是通过不断设置DOM元素的`opacity`属性来实现，而`fadeToggle()`则根据元素是否可见来决定下一步动作。

  ​

* 自定义动画：animate

  可以实现任意动画效果，我们需要传入的参数就是DOM元素最终的CSS状态和时间，jQuery在时间段内不断调整CSS直到达到我们设定的值

  ```js
  var div = $('#test-animate');
  div.animate({
      opacity: 0.25,
      width: '256px',
      height: '256px'
  }, 3000); // 在3秒钟内CSS过渡到设定值
  ```

  `animate()`还可以再传入一个函数，当动画结束时，该函数将被调用：

  ```js
  var div = $('#test-animate');
  div.animate({
      opacity: 0.25,
      width: '256px',
      height: '256px'
  }, 3000, function () {
      console.log('动画已结束');
      // 恢复至初始状态:
      $(this).css('opacity', '1.0').css('width', '128px').css('height', '128px');
  });
  ```

  ​

* 串行动画

  jQuery的动画效果还可以串行执行，通过`delay()`方法还可以实现暂停，这样，我们可以实现更复杂的动画效果：

  ```js
  var div = $('#test-animates');
  // 动画效果：slideDown - 暂停 - 放大 - 暂停 - 缩小
  div.slideDown(2000)
     .delay(1000)
     .animate({
         width: '256px',
         height: '256px'
     }, 2000)
     .delay(1000)
     .animate({
         width: '128px',
         height: '128px'
     }, 2000);
  }
  ```

  ​

另外，有的动画如`slideUp()`根本没有效果。这是因为jQuery动画的原理是逐渐改变CSS的值，如`height`从`100px`逐渐变为`0`。但是很多不是block性质的DOM元素，对它们设置`height`根本就不起作用，所以动画也就没有效果。

此外，jQuery也没有实现对`background-color`的动画效果，用`animate()`设置`background-color`也没有效果。这种情况下可以使用CSS3的`transition`实现动画效果。

