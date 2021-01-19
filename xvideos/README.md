# 技术栈

- scrapy

# 坑

#### 1. 用scrapy.Request模拟请求获取数据被报400请求错误

可以使用 fiddler查看对比request，浏览器自己和scrapy请求的包头

解决：使用scrapy.Request的话就把（ ‘Connection’: ‘keep-alive’, ‘Content-Length’: ‘’,）这两个信息去掉

请求中有几个头文件不建议使用通用HTTP库。大多数库将自己生成这些，如下

- Host
- Content-Length

Content-Length 是内容长度头，scrapy会自动计算出来，并自动添加

#### 2. cookies添加一次即可，该项目没有合并cookies的需求

#### 3. 在scrapy 里用scrapy.Request，不要用requests，会导致堵塞

#### 4. 引用cookie文件相对路径神奇的失效，采用绝对路径引入