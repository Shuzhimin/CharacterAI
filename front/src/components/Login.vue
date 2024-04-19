<template>
  <div class="login_container">
    <div class="title">
      <p>AI虚拟角色养成系统 V1.0</p>
    </div>
<!--    <div class="skip">-->
<!--      <a href="http://localhost:8080/home#/userhome">跳转到用户页面</a>-->
<!--    </div>-->
<!--    <div class="skip">-->
<!--      <a href="http://localhost:8080/home#/adminhome">跳转到教材发行人员页面</a>-->
<!--    </div>-->
<!--    <div class="skip">-->
<!--      <a href="http://localhost:8080/home#/buyerhome">跳转到采购人员页面</a>-->
<!--    </div>-->
    <div class="login_box">
      <!--头像区域-->
      <div class="avatar_box">
        <img src="../assets/logo.png" alt="">
      </div>
      <!--登陆表单区域-->
      <el-form ref="loginFormRef" :model="loginForm" :rules="loginFormRules"  label-width="0px" class="login_form">
        <!--用户名-->
        <el-form-item prop="username">
          <el-input v-model="loginForm.username" prefix-icon="el-icon-user" placeholder="账号"></el-input>
        </el-form-item>
        <!--密码-->
        <el-form-item prop="password">
          <el-input v-model="loginForm.password" prefix-icon="el-icon-lock"
                    type="password" :show-password="true" placeholder="密码"></el-input>
        </el-form-item>
<!--        <template>-->
<!--          <el-radio v-model="radio" label="1">学生/教师</el-radio>-->
<!--          <el-radio v-model="radio" label="2">教材发行人员</el-radio>-->
<!--          <el-radio v-model="radio" label="3">采购人员</el-radio>-->
<!--        </template>-->

        <!--按钮区-->
        <el-form-item class="btns">
<!--          <el-select class="select" v-model="value" placeholder="请选择">-->
<!--            <el-option-->
<!--                v-for="item in options"-->
<!--                :key="item.value"-->
<!--                :label="item.label"-->
<!--                :value="item.value">-->
<!--            </el-option>-->
<!--          </el-select>-->
          <el-button type="primary" @click="login" style="float: left">登录</el-button>
          <el-button type="info" @click="openDialog()">注册</el-button>



        </el-form-item>
      </el-form>
    </div>
    <el-dialog :visible.sync="dialogFormVisible" style="">
      <el-form :model="query" ref="register" :rules="registerFormRules">
        <el-form-item label="用户名" :label-width="formLabelWidth" prop="username">
          <el-input v-model="query.username" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="密码" :label-width="formLabelWidth" prop="password">
          <el-input type="password" v-model="query.password" autocomplete="off" :show-password="true"></el-input>

        </el-form-item>
        <el-form-item label="再次确认密码" :label-width="formLabelWidth" prop="repassword">
          <el-input type="password" v-model="query.repassword" autocomplete="off" :show-password="true"></el-input>
<!--          <span>两次密码不一致</span>-->
        </el-form-item>
<!--        <el-form-item label="人物角色头像生成" class="a">-->
<!--          <el-button @click="showGenerateAvatarDialog">AI生成角色头像</el-button>-->
<!--        </el-form-item>-->
        <el-form-item label="头像" :label-width="formLabelWidth">
          <GenerateAvatar :avatarUrl="query.avatar_url" @returnUrl="getAvatarUrl"></GenerateAvatar>
        </el-form-item>
      </el-form>

      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="register()" :disabled="registerFlag">注 册</el-button>
      </div>
    </el-dialog>
    <GenerateAvatarDialog v-if="generateAvatarDialogVisible" @closeDialog="closeGenerateAvatarDialog" :DialogShowFlag="generateAvatarDialogVisible" :avatarUrl="query.avatar_url"></GenerateAvatarDialog>
  </div>
</template>

