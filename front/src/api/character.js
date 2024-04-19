import http from '../plugins/http'

let request = ""

export function character_select(){
  return http.get('/api/character/select')
}

export function character_create(params){
  return http.postJson('/api/character/create', params)
}

export function character_delete(params){
  return http.postList('/api/character/delete', params)
}

export function character_update(params, cid){
  return http.postJson('/api/character/update?cid='+cid, params)
}

