# API 文档

## 获取 Token

登录到Cola Dnslog的Web平台，在用户信息处获取到Token

> ⚠️ Token是长期有效的，如果Token泄漏，请点击`获取新Token`按钮，获取新的Token，并修改您的密码。

![image-20220811153203578](docs_resource/image-20220811153203578.png)

在之后的调用中需要在Header中添加您的Token，形如：

```sh
curl -s -H "Authorization: Bearer xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" <url>
```

## 获取相关服务信息

接口URL `http://1.1.1.1:28001/api/user/get_my_server_info`

例，获取我的Cola Dnslog服务信息

```sh
curl -s -H "Authorization: Bearer xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" 'http://1.1.1.1:28001/api/user/get_my_server_info' | jq
{
  "code": 20000,
  "message": "success",
  "data": {
    "logid": "5ej",
    "domain": "5ej.example.com",
    "http": "x.x.x.x",
    "ldap": "x.x.x.x:1389",
    "rmi": "x.x.x.x:1099"
  }
}
```

## 获取记录

### DNS

接口URL `http://1.1.1.1:28001/api/dnslog/?page=1&limit=3&sort=-id`

> page: 第几页
>
> limit: 获取几条数据
>
> sort: 排序方式可选两种+id和-id（默认），-id为倒序

例，获取最新的3条dns请求：

```sh
curl -s -H "Authorization: Bearer xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" 'http://1.1.1.1:28001/api/dnslog/?page=1&limit=3&sort=-id' | jq
{
  "code": 20000,
  "page": 1,
  "limit": 3,
  "data": {
    "total": 216,
    "items": [
      {
        "record_time": "2022-08-10T17:28:27",
        "record": "file1.5ej.example.com",
        "owner_id": 1,
        "id": 216,
        "ip_from": "x.x.x.x"
      },
      {
        "record_time": "2022-08-10T17:28:27",
        "record": "file1.5ej.example.com",
        "owner_id": 1,
        "id": 215,
        "ip_from": "x.x.x.x"
      },
      {
        "record_time": "2022-08-10T17:28:24",
        "record": "file1.5ej.example.com",
        "owner_id": 1,
        "id": 214,
        "ip_from": "x.x.x.x"
      }
    ]
  }
}
```

### HTTP

接口URL `http://1.1.1.1:28001/api/httplog/?page=1&limit=3&sort=-id`

> page: 第几页
>
> limit: 获取几条数据
>
> sort: 排序方式可选两种+id和-id（默认），-id为倒序

例，获取最新的3条http请求：

```sh
curl -s -H "Authorization: Bearer xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" 'http://1.1.1.1:28001/api/httplog/?page=1&limit=3&sort=-id' | jq
{
  "code": 20000,
  "page": 1,
  "limit": 3,
  "data": {
    "total": 43,
    "items": [
      {
        "request_method": "GET",
        "path": "/5ej/longxxxxxxxxxxx",
        "id": 43,
        "ip_from": "x.x.x.x",
        "record_time": "2022-08-01T17:52:01",
        "owner_id": 1,
        "headers": "Host: x.x.x.x\nUser-Agent: curl/7.64.1\nAccept: */*\n\n",
        "content_length": -1,
        "body_data": null,
        "useragent": "curl/7.64.1"
      },
      {
        "request_method": "POST",
        "path": "/5ej/longxxxxxxxxxxx",
        "id": 42,
        "ip_from": "x.x.x.x",
        "record_time": "2022-08-01T17:51:52",
        "owner_id": 1,
        "headers": "Host: x.x.x.x\nUser-Agent: curl/7.64.1\nAccept: */*\nContent-Length: 4897552\nContent-Type: application/x-www-form-urlencoded\nExpect: 100-continue\n\n",
        "content_length": 4897552,
        "body_data": "xxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "useragent": "curl/7.64.1"
      },
      {
        "request_method": "POST",
        "path": "/5ej/largefile123",
        "id": 41,
        "ip_from": "x.x.x.x",
        "record_time": "2022-08-01T17:50:40",
        "owner_id": 1,
        "headers": "Host: x.x.x.x\nUser-Agent: curl/7.64.1\nAccept: */*\nContent-Length: 4897552\nContent-Type: application/x-www-form-urlencoded\nExpect: 100-continue\n\n",
        "content_length": 4897552,
        "body_data": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "useragent": "curl/7.64.1"
      }
    ]
  }
}
```

### LDAP

接口URL `http://1.1.1.1:28001/api/ldaplog/?page=1&limit=3&sort=-id`

> page: 第几页
>
> limit: 获取几条数据
>
> sort: 排序方式可选两种+id和-id（默认），-id为倒序

例，获取最新的3条ldap请求：

```sh
curl -s -H "Authorization: Bearer xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" 'http://1.1.1.1:28001/api/ldaplog/?page=1&limit=3&sort=-id' | jq
{
  "code": 20000,
  "page": 1,
  "limit": 3,
  "data": {
    "total": 48,
    "items": [
      {
        "record_time": "2022-08-01T17:50:33",
        "pathname": "xxx/xxx/5ej",
        "owner_id": 1,
        "id": 48,
        "ip_from": "x.x.x.x"
      },
      {
        "record_time": "2022-08-01T17:50:33",
        "pathname": "xxx/xxx/5ej",
        "owner_id": 1,
        "id": 47,
        "ip_from": "x.x.x.x"
      },
      {
        "record_time": "2022-08-01T17:50:32",
        "pathname": "xxx/xxx/5ej",
        "owner_id": 1,
        "id": 46,
        "ip_from": "x.x.x.x"
      }
    ]
  }
}
```

### RMI

接口URL `http://1.1.1.1:28001/api/rmilog/?page=1&limit=3&sort=-id`

> page: 第几页
>
> limit: 获取几条数据
>
> sort: 排序方式可选两种+id和-id（默认），-id为倒序

例，获取最新的3条rmi请求：

```sh
curl -s -H "Authorization: Bearer kuhrescmvuezb8rwjh62poistpkcvba4" 'http://1.1.1.1:28001/api/rmilog/?page=1&limit=3&sort=-id' | jq
{
  "code": 20000,
  "page": 1,
  "limit": 3,
  "data": {
    "total": 51,
    "items": [
      {
        "rmi_client_ip": "x.x.x.x",
        "record_time": "2022-08-10T02:20:56",
        "id": 51,
        "objectname": "hellox5ej",
        "ip_from": "x.x.x.x",
        "owner_id": 1
      },
      {
        "rmi_client_ip": "x.x.x.x",
        "record_time": "2022-08-10T02:10:18",
        "id": 50,
        "objectname": "hellox5ej",
        "ip_from": "x.x.x.x",
        "owner_id": 1
      },
      {
        "rmi_client_ip": "x.x.x.x",
        "record_time": "2022-08-10T02:09:59",
        "id": 49,
        "objectname": "xxxx5ej",
        "ip_from": "x.x.x.x",
        "owner_id": 1
      }
    ]
  }
}
```























