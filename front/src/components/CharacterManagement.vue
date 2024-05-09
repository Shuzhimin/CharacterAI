<template>
  <div>
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{path: '/userhome'}" style="color: white">首页</el-breadcrumb-item>
      <el-breadcrumb-item style="color: white">系统管理</el-breadcrumb-item>
      <el-breadcrumb-item :to="{path: '/accountmanagement'}" style="color: white">账号管理</el-breadcrumb-item>
      <el-breadcrumb-item style="color: white">角色管理</el-breadcrumb-item>
    </el-breadcrumb>
    <el-card style="margin-top: 15px">
      <el-row :gutter="20" style="padding-bottom: 20px">
        <el-col :span="7">
          <!--  搜索区  -->
          <el-input placeholder="请输入角色名" v-model="character_name_search" clearable>
            <!--            <el-button slot="append" icon="el-icon-search" @click="getBookList()"></el-button>-->
          </el-input>

        </el-col>

        <el-col :span="2">
          <el-button type="primary" icon="el-icon-search" @click="searchUser">搜索</el-button>
        </el-col>


      </el-row>

      <el-table :data="table_data" border fit stripe>
        <el-table-column label="角色id" prop="cid" align="center"></el-table-column>
        <el-table-column label="角色名" prop="name" align="center"></el-table-column>
        <el-table-column label="角色描述" prop="description" align="center"></el-table-column>
        <el-table-column label="角色分类" prop="category" align="center"></el-table-column>
        <el-table-column label="头像描述" prop="avatar_description" align="center"></el-table-column>
        <el-table-column label="头像" prop="avatar_url" align="center">
          <template slot-scope="scope">
            <div>
              <el-image
                style="width: 100px; height: 100px"
                :src="scope.row.avatar_url"
                :preview-src-list="[scope.row.avatar_url]">
              </el-image>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="注册时间" prop="created_at" align="center"></el-table-column>
        <el-table-column label="更新时间" prop="updated_at" align="center"></el-table-column>
        <el-table-column label="共享情况" prop="is_shared" align="center">
          <template slot-scope="scope">
            <span>{{shared_status(scope.row)}}</span>
          </template>
        </el-table-column>
        <el-table-column label="操作"  align="center">
          <template slot-scope="scope">
            <el-button size="medium" @click="openEdit(scope.row)" circle>编辑</el-button>
            <el-button size="medium" @click="delete_user(scope.row)" circle>删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-dialog title="个人信息" :visible.sync="dialogFormVisible">
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
        <div slot="footer" class="dialog-footer">
          <el-button @click="dialogFormVisible = false">取 消</el-button>
          <el-button type="primary" @click="modify()">确 定</el-button>
        </div>
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
import GenerateAvatarDialog from '@/components/dialog/GenerateAvatarDialog';
import GenerateAvatar from '@/components/GenerateAvatar';
import AddAccountDialog from '@/components/dialog/AddAccountDialog';
import { user_select, user_delete, user_update, user_me } from '@/api/user';
import { character_select } from '@/api/character';
export default {
  name: 'CharacterManagement',
  components: { AddAccountDialog, GenerateAvatarDialog, GenerateAvatar },
  data() {
    return {
      character_name_search: '',
      table_data: [
        {
          uid: 1,
          name: 'admin',
          role: '管理员',
          avatar_description: '图像描述',
          avatar_url: 'https://lingyou-1302942961.cos.ap-beijing.myqcloud.com/lingyou/16790385261248df6fb83-63b0-4497-826e-b5f2cfbe97a3.jpg',
          created_at: '2024-03-01 12:00',
          updated_at: '2024-03-01 12:00'
        }
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
      uid: null
    }
  },
  created() {
    if (localStorage.getItem("cm_uid") === null){
      this.$message.warning("未选择用户！")
      this.$router.push('/accountmanagement')
    }
    this.uid = localStorage.getItem('cm_uid')
    this.get_character()
  },
  methods: {
    shared_status(row){
      if (row.is_shared){
        return '共享'
      }
      else {
        return '非共享'
      }
    },
    searchUser(){
      console.log('查询用户')
    },
    addAccount(){
      console.log('新增用户')
      this.addAccountDialogVisible = true;
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
    get_character(){
      let params = {
        cid: this.uid,
        category: 'other'
      }
      character_select(params).then(res => {
        if (res.status === 200){
          this.table_data = res.data
          console.log(this.table_data)
        }
      })
    },
    delete_user(row){
      let params = [
        row.uid
      ]
      user_delete(params).then(res => {
        this.$message.success("删除成功！")
        this.get_user()
      })
    },
    openEdit(row) {
      this.dialogFormVisible = true
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
        "name": this.form.username,
        "avatar_description": this.form.avatarDescription,
        "avatar_url": this.form.avatar_url
      }
      user_update(params).then(res => {
        if (res.status === 200){
          this.$message.success("修改成功！")
          this.dialogFormVisible = false
        }
      })
    },
  }
};
</script>

<style scoped>
.el-breadcrumb__item {
  color: white;
}
:deep(.el-breadcrumb__inner) {
  color: white;
}
</style>