<script>
import GenerateAvatarDialog from '@/components/dialog/GenerateAvatarDialog';
import GenerateAvatar from '@/components/GenerateAvatar';
import { register, login, user_me } from '@/api/user';
export default {
  components: {
    GenerateAvatarDialog,
    GenerateAvatar
  },
  data () {
    const equalToPassword = (rule, value, callback) => {
      if (this.query.password !== this.query.repassword) {
        console.log(1)
        callback(new Error("两次输入的密码不一致"))
      }
      else {
        console.log(2)
        callback()
      }
    }
    return {
      radio: 1,
      // 这是登陆表单的数据绑定对象
      loginForm: {
        username: '',
        password: '',
        // status: 0
      },
      // 表单的验证规则对象
      loginFormRules: {
        // 验证用户名是否合法
        username: [
          { required: true, message: '请输入账号', trigger: 'blur' },
          { min: 1, max: 10, message: '长度在 1 到 10 个字符', trigger: 'blur' }
        ],
        // 验证密码是否合法
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 1, max: 15, message: '长度在 1 到 15 个字符', trigger: 'blur' }
        ]
      },
      options: [{
        value: 1,
        label: '教师'
      }, {
        value: 2,
        label: '学生'
      }, {
        value: 3,
        label: '教材发行人员'
      }, {
        value: 4,
        label: '采购人员'
      }],
      value: '',
      registerOption: [
        {
          value: 1,
          label: '学生'
        },
        {
          value: 2,
          label: '教师'
        }
      ],
      registerValue: '',
      dialogFormVisible: false,
      formLabelWidth: '120px',
      query: {
        username: '',
        password: '',
        repassword: '',
        avatar_url: ''
      },
      registerFormRules: {
        // 验证用户名是否合法
        username: [
          { required: true, message: '请输入账号', trigger: 'blur' },
          { min: 1, max: 10, message: '长度在 1 到 10 个字符', trigger: 'blur' }
        ],
        // 验证密码是否合法
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 1, max: 15, message: '长度在 1 到 15 个字符', trigger: 'blur' }
        ],
        repassword: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 1, max: 15, message: '长度在 1 到 15 个字符', trigger: 'blur' },
          { validator: equalToPassword, message: '两次输入的密码不一致', trigger: 'blur' }
        ],
      },
      registerFlag: false,
      receive: {

      },
      generateAvatarDialogVisible: false,
    }
  },
  methods: {
    // 点击重置按钮，重置登录表单
    openDialog () {
      // console.log(this)
      this.dialogFormVisible=true
      // this.query.status=this.value
      console.log("zzz")
      // console.log(this.query.status)
    },
    //
    login () {

      this.$refs['loginFormRef'].validate((valid) => {
        if (valid) {
          console.log('登录')

          let params = {
            "username": this.loginForm.username,
            "password": this.loginForm.password
          }
          login(params).then(res => {
            console.log(res)
            if (res.status === 200){
              window.localStorage.setItem("token", res.data.token_type + " " + res.data.access_token)

              user_me().then(res =>{
                console.log(res)
                window.localStorage.setItem("uid", res.data.uid)
                window.localStorage.setItem("name", res.data.name)
                window.localStorage.setItem("description", res.data.avatar_description)
                window.localStorage.setItem("avatarUrl", res.data.avatar_url)
                window.localStorage.setItem("role", res.data.role)

                this.$message.success("登录成功！")
                this.$router.push('/userhome')
              })


            }
          })


        }
      })

      // if (this.value === ''){
      //   return this.$message.error('请选择账号类别')
      // }
      // this.loginForm.status=this.value
      // console.log(this.loginForm)
      // const {data: res} = await this.$http.get('/orderbook/user/login',{params: this.loginForm})
      // console.log(res)
      //
      // if (res.code !== 200){
      //   return this.$message.error(res.msg)
      // }
      //
      // this.$userid=res.data.id
      // window.sessionStorage.setItem("userid",this.$userid)
      // this.$username=res.data.username
      // window.sessionStorage.setItem("username",this.$username)
      // this.$token=res.token
      // window.sessionStorage.setItem("token",this.$token)
      // this.$tel=res.data.tel
      // window.sessionStorage.setItem("tel",this.$tel)
      // this.$status=res.data.status
      // window.sessionStorage.setItem("status",this.$status)
      //
      // if (this.$status === 1){
      //   this.$message.success(this.$username+'登录成功')
      //   this.$router.push('/userhome')
      // }
      // else if (this.$status === 2){
      //   this.$message.success('教师登录成功')
      //   this.$router.push('/userhome')
      // }
      // else if (this.$status === 3){
      //   this.$message.success('教材发行人员登录成功')
      //   this.$router.push('/adminhome')
      // }
      // else if (this.$status === 4){
      //   this.$message.success('采购人员登录成功')
      //   this.$router.push('/buyerhome')
      // }
      //
      // // this.$refs.loginFormRef.validate(async valid => {
      // //   if (!valid) return
      // //   const { data: res } = await this.$http.post('login', this.loginForm)
      // //   // console.log(res)
      // //   if (res.meta.status !== 200) {
      // //     return this.$message.error('登录失败！')
      // //   }
      // //   this.$message.success('登录成功！')
      // //   // 1、将登陆成功之后的 token 保存到客户端的 sessionStorage 中
      // //   //  1.1、 项目中除了登陆之外的其他API接口，必须在登陆之后才能访问
      // //   //  1.2、 token 只应在当前网站打开期间生效，所以将 token保存在sessionStorage 中
      // //   console.log(res)
      // //   window.sessionStorage.setItem('token', res.data.token)
      // //   // 2、 通过编程式导航跳转到后台主页，路由地址是 /home
      // //   this.$router.push('/home')
      // // // })
    },
    register(){

      this.$refs['register'].validate((valid) => {
        if (valid) {
          console.log('注册')

          let params = {
            "name": this.query.username,
            "password": this.query.password,
            "avatar_description": this.query.avatarDescription,
            "avatar_url": this.query.avatar_url
          }

          register(params).then(res => {
            console.log(res)
            if (res.status === 200){
              this.$message.success("注册成功！")
            }
          })

          this.dialogFormVisible = false
        }
      })

      // const {data: res} = await this.$http.get('/orderbook/user/registerUser',{params: this.query})
      //
      // this.receive=res.data
      // console.log(this.receive)
      // if (res.code !== 200){
      //   return this.$message.error(res.msg)
      // }
      // else {
      //   this.dialogFormVisible=false
      //   return this.$message.success(res.msg)
      // }


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
      this.query.avatar_url = url
      this.query.avatarDescription = avatarDescription
      console.log(url)
    }
  }
}
</script>

