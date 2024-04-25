import http from '../plugins/http'

let request = ""

export function register(params){
  return http.postJson('/api/user/register', params)
}

export function login(params){
  return http.postToParams('/api/user/login', params)
}

export function user_me(params){
  return http.get('/api/user/me', params)
}

export function user_update(params){
  return http.postJson('/api/user/update', params)
}

export function user_all(){
  return http.get('/api/user/all')
}

export function user_update_password(params){
  return http.postJson('/api/user/update-password', params)
}
