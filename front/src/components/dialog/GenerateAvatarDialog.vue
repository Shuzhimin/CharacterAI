<template>
  <el-dialog
    title="AI生成头像"
    :visible.sync="dialog_data.dialogVisible"
    width="50%"
    :close-on-click-modal="false"
    :before-close="handleClose"
  >
    <div class="avatar-dialog-content">
      <el-input v-model="dialog_data.avatarDescription" :rows="4" type="textarea"
                :autosize="{ minRows: 6, maxRows: 8 }"
                placeholder="请输入头像的描述"></el-input>
      <span style="position: absolute; bottom: 10px; right: 10px; color: #999;">{{ avatarDescriptionLength }}/100</span>

      <el-button @click="generateAvatar" class="generate-avatar-button">生成头像</el-button>
      <el-image v-if="dialog_data.avatarUrl" :src="dialog_data.avatarUrl"
                style="max-width: 150px; max-height: 150px;"></el-image>

      <el-button @click="saveAvatar" type="primary" class="enter-button">确定</el-button>
    </div>
  </el-dialog>
</template>

<script>
import { simulateAvatar } from '@/api/createrole';

export default {
  name: 'GenerateAvatarDialog',
  props: ['DialogShowFlag', 'avatarUrl'],
  data() {
    return{
      dialog_data: {
        avatarDescription: '',
        dialogVisible: false,
        avatarUrl: ''
      }

    }
  },
  created() {

  },
  mounted() {
    this.dialog_data.dialogVisible = this.DialogShowFlag
    this.dialog_data.avatarUrl = this.avatarUrl
  },
  computed: {
    avatarDescriptionLength() {
      return this.dialog_data.avatarDescription.length;
    }
  },
  methods: {
    handleClose() {
      this.$emit('closeDialog')
    },
    generateAvatar() {
      const response2 = simulateAvatar(this.dialog_data.avatarDescription);
      this.dialog_data.avatarUrl = response2.data.AvatarUrl;
      console.log('头像生成：', response2);
      // 假设后端接口返回头像 URL
      setTimeout(() => {
        this.dialog_data.avatarUrl
      }, 1000);
    },
    saveAvatar() {
      // 保存头像到本地的逻辑，这里使用假数据
      console.log('头像已保存');
      // 关闭对话框
      this.dialog_data.dialogVisible = false;
      this.handleClose()
    },
  }
};
</script>

<style scoped>
.avatar-dialog-content {
  text-align: center; /* 让内容居中显示 */
}
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
.generate-avatar-button {
  float: left;
  margin-top: 20px; /* 可以根据需要调整按钮与其他元素之间的间距 */
}
.enter-button {
  margin-top: 200px;
}
</style>
