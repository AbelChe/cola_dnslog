<template>
  <div class="app-container">
    <el-row :gutter="20">
      <el-col :span="18" :xs="24">
        <el-card>
          <h1>User Info</h1>
          <el-form :data="userinfo">
            <el-form-item label="Username">
              <el-input v-model="userinfo.name" disabled="disabled" />
            </el-form-item>
            <el-form-item label="token">
              <el-input v-model="userinfo.token" disabled="disabled" />
            </el-form-item>
            <el-form-item label="logid">
              <el-input v-model="userinfo.logid" />
            </el-form-item>
            <el-form-item label="Dingtalk Robot Token">
              <el-input v-model="userinfo.dingtalk_robot_token" />
            </el-form-item>
            <el-form-item label="Bark Url">
              <el-input v-model="userinfo.bark_url" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="Submit">Update</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { getInfo, updateInfo } from '@/api/user'

export default {
  data() {
    return {
      userinfo: {}
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
<style lang="scss">
</style>