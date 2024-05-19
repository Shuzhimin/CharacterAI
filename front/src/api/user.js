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

export function user_select(params){
  return http.get('/api/user/select', params)
}

export function user_update_password(params){
  return http.postJson('/api/user/update-password', params)
}

// export function user_delete(params){
//   return http.postList('/api/user/delete', params)
// }
