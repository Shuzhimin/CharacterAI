const DEV_ROOT = 'http://localhost:63342';
const SYSTEM_ROOT = 'http://45.41.95.10:12345';
const FAST_API = {
  // 对博客的相关操作
  ACCOUNT_INFO: SYSTEM_ROOT+'/api/account/info',
  ACCOUNT_TWEET: SYSTEM_ROOT + '/api/account/tweet',
  ACCOUNT_CHATGLM: SYSTEM_ROOT + '/api/account/chatgml',

  ACCOUNT_RETWEET: SYSTEM_ROOT + '/api/account/retweet',
  ACCOUNT_QUTOE: SYSTEM_ROOT + '/api/account/quote',
  ACCOUNT_QUTOES: SYSTEM_ROOT + '/api/account/quotes',
  ACCOUNT_REPLY: SYSTEM_ROOT + '/api/account/reply',
  ACCOUNT_REPLYS: SYSTEM_ROOT + '/api/account/replys',
  ACCOUNT_REPLY2REPLY: SYSTEM_ROOT + '/api/account/reply2reply',
  ACCOUNT_REPLY_LIKE: SYSTEM_ROOT + '/api/account/reply-like',
  ACCOUNT_LIKE: SYSTEM_ROOT + '/api/account/like',
  ACCOUNT_FOLLOW: SYSTEM_ROOT + '/api/account/follow',
  ACCOUNT_UNFOLLOW: SYSTEM_ROOT + '/api/account/unfollow',
  ACCOUNT_TASK_INFO: SYSTEM_ROOT + '/api/account/task-info',
  ACCOUNT_INCREASE_PAGE_VIEW: SYSTEM_ROOT + '/api/account/increase_page_view',

  // 智能养殖
  ACCOUNT_CRAWEL_TWEET: SYSTEM_ROOT + '/api/account/craweltweet',
  ACCOUNT_CRAWEL_COMMENT: SYSTEM_ROOT + '/api/account/crawelcomment',
  ACCOUNT_CRAWEL_LIKE: SYSTEM_ROOT + '/api/account/crawellike',
  ACCOUNT_CRAWEL_FOLLOWER: SYSTEM_ROOT + '/api/account/crawelfollower',
  ACCOUNT_CRAWEL_FOLLOWING: SYSTEM_ROOT + '/api/account/crawelfollowing',
  ACCOUNT_CRAWEL_QUOTE_ME: SYSTEM_ROOT + '/api/account/crawelquoteme',
  ACCOUNT_CRAWEL_REPLY_ME: SYSTEM_ROOT + '/api/account/crawelreplyme',
  ACCOUNT_CRAWEL_LIKE_ME: SYSTEM_ROOT + '/api/account/crawellikeme',

  ACCOUNT_HOME_LINE_TWEET: SYSTEM_ROOT + '/api/account/homelinetweet',
  ACCOUNT_HOME_LINE_USER: SYSTEM_ROOT + '/api/account/homelineuser',
  ACCOUNT_CHARACTERSET: SYSTEM_ROOT + '/api/account/characterset',



  // 受控账号管理
  ACCOUNT_ACCOUNTS: SYSTEM_ROOT + '/api/account/accounts',
  ACCOUNT_HEALTH: SYSTEM_ROOT + '/api/account/health',
  ACCOUNT_TASKS: SYSTEM_ROOT + '/api/account/tasks',
  ACCOUNT_GET_ONE_USER: SYSTEM_ROOT + '/api/account/getoneuser',
  ACCOUNT_BOT_ACCOUNT: SYSTEM_ROOT + '/api/account/bot_account',
  ACCOUNT_BY_CHARACTER: SYSTEM_ROOT + '/api/account/by_character',


  // 用户管理 previous
  // USER: SYSTEM_ROOT + '/api/user',
  // USER_LOGIN: SYSTEM_ROOT + '/api/user/login',
  // USERS: SYSTEM_ROOT + '/api/users/',
  // USERS_ME: SYSTEM_ROOT + '/api/users/me/',
  // ACCOUNT_ASSIGN: SYSTEM_ROOT + '/api/account/assign'

  // 权限管理
  LOGIN: SYSTEM_ROOT + '/login',
  GET_INFO: SYSTEM_ROOT + '/getInfo',
  LOGOUT: SYSTEM_ROOT + '/logout',
  SYSTEM_USER_PROFILE: SYSTEM_ROOT + '/system/user/profile',
  SYSTEM_USER_PROFILE_ID: SYSTEM_ROOT + '/system/user/profile/',
  SYSTEM_USER_PROFILE_UPDATE_PWD: SYSTEM_ROOT + '/system/user/profile/updatePwd',
  SYSTEM_USER_LIST: SYSTEM_ROOT + '/system/user/list',
  SYSTEM_ROLE_ALL_LIST: SYSTEM_ROOT + '/system/role/allList',
  SYSTEM_USER_ID: SYSTEM_ROOT + '/api/user/',
  SYSTEM_USER_USERNAME: SYSTEM_ROOT + '/api/user/',
  SYSTEM_USER: SYSTEM_ROOT + '/system/user',
  SYSTEM_USER_DELETE_USER: SYSTEM_ROOT + '/system/user/',

  SYSTEM_USER_RESET_PWD: SYSTEM_ROOT + '/system/user/resetPwd',
  SYSTEM_USER_CHANGE_STATUS: SYSTEM_ROOT + '/system/user/changeStatus',
  SYSTEM_ROLE_LIST: SYSTEM_ROOT + '/system/role/list',
  SYSTEM_MENU_TREE_SELECT: SYSTEM_ROOT + '/system/menu/treeselect',
  SYSTEM_ROLE_ASSIGN: SYSTEM_ROOT + '/system/role/',
  SYSTEM_ROLE_DELETE: SYSTEM_ROOT + '/system/role/',
  SYSTEM_ROLE_ADD: SYSTEM_ROOT + '/system/role',
  SYSTEM_ROLE_CHANGE_STATUS: SYSTEM_ROOT + '/system/role/changeStatus',
  SYSTEM_MENU_LIST: SYSTEM_ROOT + '/system/menu/list',
  DEV_API_SYSTEM_MENU: SYSTEM_ROOT + '/dev-api/system/menu', // 创建菜单接口(目录、菜单、按钮)
  SYSTEM_MENU1_ID: SYSTEM_ROOT + '/system/menu1/', // 获取指定菜单信息
  SYSTEM_MENU: SYSTEM_ROOT + '/system/menu', //更新菜单接口
  SYSTEM_MENU_DELETE: SYSTEM_ROOT + '/system/menu/', // 删除菜单接口



};

export {
  DEV_ROOT,
  FAST_API,
  SYSTEM_ROOT
}
