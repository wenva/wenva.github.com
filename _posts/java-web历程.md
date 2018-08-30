JAVA WEB发展历程

* 第一阶段：静态网页
	* 服务端放置写好的html
	* 不足：无法展示一些动态的信息

* 第二阶段：servlet（动态网页）
	* 通过代码生成整个html
	* 不足：效率底下，而且代码中会混合大量html标签
	```java
out.write("<!DOCTYPE html>\r\n");
out.write("<html>\r\n");
out.write("<head>\r\n");
out.write("<title>Index Page</title>\r\n");
out.write("</head>\r\n");
out.write("<body>\r\n");
out.write("Hello, " + new Date() + "\r\n");
out.write("</body>\r\n");
out.write("</html>\r\n");
    ```

* 第三阶段：JSP
	* html中嵌入代码即JSP文件
```
    <!DOCTYPE html>
<html>
<head>
<title>Index Page</title>
</head>
<body>
Hello, <%=new Date()%>
</body>
</html
```
	* 不足：JSP包含大量代码

* 第四阶段：Servlet+JSP
    * 页面部分采用JSP
    * 逻辑采用Servlet

* 第五阶段：MVC
    * 进一步抽象化

* 第六阶段：Struts
    * 抽象处理类，即每个请求对应一个类
    * 路由抽象到xml配置中，而不是通过if-else判断

* 第七阶段：Spring
    * 每个请求对应一个类方法
    * IOC
    * AOP