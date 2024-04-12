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
            :visible.sync="delDialogVisible"
            width="30%"
            :before-close="handleClose">
            <span>是否确定删除此角色！(该操作无法恢复)</span>
            <span slot="footer" class="dialog-footer">
              <el-button @click="delDialogVisible = false">取 消</el-button>
              <el-button type="primary" @click="delDialogVisible = false">确 定</el-button>
            </span>
          </el-dialog>
          <el-dialog
            title="提示"
            :visible.sync="editDialogVisible"
            width="30%"
            :before-close="handleClose">
            <el-form :model="editForm" label-position="top" style="max-width: 400px; margin: 0 auto; ">
              <el-form-item label="角色分类" :prop="'selectedCategory'" required>
                <el-select v-model="editForm.selectedCategory" placeholder="请选择角色分类">
                  <el-option label="美食" value="food"></el-option>
                  <el-option label="旅游" value="travel"></el-option>
                  <el-option label="科技" value="technology"></el-option>
                  <el-option label="健康" value="health"></el-option>
                  <el-option label="法律" value="law"></el-option>
                  <el-option label="其他" value="other"></el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="创建角色名称" :prop="'bot_name'" required>
                <el-input v-model="editForm.bot_name" style="background-color: #cccccc"></el-input>
              </el-form-item>
              <el-form-item label="创建角色的身份背景" :prop="'bot_info'" required>
                <el-input v-model="editForm.bot_info" :rows="4" type="textarea"
                          :autosize="{ minRows: 6, maxRows: 8 }"
                          placeholder="请输入身份背景"></el-input>
                <span style="position: absolute; bottom: 10px; right: 10px; color: #999;">{{ bot_infoLength }}/100</span>
              </el-form-item>
<!--              <el-form-item label="人物角色头像生成" class="a">-->
<!--                <el-button @click="showGenerateAvatarDialog">AI生成角色头像</el-button>-->
<!--              </el-form-item>-->
              <el-form-item label="头像" >
                <GenerateAvatar :avatarUrl="editForm.avatarUrl"></GenerateAvatar>
              </el-form-item>
              <!--          <el-form-item label="对话人物名称" :prop="'user_name'" required>-->
              <!--            <el-input v-model="createForm.user_name" class="a"></el-input>-->
              <!--          </el-form-item>-->
              <!--          <el-form-item label="对话人物身份背景" :prop="'user_info'" required>-->
              <!--            <el-input v-model="createForm.user_info" class="user_info_input" :rows="4" type="textarea"-->
              <!--                      :autosize="{ minRows: 6, maxRows: 8 }"-->
              <!--                      placeholder="请输入身份背景"></el-input>-->
              <!--            <span style="position: absolute; bottom: 10px; right: 10px; color: #999;">{{ user_infoLength }}/100</span>-->
              <!--          </el-form-item>-->
              <!--          <el-form-item label="对话人物头像生成" class="a">-->
              <!--            <el-button @click="generateDialogueAvatar">一键生成对话人物头像</el-button>-->
              <!--            <el-image v-if="dialogueAvatarUrl" :src="dialogueAvatarUrl"-->
              <!--                      style="max-width: 100px; max-height: 100px; margin-top: 10px;"></el-image>-->
              <!--          </el-form-item>-->
              <el-form-item>
                <el-button type="primary" @click="handleCreate">立即创建</el-button>
              </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
              <el-button @click="editDialogVisible = false">取 消</el-button>
              <el-button type="primary" @click="editDialogVisible = false">确 定</el-button>
            </span>
          </el-dialog>
          <!-- 头像生成对话框 -->
          <GenerateAvatarDialog v-if="generateAvatarDialogVisible" @closeDialog="closeGenerateAvatarDialog" :DialogShowFlag="generateAvatarDialogVisible" :avatarUrl="editForm.avatarUrl"></GenerateAvatarDialog>
<!--          <el-dialog-->
<!--            title="AI生成头像"-->
<!--            :visible.sync="generateAvatarDialogVisible"-->
<!--            width="50%"-->
<!--            :close-on-click-modal="false"-->
<!--          >-->
<!--            <div class="avatar-dialog-content">-->
<!--              <el-input v-model="avatarDescription" :rows="4" type="textarea"-->
<!--                        :autosize="{ minRows: 6, maxRows: 8 }"-->
<!--                        placeholder="请输入头像的描述"></el-input>-->
<!--              <span style="position: absolute; bottom: 10px; right: 10px; color: #999;">{{ avatarDescriptionLength }}/100</span>-->

<!--              <el-button @click="generateAvatar" class="generate-avatar-button">生成头像</el-button>-->
<!--              <el-image v-if="editForm.avatarUrl" :src="editForm.avatarUrl"-->
<!--                        style="max-width: 150px; max-height: 150px;"></el-image>-->

<!--              <el-button @click="saveAvatar" type="primary" class="enter-button">确定</el-button>-->
<!--            </div>-->
<!--          </el-dialog>-->
        </el-header>
        <el-main>
          <div v-for="(item, index) in history_message" class="msgCss" :style="{textAlign: item.align}">
            <el-row style="padding-top: 20px">
              <div v-if="item.owner === 'bot'" class="block">
                <el-avatar @click.native="editDialogVisible = true" :size="50" :src="item.avatar_url"></el-avatar>
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
import GenerateAvatarDialog from '@/components/dialog/GenerateAvatarDialog';
import GenerateAvatar from '@/components/GenerateAvatar';
import Character from '@/components/dialog/Character';
import { simulateAvatar, simulateCreateCharacter } from '@/api/createrole';
export default {
  name: 'Dialogue',
  components: { Character, GenerateAvatarDialog, GenerateAvatar },
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
      editForm: {
        bot_name: '',
        bot_info: '',
        // user_name: '',
        // user_info: ''
        selectedCategory: '',
        avatarUrl: '',// 生成的头像 URL
      },
      avatarDescription: '',
      delDialogVisible: false,
      editDialogVisible: false,
      generateAvatarDialogVisible: false,
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
  computed: {
    bot_infoLength() {
      return this.editForm.bot_info
    },
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
        this.delDialogVisible = true
      }
      else if (command === 'b'){
        this.editDialogVisible = true
        let params = {
          id: '1',
          data: '测试数据'
        }
        console.log(params)
        // testAPI(params).then(res => {
        //   console.log(res)
        // })
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
    handleCreate() {
      // 处理创建角色的逻辑，可以发送请求给后端进行处理
      // 调用模拟接口函数，并传入角色信息
      const response1 = simulateCreateCharacter(this.createForm);
      this.createdCharacterId = response1.data.characterId; // 保存角色 ID
      // 输出模拟的响应数据到控制台，可以根据需要进行后续处理
      console.log('创建角色信息：', response1);

      if (response1.success) {
        // this.$message.success('创建角色成功');
        // 弹出提示框
        this.showSuccessMessageBox();
      }
    },
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
