# AI物流智能客服系统（LLM Agent）V2
版本号：v2.0.0

项目简介：
LLM + Tool Calling 架构

技术栈：\p
Python / FastAPI / SQLAlchemy / SQLite
LLM Agent 架构 / Intent Recognition / Repository Pattern
分层架构设计 / RESTful API
## 快速开始
### 一、创建虚拟环境
在pycharm新建项目
````bash
# 在根目录创建名为 .venv 的虚拟环境
python -m venv .venv
````
激活虚拟环境
````bash
.venv\Scripts\activate
````
### 二、安装依赖
保持打开虚拟环境，运行
````bash
pip install -r requirements.txt
````

### 三、连接数据库
数据库文件:data/orders.db，可以先删除，再初始化并添加数据
````bash
#初始化数据库，建立表格和字段
 python -m app.database.init_db
````
````bash
#往里面添加数据
 python -m app.database.seed
````
可以用navicat查看数据是否添加成功
### 四、运行main
在虚拟环境中运行main，相关命令：
````bash
.venv\Scripts\activate  #如果虚拟环境已经激活，这条命令可忽略
python -m app.main
````
示例：
![img_4.png](img_4.png)

运行成功后可点击\
http://127.0.0.1:8000/docs

进入网址后点击“POST”找到try it out 按钮并点击
![img_1.png](img_1.png)

输入示例数据并点击按钮
![img_2.png](img_2.png)

输出：
![img_3.png](img_3.png)

