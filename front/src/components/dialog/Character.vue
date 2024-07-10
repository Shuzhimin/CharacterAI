<template>
  <el-dialog
    title="提示"
    :visible.sync="editDialogVisible"
    width="30%"
    :before-close="handleClose">
    <div>
      <div class="content">
        <div>
          <el-form :model="createForm" label-position="top" style="max-width: 400px; margin: 0 auto; ">
            <el-form-item label="角色分类" :prop="'selectedCategory'" required>
              <el-select v-model="createForm.selectedCategory" placeholder="请选择角色分类">
                <el-option label="美食" value="food"></el-option>
                <el-option label="旅游" value="travel"></el-option>
                <el-option label="科技" value="technology"></el-option>
                <el-option label="健康" value="health"></el-option>
                <el-option label="法律" value="law"></el-option>
                <el-option label="其他" value="other"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="创建角色名称" :prop="'bot_name'" required>
              <el-input v-model="createForm.bot_name" ></el-input>
            </el-form-item>
            <el-form-item label="创建角色的身份背景" :prop="'bot_info'" required>
              <el-input v-model="createForm.bot_info" :rows="4" type="textarea"
                        :autosize="{ minRows: 6, maxRows: 8 }"
                        placeholder="请输入身份背景"></el-input>
              <span style="position: absolute; bottom: 10px; right: 10px; color: #999;">{{ bot_infoLength }}/100</span>
            </el-form-item>
            <el-form-item label="人物角色头像生成" class="a">
              <el-button @click="showGenerateAvatarDialog">AI生成角色头像</el-button>
            </el-form-item>
            <!-- 头像生成对话框 -->
            <el-dialog
              title="AI生成头像"
              :visible.sync="dialogVisible"
              width="50%"
              :close-on-click-modal="false"
            >
              <div class="avatar-dialog-content">
                <el-input v-model="avatarDescription" :rows="4" type="textarea"
                          :autosize="{ minRows: 6, maxRows: 8 }"
                          placeholder="请输入头像的描述"></el-input>
                <span style="position: absolute; bottom: 10px; right: 10px; color: #999;">{{ avatarDescriptionLength }}/100</span>

                <el-button @click="generateAvatar" class="generate-avatar-button">生成头像</el-button>
                <el-image v-if="createForm.avatarUrl" :src="createForm.avatarUrl"
                          style="max-width: 150px; max-height: 150px;"></el-image>

                <el-button @click="saveAvatar" type="primary" class="enter-button">确定</el-button>
              </div>
            </el-dialog>
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
        </div>
      </div>
    </div>
  </el-dialog>
</template>

<script>
import {
  simulateAvatar,
  // simulateCharacterAvatar,
  simulateCreateCharacter,
  // simulateDialogueAvatar
} from '@/api/createrole'; // 假设 api.js 存放在 src 目录下
export default {
  name: 'Character',
  data() {
    return {
      createForm: {
        bot_name: '',
        bot_info: '',
        // user_name: '',
        // user_info: ''
        selectedCategory: '',
        avatarUrl: '',// 生成的头像 URL
      },
      dialogVisible: false, // 对话框可见性
      avatarDescription: '', // 头像描述
      createdCharacterId: '', // 用于保存创建的角色 ID
      // characterAvatarUrl: '', // 存储生成的角色头像 URL
      // dialogueAvatarUrl: '' // 存储生成的对话人物头像 URL
    }
  },
  computed: {
    bot_infoLength() {
      return this.createForm.bot_info.length;
    },
    avatarDescriptionLength() {
      return this.avatarDescription.length;
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
        // this.$message.success('创建角色成功');
        // 弹出提示框
        this.showSuccessMessageBox();
      }
    },
    // generateCharacterAvatar() {
    //   const response2 = simulateAvatar(this.createForm);
    //   this.characterAvatarUrl = response2.data.AvatarUrl;
    //   console.log('创建角色头像生成：', response2);
    //   // 假设后端接口返回头像 URL
    //   setTimeout(() => {
    //     this.characterAvatarUrl
    //   }, 1000);
    //
    // },
    showGenerateAvatarDialog() {
      // 显示生成头像对话框
      this.dialogVisible = true;
    },
    generateAvatar() {
      const response2 = simulateAvatar(this.avatarDescription);
      this.createForm.avatarUrl = response2.data.AvatarUrl;
      console.log('头像生成：', response2);
      // 假设后端接口返回头像 URL
      setTimeout(() => {
        this.createForm.avatarUrl
      }, 1000);
    },
    saveAvatar() {
      // 保存头像到本地的逻辑，这里使用假数据
      console.log('头像已保存');
      // 关闭对话框
      this.dialogVisible = false;
    },
    // generateDialogueAvatar() {
    //   const response3 = simulateAvatar(this.createForm);
    //   this.dialogueAvatarUrl = response3.data.AvatarUrl;
    //   console.log('对话头像生成：', response3);
    //   // 假设后端接口返回头像 URL
    //   setTimeout(() => {
    //     this.dialogueAvatarUrl
    //   }, 1000);
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
    }
  }
};
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

.avatar-dialog-content {
  text-align: center; /* 让内容居中显示 */
}
.generate-avatar-button {
  float: left;
  margin-top: 20px; /* 可以根据需要调整按钮与其他元素之间的间距 */
}
.enter-button {
  margin-top: 200px;
}

</style>
