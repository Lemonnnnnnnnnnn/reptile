- 网站http://freeproxylists.net/执行`scrapy crawl fpl`将会将可用的IP写入proxy.txt文件
- 网站http://free-proxy-list.net/可以在请求中直接获取所有IP地址，在judge_ip文件夹中运行judge_ip.py文件可将校验后的IP写入
- 网站https://proxyscrape.com/free-proxy-list可直接下载免费ip列表，用judge_ip.py文件进行校验即可



## 未：
- 网站：http://free-proxy.cz/zh/
- https://proxyscrape.com/free-proxy-list 网站中有socket4,socket5的ip地址可下载

# 自动化

1. 进入crawler 执行命令 scrapy crawl fpl 在crawler文件夹下生成http.txt文件
2. 执行ez_crawler文件，继续写入http.txt,生成socks5.txt和socks4.txt
3. 对三个文件执行judge_ip校对，生成三个已校对的IP txt文件
4. 将以上命令打包成exe文件