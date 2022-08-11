import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'

/**
 * Note: sub-menu only appear when route children.length >= 1
 * Detail see: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noRedirect           if set noRedirect will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    control the page roles (you can set multiple roles)
    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
    icon: 'svg-name'/'el-icon-x' the icon show in the sidebar
    noCache: true                if set true, the page will no be cached(default is false)
    affix: true                  if set true, the tag will affix in the tags-view
    breadcrumb: false            if set false, the item will hidden in breadcrumb(default is true)
    activeMenu: '/example/list'  if set path, the sidebar will highlight the path you set
  }
 */

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
export const constantRoutes = [
  {
    path: '/redirect',
    component: Layout,
    hidden: true,
    children: [
      {
        path: '/redirect/:path(.*)',
        component: () => import('@/views/redirect/index')
      }
    ]
  },
  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },
  {
    path: '/auth-redirect',
    component: () => import('@/views/login/auth-redirect'),
    hidden: true
  },
  {
    path: '/404',
    component: () => import('@/views/error-page/404'),
    hidden: true
  },
  {
    path: '/401',
    component: () => import('@/views/error-page/401'),
    hidden: true
  },
  {
    path: '/',
    component: Layout,
    redirect: '/coladnslog',
    children: [
      {
        path: 'coladnslog',
        component: () => import('@/views/coladnslog/index'),
        name: 'Cola Dnslog',
        meta: { title: 'Cola Dnslog', icon: 'dnslog', affix: true }
      }
    ]
  },
  {
    path: '/dnslog',
    component: Layout,
    redirect: 'dnslog',
    children: [
      {
        path: 'index',
        component: () => import('@/views/dnslog/index'),
        name: 'Dnslog',
        meta: { title: 'Dnslog', icon: 'dns', affix: false, noCache: true }
      }
    ]
  },
  {
    path: '/httplog',
    component: Layout,
    redirect: 'httplog',
    children: [
      {
        path: 'index',
        component: () => import('@/views/httplog/index'),
        name: 'Httplog',
        meta: { title: 'Httplog', icon: 'http', affix: false, noCache: true }
      }
    ]
  },
  {
    path: '/ldaplog',
    component: Layout,
    redirect: 'ldaplog',
    children: [
      {
        path: 'index',
        component: () => import('@/views/ldaplog/index'),
        name: 'Ldaplog',
        meta: { title: 'Ldaplog', icon: 'ldap', affix: false, noCache: true }
      }
    ]
  },
  {
    path: '/rmilog',
    component: Layout,
    redirect: 'rmilog',
    children: [
      {
        path: 'index',
        component: () => import('@/views/rmilog/index'),
        name: 'Rmilog',
        meta: { title: 'Rmilog', icon: 'rmi', affix: false }
      }
    ]
  },
  {
    path: '/profile',
    component: Layout,
    redirect: '/profile/index',
    children: [
      {
        path: 'index',
        component: () => import('@/views/profile/index'),
        name: 'Profile',
        meta: { title: 'Profile', icon: 'user', noCache: true }
      }
    ]
  },
  {
    path: 'documentation',
    component: Layout,
    children: [
      {
        path: 'https://abelche.github.io/cola_dnslog/',
        name: 'Documentation',
        meta: { title: 'API Documentation', icon: 'documentation', affix: false, noCache: true }
      }
    ]
  }
]

const createRouter = () => new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
