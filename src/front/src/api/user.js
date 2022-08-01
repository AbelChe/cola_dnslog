import request from '@/utils/request'

export function login(data) {
  return request({
    url: '/api/user/auth',
    method: 'post',
    data,
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    transformRequest: [
      (data) => {
        let ret = ''
        for (const it in data) {
          ret +=
            encodeURIComponent(it) + '=' + encodeURIComponent(data[it]) + '&'
        }
        return ret
      }
    ]
  })
}

export function getInfo() {
  return request({
    url: '/api/user/info',
    method: 'get'
  })
}

export function updateInfo(data) {
  return request({
    url: '/api/user/info/update',
    method: 'post',
    data
  })
}

export function newToken() {
  return request({
    url: '/api/user/new_token',
    method: 'post'
  })
}

export function changePassword(data) {
  return request({
    url: '/api/user/info/change_password',
    method: 'post',
    data
  })
}

export function getMyServerinfo() {
  return request({
    url: '/api/user/get_my_server_info',
    method: 'get'
  })
}

export function getDingtalkSwitchStatus() {
  return request({
    url: '/api/user/get_dingtalk_switch_status',
    method: 'get'
  })
}

export function changeDingtalkSwitchStatus(data) {
  return request({
    url: '/api/user/change_dingtalk_switch_status',
    method: 'get',
    data
  })
}

export function getBarkSwitchStatus() {
  return request({
    url: '/api/user/get_bark_switch_status',
    method: 'get'
  })
}

export function changeBarkSwitchStatus(data) {
  return request({
    url: '/api/user/change_bark_switch_status',
    method: 'get',
    data
  })
}