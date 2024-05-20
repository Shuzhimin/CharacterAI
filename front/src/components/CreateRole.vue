<template>
  <div>
    <div class="content">
      <div>
        <el-form :model="createForm" label-position="top" style="max-width: 400px; margin: 0 auto; ">
          <el-form-item label="角色分类" :prop="'selectedCategory'" required>
            <el-select v-model="createForm.selectedCategory" placeholder="请选择角色分类">
              <el-option label="美食" value="food"></el-option>
              <el-option label="旅游" value="travel"></el-option>
              <el-option label="科技" value="tech"></el-option>
              <el-option label="健康" value="health"></el-option>
              <el-option label="法律" value="law"></el-option>
              <el-option label="其他" value="other"></el-option>
              <el-option label="长文档分析" value="doc_rag"></el-option>
              <el-option label="智能报表" value="reporter"></el-option>
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
          <el-form-item label="是否共享" prop="isShared">
            <el-switch
              v-model="createForm.isShared"
              active-text="共享"
              active-color="#13ce66"
              inactive-text="不共享"
              inactive-color="#606266">
            </el-switch>
          </el-form-item>
          <!--          <el-form-item label="人物角色头像生成" class="a">-->
          <!--            <el-button @click="showGenerateAvatarDialog">AI生成角色头像</el-button>-->
          <!--          </el-form-item>-->
          <el-form-item label="人物角色头像生成" >
            <GenerateAvatar :avatarUrl="createForm.avatarUrl" @returnUrl="getAvatarUrl"></GenerateAvatar>
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
          <el-form-item label="资料文档">
            <el-upload
              ref="upload"
              class="upload-demo"
              drag
              action="#"
              :limit="1"
              :on-success="handleSuccess"
              :on-preview="handlePreview"
              :on-remove="handleRemove"
              :on-change="handleChange"
              :before-remove="beforeRemove"
              :auto-upload="false"
              :on-exceed="handleExceed"
              :file-list="fileList"
              :http-request="handleFileUpload">
              <i class="el-icon-upload"></i>
              <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
              <div class="el-upload__tip" slot="tip">只能上传txt/pdf文件，且不超过50MB</div>
<!--              <el-button size="small" type="primary">点击上传</el-button>-->
<!--              <div slot="tip" class="el-upload__tip">只能上传jpg/png文件，且不超过500kb</div>-->
            </el-upload>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="submitUpload">立即创建</el-button>
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
      <!--      <div class="square" style="&#45;&#45;i:3;"></div>-->
      <!--      <div class="square" style="&#45;&#45;i:4;"></div>-->
    </div>
  </div>
</template>

