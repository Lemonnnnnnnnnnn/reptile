# 功能

- 爬取e站单页相簿
- 爬取e站封面

# 项目大纲

- 调用idm进行e站封面图爬取
- 调用aria2进行初次爬取，因偶发性失败将失败链接调入idm进行二次爬取
- 调用mongodb存储图片在本地的路径和链接，在new_file进行读取

# 运行

## 依赖：

```python
pip install -r requirements.txt
```

## 爬取单页相簿：

- 在constant.py自定义相关信息

- `python mutual_try.py`   在终端输入爬取地址 例如https://e-hentai.org/g/1841574/314dd10e32/**，回车后可输入下一个地址

## 爬取封面：

- **进入django/demo/views.py文件，更改第一行的path路径为当前项目所在的绝对路径**

- `cd django`
- `python manage.py runserver`（调用catch_face方法爬取封面，封面存放在`www/public`文件夹下）
- 打开`www/new_file`，可查看封面，复制链接配合mutual_try进行图片爬取

# 文件分工

组件文件：

- aria2_download 调用aria2下载，内含idm二次下载方法（aria2偶发性失效）
- catch_face 爬取封面
- common 通用方法
- constant 常量
- e1  调用aria2和爬取单页相簿
- e2 爬取多页相簿（因为没有合适的代理池，爬取多页会被限制IP）

**执行文件：**

- **mutual_try  调用e1多线程爬取单页相簿，直接运行输入地址即可**