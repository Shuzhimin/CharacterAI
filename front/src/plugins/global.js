// const domain = "https://appadmin.lulinyuan.com";
const domain = "http://211.81.248.216:8000";

const menuList = [];
let lockPage = false;
let lockPagePassword = "";

// export let minioConfig = {
//     host: '192.168.0.119',
//     port: 9000,
//     useSSL: false,
//     accessKey: 'FsVthvXaExOwUAbZ',
//     secretKey: 'DKya03bkigmXxWbU82WQKo1Rhe13SXGp',
//     bucket: "nongchang-app"
// }
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
}