<script>
import {
  simulateAvatar,
  // simulateCharacterAvatar,
  simulateCreateCharacter,
  // simulateDialogueAvatar
} from '@/api/createrole'; // 假设 api.js 存放在 src 目录下
import GenerateAvatar from '@/components/GenerateAvatar';
import { character_create } from '@/api/character';
export default {
  components: { GenerateAvatar },
  data() {
    return {
      createForm: {
        bot_name: '',
        bot_info: '',
        // user_name: '',
        // user_info: ''
        selectedCategory: '',
        avatarUrl: '',// 生成的头像 URL
        isShared: false
      },
      dialogVisible: false, // 对话框可见性
      avatarDescription: '', // 头像描述
      createdCharacterId: '', // 用于保存创建的角色 ID
      // characterAvatarUrl: '', // 存储生成的角色头像 URL
      // dialogueAvatarUrl: '' // 存储生成的对话人物头像 URL
      fileList: [],
      fileCount: 0,
    }
  },
  created() {
    window.sessionStorage.setItem('activePath', '/createrole')
    this.$emit('updateParentValue', '/createrole')
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
    handleCreate(file) {
      // // 处理创建角色的逻辑，可以发送请求给后端进行处理
      // // 调用模拟接口函数，并传入角色信息
      // const response1 = simulateCreateCharacter(this.createForm);
      // this.createdCharacterId = response1.data.characterId; // 保存角色 ID
      // // 输出模拟的响应数据到控制台，可以根据需要进行后续处理
      // console.log('创建角色信息：', response1);
      //
      // if (response1.success) {
      //   // this.$message.success('创建角色成功');
      //   // 弹出提示框
      //   this.showSuccessMessageBox();
      // }
      console.log('zzz')
      console.log(file)
      // file.filename = file.name
      // let params = {
      //   "name": this.createForm.bot_name,
      //   "description": this.createForm.bot_info,
      //   "avatar_description":this.createForm.avatarDescription,
      //   "avatar_url":this.createForm.avatar_url,
      //   "category": this.createForm.selectedCategory,
      //   "uid": window.localStorage.getItem("uid"),
      //   "is_shared": this.createForm.isShared,
      //   "file": file
      // }
      const params = new FormData()
      params.append("name", this.createForm.bot_name)
      params.append("description", this.createForm.bot_info)
      params.append("avatar_description", this.createForm.avatarDescription)
      params.append("avatar_url", this.createForm.avatar_url)
      params.append("category", this.createForm.selectedCategory)
      params.append("uid", window.localStorage.getItem("uid"))
      params.append("is_shared", this.createForm.isShared)
      if (file !== null){
        params.append("file", file)
      }

      this.$message.info("解析上传的文件需要一定的时间，请耐心等待~")
      character_create(params).then(res => {
        console.log(res)
        if (res.status === 200){
          // this.$message.success("创建成功！")
          this.$confirm(`角色创建成功，可以选择与创建角色对话或回到首页查看角色`, {
            confirmButtonText: '与创建角色对话',
            cancelButtonText: '回到首页查看角色',
            type: 'success'
          }).then(() => {
            // 点击与创建角色对话按钮的逻辑
            console.log('与创建角色对话');
            console.log(this.createForm)
            localStorage.setItem('roleCategory', this.createForm.selectedCategory)
            localStorage.setItem('roleMess_name', this.createForm.bot_name)
            localStorage.setItem('roleMess_avatar_url', this.createForm.avatar_url)
            localStorage.setItem('roleMess_description', this.createForm.bot_info)
            localStorage.setItem('roleMess_avatar_description', this.createForm.avatarDescription)
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
              selectedCategory: '',
              avatarUrl: '',
            };
          });
        }
      })
    },
    getAvatarUrl(url, avatarDescription){
      this.createForm.avatar_url = url
      this.createForm.avatarDescription = avatarDescription
      console.log(url)
    },
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
    handleSuccess(response, file, fileList){
      console.log(fileList)
    },
    handleRemove(file, fileList) {
      console.log(file, fileList);
    },
    handlePreview(file) {
      console.log(file);
    },
    handleExceed(files, fileList) {
      this.$message.warning(`当前限制选择 1 个文件，本次选择了 ${files.length} 个文件，共选择了 ${files.length + fileList.length} 个文件`);
    },
    beforeRemove(file, fileList) {
      console.log(fileList)
      return this.$confirm(`确定移除 ${ file.name }？`);
    },
    handleChange(file, fileList){
      this.fileCount = fileList.length
    },
    handleFileUpload(file) {
      console.log(111)
      console.log(file)
      this.handleCreate(file.file)
    },
    submitUpload() {
      console.log("创建")
      console.log(this.fileList)
      if (this.fileCount === 0){
        this.handleCreate(null)
      }
      else {
        this.$refs.upload.submit();
      }

    }
  }
}
</script>

<style scoped>

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
  bottom: 0px;
  left: 200px;
  width: 400px;
  height: 400px;
  /*background: #fffd87;*/
  background: #32A7D6;
}

.color:nth-child(3) {
  bottom: 50px;
  right: 50px;
  width: 300px;
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
  bottom: 50px;
  right: 300px;
  width: 50px;
  height: 50px;
  z-index: 2;
}

/*.box .square:nth-child(4) {*/
/*  bottom: -80px;*/
/*  left: 300px;*/
/*  width: 50px;*/
/*  height: 50px;*/
/*}*/

/*.box .square:nth-child(5) {*/
/*  bottom: -200px;*/
/*  right: 140px;*/
/*  width: 60px;*/
/*  height: 60px;*/
/*}*/

</style>
