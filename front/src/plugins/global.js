const socket = '211.81.248.218:8000'
const domain = "http://" + socket;
const menuList = [];
let lockPage = false;
let lockPagePassword = "";

export let minioConfig = {
    host: 'files.lulinyuan.com',
    port: 443,
    useSSL: true,
    accessKey: 'T3TCCDt6PCRDvmBW',
    secretKey: '9gO4rXVwdQkaKI9vBVBo0py2vZcsY4mC',
    bucket: "nongchang-app"
}

export default{
    menuList,     //菜单
    lockPage,
    domain,
    lockPagePassword,
    socket
}
