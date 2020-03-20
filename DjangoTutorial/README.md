# 补充一些阅读django 官方文档的笔记

## 模型
**differentiate null=True, blank=True in django**
null=True sets NULL (versus NOT NULL) on the column in your DB. Blank values for Django field types such as DateTimeField or ForeignKey will be stored as NULL in the DB.

blank=True determines whether the field will be required in forms. This includes the admin and your own custom forms. If blank=True then the field will not be required, whereas if it's False the field cannot be blank.
```Python
class Test(models.Model):
    charNull        = models.CharField(max_length=10, null=True)
    charBlank       = models.CharField(max_length=10, blank=True)
    charNullBlank   = models.CharField(max_length=10, null=True, blank=True)

    intNull         = models.IntegerField(null=True)
    intBlank        = models.IntegerField(blank=True)
    intNullBlank    = models.IntegerField(null=True, blank=True)

    dateNull        = models.DateTimeField(null=True)
    dateBlank       = models.DateTimeField(blank=True)
    dateNullBlank   = models.DateTimeField(null=True, blank=True)   
```
The database fields created for MySQL 5.6 are :
```sql
CREATE TABLE Test (
     `id`            INT(11)     r    AUTO_INCREMENT,
     `charNull`      VARCHAR(10) NULL DEFAULT NULL,
     `charBlank`     VARCHAR(10) NOT  NULL,
     `charNullBlank` VARCHAR(10) NULL DEFAULT NULL,

     `intNull`       INT(11)     NULL DEFAULT NULL,
     `intBlank`      INT(11)     NOT  NULL,
     `intNullBlank`  INT(11)     NULL DEFAULT NULL,

     `dateNull`      DATETIME    NULL DEFAULT NULL,
     `dateBlank`     DATETIME    NOT  NULL,
     `dateNullBlank` DATETIME    NULL DEFAULT NULL
)
```

## 执行查询
一旦创建 数据模型 后，Django 自动给予你一套数据库抽象 API，允许你创建，检索，更新和删除对象。本页介绍如何使用这些 API。参考 数据模型参考 获取所有查询选项的完整细节。


### 缓存和QuerySet
每个 QuerySet 都带有缓存，尽量减少数据库访问。理解它是如何工作的能让你编写更高效的代码。

新创建的 QuerySet 缓存是空的。一旦要计算 QuerySet 的值，就会执行数据查询，随后，Django 就会将查询结果保存在 QuerySet 的缓存中，并返回这些显式请求的缓存（例如，下一个元素，若 QuerySet 正在被迭代）。后续针对 QuerySet 的计算会复用缓存结果。
```Python
>>> print([e.headline for e in Entry.objects.all()]) # Queries the database
>>> print([e.pub_date for e in Entry.objects.all()]) # Queries the database again

# To avoid this problem, save the QuerySet and reuse it:
>>> queryset = Entry.objects.all()
>>> print([p.headline for p in queryset]) # Evaluate the query set.
>>> print([p.pub_date for p in queryset]) # Re-use the cache from the evaluation.
```

**当 QuerySet 未被缓存时**
查询结果集并不总是缓存结果。当仅计算查询结果集的部分时，会校验缓存，若没有填充缓存，则后续查询返回的项目不会被缓存。特别地说，这意味着使用数组切片或索引的 限制查询结果集 不会填充缓存。
例如，重复的从某个查询结果集对象中取指定索引的对象会每次都查询数据库:
```Python
>>> queryset = Entry.objects.all()
>>> print(queryset[5]) # Queries the database
>>> print(queryset[5]) # Queries the database again
```

不过，若全部查询结果集已被检出，就会去检查缓存:
```Python
>>> queryset = Entry.objects.all()
>>> [entry for entry in queryset] # Queries the database
>>> print(queryset[5]) # Uses cache
>>> print(queryset[5]) # Uses cache
```

以下展示一些例子，这些动作会触发计算全部的查询结果集，并填充缓存的过程:
```Python
>>> [entry for entry in queryset]
>>> bool(queryset)
>>> entry in queryset
>>> list(queryset)
```

注解：只是打印查询结果集不会填充缓存。因为调用 __repr__() 仅返回了完整结果集的一个切片。

### 通过 Q 对象完成复杂查询
在类似 filter() 中，查询使用的关键字参数是通过 "AND" 连接起来的。如果你要执行更复杂的查询（例如，由 OR 语句连接的查询），你可以使用 Q 对象。
若提供了 Q 对象，那么它必须位于所有关键字参数之前。例子:
```Python
# 有效查询:
Poll.objects.get(
    Q(pub_date=date(2005, 5, 2)) | Q(pub_date=date(2005, 5, 6)),
    question__startswith='Who',
)
# 无效查询:
Poll.objects.get(
    question__startswith='Who',
    Q(pub_date=date(2005, 5, 2)) | Q(pub_date=date(2005, 5, 6))
)
```

### 复制模型实例
虽然django没有built-in 方法可以复制模型实例，但也可以通过一个很简单的把pk设为None的方法来达到此目的。
```Python
blog = Blog(name='My blog', tagline='Blogging is easy')
blog.save() # blog.pk == 1

blog.pk = None
blog.save() # blog.pk == 2
```

不过该方法对于继承模型、有外键关联等情况还有诸多限制，参考：/topics/db/queries/#copying-model-instances

## Managers
Manager 是一种接口，它赋予了 Django 模型操作数据库的能力。Django 应用中每个模型拥有至少一个 Manager。
默认情况下，Django 为每个模型类添加了一个名为 objects 的 Manager。不过，若你想将 objects 用作字段名，或想使用 objects 以外的 Manager 名字，就要在模型基类中重命名。要为指定类重命名 Manager，在该模型中定义一个类型为 models.Manager 的属性。

This example also pointed out another interesting technique: using multiple managers on the same model. You can attach as many Manager() instances to a model as you'd like. This is a non-repetitive way to define common "filters" for your models.

```Python
class AuthorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role='A')

class EditorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role='E')

class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(max_length=1, choices=[('A', _('Author')), ('E', _('Editor'))]) # 应该是 import gettext_lazy as _
    people = models.Manager()
    authors = AuthorManager()
    editors = EditorManager()
```

上例允许你调用 Person.authors.all()， Person.editors.all() 和 Person.people.all()，返回符合期望的结果。


## Django F()表达式
在投票程序中，最简单的投票表示为：先从数据库中取出实例，然后把它的值放入内存中并使用我们熟悉的python运算符操作它，然后把对象保存到数据库中。
但是如果恰巧在同一时刻有2个人在2个线程投这个票，那么会导致取出的votes数都相同，比如42，但两个人投票后的值均变成：43(selected_choice.votes += 1)，但实际期望结果是 44。

这个问题被称为 竞争条件。 可以通过阅读 Avoiding race conditions using F() 来解决这个问题。
```Python
selected_choice.votes = F('votes') + 1
selected_choice.save()
```

