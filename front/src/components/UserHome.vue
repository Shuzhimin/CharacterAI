<template>
  <el-container class="home-container">
    <!--   头部区域   -->
    <el-header>
      <div>
        <img src="src/assets/heima.png" alt="">
        <span>AI角色</span>
      </div>
      <div>
        <el-avatar :size="50" :src="cur_account.avatar_url" @click.native="openDialog" style="padding-right: 50px;"></el-avatar>
        <el-button type="info" @click="openDialog1" style="background-color: #d0ba13;padding-right: 20px">
          修改密码
        </el-button>
        <el-dialog title="修改密码" :visible.sync="dialogFormVisible1">
          <el-form :model="form">
            <el-form-item label="用户名" :label-width="formLabelWidth">
              <el-input v-model="form.username" autocomplete="off" :disabled="true"></el-input>
            </el-form-item>
            <el-form-item label="请输入当前密码" :label-width="formLabelWidth">
              <el-input v-model="form.password" :show-password="true" autocomplete="off"
                        :disabled="false"></el-input>
            </el-form-item>
            <el-form-item label="请输入新密码" :label-width="formLabelWidth">
              <el-input v-model="form.new_password" :show-password="true" autocomplete="off"
                        :disabled="false"></el-input>
            </el-form-item>

          </el-form>
          <div slot="footer" class="dialog-footer">
            <el-button @click="dialogFormVisible1 = false">取 消</el-button>
            <el-button type="primary" @click="modify1()">确 定</el-button>
          </div>
        </el-dialog>
        <el-dialog title="个人信息" :visible.sync="dialogFormVisible">
          <el-form :model="form">
            <el-form-item label="" :label-width="formLabelWidth">
              <el-switch
                  v-model="form.modifyFlag"
                  active-text="修改"
                  active-color="#13ce66"
                  inactive-text="不修改"
                  inactive-color="#ff4949">
              </el-switch>
            </el-form-item>
            <el-form-item label="用户名" :label-width="formLabelWidth">
              <el-input v-model="form.username" autocomplete="off" :disabled="true"></el-input>
            </el-form-item>
            <el-form-item v-if="!form.modifyFlag" label="用户头像" :label-width="formLabelWidth">
              <el-image :src="form.avatar_url" style="max-width: 150px; max-height: 150px;"></el-image>
            </el-form-item>

<!--            <el-form-item v-if="form.modifyFlag" label="新密码" :label-width="formLabelWidth">-->
<!--              <el-input v-model="form.new_password" :show-password="true" autocomplete="off" :disabled="!form.modifyFlag"></el-input>-->
<!--            </el-form-item>-->
<!--            <el-form-item v-if="form.modifyFlag" label="再次确认新密码" :label-width="formLabelWidth">-->
<!--              <el-input v-model="form.check_password" :show-password="true" autocomplete="off" :disabled="!form.modifyFlag"></el-input>-->
<!--            </el-form-item>-->
<!--            <el-form-item v-if="form.modifyFlag" label="人物角色头像生成" class="a">-->
<!--              <el-button @click="showGenerateAvatarDialog">AI生成角色头像</el-button>-->
<!--            </el-form-item>-->
            <el-form-item v-if="form.modifyFlag" label="头像" :label-width="formLabelWidth">
              <GenerateAvatar :avatarUrl="cur_account.avatar_url" :description="cur_account.description" @returnUrl="getAvatarUrl"></GenerateAvatar>
            </el-form-item>

          </el-form>
          <div slot="footer" class="dialog-footer">
            <el-button @click="dialogFormVisible = false">取 消</el-button>
            <el-button type="primary" @click="modify()">确 定</el-button>
          </div>
        </el-dialog>
        <GenerateAvatarDialog v-if="generateAvatarDialogVisible" @closeDialog="closeGenerateAvatarDialog" :DialogShowFlag="generateAvatarDialogVisible" :avatarUrl="cur_account.avatar_url"></GenerateAvatarDialog>
        <el-button type="info" @click="logout" style="background-color: #d01355">
          退出
        </el-button>
      </div>

    </el-header>
    <!--  页面主体区域  -->
    <el-container>
      <!--   侧边栏   -->
      <el-aside :width="isCollapsed ? '64px' : '200px'">
        <div class="toggle-button" @click="toggleCollapse">|||</div>
        <!--    侧边栏菜单区域    -->
        <el-menu
            background-color="#333744"
            text-color="#fff"
            active-text-color="#409eff"
            :unique-opened="true"
            :collapse="isCollapsed"
            :collapse-transition="false"
            :router="true"
            :default-active="activePath" >
