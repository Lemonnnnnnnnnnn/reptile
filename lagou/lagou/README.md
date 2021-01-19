# 踩坑：

### 请求头Content-Type字段代表了发送数据的格式：

- **application/x-www-form-urlencoded** ：form表单数据被编码为key/value格式发送到服务器（表单默认的提交数据的格式）
- scrapy会自动将数据转化为符合请求头格式的字符串。

由于在项目中随意的将数据转化为json格式的字符串进行提交，服务器总是返回一样的数据

```python
yield scrapy.FormRequest(url=self.Ajaxurl, headers=self.headers, formdata=body, cookies=self.cookies,
                         callback=self.parsePage,
                         method="POST")
```

- 将**scrapy.Request**改为**scrapy.FormRequest**
- 将数据由**body = json.dumbs(data)**修改为**formdata=data**

成功返回正常数据