import http from '../plugins/http'

let request = ""

export function generation(params){
  return http.postJson('/api/generation/image', params)
}
