<template>
  <div style="height: 100%; background-color: #f6f7f9">
    <el-card style="height: 100%; min-height: 100%">
      <el-container style="height: 100%; max-height: 100vh">
        <el-header class="block" style="white-space: pre-wrap">
          <el-row style="width: 100%;display: flex;align-items: center">
            <div style="justify-content: left">
              <span style="color: black; font-size: large;text-align: center;white-space: pre-wrap">{{this.role.name}}</span>
            </div>
            <div style="margin-left: auto">
                <el-dropdown trigger="hover" @command="handleCommand">
                    <el-button type="primary">
                        更多<el-icon class="el-icon--right"><arrow-down /></el-icon>
                    </el-button>
                    <template #dropdown>
                        <el-dropdown-menu>
                            <el-dropdown-item command="a">删除智能体</el-dropdown-item>
                            <el-dropdown-item command="b">修改智能体</el-dropdown-item>
                            <el-dropdown-item command="c">新建对话</el-dropdown-item>
                        </el-dropdown-menu>
                    </template>
                </el-dropdown>
            </div>
          </el-row>
          <el-dialog
            title="提示"
            v-model="delDialogVisible"
            width="30%"
            :before-close="handleClose">
            <span>是否确定删除此智能体！(该操作无法恢复)</span>
              <template #footer>
                  <span slot="footer" class="dialog-footer">
                      <el-button @click="delDialogVisible = false">取 消</el-button>
                      <el-button type="primary" @click="delDialogVisible = false;delete_character()">确 定</el-button>
                  </span>
              </template>

          </el-dialog>
          <el-dialog
            title="提示"
            v-model="editDialogVisible"
            width="30%"
            :before-close="handleClose">
            <el-form :model="editForm" label-position="top" style="max-width: 400px; margin: 0 auto; ">
              <el-form-item label="智能体分类" :prop="'selectedCategory'" required>
                <el-select v-model="editForm.selectedCategory" placeholder="请选择智能体分类" style="border: 2px solid whitesmoke;background-color: white; ">
                  <el-option label="美食" value="food"></el-option>
                  <el-option label="旅游" value="travel"></el-option>
                  <el-option label="科技" value="technology"></el-option>
                  <el-option label="健康" value="health"></el-option>
                  <el-option label="法律" value="law"></el-option>
                  <el-option label="其他" value="other"></el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="智能体名称" :prop="'bot_name'" required>
                <el-input v-model="editForm.bot_name" class="character_name_input" style="border: 2px solid whitesmoke;background-color: white"></el-input>
              </el-form-item>
              <el-form-item label="智能体描述">
                <el-input v-model="editForm.description" :rows="4" type="textarea"
                          :autosize="{ minRows: 6, maxRows: 8 }"
                          placeholder="请输入智能体的描述"></el-input>
              </el-form-item>
              <el-form-item label="头像" >
                <GenerateAvatar :avatarUrl="editForm.avatarUrl" :description="editForm.avatar_description" @returnUrl="getAvatarUrl"></GenerateAvatar>
              </el-form-item>
            </el-form>
              <template #footer>
                  <span  class="dialog-footer">
                      <el-button @click="editDialogVisible = false">取 消</el-button>
                      <el-button type="primary" @click="update_user">确 定</el-button>
                  </span>
              </template>

          </el-dialog>
          <!-- 头像生成对话框 -->
          <GenerateAvatarDialog v-if="generateAvatarDialogVisible" @closeDialog="closeGenerateAvatarDialog" :DialogShowFlag="generateAvatarDialogVisible" :avatarUrl="editForm.avatarUrl"></GenerateAvatarDialog>
        </el-header>
        <el-main style="height: 100%; width: 100%;">
          <div >
            <div v-if="history_message.length === 0" style="display: flex;flex-direction: column;justify-content: center;align-items: center">
              <span style="color: white">快开始与智能体进行对话吧！</span>
            </div>
            <div v-for="(item, index) in history_message" class="msgCss" :style="{textAlign: item.align}">
              <el-row style="padding-top: 20px">
                <div v-if="item.owner === 'bot'" class="block">
                  <div style="width: 50px;height: 50px;flex-shrink: 0">
                    <el-avatar @click.native="openEdit" :size="50" :src="item.avatar_url" style="width: 50px"></el-avatar>
                  </div>
                  <div v-if="item.content !== ''" style="background-color: gray;padding-top: 10px;padding-bottom: 10px;" class="content">
                    <span :style="{ whiteSpace: 'pre-wrap' }">{{item.content}}</span>
                  </div>
<!--                  <span v-if="item.content !== ''" style="background-color: gray;padding-top: 10px;padding-bottom: 10px;" class="content">{{item.content}}</span>-->
                  <div v-if="item.img_url !== ''">
                    <el-image
                      style="width: 500px; height: 400px; padding-left: 20px"
                      fit="fill"
                      :src="item.img_url"
                      :preview-src-list="[item.img_url]">
                    </el-image>
                  </div>
                  <div style="width: 80px;height: 80px; flex-shrink: 0">
