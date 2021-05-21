import {resetRouter} from '@/router'

export function resetTokenAndClearUser() {
  // 退出登陆 清除用户资料
  sessionStorage.setItem('userImg','')
  sessionStorage.setItem('userName', '')
  sessionStorage.setItem('userId', '')
  sessionStorage.setItem('gender', '')
  sessionStorage.setItem('token', '')
  // 重设路由
  resetRouter()
}

export const defaultDocumentTitle = '新闻中心'

export function getDocumentTitle(pageTitle) {
  if (pageTitle) return `${defaultDocumentTitle} - ${pageTitle}`
  return `${defaultDocumentTitle}`
}
