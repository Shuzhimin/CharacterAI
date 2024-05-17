import http from '../plugins/http'
import axios from 'axios';
import global from '../plugins/global'
let request = ""
const ax = axios.create({
  baseURL: global.domain,
  timeout: 5000
})
export function character_select(params){
  return http.get('/api/character/select', params)
}

export function character_create(params){

  // const token = localStorage.getItem("token");//这里取token之前，你肯定需要先拿到token,存一下
  // return ax({
  //   url: '/api/character/create',
  //   method: 'POST',
  //   headers: {
  //     "content-type": "multipart/form-data",
  //     "Authorization": token
  //   },
  //   data: params,
  // })


  return http.postToFile('/api/character/create', params)
}

export function character_delete(params){
  return http.postList('/api/character/delete', params)
}

export function character_update(params, cid){
  return http.postJson('/api/character/update?cid='+cid, params)
}

