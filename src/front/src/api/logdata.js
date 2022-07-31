import request from '@/utils/request'

export function fetchListDnslog(query) {
  return request({
    url: '/api/dnslog/',
    method: 'get',
    params: query
  })
}

export function fetchListHttplog(query) {
  return request({
    url: '/api/httplog/',
    method: 'get',
    params: query
  })
}

export function fetchListLdaplog(query) {
  return request({
    url: '/api/ldaplog/',
    method: 'get',
    params: query
  })
}

export function fetchListRmilog(query) {
  return request({
    url: '/api/rmilog/',
    method: 'get',
    params: query
  })
}