<!--          &lt;!&ndash;  一级菜单  &ndash;&gt;-->
<!--          <div v-for="(item, index) in menulist.childrens">-->
<!--            <template slot="title">-->
<!--              &lt;!&ndash; 图标 &ndash;&gt;-->
<!--              <i :class="iconsObj[item.id]"></i>-->
<!--              &lt;!&ndash; 文本 &ndash;&gt;-->
<!--              <span>{{item.authName}}</span>-->
<!--            </template>-->
<!--            &lt;!&ndash; 二级菜单 &ndash;&gt;-->
<!--            <el-menu-item-->
<!--              :index="item.path"-->
<!--              :key="item.id"-->
<!--              @click="saveNavState(item.path)">-->
<!--              <template slot="title">-->
<!--                &lt;!&ndash; 图标 &ndash;&gt;-->
<!--                <i class="el-icon-menu"></i>-->
<!--                &lt;!&ndash; 文本 &ndash;&gt;-->
<!--                <span>{{ item.authName }}</span>-->
<!--              </template>-->
<!--            </el-menu-item>-->
<!--          </div>-->
          <el-submenu :index="item.id+''" v-for="item in menulist" :key="item.id">
            <!-- 一级菜单模板区域 -->
            <template slot="title">
              <!-- 图标 -->
              <i :class="iconsObj[item.id]"></i>
              <!-- 文本 -->
              <span>{{item.authName}}</span>
            </template>
            <!-- 二级菜单 -->
            <el-menu-item
                :index="subItem.path"
                v-for="subItem in item.childrens"
                :key="subItem.id"
                @click="saveNavState(subItem.path)">
              <template slot="title">
                <!-- 图标 -->
                <i class="el-icon-menu"></i>
                <!-- 文本 -->
                <span>{{ subItem.authName }}</span>
              </template>
            </el-menu-item>
          </el-submenu>
        </el-menu>
      </el-aside>
      <!--   右侧内容主体   -->
      <el-main>
        <!--    路由占位符    -->
        <router-view :value="activePath" @updateParentValue="handleUpdate"></router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import GenerateAvatarDialog from '@/components/dialog/GenerateAvatarDialog';
