import http from '../plugins/http'

export function report(params){
  return http.postJson('/api/report/character', params)
}
