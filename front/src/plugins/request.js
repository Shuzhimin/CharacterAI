// 导入axios
import axios from 'axios'
import Router from '@/router/index'
import global from './global'
import vuex from '@/store/index'

// 使用element-ui Message做消息提醒
import { Message } from 'element-ui';


//1. 创建新的axios实例，
const service = axios.create({
    // 公共接口--这里注意后面会讲
    baseURL: global.domain,
    // 超时时间 单位是ms，这里设置了90s的超时时间
    timeout: 180 * 1000
})
// 2.请求拦截器
service.interceptors.request.use(config => {
    //发请求前做的一些处理，数据转化，配置请求头，设置token,设置loading等，根据需求去添加
    //config.data = JSON.stringify(config.data); //数据转化,也可以使用qs转换
     config.headers = {
        'X-Requested-With':'XMLHttpRequest',
         //'Content-Type':'application/x-www-form-urlencoded;charset=UTF-8' //配置请求头
     }
     if(config.type==='form'){
         config.headers = {
             'X-Requested-With':'XMLHttpRequest',
             'Content-Type':'application/x-www-form-urlencoded;charset=UTF-8' //配置请求头
         }
     }else if(config.type==='file'){
         config.headers = {
             'X-Requested-With':'XMLHttpRequest',
             'Content-Type':'multipart/form-data;charset=UTF-8' //配置请求头
         }
     }else {
         config.headers = {
             'X-Requested-With':'XMLHttpRequest',
             'Content-Type':'application/json;charset=UTF-8' //配置请求头
         }
     }
    //注意使用token的时候需要引入cookie方法或者用本地localStorage等方法，推荐js-cookie
    const token = localStorage.getItem("token");//这里取token之前，你肯定需要先拿到token,存一下
    if(token){
        //config.params = {'token':token} //如果要求携带在参数中
        // config.headers.Authorization= "Bearer " + token; //如果要求携带在请求头中
        config.headers.Authorization = token; //如果要求携带在请求头中
    }
    return config
}, error => {
    Promise.reject(error)
})

// 3.响应拦截器
service.interceptors.response.use(response => {
    console.log(response)
    //接收到响应数据并成功后的一些共有的处理，关闭loading等
    if(response.status !== 200 ){
        // Message.error(response.data.message)
        if(response.status === 20006 ||response.status === 20002){
            localStorage.removeItem("token");
            localStorage.removeItem("userInfo");
            vuex.commit("setToken", null)
            window.location.reload()
        }
    }
    return response
}, error => {
    /***** 接收到异常响应的处理开始 *****/
    if (error && error.response) {
        // 1.公共错误处理
        // 2.根据响应码具体处理
        switch (error.response.status) {
            case 400:
                Message.error('错误请求');
                break;
            case 401:
                Message.error('未授权，请重新登录');
                break;
            case 403:
                Message.error('拒绝访问');
                break;
            case 404:
                Message.error('请求错误,未找到该资源');
                //window.location.href = "/NotFound"
                break;
            case 405:
                Message.error('请求方法未允许');
                break;
            case 408:
                Message.error('请求超时');
                break;
            case 500:
                Message.error('服务器端出错');
                break;
            case 501:
                Message.error('网络未实现');
                break;
            case 502:
                Message.error('网络错误');
                break;
            case 503:
                Message.error('服务不可用');
                break;
            case 504:
                Message.error('网络超时');
                break;
            case 505:
                Message.error('http版本不支持该请求');
                break;
            default:
                Message.error(`连接错误${error.response.status}`)
        }
    } else {
        // 超时处理
        if (JSON.stringify(error).includes('timeout')) {
            Message.error('服务器响应超时，请稍后再试');
        }else{
            Message.error('连接服务器失败');
        }
    }

    /***** 处理结束 *****/
    //如果不需要错误处理，以上的处理过程都可省略
    return Promise.resolve(error.response)
})
//4.导入文件
export default service
