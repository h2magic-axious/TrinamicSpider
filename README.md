# 组件：

## 1. 网页本地化

将Trinamic官网的所有产品的详情页面下载到本地

## 2. Section分拣

从每个HTML页面中，分拣出有用的section元素，并规范化输出

## 3. Json序列化

根据分拣出的section， 生成Json格式的产品记录

## 4. Render渲染

输入一个Json文件，渲染成Html格式的字符串，用以上传到网站页面

## 5. WP-API封装

标准化WP-API的使用方式

## 6. 文件下载器

解析Json文件，下载记录中的媒体和资源文件

## 7. 七牛API封装

标准化七牛云的API的使用方式，用以上传文件

# Guide
> 每个文件中的main函数会执行该组件的所有功能

## Spider.py
根据Reference.py中的PRODUCT变量，爬取所有商品的详情页面

## SectionSorter.py
根据Spider爬到的所有HTML文件，处理每个页面的数据：

1. **Trinamic_Fields**：记录所有商品的参数信息
2. **Trinamic_Picture**：记录所有商品的功能图片
3. **Trinamic_Resource**：记录所有商品的资源文件
4. **Trinamic_Json**：记录每个商品的详细信息

## Render.py
根据**Trinamic_Json**中文件，对应的渲染成HTML页面，存放在**Trinamic_Render**目录下

## Wordpress.py
根据**Trinamic_Render**中文件，上传/更新 网站上的对应页面，如果某个记录没有发布在网站上，会被新建文章发布

## Downloader.py
根据**Trinamic_Resource**和**Trinamic_Picture**中的记录，下载所有的静态资源，存放在**Download_Resource**目录下

## Qiniu.py
将**Download_Resource**中的所有文件上传到七牛云

# 推荐脚本执行顺序
1. Spider.py
2. SectionSorter.py
3. Render.py
4. Wordpress.py
5. Downloader.py
6. Qiniu.py