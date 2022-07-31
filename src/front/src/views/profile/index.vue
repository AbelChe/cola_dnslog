<template>
  <div class="app-container">
    <el-row :gutter="20">
      <el-col :lg="12" :md="12" :sm="24" :xs="24">
        <el-card>
          <h1>User Info</h1>
          <el-form :data="userinfo">
            <el-form-item label="Username">
              <el-input v-model="userinfo.name" disabled />
            </el-form-item>
            <el-form-item label="Token">
              <el-tooltip class="item" effect="dark" content="获取一个新token" placement="right">
                <el-button style="margin:0;padding: 5px;" type="danger" round @click="dialogVisible = true"><i
                  class="el-icon-refresh"
                /></el-button>
              </el-tooltip>
              <el-input v-model="userinfo.token" disabled />
            </el-form-item>
            <el-form-item label="Logid">
              <el-input v-model="userinfo.logid" />
            </el-form-item>
            <el-form-item label="Dingtalk Robot">
              <el-switch
                ref="dingtalkswitch"
                v-model="dingtalk_switch"
                active-color="#13ce66"
                inactive-color="#ff4949"
                :disabled="switchdisabled"
                @change="ChangeDingtalkSwitch"
              />
              <el-input v-model="userinfo.dingtalk_robot_token" />
            </el-form-item>
            <el-form-item label="Bark">
              <el-input v-model="userinfo.bark_url" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="Submit">Update</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
      <el-col :lg="12" :md="12" :sm="24" :xs="24">
        <el-card>
          <h1>Change Password</h1>
          <el-form :data="userinfo">
            <el-form-item label="Current Password">
              <el-input v-model="current_password" type="password" />
            </el-form-item>
            <el-form-item label="New Password">
              <el-input v-model="new_password" type="password" />
            </el-form-item>
            <el-form-item label="New Password Again">
              <el-input v-model="new_password2" type="password" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="cgPassword">Confirm</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
    </el-row>

    <el-dialog title="Attention" :visible.sync="dialogVisible" width="30%" :before-close="handleClose">
      <h3 style="font-size:18px;">Are you sure rebuild the token?</h3>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">Cancel</el-button>
        <el-button v-loading.fullscreen.lock="fullscreenLoading" type="danger" @click="Refresh_token">Confirm
        </el-button>
      </span>
    </el-dialog>
  </div>

</template>

<script>
import { getInfo, updateInfo, newToken, changePassword, getDingtalkSwitchStatus, changeDingtalkSwitchStatus } from '@/api/user'

export default {
  data() {
    return {
      userinfo: {},
      new_token: '',
      dialogVisible: false,
      fullscreenLoading: false,
      current_password: '',
      new_password: '',
      new_password2: '',
      dingtalk_switch: true
    }
  },
  mounted() {
    this.formKeyArr = []
    this.getList(),
    this.getDtstatus()
  },
  methods: {
    getDtstatus() {
      getDingtalkSwitchStatus().then((res) => {
        this.dingtalk_switch = res.data.status
        switchdisabled = false
      })
    },
    ChangeDingtalkSwitch() {
      changeDingtalkSwitchStatus().then((res) => {
        this.$notify({
          title: '成功',
          message: 'Dingtalk Robot 推送开关更新成功',
          type: 'success'
        })
        switchdisabled = res.data.status
      })
    },
    Refresh_token() {
      this.fullscreenLoading = true
      newToken().then((res) => {
        this.fullscreenLoading = false
        this.$notify({
          title: '成功',
          message: 'token更新成功',
          type: 'success'
        })
        location.reload()
      })
      this.dialogVisible = false
    },
    getList() {
      getInfo()
        .then((res) => {
          console.log(res)
          this.listLoading = true
          this.userinfo = res.data
          setTimeout(() => {
            this.listLoading = false
          }, 0.2 * 1000)
        })
    },
    Submit() {
      const postdata = {}
      postdata['dingtalk_robot_token'] = this.userinfo.dingtalk_robot_token ? this.userinfo.dingtalk_robot_token : ''
      postdata['bark_url'] = this.userinfo.bark_url ? this.userinfo.bark_url : ''
      postdata['logid'] = this.userinfo.logid ? this.userinfo.logid : ''
      updateInfo(postdata).then((res) => {
        this.$notify({
          title: '成功',
          message: '更新成功',
          type: 'success'
        })
        this.getList()
      }).catch((err) => {
        this.$notify.error({
          title: '失败',
          message: err
        })
        this.getList()
      })
    },
    cgPassword() {
      const postdata = {}
      if (this.new_password === this.new_password2) {
        postdata['password'] = this.current_password
        postdata['new_password'] = this.new_password
        console.log(postdata)
        changePassword(postdata).then((res) => {
          this.$notify({
            title: '成功',
            message: '更新成功',
            type: 'success'
          })
          this.$cookieStore.delCookie('token')
          localStorage.clear()
          this.$router.push(`/login?redirect=${this.$route.fullPath}`)
        })
      } else {
        this.$notify.error({
          title: '失败',
          message: '两次密码不一致'
        })
      }
    }
  }
}
</script>
<style lang="scss">
</style>
