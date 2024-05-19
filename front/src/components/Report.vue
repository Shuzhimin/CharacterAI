<template>
  <div style="height: 100%; background-color: #242949">
    <el-card style="height: 100%; min-height: 100%">
      <el-container style="height: 100%">
        <el-header class="block" style="white-space: pre-wrap">
          <el-row style="width: 100%;display: flex;align-items: center">
            <div style="justify-content: left">
              <span style="color: white; font-size: large;text-align: center;white-space: pre-wrap">{{this.role.label}}</span>
            </div>
          </el-row>
        </el-header>
        <el-main>
          <div v-for="(item, index) in history_message" class="msgCss" :style="{textAlign: item.align}">
            <el-row style="padding-top: 20px">
              <div v-if="item.owner === 'bot'" class="block">
                <el-avatar :size="50" :src="role.img_url"></el-avatar>
                <span v-if="item.content !== ''" class="content">{{item.content}}</span><br/>
                <div v-if="item.img_url !== ''">
                  <el-image
                    style="width: 300px; height: 300px; padding-left: 20px"
                    :src="item.img_url"
                    :preview-src-list="[item.img_url]">
                  </el-image>
                </div>
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
import { report } from '@/api/report';
export default {
  name: 'Report',
  props: ['value'],
  data() {
    return{
      input_message: '',
      history_message: [
        {
          content: '我是你的专属智能报表助手，请告诉我指令把！',
          owner: 'bot',
          avata_url: 'https://lingyou-1302942961.cos.ap-beijing.myqcloud.com/lingyou/16790385261248df6fb83-63b0-4497-826e-b5f2cfbe97a3.jpg',
          img_url: ''
        },{
          content: '你好，请问我都能向你发送什么指令呢？',
          owner: 'user',
          avatar_url: '',
        },{
          content: '你可以让我生成饼状图、柱状图等。',
          owner: 'bot',
          avatar_url: 'https://lingyou-1302942961.cos.ap-beijing.myqcloud.com/lingyou/16790385261248df6fb83-63b0-4497-826e-b5f2cfbe97a3.jpg',
          img_url: ''
        },
      ],
      role: {
        id: 5,
        img_url: 'https://lingyou-1302942961.cos.ap-beijing.myqcloud.com/lingyou/16669279303510c7db712-aef9-41aa-aa22-f6dd6dcb721b.jpg?imageView2/1/w/300/h/300',
        label: '智能报表助手',
        description: '智能报表助手'
      },
      dialogVisible: false
    }
  },
  created() {
    // this.role = localStorage.getItem('roleMess')
    // this.role.label = localStorage.getItem('roleMess_label')
    // this.role.img_url = localStorage.getItem('roleMess_img_url')
    // this.role.id = localStorage.getItem('roleMess_id')
    // this.role.description = localStorage.getItem('roleMess_description')
    window.sessionStorage.setItem('activePath', '/report')
    this.$emit('updateParentValue', '/report')
  },
  methods: {
    sendMessage() {
      // if (this.input_message === '' || this.input_message === null){
      //   this.$message.error('发送信息不能为空')
      //   return
      // }
      // let mess = {
      //   content: this.input_message,
      //   owner: 'user',
      //   avatar_url: '',
      // }
      // this.history_message.push(mess)
      // this.input_message = ''
      // setTimeout(()=>{
      //   let response = {
      //     content: '这是一条自动应答',
      //     owner: 'bot',
      //     avatar_url: 'https://lingyou-1302942961.cos.ap-beijing.myqcloud.com/lingyou/16790385261248df6fb83-63b0-4497-826e-b5f2cfbe97a3.jpg',
      //   }
      //   this.history_message.push(response)
      // }, 1000)
      let params = {
        "content": this.input_message
      }
      this.history_message.push({
        "content": this.input_message,
        "owner": 'user',
        "avatar_url": '',
      })
      this.input_message = ''

      report(params).then(res => {
        if (res.status === 200){
          console.log(res)

          let message1 = {
            "content": res.data.content,
            "owner": 'bot',
            "avatar_url": 'https://lingyou-1302942961.cos.ap-beijing.myqcloud.com/lingyou/16790385261248df6fb83-63b0-4497-826e-b5f2cfbe97a3.jpg',
            "img_url": '',
          }

          let message2 = {
            "content": '',
            "owner": 'bot',
            "avatar_url": 'https://lingyou-1302942961.cos.ap-beijing.myqcloud.com/lingyou/16790385261248df6fb83-63b0-4497-826e-b5f2cfbe97a3.jpg',
            "img_url": res.data.url,
          }
          this.history_message.push(message1)
          this.history_message.push(message2)
        }
      })

    },
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
