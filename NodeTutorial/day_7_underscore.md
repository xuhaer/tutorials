正如jQuery统一了不同浏览器之间的DOM操作的差异，让我们可以简单地对DOM进行操作，underscore则提供了一套完善的函数式编程的接口，让我们更方便地在JavaScript中实现函数式编程。



* map/filter

  和`Array`的`map()`与`filter()`类似，但是underscore的`map()`和`filter()`可以作用于Object。

  ```js
  'use strict';
  _.map({ a: 1, b: 2, c: 3 }, (v, k) => k + '=' + v); // ['a=1', 'b=2', 'c=3']
  ```

  若想map()操作返回Object而不是Array, 可把_.map换成 _.mapObject

  ​

* every/some

  类似于Python中的 all/any

  ```js
  'use strict';
  // 所有元素都大于0？
  _.every([1, 4, 7, -3, -9], (x) => x > 0); // false
  // 至少一个元素大于0？
  _.some([1, 4, 7, -3, -9], (x) => x > 0); // true
  ```

  ​

* max/min

  注意:

   	1. 空集合会返回-Infinity和Infinity
  	2. 如果集合是Object，`max()`和`min()`只作用于value，忽略掉key

  ​

* groupBy

  `groupBy()`把集合的元素按照key归类，key由传入的函数返回:

  ```js
  'use strict';

  var scores = [20, 81, 75, 40, 91, 59, 77, 66, 72, 88, 99];
  var groups = _.groupBy(scores, function (x) {
      if (x < 60) {
          return 'C';
      } else if (x < 80) {
          return 'B';
      } else {
          return 'A';
      }
  });
  // 结果:
  // {
  //   A: [81, 91, 88, 99],
  //   B: [75, 77, 66, 72],
  //   C: [20, 40, 59]
  // }
  ```

  ​

* shuffle/sample

  `shuffle()`用洗牌算法随机打乱一个集合, `sample()`则是随机选择一个或多个元素



* first/last

  ```js
  'use strict';
  var arr = [2, 4, 6, 8];
  _.first(arr); // 2
  _.last(arr); // 8
  ```

  ​

* flatten

  类似于numpy中的flatten



* zip/unzip

  和python中的zip类似



* object 

  相当于python中先zip再dict

  ```js
  'use strict';

  var names = ['Adam', 'Lisa', 'Bart'];
  var scores = [85, 92, 59];
  _.object(names, scores);
  // {Adam: 85, Lisa: 92, Bart: 59}
  ```

  需注意: `_.object()`是一个函数，不是JavaScript的`Object`对象。



* range

  快速生成一个序列，不再需要用`for`循环实现了。

  相当于Python中的list(range(*))

```js
'use strict';

// 从0开始小于30，步长5:
_.range(0, 30, 5); // [0, 5, 10, 15, 20, 25]
```



因为underscore本来就是为了充分发挥JavaScript的函数式编程特性，所以也提供了大量JavaScript本身没有的高阶函数。

* bind

  ```js
  'use strict';

  var s = ' Hello  ';
  s.trim();
  // 输出'Hello'

  var fn = s.trim;
  fn(); //直接调用fn()传入的this指针是undefined. Python中可以这样使用。
  // Uncaught TypeError: String.prototype.trim called on null or undefined
  ```

  `bind()`可以帮我们把`s`对象直接绑定在`fn()`的`this`指针上, 以后调用`fn()`就可以直接正常调用了:

  ```js
  'use strict';

  var s = ' Hello  ';
  var fn = _.bind(s.trim, s);
  fn();
  // 输出Hello
  ```



* partial

  ```js
  'use strict';

  var pow2N = _.partial(Math.pow, 2);
  pow2N(3); // 8
  ```



* memoize

  如果一个函数调用开销很大，我们就可能希望能把结果缓存下来，以便后续调用时直接获得结果:

  ```js
  'use strict';

  var factorial = _.memoize(function(n) {
      console.log('start calculate ' + n + '!...');
      var s = 1, i = n;
      while (i > 1) {
          s = s * i;
          i --;
      }
      console.log(n + '! = ' + s);
      return s;
  });

  // 第一次调用:
  factorial(10); // 3628800
  // 注意控制台输出:
  // start calculate 10!...
  // 10! = 3628800

  // 第二次调用:
  factorial(10); // 3628800
  // 控制台没有输出
  ```

  ​



* once

  保证某函数只执行一次。



* delay:

  让一个函数延迟提醒，，和setTimeout相同。



* keys / allKeys

  `keys()`可以非常方便地返回一个object自身所有的key，但不包含从原型链继承下来的。

  `allKeys()`除了object自身的key，还包含从原型链继承下来的。



* values

  和`keys()`类似，`values()`返回object自身但不包含原型链继承的所有值。

  注意，没有`allValues()`。



* mapObject

  `mapObject()`就是针对object的map版本



* invert

  `invert()`把object的每个key-value来个交换，key变成value，value变成key



* extend / extendOwn

  `extend()`把多个object的key-value合并到第一个object并返回, 如果有相同的key，后面的object的value将覆盖前面的object的value。

  类似Python中dict的update

  ```js
  'use strict';

  var a = {name: 'Bob', age: 20};
  _.extend(a, {age: 15}, {age: 88, city: 'Beijing'}); // {name: 'Bob', age: 88, city: 'Beijing'}
  // 变量a的内容也改变了：
  a; // {name: 'Bob', age: 88, city: 'Beijing'}
  ```

  `extendOwn()`和`extend()`类似，但获取属性时忽略从原型链继承下来的属性。



* clone

  如果我们要复制一个object对象，就可以用`clone()`方法，它会把原有对象的所有属性都复制到新的对象中。

  浅复制, 类似Python中的copy



* chain

  如果我们有一组操作，用underscore提供的函数，写出来像这样：

  ```js
  _.filter(_.map([1, 4, 9, 16, 25], Math.sqrt), x => x % 2 === 1);
  // [1, 3, 5]
  ```

  underscore提供了把对象包装成能进行链式调用的方法，就是`chain()`函数:

  ```js
  var r = _.chain([1, 4, 9, 16, 25])
           .map(Math.sqrt)
           .filter(x => x % 2 === 1)
           .value(); // 因为每一步返回的都是包装对象，所以最后一步的结果需要调用value()获得最终结果。
  console.log(r); // [1, 3, 5]
  ```

