<template>
  <div style="height: 100%; background-color: #242949">
    <el-card style="height: 100%; min-height: 100%">
      <el-container style="height: 100%">
        <el-header class="block" style="white-space: pre-wrap">
          <el-row style="width: 100%;display: flex;align-items: center">
            <div style="justify-content: left">
              <span style="color: white; font-size: large;text-align: center;white-space: pre-wrap">{{this.role.label}}</span>
            </div>
            <div style="margin-left: auto">
              <el-dropdown trigger="hover" split-button type="primary" @command="handleCommand">
                更多
                <el-dropdown-menu slot="dropdown">
                  <el-dropdown-item command="a">删除角色</el-dropdown-item>
                  <el-dropdown-item command="b">修改角色</el-dropdown-item>
                </el-dropdown-menu>
              </el-dropdown>
            </div>
          </el-row>
          <el-dialog
            title="提示"
            :visible.sync="dialogVisible"
            width="30%"
            :before-close="handleClose">
            <span>是否确定删除此角色！(该操作无法恢复)</span>
            <span slot="footer" class="dialog-footer">
              <el-button @click="dialogVisible = false">取 消</el-button>
              <el-button type="primary" @click="dialogVisible = false">确 定</el-button>
            </span>
          </el-dialog>
        </el-header>
        <el-main>
          <div v-for="(item, index) in history_message" class="msgCss" :style="{textAlign: item.align}">
            <el-row style="padding-top: 20px">
              <div v-if="item.owner === 'bot'" class="block">
                <el-avatar :size="50" :src="item.avatar_url"></el-avatar>
                <span class="content">{{item.content}}</span>
              </div>
              <div v-if="item.owner === 'user'" class="block" style="float: right">
                <span class="content">{{item.content}}</span>
                <el-avatar :size="50" :src="item.avatar_url"></el-avatar>
              </div>
            </el-row>

          </div>
        </el-main>
        <el-footer>
          <el-input
            v-model="input_message"
            style=""
            placeholder="请输入"
            @keyup.enter.native="sendMessage"
            clearable>
            <el-button slot="append" icon="el-icon-s-promotion button-icon" @click="sendMessage"></el-button>
          </el-input>
        </el-footer>
      </el-container>
    </el-card>
  </div>
</template>

<script>
import { testAPI } from '@/api/test';
export default {
  name: 'Dialogue',
  props: ['value'],
  data() {
    return{
      input_message: '',
      history_message: [
        {
          content: '我是你的专属AI角色，请跟我聊天吧！',
          owner: 'bot',
          avatar_url: 'https://lingyou-1302942961.cos.ap-beijing.myqcloud.com/lingyou/16790385261248df6fb83-63b0-4497-826e-b5f2cfbe97a3.jpg',
        },{
          content: '你好，很高兴认识你，你能告诉我中国有哪些有名的小吃吗？',
          owner: 'user',
          avatar_url: '',
        },{
          content: '中国的小吃有很多，例如胡辣汤、油条、粽子等。',
          owner: 'bot',
          avatar_url: 'https://lingyou-1302942961.cos.ap-beijing.myqcloud.com/lingyou/16790385261248df6fb83-63b0-4497-826e-b5f2cfbe97a3.jpg',
        },
      ],
      role: {
        id: 5,
        img_url: 'https://aitopia-1302942961.cos.ap-beijing.myqcloud.com/lingyou/1688809087917a4bed63a-5757-48d5-b6a9-1b6d4c81be00.png?imageView2/1/w/300/h/300',
        label: 'test5',
        description: 'test5'
      },
      dialogVisible: false
    }
  },
  created() {
    // this.role = localStorage.getItem('roleMess')
    this.role.label = localStorage.getItem('roleMess_label')
    this.role.img_url = localStorage.getItem('roleMess_img_url')
    this.role.id = localStorage.getItem('roleMess_id')
    this.role.description = localStorage.getItem('roleMess_description')
    window.sessionStorage.setItem('activePath', '/dialogue')
    this.$emit('updateParentValue', '/dialogue')
  },
  methods: {
    sendMessage() {
      if (this.input_message === '' || this.input_message === null){
        this.$message.error('发送信息不能为空')
        return
      }
      let mess = {
        content: this.input_message,
        owner: 'user',
        avatar_url: '',
      }
      this.history_message.push(mess)
      this.input_message = ''
      setTimeout(()=>{
        let response = {
          content: '这是一条自动应答',
          owner: 'bot',
          avatar_url: 'https://lingyou-1302942961.cos.ap-beijing.myqcloud.com/lingyou/16790385261248df6fb83-63b0-4497-826e-b5f2cfbe97a3.jpg',
        }
        this.history_message.push(response)
      }, 1000)
    },
    handleClose(done) {
      this.$confirm('确认关闭？')
        .then(_ => {
          done();
        })
        .catch(_ => {});
    },
    handleCommand(command) {
      if (command === 'a'){
        this.dialogVisible = true
      }
      else if (command === 'b'){
        let params = {
          id: '1',
          data: '测试数据'
        }
        testAPI(params).then(res => {
          console.log(res)
        })
      }
    }
  }
};
</script>

<style scoped>
.el-header {
  background-color: #242949;
  height: 10%;
  border-radius: 10px;
}
.el-main {
  height: 70%;
  background-color: #212529;
  border-radius: 10px;
}
.el-footer {
  height: 20%;
  padding-bottom: 20px;
  background-color: #212529;
  display: flex;
  justify-content: center; /* 水平居中 */
  align-items: center;     /* 垂直居中 */
  border-radius: 95px;
}
.el-card {
  background-color: #212529;
  border: 0;
}
/*搜索组件最外层div */
.el-input {
  background-color: #242949;
  width: 100%;
  height: 100%;
  margin-right: 15px;
  border-radius: 95px;
  display: flex;
  justify-content: center; /* 水平居中 */
  align-items: center;     /* 垂直居中 */
  color: white;
}
/*搜索input框 */
:deep(.el-input__inner) {
  background-color: transparent;
  border-radius: 95px;
  /*-moz-border-radius-topright: 95px;*/
  border: 0;
  box-shadow: 0 0 0 0px;
  color: white;
}
/*搜索button按钮 */
:deep(.el-input-group__append) {
  width: 60px;
  background-color: transparent;
  border-radius: 95px;
  border: 0;
  box-shadow: 0 0 0 0px;
  font-size: 50px;
  float: right;
}
.msgCss {
  font-size: 16px;
  font-weight: 500;
}
.block {
  display: flex;
  align-items: center;     /* 垂直居中 */
}
.content {
  color: white;
  padding-left: 20px;
  padding-right: 20px;
}
:deep(.el-card__body) {
  height: 100%;
}
 .el-dropdown-link {
   cursor: pointer;
   color: #409EFF;
 }
.el-icon-arrow-down {
  font-size: 12px;
}
</style>
