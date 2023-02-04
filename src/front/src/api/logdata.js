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

export function deleteDnslog(query) {
  return request({
    url: '/api/dnslog/delete',
    method: 'get',
    params: query
  })
}

export function deleteDnslog_all(query) {
  return request({
    url: '/api/dnslog/delete/all',
    method: 'get'
  })
}

export function deleteHttplog(query) {
  return request({
    url: '/api/httplog/delete',
    method: 'get',
    params: query
  })
}

export function deleteHttplog_all(query) {
  return request({
    url: '/api/httplog/delete/all',
    method: 'get'
  })
}

export function deleteLdaplog(query) {
  return request({
    url: '/api/ldaplog/delete',
    method: 'get',
    params: query
  })
}

export function deleteLdaplog_all(query) {
  return request({
    url: '/api/ldaplog/delete/all',
    method: 'get'
  })
}

export function deleteRmilog(query) {
  return request({
    url: '/api/rmilog/delete',
    method: 'get',
    params: query
  })
}

export function deleteRmilog_all(query) {
  return request({
    url: '/api/rmilog/delete/all',
    method: 'get'
  })
}
