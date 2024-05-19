import http from '../plugins/http'

export function admin_user_select(params){
  return http.get('/api/admin/user/select', params)
}

export function admin_character_select(params){
  return http.get('/api/admin/character/select', params)
}

export function admin_user_delete(params){
  return http.postList('/api/admin/user/delete', params)
}

export function admin_user_update_profile(params){
  return http.postJson('/api/admin/user/update-profile', params)
}

export function admin_user_update_role(params){
  return http.postJson('/api/admin/user/update-role', params)
}
