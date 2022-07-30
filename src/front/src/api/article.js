import request from '@/utils/request'

export function fetchListDnslog(query) {
  return request({
    // url: '/vue-element-admin/article/list',
    url: '/api/dnslog/',
    method: 'get',
    params: query
  })
}

export function fetchListHttplog(query) {
  return request({
    // url: '/vue-element-admin/article/list',
    url: '/api/httplog/',
    method: 'get',
    params: query
  })
}

export function fetchListLdaplog(query) {
  return request({
    // url: '/vue-element-admin/article/list',
    url: '/api/ldaplog/',
    method: 'get',
    params: query
  })
}

export function fetchListRmilog(query) {
  return request({
    // url: '/vue-element-admin/article/list',
    url: '/api/rmilog/',
    method: 'get',
    params: query
  })
}

export function fetchArticle(id) {
  return request({
    url: '/vue-element-admin/article/detail',
    method: 'get',
    params: { id }
  })
}

export function fetchPv(pv) {
  return request({
    url: '/vue-element-admin/article/pv',
    method: 'get',
    params: { pv }
  })
}

export function createArticle(data) {
  return request({
    url: '/vue-element-admin/article/create',
    method: 'post',
    data
  })
}

export function updateArticle(data) {
  return request({
    url: '/vue-element-admin/article/update',
    method: 'post',
    data
  })
}
