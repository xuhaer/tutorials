### 2.4. 使用Flowable REST API

这个章节展示了与[上一章节](https://tkjohn.github.io/flowable-userguide/#getting.started.command.line)相同的例子：部署一个流程定义，启动一个流程实例，获取任务列表并完成一个任务。

#### 2.4.1. 安装REST应用

从flowable.org网站下载.zip文件后，可以在*wars*文件夹下找到REST应用。要运行这个WAR文件，需要一个servlet容器，例如[Tomcat](http://tomcat.apache.org/)、[Jetty](http://www.eclipse.org/jetty/)等。

使用Tomcat的步骤如下：

- 下载并解压缩最新的Tomcat zip文件（在Tomcat网站中选择’Core’发行版）。
- 将flowable-rest.war文件从解压的Flowable发行版的*wars*文件夹中复制到解压的Tomcat文件夹下的*webapps*文件夹下。
- 使用命令行，转到Tomcat文件夹下的*bin*文件夹。
- 执行'*./catalina.sh run*'启动Tomcat服务器。

在下面的章节中，我们使用cURL展示各种REST调用。所有的REST调用默认都使用*基本认证*保护，所有的调用的用户都是 *rest-admin*，密码为’test'。

在启动后，通过执行下列命令验证应用运行正常：

```bash
curl --user rest-admin:test http://localhost:8080/flowable-rest/service/management/engine
# 返回json格式的响应
```

#### 2.4.2. 部署流程定义

第一步是部署一个流程定义。使用REST API时，需要将一个.bpmn20.xml文件（或对于多个流程引擎，一个.zip文件）作为’multipart/formdata’上传：

```bash
curl --user rest-admin:test -F "file=@src/main/resources/holiday-request.bpmn20.xml" http://localhost:8080/flowable-rest/service/repository/deployments
# 这里注意file=@的路径, src/main/resources/
```

返回:

```bash
{"id":"5987eb03-fd0a-11e8-a317-ca24aa97722b","name":"holiday-request","deploymentTime":"2018-12-11T14:02:32.838+08:00","category":null,"parentDeploymentId":null,"url":"http://localhost:8080/flowable-rest/service/repository/deployments/5987eb03-fd0a-11e8-a317-ca24aa97722b","tenantId":""}
```

要验证流程定义已经正确部署，可以请求流程定义的列表：

```bash
curl --user rest-admin:test http://localhost:8080/flowable-rest/service/repository/process-definitions
```

#### 2.4.3. 启动流程实例

使用REST API启动一个流程实例与使用Java API很像：提供*key*作为流程定义的标识，并使用一个map作为初始化流程变量：

```js
curl --user rest-admin:test -H "Content-Type: application/json" -X POST -d '{ "processDefinitionKey":"holidayRequest", "variables": [ { "name":"employee", "value": "John Doe" }, { "name":"nrOfHolidays", "value": 7 }]}' http://localhost:8080/flowable-rest/service/runtime/process-instances
```

返回的key为:

```python
dict_keys(['id', 'url', 'name', 'businessKey', 'suspended', 'ended', 'processDefinitionId', 'processDefinitionUrl', 'activityId', 'startedBy', 'started', 'variables', 'callbackId', 'callbackType', 'tenantId', 'completed'])
```

#### 2.4.4. 任务列表与完成任务

当流程实例启动后，第一个任务会指派给’managers’组。要获取这个组的所有任务，可以通过REST API进行任务查询：

```bash
curl --user rest-admin:test -H "Content-Type: application/json" -X POST -d '{ "candidateGroup" : "managers" }' http://localhost:8080/flowable-rest/service/query/tasks
```

这将返回’manager’组的所有任务的列表。

然后，可以这样完成任务(`id`为上面query/tasks返回的`id`)：

```bash
curl --user rest-admin:test -H "Content-Type: application/json" -X POST -d '{ "action" : "complete", "variables" : [ { "name" : "approved", "value" : true} ]  }' http://localhost:8080/flowable-rest/service/runtime/tasks/701c4b3f-fd0b-11e8-a317-ca24aa97722b
```

