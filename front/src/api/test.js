import http from '../plugins/http'

let request = ""

export function testAPI(params){
  return http.postToParams('/library_occupy/admin/login', params)
}
