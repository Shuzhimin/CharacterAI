import http from '../plugins/http'

let request = ""

export function chat_select(params) {
  return http.get('/api/chat/select', params)
}
