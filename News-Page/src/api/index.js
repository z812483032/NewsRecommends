import request from '@/utils/request'
import axios from "axios";

export function login(userid, password){
  let data = {
    userid: userid,
    password: password,
  }
  // console.log(data)
  let req = request.post('api/user/login/', data)
  return req
}

export function getTourists(){
  let req = request.get('api/user/tourists/')
  return req
}

export function register(userid, password, username,  words, gender){
  let data = {
    userid: userid,
    password: password,
    tags: words,
    gender: gender,
    username: username,
  }
  console.log(data)
  let req = request.post('api/user/regis/', data)
  return req
}

export function getPicture(){
  let res = request.get('api/news/pict/')
  return res
}

export function getNewsDetail(newsid,userid){
  let res = request.get('api/news/id/?newsid='+newsid+'&userid='+userid)
  return res
}

export function getAllNewsDetail(){
  let res = request.get('api/news/all/')
  return res
}

export function getTypeNewsDetail(type){
  let res = request.get('api/news/typ/?type='+type)
  return res
}

export function updateHistory(userid,newsid){
  let res = request.get('api/news/his/?userid='+userid+'&newsid='+newsid)
}

export function getUserHistory(userid){
  let res = request.get('api/user/his/?userid='+userid)
  return res
}

export function getRecNewsDetail(userid){
  let res = request.get('api/user/rec/?userid='+userid)
  return res
}

export function getSimilarnews(newsid){
  let res = request.get('api/news/recbs/?newsid='+newsid)
  return res
}

export function getHotNews(){
  let res = request.get('api/news/nhr/')
  return res
}

export function getComments(newsid){
  let res = request.get('api/news/com/?newsid='+newsid)
  return res
}

export function getUserdetail(newsid){
  let res = request.get('api/user/det/?userid='+newsid)
  return res
}

export function updateUser(userid, username, gender){
  let data = {
    'userid': userid,
    'username': username,
    'gender': gender,
  }
  let res = request.post('api/user/upb/', data)
  return res
}

export function updateTags(userid, tags){
  let data = {
    'userid': userid,
    'tags': tags
  }
  let res = request.post('api/user/uptags/',data)
  return res
}
export function getHotSpot(){
  let res = request.get('api/news/hotnews/')
  return res
}
export function submitComments(userid, newsid, comments){
  let data = {
    'userid': userid,
    'newsid':newsid,
    'comment': comments,
  }
  let res = request.post('api/news/subcom/',data)
  return res
}
export function submitCommentsToUser(userid, newsid, comments, touserid){
  let data = {
    'userid': userid,
    'newsid':newsid,
    'comment': comments,
    'touserid': touserid,
  }
  let res = request.post('api/news/subcomtou/',data)
  return res
}
export function updateGiveLike(userid, newsid, like){
  let res = request.get('api/news/updgivelike/?userid='+userid+'&newsid='+newsid+'&like='+like)
  return res
}
export function getMessage(userid){
  let res = request.get('api/user/message/?userid='+userid)
  return res
}
export function getTip(userid){
  let res = request.get('api/user/gettip/?userid='+userid)
  return res
}
export function setHadRead(id){
  let res = request.get('api/user/sethadread/?id='+id)
  return res
}
export function getTags(id){
  let res = request.get('api/user/getRegistrPageData/')
  return res
}
export function updateRec(newsid, userid){
  let res = request.get('api/news/updateRec/?newsid='+newsid+'&userid='+userid)
  return res
}
export function updateUserHeadportrait(userid, picurl){
  let data = {
    userid: userid,
    picurl: picurl,
  }
  let res = request.post('api/user/updateheadpic/', data)
  return res
}