<!--                    <el-avatar :size="60"></el-avatar>-->
                  </div>
                </div>
                <div v-if="item.owner === 'user'" class="block" style="float: right; padding-right: 20px;">
                  <div style="width: 80px;height: 80px;flex-shrink: 0;">
<!--                    <el-avatar :size="50" style="width: 50px"></el-avatar>-->
                  </div>
                  <span style="background-color: deepskyblue;padding-top: 10px;padding-bottom: 10px;position:absolute; right: 50px" class="content">{{item.content}}</span>
                  <div style="width: 50px;height: 50px; flex-shrink: 0;position:absolute;right:0px;">
                    <el-avatar :size="60" :src="item.avatar_url"></el-avatar>
                  </div>
                  <!--                <el-avatar @click.native="editDialogVisible = true" :size="50" :src="item.avatar_url" style="width: 50px"></el-avatar>-->
                </div>
              </el-row>

            </div>
          </div>

        </el-main>
        <el-footer>
          <el-input
            v-model="input_message"
            placeholder="请输入"
            @keyup.enter.native="sendMessage"
            style="margin-bottom: 20px"
            clearable>
              <template #append>
<!--                  <el-button :icon="Promotion" @click="sendMessage"></el-button>-->
                  <el-icon @click="sendMessage"><Promotion /></el-icon>
              </template>

          </el-input>
        </el-footer>
      </el-container>
    </el-card>
  </div>
</template>

