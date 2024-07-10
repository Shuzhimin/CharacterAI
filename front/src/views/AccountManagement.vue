<template>
  <div>
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{path: '/userhome'}" style="">首页</el-breadcrumb-item>
<!--      <el-breadcrumb-item style="color: white">系统管理</el-breadcrumb-item>-->
      <el-breadcrumb-item style="color: white">账号管理</el-breadcrumb-item>
    </el-breadcrumb>
    <el-card style="margin-top: 15px">
      <el-row :gutter="20" style="padding-bottom: 20px">
        <el-col :span="7">
          <!--  搜索区  -->
          <el-input placeholder="请输入用户名" v-model="username_search" clearable @input="get_user">
            <!--            <el-button slot="append" icon="el-icon-search" @click="getBookList()"></el-button>-->
          </el-input>

        </el-col>

        <el-col :span="2">
          <el-button type="primary" @click="searchUser" plain>
              <el-icon class="el-icon--left"><Search /></el-icon>
              搜索
          </el-button>
        </el-col>

        <el-col :span="2">
          <el-button type="primary" @click="addAccount" plain>
            <el-icon class="el-icon--left"><Plus /></el-icon>
            新增用户
          </el-button>
        </el-col>

      </el-row>

      <el-table :data="table_data" border fit :row-class-name="tableRowClassName">
        <el-table-column label="账号ID" prop="uid" align="center" width="130"></el-table-column>
        <el-table-column label="账号名" prop="name" align="center"></el-table-column>
        <el-table-column label="账户角色" prop="role" align="center">
          <template v-slot:default="{row}">
            <el-switch
              v-model="row.role"
              inline-prompt
              active-text="admin"
              active-color="#13ce66"
              inactive-text="user"
              inactive-color="#ff4949"
              @change="handleAdminChange(row)">
            </el-switch>
          </template>
        </el-table-column>
        <el-table-column label="头像描述" prop="avatar_description" align="center" :show-overflow-tooltip="true"></el-table-column>
        <el-table-column label="头像" prop="avatar_url" align="center">
          <template v-slot:default="{row}">
            <div>
              <el-image
                style="width: 100px; height: 100px;border-radius: 20%"
                :src="row.avatar_url"
                preview-teleported
                :preview-src-list="[row.avatar_url]">
              </el-image>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="注册时间" prop="created_at" align="center" :show-overflow-tooltip="true"></el-table-column>
        <el-table-column label="更新时间" prop="updated_at" align="center" :show-overflow-tooltip="true"></el-table-column>
        <el-table-column label="操作"  align="center">
          <template v-slot:default="{row}">
            <div class="button-group mb-4">
              <el-button type="primary" :icon="Edit" @click="openEdit(row)" circle plain></el-button>
              <el-button type="danger" :icon="Delete" @click="delete_user_check(row)" circle plain/>
              <el-button type="success" @click="character_management(row)" round style="margin-top: 5px; margin-left: 0px;" plain>角色管理</el-button>
            </div>
          </template>
        </el-table-column>
      </el-table>
      <el-dialog
        title="提示"
        v-model="delDialogVisible"
        width="30%"
        :before-close="handleClose">
        <span>是否确定删除此角色！(该操作无法恢复)</span>
        <template #footer>
        <span slot="footer" class="dialog-footer">
              <el-button @click="delDialogVisible = false">取 消</el-button>
              <el-button type="primary" @click="delDialogVisible = false;delete_user()">确 定</el-button>
            </span>
        </template>
      </el-dialog>
      <el-dialog title="个人信息"
                 v-model="dialogFormVisible">
        <el-form :model="form">
          <el-form-item label="" :label-width="formLabelWidth">
            <el-switch
              v-model="form.modifyFlag"
              active-text="修改"
              active-color="#13ce66"
              inactive-text="不修改"
              inactive-color="#ff4949">
            </el-switch>
          </el-form-item>
          <el-form-item label="用户名" :label-width="formLabelWidth">
            <el-input v-model="form.username" autocomplete="off" :disabled="true"></el-input>
          </el-form-item>
          <el-form-item v-if="!form.modifyFlag" label="用户头像" :label-width="formLabelWidth">
            <el-image :src="form.avatar_url" style="max-width: 150px; max-height: 150px;"></el-image>
          </el-form-item>

          <!--            <el-form-item v-if="form.modifyFlag" label="新密码" :label-width="formLabelWidth">-->
          <!--              <el-input v-model="form.new_password" :show-password="true" autocomplete="off" :disabled="!form.modifyFlag"></el-input>-->
          <!--            </el-form-item>-->
          <!--            <el-form-item v-if="form.modifyFlag" label="再次确认新密码" :label-width="formLabelWidth">-->
          <!--              <el-input v-model="form.check_password" :show-password="true" autocomplete="off" :disabled="!form.modifyFlag"></el-input>-->
          <!--            </el-form-item>-->
<!--          <el-form-item v-if="form.modifyFlag" label="人物角色头像生成" class="a">-->
<!--            <el-button @click="showGenerateAvatarDialog">AI生成角色头像</el-button>-->
<!--          </el-form-item>-->
          <el-form-item v-if="form.modifyFlag" label="头像" :label-width="formLabelWidth">
            <GenerateAvatar :avatarUrl="form.avatar_url" :description="form.description" @returnUrl="getAvatarUrl"></GenerateAvatar>
          </el-form-item>

        </el-form>
        <template #footer>
          <div slot="footer" class="dialog-footer">
            <el-button @click="dialogFormVisible = false">取 消</el-button>
            <el-button type="primary" @click="modify()">确 定</el-button>
          </div>
        </template>

      </el-dialog>
      <el-pagination
        style="padding-top: 20px"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="search_query.pagenum"
        :page-sizes="[1, 2, 5, 10]"
        :page-size="search_query.pagesize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="search_query.total">
      </el-pagination>
    </el-card>
    <AddAccountDialog v-if="addAccountDialogVisible" @closeDialog="closeAddAccountDialog" :DialogShowFlag="addAccountDialogVisible"></AddAccountDialog>
  </div>

