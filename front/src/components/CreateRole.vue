<template>
  <div>
    <div class="content">
<!--       页面内ds[xiygai-->
      <div>
        <el-form :model="createForm" label-position="top" style="max-width: 400px; margin: 0 auto; ">
          <el-form-item label="创建角色名称" :prop="'bot_name'" required>
            <el-input v-model="createForm.bot_name" class="content"></el-input>
          </el-form-item>
          <el-form-item label="创建角色的身份背景" :prop="'bot_info'" required>
            <el-input v-model="createForm.bot_info" class="bot_info_input" :rows="4" type="textarea"
                      :autosize="{ minRows: 6, maxRows: 8 }"
                      placeholder="请输入身份背景"></el-input>
            <span style="position: absolute; bottom: 10px; right: 10px; color: #999;">{{ bot_infoLength }}/100</span>
          </el-form-item>
          <el-form-item label="人物角色头像生成" class="a">
            <el-button @click="generateCharacterAvatar">一键生成角色头像</el-button>
            <el-image v-if="characterAvatarUrl" :src="characterAvatarUrl"
                      style="max-width: 100px; max-height: 100px; margin-top: 10px;"></el-image>
          </el-form-item>
          <el-form-item label="对话人物名称" :prop="'user_name'" required>
            <el-input v-model="createForm.user_name" class="a"></el-input>
          </el-form-item>
          <el-form-item label="对话人物身份背景" :prop="'user_info'" required>
            <el-input v-model="createForm.user_info" class="user_info_input" :rows="4" type="textarea"
                      :autosize="{ minRows: 6, maxRows: 8 }"
                      placeholder="请输入身份背景"></el-input>
            <span style="position: absolute; bottom: 10px; right: 10px; color: #999;">{{ user_infoLength }}/100</span>
          </el-form-item>
          <el-form-item label="对话人物头像生成" class="a">
            <el-button @click="generateDialogueAvatar">一键生成对话人物头像</el-button>
            <el-image v-if="dialogueAvatarUrl" :src="dialogueAvatarUrl"
                      style="max-width: 100px; max-height: 100px; margin-top: 10px;"></el-image>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleCreate">立即创建</el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
    <div class="color"></div>
    <div class="color"></div>
    <div class="color"></div>
    <div class="box">
      <div class="square" style="--i:0;"></div>
      <div class="square" style="--i:1;"></div>
      <div class="square" style="--i:2;"></div>
      <div class="square" style="--i:3;"></div>
      <div class="square" style="--i:4;"></div>
    </div>
  </div>
</template>

<script>
import {
  simulateAvatar,
  simulateCharacterAvatar,
  simulateCreateCharacter,
  simulateDialogueAvatar
} from '@/api/createrole'; // 假设 api.js 存放在 src 目录下
export default {
  data() {
    return {
      createForm: {
        bot_name: '',
        bot_info: '',
        user_name: '',
        user_info: ''
      },
      createdCharacterId: '', // 用于保存创建的角色 ID
      characterAvatarUrl: '', // 存储生成的角色头像 URL
      dialogueAvatarUrl: '' // 存储生成的对话人物头像 URL
    }
  },
  computed: {
    bot_infoLength() {
      return this.createForm.bot_info.length;
    },
    user_infoLength() {
      return this.createForm.user_info.length;
    }
  },
  methods: {

    handleCreate() {
      // 处理创建角色的逻辑，可以发送请求给后端进行处理
      // 调用模拟接口函数，并传入角色信息
      const response1 = simulateCreateCharacter(this.createForm);
      this.createdCharacterId = response1.data.characterId; // 保存角色 ID
      // 输出模拟的响应数据到控制台，可以根据需要进行后续处理
      console.log('创建角色信息：', response1);

      if (response1.success) {
        // 提示创建成功
        // this.$message.success('创建角色成功');
        // 弹出提示框
        this.showSuccessMessageBox();
      }
    },
    generateCharacterAvatar() {
      const response2 = simulateAvatar(this.createForm);
      this.characterAvatarUrl = response2.data.AvatarUrl;
      console.log('创建角色头像生成：', response2);
      // 假设后端接口返回头像 URL
      setTimeout(() => {
        this.characterAvatarUrl
      }, 1000);

    },
    generateDialogueAvatar() {
      const response3 = simulateAvatar(this.createForm);
      this.dialogueAvatarUrl = response3.data.AvatarUrl;
      console.log('对话头像生成：', response3);
      // 假设后端接口返回头像 URL
      setTimeout(() => {
        this.dialogueAvatarUrl
      }, 1000);
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
    }
  }
}
</script>

<style scoped>
/* 可以添加样式来自定义页面的外观 */

/*.bot_info_input {*/
/*  width: 100%; !* 设置输入框宽度为100% *!*/
/*  height: 150px; !* 设置输入框的高度 *!*/
/*}*/

/*.user_info_input {*/
/*  width: 100%; !* 设置输入框宽度为100% *!*/
/*  height: 150px; !* 设置输入框的高度 *!*/
/*}*/

button {
  background-color: #4CAF50; /* 设置按钮背景颜色为绿色 */
  color: white; /* 设置按钮文字颜色为白色 */
  padding: 15px 25px; /* 设置按钮的内边距 */
  border: none; /* 去除按钮边框 */
  border-radius: 8px; /* 设置按钮的圆角 */
  cursor: pointer; /* 设置鼠标样式为手型 */
  transition: background-color 0.3s ease; /* 添加背景颜色渐变过渡效果 */
}

button:hover {
  background-color: #45a049; /* 设置鼠标悬停时按钮的背景颜色 */
}

/* 渐变背景 */
.color{
  position: absolute;
  filter: blur(150px);
}
.color:nth-child(1) {
  top: -350px;
  width: 600px;
  height: 600px;
  /*background: #ff359b;*/
  background: #475264;
}

.color:nth-child(2) {
  bottom: -150px;
  left: 100px;
  width: 500px;
  height: 500px;
  /*background: #fffd87;*/
  background: #32A7D6;
}

.color:nth-child(3) {
  bottom: 50px;
  right: 100px;
  width: 500px;
  height: 500px;
  /*background: #0746AD;*/
  background: #3269D6;
}

/* 方块动画 */
.box .square {
  position: absolute;
  backdrop-filter: blur(5px);
  box-shadow: 0 25px 45px rgb(0, 0, 0, 0.1);
  border: 1px solid rgb(255, 255, 255, 0.5);
  border-right: 1px solid rgb(255, 255, 255, 0.2);
  border-bottom: 1px solid rgb(255, 255, 255, 0.2);
  background: rgb(255, 255, 255, 0.1);
  border-radius: 10px;
  animation: animate 10s linear infinite;
}

/* 动画 */
@keyframes animate {
  0%, 100% {
    transform: translateY(-40px);
  }
  50% {
    transform: translate(40px);
  }
}

.box .square:nth-child(1) {
  top: 200px;
  right: 200px;
  width: 100px;
  height: 100px;
}

.box .square:nth-child(2) {
  bottom: 100px;
  left: 300px;
  width: 120px;
  height: 120px;
  z-index: 2;
}

.box .square:nth-child(3) {
  bottom: -10px;
  right: 300px;
  width: 80px;
  height: 80px;
  z-index: 2;
}

.box .square:nth-child(4) {
  bottom: -80px;
  left: 300px;
  width: 50px;
  height: 50px;
}

.box .square:nth-child(5) {
  bottom: -200px;
  right: 140px;
  width: 60px;
  height: 60px;
}

</style>
