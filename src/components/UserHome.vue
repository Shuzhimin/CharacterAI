<template>
  <el-container class="home-container">
    <!--   头部区域   -->
    <el-header>
      <div>
        <img src="src/assets/heima.png" alt="">
        <span>AI角色</span>
      </div>
      <div>
        <el-button type="info" @click="openDialog" style="background-color: #d0ba13;padding-right: 20px">
          查看个人信息
        </el-button>
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
            <el-form-item label="学号" :label-width="formLabelWidth">
              <el-input v-model="form.sno" autocomplete="off" :disabled="true"></el-input>
            </el-form-item>
            <el-form-item label="姓名" :label-width="formLabelWidth">
              <el-input v-model="form.name" autocomplete="off" :disabled="!form.modifyFlag"></el-input>
            </el-form-item>
            <el-form-item label="邮箱" :label-width="formLabelWidth">
              <el-input v-model="form.email" autocomplete="off" :disabled="!form.modifyFlag"></el-input>
            </el-form-item>
            <el-form-item label="新密码" :label-width="formLabelWidth">
              <el-input v-model="form.new_password" :show-password="true" autocomplete="off" :disabled="!form.modifyFlag"></el-input>
            </el-form-item>
            <el-form-item label="再次确认新密码" :label-width="formLabelWidth">
              <el-input v-model="form.check" :show-password="true" autocomplete="off" :disabled="!form.modifyFlag"></el-input>
            </el-form-item>
          </el-form>
          <div slot="footer" class="dialog-footer">
            <el-button @click="dialogFormVisible = false">取 消</el-button>
            <el-button type="primary" @click="modify()">确 定</el-button>
          </div>
        </el-dialog>
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
          <!--  一级菜单  -->
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
        <router-view></router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
export default {
  name: 'home',
  data () {
    return {
      // 左侧菜单数据
      menulist: [
        {
          id: 101,
          authName: "查看",
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
              path: '/create'
            }
          ]
        }
      ],
      iconsObj: {
        125: 'iconfont icon-user',
        103: 'el-icon-document',
        101: 'el-icon-location',
        102: 'iconfont icon-danju',
        145: 'iconfont icon-baobiao'
      },
      // 是否折叠
      isCollapsed: false,
      // 被激活的链接地址
      activePath: '',
      dialogFormVisible: false,
      formLabelWidth: '120px',
      form: {
        id: '',
        sno: '',
        name: '',
        new_password: '',
        check: '',
        email: '',
        modifyFlag: false
      },
    }
  },
  created () {
    // this.getMenuList()

    this.activePath = window.sessionStorage.getItem('activePath')
    this.form.id = window.sessionStorage.getItem('id')

    this.getMsg()
    this.form.id = window.sessionStorage.getItem('id')
    this.form.sno = window.sessionStorage.getItem('sno')
    this.form.name = window.sessionStorage.getItem('name')
    this.form.email = window.sessionStorage.getItem('email')
  },
  methods: {
    logout () {
      window.sessionStorage.clear()
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
      this.form.new_password=''
      this.form.check=''
    },
    async modify(){
      if (this.form.modifyFlag === false){
        this.dialogFormVisible = false
        return
      }else {
        if (this.form.new_password !== this.form.check){
          this.$message.error("两次输入密码不一致！")
          return
        }
        const {data: res} = await this.$http.get('/library_occupy/student/modify', {params: this.form})
        console.log(res)
        if (res.flag === false){
          this.$message.success(res.msg)
        }
        else {
          this.$message.success("修改成功！请重新登录")
          this.logout()
        }
        this.dialogFormVisible = false
      }
    },
    async getMsg(){
      const {data: res} = await this.$http.get('/library_occupy/student/getMsg', {params: {'id': this.form.id}})
      console.log(res)
      window.sessionStorage.setItem('id',res.data.id)
      window.sessionStorage.setItem('sno',res.data.sno)
      window.sessionStorage.setItem('name',res.data.name)
      window.sessionStorage.setItem('status',res.data.status)
      window.sessionStorage.setItem('email',res.data.email)
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
  background-color: #eaedf1;
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