<script>
import GenerateAvatarDialog from '../components/dialog/GenerateAvatarDialog';
import GenerateAvatar from '../components/GenerateAvatar';
import Character from '../components/dialog/Character';
import { simulateAvatar, simulateCreateCharacter } from '../api/createrole';
import { character_delete, character_update, character_select } from '../api/character';
import { connectionWebSocket, connectionWebSocketWithoutChatId, send } from '../plugins/websocket-client';
import { chat_select } from '@/api/chat';
export default {
  name: 'Dialogue',
  components: { Character, GenerateAvatarDialog, GenerateAvatar },
  props: ['value'],
  data() {
    return{
      wbClient: null,
      input_message: '',
      history_message: [
        // {
        //     img_url: '',
        //   content: '我是你的专属AI角色，请跟我聊天吧！',
        //   owner: 'bot',
        //   avatar_url: 'https://lingyou-1302942961.cos.ap-beijing.myqcloud.com/lingyou/16790385261248df6fb83-63b0-4497-826e-b5f2cfbe97a3.jpg',
        // },{
        //   content: '你好，很高兴认识你，你能告诉我中国有哪些有名的小吃吗？',
        //   owner: 'user',
        //   avatar_url: '',
        // },{
        //   img_url: '',
        //   content: '中国的小吃有很多，例如胡辣汤、油条、粽子等。',
        //   owner: 'bot',
        //   avatar_url: 'https://lingyou-1302942961.cos.ap-beijing.myqcloud.com/lingyou/16790385261248df6fb83-63b0-4497-826e-b5f2cfbe97a3.jpg',
        // },
      ],
      role: {
        id: 5,
        img_url: 'https://aitopia-1302942961.cos.ap-beijing.myqcloud.com/lingyou/1688809087917a4bed63a-5757-48d5-b6a9-1b6d4c81be00.png?imageView2/1/w/300/h/300',
        label: 'test5',
        description: 'test5'
      },
      editForm: {
        bot_name: '',
        description: '',
        // user_name: '',
        // user_info: ''
        selectedCategory: '',
        avatarUrl: '',// 生成的头像 URL
      },
      avatarDescription: '',
      delDialogVisible: false,
      editDialogVisible: false,
      generateAvatarDialogVisible: false,
      chat_id: -1,
      cur_message: ''
    }
  },
  created() {
    // this.role = localStorage.getItem('roleMess')

    if (localStorage.getItem("roleMess_id") === null){
      console.log("zzzz")
      this.$message.warning('请先到主页选择一个角色！')
      this.$router.push('/mainpage')
    }
    this.role.category = localStorage.getItem('roleCategory')
    this.role.name = localStorage.getItem('roleMess_name')
    this.role.img_url = localStorage.getItem('roleMess_avatar_url')
    this.role.id = localStorage.getItem('roleMess_id')
    let params = {
      "cid": this.role.id
    }
    character_select(params).then(res => {
      if (res.status === 200){
        if (res.data.characters.length === 0){
          this.$message.error("该角色不存在！")
          this.$router.push('/mainpage')
        }
      }
    })
    this.role.description = localStorage.getItem('roleMess_description')
    this.role.avatar_description = localStorage.getItem('roleMess_avatar_description')
    window.sessionStorage.setItem('activePath', '/dialogue')
    this.$emit('updateParentValue', '/dialogue')
  },
  computed: {
    bot_infoLength() {
      return this.editForm.description.length
    },
  },
  mounted() {
    this.getChat()


  },
  methods: {
    getChat(){
      let params = {
        cid: this.role.id
      }
      chat_select(params).then(res => {
        // console.log(res)
        if (res.status === 200){
          if (res.data.length === 0){
            let token = localStorage.getItem('token')
            let cid = localStorage.getItem('roleMess_id')
            token = token.split(' ')[1]
            this.wbClient = connectionWebSocketWithoutChatId(token, cid, this.handle_message)
            return
          }
          let d = res.data[res.data.length-1]
          // console.log(res.data[res.data.length-1])
          this.chat_id = d.chat_id
          for (var i = 0;i < d.history.length;i++){
            let c = d.history[i]
            let h = {
              content: c.content,
              owner: '',
              avatar_url: '',
              img_url: ''
            }
            if (c.sender === 'user'){
              h.owner = 'user'
              h.avatar_url = localStorage.getItem('avatarUrl')
            }
            else {
              h.owner = 'bot'
              h.avatar_url = this.role.img_url
            }
            this.history_message.push(h)
          }

          let token = localStorage.getItem('token')
          let cid = localStorage.getItem('roleMess_id')
          token = token.split(' ')[1]
          this.wbClient = connectionWebSocket(token, cid, this.chat_id, this.handle_message)
        }
      })
    },
    handle_message(msg) {
      console.log("接受到消息")
      console.log(msg)
      const data = JSON.parse(msg.data)
      console.log(data)
      this.cur_message += data.content
      if (data.is_end_of_stream === true){
          var l = this.history_message.length
          this.history_message.splice(l - 1, 1)
        this.history_message.push({
          content: this.cur_message,
          owner: 'bot',
          avatar_url: this.role.img_url,
          img_url: ''
        })
        this.cur_message = ''
        for (var i=0;i<data.images.length;i++){
          this.history_message.push(({
            content: '',
            owner: 'bot',
            avatar_url: this.role.img_url,
            img_url: data.images[i]
          }))
          // console.log(data.images[i])
        }

      }

    },
    sendMessage() {
      if (this.input_message === '' || this.input_message === null){
        this.$message.error('发送信息不能为空')
        return
      }
      let mess = this.input_message
      send(this.wbClient, mess, this.role.id)

      this.history_message.push({
        content: mess,
        owner: 'user',
        avatar_url: localStorage.getItem('avatarUrl'),
        // avatar_url: 'https://lingyou-1302942961.cos.ap-beijing.myqcloud.com/lingyou/16790385261248df6fb83-63b0-4497-826e-b5f2cfbe97a3.jpg',
      })
        this.history_message.push({
            content: "请等待片刻",
            owner: 'bot',
            avatar_url: this.role.img_url,
            img_url: ''
            // avatar_url: 'https://lingyou-1302942961.cos.ap-beijing.myqcloud.com/lingyou/16790385261248df6fb83-63b0-4497-826e-b5f2cfbe97a3.jpg',
        })

      this.input_message = ''


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
    },
    handleClose(done) {
      this.$confirm('确认关闭？')
        .then(_ => {
          done();
        })
        .catch(_ => {});
    },
    openEdit(){
      this.editDialogVisible = true
      this.editForm.selectedCategory = this.role.category
      this.editForm.bot_name = this.role.name
      this.editForm.avatarUrl = this.role.img_url
      this.editForm.id = this.role.id
      this.editForm.description = this.role.description
      this.editForm.avatar_description = this.role.avatar_description
    },
    handleCommand(command) {
        console.log(command)
      if (command === 'a'){
        this.delDialogVisible = true
      }
      else if (command === 'b'){
        this.openEdit()
      }
      else if (command === 'c'){
        this.$confirm('新建对话当前对话内容将会被清空。是否新建对话？').then(_ => {
          console.log("新建")
          this.wbClient.close()
          let token = localStorage.getItem('token')
          let cid = localStorage.getItem('roleMess_id')
          token = token.split(' ')[1]
          this.wbClient = connectionWebSocketWithoutChatId(token, cid, this.handle_message)
          this.history_message = []
          this.getChat()
        }).catch(_ => {})
      }
    },
    generateAvatar() {
      const response2 = simulateAvatar(this.avatarDescription);
      this.editForm.avatarUrl = response2.data.AvatarUrl;
      console.log('头像生成：', response2);
      // 假设后端接口返回头像 URL
      setTimeout(() => {
        this.editForm.avatarUrl
      }, 1000);
    },
    saveAvatar() {
      // 保存头像到本地的逻辑，这里使用假数据
      console.log('头像已保存');
      // 关闭对话框
      this.generateAvatarDialogVisible = false;
    },
    // handleCreate() {
    //   // 处理创建角色的逻辑，可以发送请求给后端进行处理
    //   // 调用模拟接口函数，并传入角色信息
    //   const response1 = simulateCreateCharacter(this.createForm);
    //   this.createdCharacterId = response1.data.characterId; // 保存角色 ID
    //   // 输出模拟的响应数据到控制台，可以根据需要进行后续处理
    //   console.log('创建角色信息：', response1);
    //
    //   if (response1.success) {
    //     // this.$message.success('创建角色成功');
    //     // 弹出提示框
    //     this.showSuccessMessageBox();
    //   }
    // },
    showSuccessMessageBox() {
      this.$confirm(`角色创建成功，您的角色 ID 是 ${this.createdCharacterId}，可以选择与创建角色对话或回到首页查看角色`, '创建成功', {
        confirmButtonText: '与创建角色对话',
        cancelButtonText: '回到首页查看角色',
        type: 'success'
      }).then(() => {
        // 点击与创建角色对话按钮的逻辑
        console.log('与创建角色对话');
        // 跳转到与创建角色对话的页面
        this.$router.push('/dialogue');
      }).catch(() => {
        // 点击回到首页查看角色按钮的逻辑
        console.log('回到首页查看角色');
        // 跳转到首页的页面
        this.$router.push('/mainpage');
      }).finally(() => {
        // 清空表单数据
        this.createForm = {
          bot_name: '',
          bot_info: '',
          user_name: '',
          user_info: ''
        };
      });
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
    delete_character(){
      let params = [
        parseInt(localStorage.getItem("roleMess_id"))
      ]
      console.log("zzz")
      console.log(params)
      character_delete(params).then(res => {
        console.log(res)
        console.log("删除！")
        this.$message.success("删除角色成功！")
        localStorage.removeItem("roleMess_id")
        localStorage.removeItem("roleMess_name")
        localStorage.removeItem("roleMess_avatar_url")
        localStorage.removeItem("roleCategory")
        localStorage.removeItem("roleMess_description")
        localStorage.removeItem("roleMess_avatar_description")
        window.sessionStorage.setItem('activePath', '/mainpage')
        this.$router.push('/mainpage')
      })
    },
    getAvatarUrl(url, avatarDescription){
      this.editForm.avatarUrl = url
      this.editForm.avatar_description = avatarDescription
      console.log(url)
    },
    update_user(){
      let params = {
        "name": this.editForm.bot_name,
        "description": this.editForm.description,
        "category": this.editForm.selectedCategory,
        "avatar_description": this.editForm.avatar_description,
        "avatar_url": this.editForm.avatarUrl
      }
      character_update(params, this.editForm.id).then(res => {
        if (res.status === 200){
          console.log(res)
          this.$message.success("修改成功")
        }
        this.editDialogVisible = false
      })
    },
    getChatHistory() {
      let params = {
        chat_id: '',
        cid: ''
      }
    }
  }
};
</script>

<style scoped>
.el-header {
  /*background-color: #242949;*/
  background-color: #f6f7f9;
  height: 5%;
  border-radius: 10px;
}
.el-main {
  height: 60%;
  /*background-color: #212529;*/
  background-color: #f6f7f9;
  border-radius: 10px;
}
.el-footer {
  height: 10%;
  padding-bottom: 20px;
  /*background-color: #212529;*/
  background-color: #f6f7f9;
  display: flex;
  justify-content: center; /* 水平居中 */
  align-items: center;     /* 垂直居中 */
  border-radius: 10px;
}
.el-card {
  /*background-color: #212529;*/
  background-color: #f6f7f9;
  border: 0;
}
/*搜索组件最外层div */
.el-input {
  /*background-color: #242949;*/
  background-color: white;
  width: 100%;
  height: 100%;
  margin-right: 15px;
  border-radius: 10px;
  display: flex;
  justify-content: center; /* 水平居中 */
  align-items: center;     /* 垂直居中 */
  color: white;
}

:deep(.el-input__wrapper) {
    height: 90%;
    background-color: transparent;
    border: 0;
    box-shadow: 0 0 0 0px;
}

/*搜索input框*/
:deep(.el-input__inner) {
  background-color: transparent;
  border-radius: 95px;
  /*-moz-border-radius-topright: 95px;*/
  border: 0;
  box-shadow: 0 0 0 0px;
  /*color: #808080;*/
  color: #cccccc
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
    width: 100%;
  display: flex;
  align-items: flex-start;     /* center 垂直居中 flex-start 在开头  */
}
.content {
  color: white;
  padding-left: 20px;
  padding-right: 20px;
  border-radius: 35px;
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
