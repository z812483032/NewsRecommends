import request from '@/utils/request'

export function fetchNewsData() {
    let req = request.get('/news')
    return req
}

export function fetchUserData() {
    let req = request.get('/user/all')
    return req
}

export function fetchCommentsData() {
    let req = request.get('/user/allcomments/')
    return req
}

export function delUserData(userid) {
    let req = request.get('/user/del?userid=' + userid)
    return req
}

export function delCommentData(commentsid, userid, newsid, choose) {
    let req = request.get('/user/delcomment?commentsid=' + commentsid + '&userid=' + userid + '&newsid=' + newsid + '&choose=' + choose)
    return req
}

export function updateUserData(userid1, username1, gender1, ip1, tags1) {
    if (gender1 == '女') {
        gender1 = 0
    } else {
        gender1 = 1
    }
    let data = {
        userid: userid1,
        username: username1,
        gender: gender1,
        ip: ip1,
        tags: tags1,
    }
    console.log('data', data)
    let req = request.post('/user/up/', data)
    console.log('req', req)
    return req
}

export function delNewsData(newsurl) {
    let req = request.get('/news/del?url=' + newsurl)
    return req
}

export function getData() {
    let req = request.get('/management/homedata')
    return req
}

export function urlspider(time, gettime) {
    let req = request.get('/spider/urlbegin/?time=' + time + '&oritime=' + gettime)
    return req
}

export function detailspider(time, gettime) {
    let req = request.get('/spider/detailbegin/?time=' + time + '&oritime=' + gettime)
    return req
}

export function getSpiderPageData() {
    let req = request.get('/spider/getspiderdata/')
    return req
}

export function getRecommendPageData() {
    let req = request.get('/recommend/getrecommenddata/')
    return req
}

export function closeurlspider() {
    let req = request.get('spider/closeserve/?servename=url')
    return req
}

export function closedetailspider() {
    let req = request.get('spider/closeserve/?servename=detail')
    return req
}

export function download(filepath) {
    let req = request.get('download/logs/?filepath=' + filepath)
    return req
}

export function recommendOn(time, gettime) {
    let req = request.get('/recommend/startrecommend/?time=' + time + '&oritime=' + gettime)
    return req
}

export function recommendOff() {
    let req = request.get('recommend/stopsystem/?servename=recommend')
    return req
}

export function analysisOn(time, gettime) {
    let req = request.get('/recommend/startanalysis/?time=' + time + '&oritime=' + gettime)
    return req
}

export function analysisOff() {
    let req = request.get('recommend/stopsystem/?servename=analysis')
    return req
}

export function getSearchNewsResult(keyword) {
    let req = request.get('news/search?keyword=' + keyword)
    return req
}

export function getSearchUserResult(keyword) {
    let req = request.get('user/search?keyword=' + keyword)
    return req
}

export function getSearchCommentsResult(keyword) {
    let req = request.get('comments/search?keyword=' + keyword)
    return req
}
