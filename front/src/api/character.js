import http from '../plugins/http'

let request = ""

export function character_select(params){
  return http.postJson('/api/character/select', params)
}

export function character_create(params){
  return http.postJson('/api/character/create', params)
}

