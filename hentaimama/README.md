# 技术栈

- scrapy

# 坑

- 由**jwplayer**生成的**dom**元素无法获取，用**scrapy_splash**和**scrapy_selenium**进行渲染均失效，最后用正则提取**scrpit**中的下载链接
- 引用cookie文件相对路径神奇的失效，采用绝对路径引入