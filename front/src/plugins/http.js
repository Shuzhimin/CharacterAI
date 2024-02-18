// 导入封装好的axios实例
import request from './request'
import qs from 'qs'

const http = {
    /**
     * methods: 请求
     * @param url 请求地址
     * @param params 请求参数
     */
    get(url,params){
        const config = {
            method: 'get',
            url:url,
            type:'form'
        }
        if(params) config.params = params
        return request(config)
    },
    post(url,params){
        const config = {
            method: 'post',
            url:url
        };
        if(params) config.data = qs.stringify(params)
        return request(config)
    },

    postToParams(url,params){
        const config = {
            method: 'post',
            url:url,
            type:'form',
        };
        if(params) config.data = qs.stringify(params);
        return request(config)
    },
    postJson(url,params){
        const config = {
            method: 'post',
            url:url
        };
        if(params) config.data = qs.parse(params)
        return request(config)
    },
    postToFile(url,params){
        const config = {
            method: 'post',
            url:url,
            type:'file',
        };
        if(params) config.data = params;
        return request(config)
    },
    put(url,params){
        const config = {
            method: 'put',
            url:url
        }
        if(params) config.params = params
        return request(config)
    },
    delete(url,params){
        const config = {
            method: 'delete',
            url:url
        }
        if(params) config.params = params
        return request(config)
    }
}
//导出
export default http