import GenerateAvatar from '@/components/GenerateAvatar';
import { user_me, user_update,user_update_password } from '@/api/user';
export default {
  name: 'home',
  components: { GenerateAvatarDialog, GenerateAvatar },
  data () {
    return {
      // 左侧菜单数据
      menulist: [
        {
          id: 101,
          authName: "功能",
          path: null,
          childrens: [
            {
              id: 1011,
              authName: "首页",
              path: '/mainpage'
            },
            {
              id: 1012,
              authName: "对话",
              path: '/dialogue'
            },
            {
              id: 1013,
              authName: '创建角色',
              path: '/createrole'
            },
            // {
            //   id: 1014,
            //   authName: '智能报表',
            //   path: '/report'
            // }
          ]
        }
      ],
      iconsObj: {
        125: 'iconfont icon-user',
        103: 'el-icon-document',
        101: 'el-icon-location',
        102: 'el-icon-s-tools',
        145: 'iconfont icon-baobiao'
      },
      // 是否折叠
      isCollapsed: false,
      // 被激活的链接地址
      activePath: '',
      dialogFormVisible: false,
      dialogFormVisible1: false,
      generateAvatarDialogVisible: false,
      formLabelWidth: '120px',
      form: {
        username: '',
        avatar_url: '',
        character_num: '',
        password: '',
        new_password: '',
        modifyFlag: false

      },
      cur_account: {
        id: 1,
        username: 'test',
        description: '',
        role: '',
        avatar_url: 'https://lingyou-1302942961.cos.ap-beijing.myqcloud.com/lingyou/16790385261248df6fb83-63b0-4497-826e-b5f2cfbe97a3.jpg',

      },

    }
  },
  created () {
    // this.getMenuList()

    this.activePath = window.sessionStorage.getItem('activePath')
    this.cur_account.id = window.localStorage.getItem("uid")
    this.cur_account.username = window.localStorage.getItem("name")
    this.cur_account.description = window.localStorage.getItem("description")
    this.cur_account.role = window.localStorage.getItem("role")
    this.cur_account.avatar_url = window.localStorage.getItem("avatarUrl")

    this.form.username = this.cur_account.username
    this.form.avatar_url = this.cur_account.avatar_url
    this.form.character_num = this.cur_account.character_num
    this.form.avatar_url = this.cur_account.avatar_url

    user_me().then(res => {
      if (res.data.role === "admin"){
        this.menulist.push({
          id: 102,
          authName: "管理",
          path: null,
          childrens: [
            {
              id: 1015,
              authName: "账号管理",
              path: '/accountmanagement'
            }
          ]
        })
        // this.menulist[0].childrens.push({
        //   id: 1015,
        //   authName: "账号管理",
        //   path: '/accountmanagement'
        // },)
      }
    })
  },
  methods: {

    logout () {
      window.sessionStorage.clear()
      localStorage.clear()
      this.$router.push('/login')
    },

    // 点击按钮，切换菜单折叠与展开
    toggleCollapse () {
      this.isCollapsed = !this.isCollapsed
    },
    // 保存链接的激活状态
    saveNavState (activePath) {
      window.sessionStorage.setItem('activePath', activePath)
      this.activePath = activePath
    },
    openDialog(){
      this.dialogFormVisible=true
      this.form.modifyFlag=false
    },
    openDialog1(){
      this.dialogFormVisible1=true
      this.form.password=''
      this.form.new_password=''
    },
    modify(){
      let params = {
        "name": this.form.username,
        "avatar_description": this.form.avatarDescription,
        "avatar_url": this.form.avatar_url
      }
      user_update(params).then(res => {
        if (res.status === 200){
          this.$message.success("修改成功！")
          user_me().then(res =>{
            console.log(res)
            window.localStorage.setItem("uid", res.data.uid)
            window.localStorage.setItem("name", res.data.name)
            window.localStorage.setItem("description", res.data.avatar_description)
            window.localStorage.setItem("avatarUrl", res.data.avatar_url)
            window.localStorage.setItem("role", res.data.role)
          })
          this.dialogFormVisible = false
        }
      })
    },
    modify1(){
      let params = {
        "old_password": this.form.password,
        "new_password": this.form.new_password,
      }
      user_update_password(params).then(res => {
        if (res.status === 200){
          this.$message.success("修改密码成功！")
          user_me().then(res =>{
            console.log(res)
            window.localStorage.setItem("password", res.data.password)
          })
          this.dialogFormVisible1 = false
        }
      })
    },
    getMsg(){

    },
    handleUpdate(newVal) {
      this.activePath = newVal; // 更新父组件的值为子组件传递的新值
    },
    showGenerateAvatarDialog() {
      // 显示生成头像对话框
      console.log(this.generateAvatarDialogVisible)
      this.generateAvatarDialogVisible = true;
      console.log(this.generateAvatarDialogVisible)
    },
    closeGenerateAvatarDialog() {
      this.generateAvatarDialogVisible = false;
    },
    getAvatarUrl(url, avatarDescription){
      this.form.avatar_url = url
      this.form.avatarDescription = avatarDescription
      console.log(url)
    }
  }
}
</script>

<style lang="less" scoped>
.el-header {
  background-color: #373d41;
  display: flex;
  justify-content: space-between;
  padding-left: 0;
  align-items: center;
  color: #ffffff;
  font-size: 20px;
  > div{
    display: flex;
    align-items: center;
    span {
      margin-left: 15px;
    }
  }
}
.el-aside {
  background-color: #333744;
  .el-menu {
    border-right: 0px;
  }
}
.el-main {
  //background-color: #eaedf1;
  background-color: #212529;
  height: 100%;
}
.home-container {
  position: absolute;
  height: 100%;
  width: 100%;
}
.iconfont {
  margin-right: 10px;
}
.toggle-button{
  background-color: #4a5064;
  font-size: 10px;
  line-height: 24px;
  color: #fff;
  text-align: center;
  letter-spacing: 0.2em;
  cursor: pointer;
}
</style>