<!--需手动安装less和lessloader :npm install less@3.9.0
                              npm insatll less-loader@4.1.0
                              ui界面安装版本过高会报错-->
<style lang="less" scoped>
.login_container{
  background-color: #F7F7F7;
  position: absolute;
  height: 100%;
  width: 100%;
}
.login_box{
  width: 450px;
  height: 300px;
  background-color: #fff;
  border-radius: 3px;
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%,-50%);

  .avatar_box{
    height: 80px;
    width: 80px;
    border: 1px solid #eee;
    border-radius: 50%;
    padding: 10px;
    box-shadow: 0 0 10px #eee;
    position: absolute;
    left: 50%;
    transform: translate(-50%,-50%);
    background-color: #fff;
    img{
      width: 100%;
      height: 100%;
      border-radius: 50%;
      background-color: #eee;
    }
  }
}
.btns{
  display: flex;
  //justify-content: flex-end; // 右对齐
  justify-content: center; // 居中
}
.login_form{
  position: absolute;
  bottom: 0;
  width: 100%;
  padding: 0 20px;
  box-sizing: border-box;
}
.select{
  //margin-right: 38px;

  width: 50%;
  margin-left: 20px;
  margin-right: 20px;
  float: left;

}
.title {
  font-size: 50px;
  Font-Family: "华文彩云";
  font-weight:bold;
  text-align:center;
  color: #000000;
  display : inline
}
</style>
