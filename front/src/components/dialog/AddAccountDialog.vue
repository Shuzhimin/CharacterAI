<template>
  <el-dialog
    title="新增账号"
    v-model="dialog_data.dialogVisible"
    width="50%"
    :close-on-click-modal="false"
    :before-close="handleClose"
  ><!--    :visible.sync="dialog_data.dialogVisible"-->
    <el-form ref="form" :model="dialog_data" label-width="80px" :rules="chooseRule">
      <el-form-item label="用户名" prop="username">
        <el-input v-model="dialog_data.username"></el-input>
      </el-form-item>
      <el-form-item label="密码" prop="password">
        <el-input type="password" v-model="dialog_data.password" autocomplete="off" :show-password="true"></el-input>
      </el-form-item>
      <el-form-item label="确认密码" prop="repassword">
        <el-input type="password" v-model="dialog_data.repassword" autocomplete="off" :show-password="true"></el-input>
      </el-form-item>
<!--      <el-form-item label="用户角色" prop="role">-->
<!--        <el-select v-model="dialog_data.role" placeholder="请选择">-->
<!--          <el-option-->
<!--            v-for="item in options"-->
<!--            :key="item.value"-->
<!--            :label="item.label"-->
<!--            :value="item.value">-->
<!--          </el-option>-->
<!--        </el-select>-->
<!--      </el-form-item>-->
<!--      <el-form-item label="用户头像" prop="avatar">-->
<!--        <el-button @click="showGenerateAvatarDialog">AI生成角色头像</el-button>-->
<!--      </el-form-item>-->
      <el-form-item label="头像">
        <GenerateAvatar :avatarUrl="dialog_data.avatar_url" @returnUrl="getAvatarUrl"></GenerateAvatar>
      </el-form-item>

    </el-form>
    <template #footer>
      <div slot="footer" class="dialog-footer">
        <el-button @click="handleClose">取 消</el-button>
        <el-button type="primary" @click="create()">确 认</el-button>
      </div>
    </template>

<!--    <GenerateAvatarDialog v-if="generateAvatarDialogVisible" @closeDialog="closeGenerateAvatarDialog" :DialogShowFlag="generateAvatarDialogVisible" :avatarUrl="dialog_data.avatarUrl"></GenerateAvatarDialog>-->

  </el-dialog>
</template>

<script>
import GenerateAvatar from '@/components/GenerateAvatar';
import { register } from '@/api/user';
export default {
  name: 'AddAccountDialog',
  components: { GenerateAvatar },
  // props: ['DialogShowFlag', 'isEdit'],
  props: {
    DialogShowFlag: {
      type: Boolean
    },
    isEdit: {
      type: Boolean,
      default: false
    }
  },
  data(){
    const equalToPassword = (rule, value, callback) => {
      if (this.dialog_data.password !== this.dialog_data.repassword) {
        console.log(1)
        callback(new Error("两次输入的密码不一致"))
      }
      else {
        console.log(2)
        callback()
      }
    }
    return {
      dialog_data: {
        title: '创建账号',
        dialogVisible: false,
        username: '',
        password: '',
        repassword: '',
        role: '', // 用户角色
        avatar_url: '',
        isEdit: false
      },

      generateAvatarDialogVisible: false,
      options: [{
        value: '0',
        label: '管理员'
      }, {
        value: '1',
        label: '普通用户'
      }],
      createRules: {
        username: [
          { required: true, message: '请输入账号', trigger: 'blur' },
          { min: 1, max: 10, message: '长度在 1 到 10 个字符', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 1, max: 15, message: '长度在 1 到 15 个字符', trigger: 'blur' }
        ],
        repassword: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 1, max: 15, message: '长度在 1 到 15 个字符', trigger: 'blur' },
          { validator: equalToPassword, message: '两次输入的密码不一致', trigger: 'blur' }
        ],
        role: [
          { required:true, message: '请选择角色', trigger: 'blur' }
        ],
      },
      editRules: {
        username: [
          { min: 1, max: 10, message: '长度在 1 到 10 个字符', trigger: 'blur' }
        ],
        password: [
          { min: 1, max: 15, message: '长度在 1 到 15 个字符', trigger: 'blur' }
        ],
        repassword: [
          { min: 1, max: 15, message: '长度在 1 到 15 个字符', trigger: 'blur' },
          { validator: equalToPassword, message: '两次输入的密码不一致', trigger: 'blur' }
        ],
        role: [
        ],
      },
    }
  },
  created() {
  },
  mounted() {
    this.dialog_data.dialogVisible = this.DialogShowFlag
    this.dialog_data.isEdit = this.isEdit
  },
  computed: {
    chooseRule() {
      if (this.dialog_data.isEdit === true) {
        return this.editRules
      }
      else {
        return this.createRules
      }
    }
  },
  methods: {
    showGenerateAvatarDialog() {
      // 显示生成头像对话框
      console.log(this.generateAvatarDialogVisible)
      this.generateAvatarDialogVisible = true;
      console.log(this.generateAvatarDialogVisible)
    },
    closeGenerateAvatarDialog() {
      this.generateAvatarDialogVisible = false;
    },
    handleClose() {
      this.$emit('closeDialog')
    },
    create() {
      this.$refs['form'].validate((valid) => {
        if (valid) {
          console.log('创建成功！')
          let params = {
            "name": this.dialog_data.username,
            "password": this.dialog_data.password,
            "avatar_description": this.dialog_data.avatarDescription,
            "avatar_url": this.dialog_data.avatar_url
          }

          register(params).then(res => {
            console.log(res)
            if (res.status === 200){
              this.$message.success("注册成功！")
            }
          })
          this.dialog_data.dialogVisible = false
          this.handleClose()
        }
      })
    },
    getAvatarUrl(url, avatarDescription){
      this.dialog_data.avatar_url = url
      this.dialog_data.avatarDescription = avatarDescription
      console.log(url)
    }

  }
};
</script>

<style scoped>

</style>
