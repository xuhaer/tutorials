前面用WebSocket 编写的聊天室有点难度，涉及WebSocket、vue等较为陌生的概念，暂搁置不管。



#### MVVM

MVVM最早由微软提出来，它借鉴了桌面应用程序的MVC思想，在前端页面中，把Model用纯JavaScript对象表示，View负责显示，两者做到了最大限度的分离。

**把Model和View关联起来的就是ViewModel。ViewModel负责把Model的数据同步到View显示出来，还负责把View的修改同步回Model。**

ViewModel如何编写？需要用JavaScript编写一个通用的ViewModel，这样，就可以复用整个MVVM模型了。

一个MVVM框架和jQuery操作DOM相比有什么区别？

我们先看用jQuery实现的修改两个DOM节点的例子：

```html
<p>Hello, <span id="name">Bart</span>!</p>
<p>You are <span id="age">12</span>.</p>
```

用jQuery修改name和age节点的内容：

```js
var name = 'Homer';
var age = 51;

$('#name').text(name);
$('#age').text(age);
```

如果我们使用MVVM框架来实现同样的功能，我们首先并不关心DOM的结构，而是关心数据如何存储。最简单的数据存储方式是使用JavaScript对象：

```js
var person = {
    name: 'Bart',
    age: 12
};
```

我们把变量`person`看作Model，把HTML某些DOM节点看作View，并假定它们之间被关联起来了。

要把显示的name从`Bart`改为`Homer`，把显示的age从`12`改为`51`，我们并不操作DOM，而是直接修改JavaScript对象：

```js
person.name = 'Homer';
person.age = 51;
```

也就是说：改变JavaScript对象的状态，会导致DOM结构作出对应的变化！这让我们的关注点从如何操作DOM变成了如何更新JavaScript对象的状态，而操作JavaScript对象比DOM简单多了！

这就是MVVM的设计思想：关注Model的变化，让MVVM框架去自动更新DOM的状态，从而把开发者从操作DOM的繁琐步骤中解脱出来！



**MVVM就是在前端页面上，应用了扩展的MVC模式，我们关心Model的变化，MVVM框架自动把Model的变化映射到DOM结构上（可以使我们的代码更专注于处理业务逻辑而不是去关心 DOM 操作），这样，用户看到的页面内容就会随着Model的变化而更新。**

常用的MVVM框架有：[Angular](https://angularjs.org/)、[Backbone.js](http://backbonejs.org/)、[Ember](http://emberjs.com/)、[Vue.js](http://vuejs.org/)、[react](http://facebook.github.io/react/) 等

Vue 示例:

```html
<head>
<!-- 引用jQuery -->
<script src="https://cdn.jsdelivr.net/npm/jquery/dist/jquery.min.js"></script>
<!-- 引用Vue -->
<script src="https://cdn.jsdelivr.net/npm/vue@2.5.21/dist/vue.js"></script>

<script>
// 初始化代码:
$(function () {
    var vm = new Vue({
        el: '#vm',
        //el指定了要把Model绑定到哪个DOM根节点上
        data: {
            name: 'Robot',
            age: 15
        }
    });
    window.vm = vm;
});
</script>
</head>

<body>
    <div id="vm">
        <p>Hello, {{ name }}!</p>
        <p>You are {{ age }} years old!</p>
    </div>
</body>
```
#### 单向绑定

打开浏览器console  执行 window.vm.name = 'Bob',Vue作为MVVM框架会自动监听Model的任何变化，在Model数据变化时，更新View的显示。这种Model到View的绑定我们称为单向绑定。



在Vue中，可以直接写`{{ name }}`绑定某个属性。如果属性关联的是对象，还可以用多个`.`引用，例如，`{{ address.zipcode }}`。

另一种单向绑定的方法是使用Vue的指令`v-text`，写法如下:

```html
<p>Hello, <span v-text="name"></span>!</p>
```

这种写法是把指令写在HTML节点的属性上，它会被Vue解析，该节点的文本内容会被绑定为Model的指定属性，注意不能再写双花括号`{{ }}`。

#### 双向绑定

单向绑定非常简单，就是把Model绑定到View，当我们用JavaScript代码更新Model时，View就会自动更新。

有单向绑定，就有双向绑定。如果用户更新了View，Model的数据也自动被更新了，这种情况就是双向绑定。(填写表单就是一个最直接的例子)

在Vue中，使用双向绑定非常容易，我们仍然先创建一个VM实例：略

然后，编写一个HTML FORM表单，并用`v-model`指令把某个`<input>`和Model的某个属性作双向绑定：

```html
<form id="vm" action="#">
    <p><input v-model="email"></p>
    <p><input v-model="name"></p>
</form>
```

双向绑定最大的好处是我们不再需要用jQuery去查询表单的状态，而是直接获得了用JavaScript对象表示的Model。

#### 处理事件

当用户提交表单时，传统的做法是响应`onsubmit`事件，用jQuery获取表单内容，检查输入是否有效，最后提交表单，或者用AJAX提交表单。

现在，获取表单内容已经不需要了，因为双向绑定直接让我们获得了表单内容，并且获得了合适的数据类型。

响应`onsubmit`事件也可以放到VM中。我们在`<form>`元素上使用指令:

```html
<form id="vm" v-on:submit.prevent="register">
```

其中，`v-on:submit="register"`指令就会自动监听表单的`submit`事件，并调用`register`方法处理该事件。使用`.prevent`表示阻止事件冒泡，这样，浏览器不再处理`<form>`的`submit`事件。

因为我们指定了事件处理函数是`register`，所以需要在创建VM时添加一个`register`函数：

```js
var vm = new Vue({
    el: '#vm',
    data: {
        ...
    },
    methods: {
        register: function () {
            // 显示JSON格式的Model:
            alert(JSON.stringify(this.$data));
            // TODO: AJAX POST...
        }
    }
});
```

在`register()`函数内部，我们可以用AJAX把JSON格式的Model发送给服务器，就完成了用户注册的功能。