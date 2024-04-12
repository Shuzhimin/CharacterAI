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
