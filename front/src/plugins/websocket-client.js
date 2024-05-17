import qs from 'qs';

let socket = null;

export function connectionWebSocket(token, cid, chat_id, handle_method){
    // socket = new WebSocket('ws://localhost:8888/webSocket/'+new Date().getTime())
    socket = new WebSocket('ws://211.81.248.218:8001/ws/chat?token='+token+'&cid='+cid+'&chat_id='+chat_id)
    socket.onopen = open
    socket.onerror = error
    socket.onmessage = handle_method;
    return socket
}
export function connectionWebSocketWithoutChatId(token, cid, handle_method){
    // socket = new WebSocket('ws://localhost:8888/webSocket/'+new Date().getTime())
    socket = new WebSocket('ws://211.81.248.218:8001/ws/chat?token='+token+'&cid='+cid)
    socket.onopen = open
    socket.onerror = error
    socket.onmessage = handle_method;
    return socket
}
export function open() {
    console.info("socket连接成功")
    // send('hello')
}
export function error() {
    console.info("socket连接失败")
}
export function getMessage(msg) {
    // console.log("zzzzzz")
    console.log(msg)
    const data = JSON.parse(msg.data)
    console.log(data)
    // if (data.procedure === "connect" && data.result.code === 200){
    //     console.log(data.result.msg)
    //     const userInfo = JSON.parse(localStorage.getItem("userInfo"))
    //     let params = {
    //         operation: "add_session",
    //         id: userInfo.id
    //     }
    //     console.log("添加session")
    //     send(JSON.stringify(params))
    // }
    // else if (data.procedure === "send_message" && data.result.code === 200){
    //
    // }

}
export function send(client, text, cid) {
    console.log(text)
    var message = {
      'sender': parseInt(window.localStorage.getItem('uid')),
      'receiver': parseInt(cid),
      'is_end_of_stream': true,
      'content': text,
      'images': []
    }
    // console.log(JSON.stringify(message))
    // console.log(qs.stringify(message))
    socket.send(JSON.stringify(message));
}
export function close() {
    console.info("socket连接关闭")
}