</template>

<script>
import GenerateAvatarDialog from '../components/dialog/GenerateAvatarDialog';
import GenerateAvatar from '../components/GenerateAvatar';
import AddAccountDialog from '../components/dialog/AddAccountDialog';
import { user_select, user_update, user_me } from '../api/user';
import { admin_user_select, admin_user_delete, admin_user_update_profile, admin_user_update_role } from '../api/admin';
import {
    Check,
    Delete,
    Edit,
    Message,
    Search,
    Star,
    Plus,
} from '@element-plus/icons-vue'

export default {
  name: 'AccountManagement',
  computed: {
    Delete() {
      return Delete
    },
    Edit() {
      return Edit
    }
  },
  components: { AddAccountDialog, GenerateAvatarDialog, GenerateAvatar },
  data() {
    return {
      username_search: '',
      table_data: [
        // {
        //   uid: 1,
        //   name: 'admin',
        //   role: '管理员',
        //   avatar_description: '图像描述',
        //   avatar_url: 'https://lingyou-1302942961.cos.ap-beijing.myqcloud.com/lingyou/16790385261248df6fb83-63b0-4497-826e-b5f2cfbe97a3.jpg',
        //   created_at: '2024-03-01 12:00',
        //   updated_at: '2024-03-01 12:00'
        // }
      ],
      search_query: {
        pagenum: 1,
        pagesize: 10,
        total: 0
      },
      receive: {
        total: 100,
      },


      addAccountDialogVisible: false,
      dialogFormVisible: false,
      formLabelWidth: '120px',
      form: {
        username: '',
        avatar_url: '',
        description: '',
        password: '',
        new_password: '',
        modifyFlag: false
      },
      delDialogVisible: false,
      delete_uid: [

      ]
    }
  },

  created() {
    this.get_user()
  },
  methods: {
    searchUser(){
      console.log('查询用户')
    },


    addAccount(){
      console.log('新增用户')
      this.addAccountDialogVisible = true;
      console.log(this.addAccountDialogVisible)
    },
    closeAddAccountDialog() {
      this.addAccountDialogVisible = false;
    },
    // 监听 pagesize 改变的事件
    handleSizeChange (newSize) {
      console.log(newSize)
      this.search_query.pagesize = newSize
      this.get_user()
    },
    // 监听 页码值 改变的时间
    handleCurrentChange (newPage) {
      console.log(newPage)
      this.search_query.pagenum = newPage
      this.get_user()
    },
    get_user(){
      let params = {
        "query": this.username_search,
        "page_num": this.search_query.pagenum,
        "page_size": this.search_query.pagesize
      }
      admin_user_select(params).then(res => {
        if (res.status === 200){
          console.log(res)
          this.table_data = res.data.users
          this.table_data.forEach((item, index) => {
            item['role'] = item['role'] === 'admin'
            if (this.username_search !== ''){
              item['score'] = res.data.scores[index]
            }
          })
          this.search_query.total = res.data.total
          console.log("数据")
          console.log(this.table_data)
        }
      })
    },
    delete_user_check(row){
      this.delete_uid = [row.uid]
      this.delDialogVisible = true
    },

    delete_user(){
      let params = this.delete_uid
      admin_user_delete(params).then(res => {
        this.$message.success("删除成功！")
        this.get_user()
      })
    },
    openEdit(row) {
      this.dialogFormVisible = true
      this.form.uid = row.uid
      this.form.username = row.name
      this.form.avatar_url = row.avatar_url
      this.form.description = row.avatar_description

    },
    getAvatarUrl(url, avatarDescription){
      this.form.avatar_url = url
      this.form.description = avatarDescription
      console.log(url)
    },
    modify(){
      let params = {
        "uid": this.form.uid,
        "name": this.form.username,
        "avatar_description": this.form.description,
        "avatar_url": this.form.avatar_url
      }
      admin_user_update_profile(params).then(res => {
        if (res.status === 200){
          this.$message.success("修改成功！")
          this.get_user()
          this.dialogFormVisible = false
        }
      })
    },
    character_management(row){
      localStorage.setItem('cm_uid', row.uid)
      this.$router.push('/charactermanagement')
    },
    handleClose(done) {
      this.$confirm('确认关闭？')
        .then(_ => {
          done();
        })
        .catch(_ => {});
    },
    handleAdminChange(row) {
      console.log("权限变更")
      console.log(row)
      let params = {
        uid: row.uid,
        role: row.role ? "admin" : "user"
      }
      admin_user_update_role(params).then(res => {
        if (res.status === 200){
          console.log(res.data)
          this.get_user()
        }
      })
    },
    tableRowClassName({ row, rowIndex }) {
      if (row['score'] < 50){
        console.log('irrelevance')
        return 'warning-row'
      }
      else {
        return ''
      }
    }
  }
};
</script>

<style scoped>
.el-breadcrumb__item {
  color: black;
}
:deep(.el-breadcrumb__inner) {
  color: black;
}
</style>
