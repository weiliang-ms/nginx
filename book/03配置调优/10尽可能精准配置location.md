### location尽可能的精确

[原文地址](https://github.com/trimstray/nginx-admins-handbook/blob/master/doc/RULES.md#rationale-32)
- [更多nginx文档](https://weiliang-ms.github.io/nginx/)
- [更多linux相关文档](https://weiliang-ms.github.io/wl-awesome/)

> 解释说明

精确的`location`匹配通常被用来加快选择过程，匹配通过后立即结束算法的执行。

使用`=`修饰符可以定义`URI`和`location`的精确匹配。它的处理速度非常快，可以节省大量的`CPU`开销。

```nginx configuration
location = / {

  ...

}

# Matches the query /v9 only and stops searching:
location = /v9 {

  ...

}

...
```

如果找到精确匹配，则搜索终止。 例如，存在`/`请求，并且请求的频率比较高，则可以定义`location = /`加快这些请求的处理速度。

### 关于nginx location匹配顺序

**例子来源以下地址**

[https://github.com/trimstray/nginx-admins-handbook#introduction](https://github.com/trimstray/nginx-admins-handbook#introduction)

> 假设配置如下

```nginx configuration
server {

	 listen           80;
	 server_name      xyz.com www.xyz.com;
	
	 location ~ ^/(media|static)/ {
	  root            /var/www/xyz.com/static;
	  expires         10d;
	 }
	
	 location ~* ^/(media2|static2) {
	  root            /var/www/xyz.com/static2;
	  expires         20d;
	 }
	
	 location /static3 {
	  root            /var/www/xyz.com/static3;
	 }
	
	 location ^~ /static4 {
	  root            /var/www/xyz.com/static4;
	 }
	
	 location = /api {
	  proxy_pass      http://127.0.0.1:8080;
	 }
	
	 location / {
	  proxy_pass      http://127.0.0.1:8080;
	 }
	
	 location /backend {
	  proxy_pass      http://127.0.0.1:8080;
	 }
	
	 location ~ logo.xcf$ {
	  root            /var/www/logo;
	  expires         48h;
	 }
	
	 location ~* .(png|ico|gif|xcf)$ {
	  root            /var/www/img;
	  expires         24h;
	 }
	
	 location ~ logo.ico$ {
	  root            /var/www/logo;
	  expires         96h;
	 }
	
	 location ~ logo.jpg$ {
	  root            /var/www/logo;
	  expires         48h;
	 }	
}
```

> 匹配规则如下

| 请求URL               | 相匹配的location                                                                                                      | 最终匹配                      |
|---------------------|-------------------------------------------------------------------------------------------------------------------|---------------------------|
| /                   | 1\) prefix match for /                                                                                            | /                         |
| /css                | 1\) prefix match for /                                                                                            | /                         |
| /api                | 1\) exact match for /api                                                                                          | /api                      |
| /api/               | 1\) prefix match for /                                                                                            | /                         |
| /backend            | 1\) prefix match for /2\) prefix match for /backend                                                               | /backend                  |
| /static             | 1\) prefix match for /                                                                                            | /                         |
| /static/header\.png | 1\) prefix match for /2\) case sensitive regex match for ^/\(media\|static\)/                                     | ^/\(media\|static\)/      |
| /static/logo\.jpg   | 1\) prefix match for /2\) case sensitive regex match for ^/\(media\|static\)/                                     | ^/\(media\|static\)/      |
| /media2             | 1\) prefix match for /2\) case insensitive regex match for ^/\(media2\|static2\)                                  | ^/\(media2\|static2\)     |
| /media2/            | 1\) prefix match for /2\) case insensitive regex match for ^/\(media2\|static2\)                                  | ^/\(media2\|static2\)     |
| /static2/logo\.jpg  | 1\) prefix match for /2\) case insensitive regex match for ^/\(media2\|static2\)                                  | ^/\(media2\|static2\)     |
| /static2/logo\.png  | 1\) prefix match for /2\) case insensitive regex match for ^/\(media2\|static2\)                                  | ^/\(media2\|static2\)     |
| /static3/logo\.jpg  | 1\) prefix match for /static32\) prefix match for /3\) case sensitive regex match for logo\.jpg$                  | logo\.jpg$                |
| /static3/logo\.png  | 1\) prefix match for /static32\) prefix match for /3\) case insensitive regex match for \.\(png\|ico\|gif\|xcf\)$ | \.\(png\|ico\|gif\|xcf\)$ |
| /static4/logo\.jpg  | 1\) priority prefix match for /static42\) prefix match for /                                                      | /static4                  |
| /static4/logo\.png  | 1\) priority prefix match for /static42\) prefix match for /                                                      | /static4                  |
| /static5/logo\.jpg  | 1\) prefix match for /2\) case sensitive regex match for logo\.jpg$                                               | logo\.jpg$                |
| /static5/logo\.png  | 1\) prefix match for /2\) case insensitive regex match for \.\(png\|ico\|gif\|xcf\)$                              | \.\(png\|ico\|gif\|xcf\)$ |
| /static5/logo\.xcf  | 1\) prefix match for /2\) case sensitive regex match for logo\.xcf$                                               | logo\.xcf$                |
| /static5/logo\.ico  | 1\) prefix match for /2\) case insensitive regex match for \.\(png\|ico\|gif\|xcf\)$                              | \.\(png\|ico\|gif\|xcf\)$ |


> 匹配顺序说明

`nginx根据uri进行最优匹配`：


- 基于前缀的`nginx` `location`匹配(没有正则表达式): 每个`location`都将根据请求`URI`进行检查
- `nginx`搜索精确的匹配: 如果=修饰符与请求`URI`完全匹配，则立即选择此特定位置块
- 如果没有找到精确的位置块(即没有相应的=修饰符)，`nginx`将继续使用非精确的前缀。它从这个`URI`的最长匹配前缀位置开始，方法如下:
    - 如果最长匹配前缀`location`有`^~`修饰符，`nginx`将立即停止搜索并选择该`location`
    - 假设最长匹配前缀`location`不使用`^~`修饰符，匹配将被临时存储，并继续执行
    - 一旦选择并存储了最长匹配前缀`location`，`nginx`就会继续计算区分大小写和不敏感的正则表达式`location`。
第一个匹配`URI`的正则表达式`location`将立即被选中来处理请求
    - 如果没有找到匹配请求`URI`的正则表达式`location`，则选择先前存储的前缀`location`来服务请求

**最长匹配解释说明：**
请求为`/a/b/c/d`时，`location A`与`location B`中`location B`为最长匹配

- `location A`
```nginx configuration
location /a {
    ...
}
```

- `location B`
```nginx configuration
location /a/b/c {
    ...
}
```