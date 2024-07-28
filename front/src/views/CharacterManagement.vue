<template>
  <div>
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{path: '/userhome'}" style="">首页</el-breadcrumb-item>
<!--      <el-breadcrumb-item style="color: white">系统管理</el-breadcrumb-item>-->
      <el-breadcrumb-item :to="{path: '/accountmanagement'}" style="">账号管理</el-breadcrumb-item>
      <el-breadcrumb-item style="color: white">智能体管理</el-breadcrumb-item>
    </el-breadcrumb>
    <el-card style="margin-top: 15px">
      <el-row :gutter="20" style="padding-bottom: 20px">
        <el-col :span="7">
          <!--  搜索区  -->
          <el-input placeholder="请输入智能体名称" v-model="character_name_search" @input="get_character" clearable>
            <!--            <el-button slot="append" icon="el-icon-search" @click="getBookList()"></el-button>-->
          </el-input>

        </el-col>

        <el-col :span="2">
          <el-button type="primary" @click="get_character" plain>
            <el-icon class="el-icon--left"><Search /></el-icon>
            搜索
          </el-button>
        </el-col>


      </el-row>

      <el-table :data="table_data" border fit :row-class-name="tableRowClassName">
        <el-table-column label="智能体id" prop="cid" align="center"></el-table-column>
        <el-table-column label="智能体名称" prop="name" align="center"></el-table-column>
        <el-table-column label="智能体描述" prop="description" align="center" :show-overflow-tooltip="true"></el-table-column>
        <el-table-column label="智能体分类" prop="category" align="center"></el-table-column>
        <el-table-column label="头像描述" prop="avatar_description" align="center"></el-table-column>
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
        <el-table-column label="共享情况" prop="is_shared" align="center">
          <template v-slot:default="{row}">
            <span>{{shared_status(row)}}</span>
          </template>
        </el-table-column>
        <el-table-column label="操作"  align="center">
          <template v-slot:default="{row}">
            <div class="button-group mb-4">
              <el-button type="primary" :icon="Edit" @click="openEdit(row)" circle plain></el-button>
              <el-button type="danger" :icon="Delete" @click="openDel(row)" circle plain/>
            </div>
          </template>
        </el-table-column>
      </el-table>
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
          <!--              <el-form-item label="创建角色的身份背景" :prop="'bot_info'" required>-->
          <!--                <el-input v-model="editForm.description" :rows="4" type="textarea"-->
          <!--                          :autosize="{ minRows: 6, maxRows: 8 }"-->
          <!--                          placeholder="请输入身份背景"></el-input>-->
          <!--                <span style="position: absolute; bottom: 10px; right: 10px; color: #999;">{{ bot_infoLength }}/100</span>-->
          <!--              </el-form-item>-->
          <!--              <el-form-item label="人物角色头像生成" class="a">-->
          <!--                <el-button @click="showGenerateAvatarDialog">AI生成角色头像</el-button>-->
          <!--              </el-form-item>-->
          <el-form-item label="智能体描述">
            <el-input v-model="editForm.description" :rows="4" type="textarea"
                      :autosize="{ minRows: 6, maxRows: 8 }"
                      placeholder="请输入智能体的描述"></el-input>
          </el-form-item>
          <el-form-item label="头像" >
            <GenerateAvatar :key="editForm.key" :avatarUrl="editForm.avatarUrl" :description="editForm.avatar_description" @returnUrl="getAvatarUrl"></GenerateAvatar>
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
          <!--              <el-form-item>-->
          <!--                <el-button type="primary" @click="handleCreate">立即创建</el-button>-->
          <!--              </el-form-item>-->
        </el-form>
        <template #footer>
          <span slot="footer" class="dialog-footer">
              <el-button @click="editDialogVisible = false">取 消</el-button>
              <el-button type="primary" @click="update_user">确 定</el-button>
            </span>
        </template>

      </el-dialog>
      <el-dialog
        title="提示"
        v-model="delDialogVisible"
        width="30%"
        :before-close="handleClose">
        <span>是否确定删除此智能体！(该操作无法恢复)</span>
        <template #footer>
           <span slot="footer" class="dialog-footer">
              <el-button @click="delDialogVisible = false">取 消</el-button>
              <el-button type="primary" @click="delDialogVisible = false;delete_user()">确 定</el-button>
            </span>
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
import GenerateAvatarDialog from '@/components/dialog/GenerateAvatarDialog';
import GenerateAvatar from '@/components/GenerateAvatar';
import AddAccountDialog from '@/components/dialog/AddAccountDialog';
import { user_select, user_update, user_me } from '@/api/user';
import { character_delete, character_select, character_update } from '@/api/character';
import { admin_character_select } from '@/api/admin';
import {Delete, Edit} from "@element-plus/icons-vue";
export default {
  name: 'CharacterManagement',
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
      uid: null,
      editForm: {
        bot_name: '',
        description: '',
        // user_name: '',
        // user_info: ''
        selectedCategory: '',
        avatarUrl: '',// 生成的头像 URL
        key: null
      },
      editDialogVisible: false,
      delDialogVisible: false,
      delId: null
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
      this.get_character()
    },
    // 监听 页码值 改变的时间
    handleCurrentChange (newPage) {
      console.log(newPage)
      this.search_query.pagenum = newPage
      this.get_character()
    },
    get_character(){
      let params = {
        uid: this.uid,
        query: this.character_name_search,
        page_num: this.search_query.pagenum,
        page_size: this.search_query.pagesize
      }
      admin_character_select(params).then(res => {
        if (res.status === 200){
          this.table_data = res.data.characters
          console.log(this.table_data)
          this.search_query.total = res.data.total
          if (this.character_name_search !== ''){
            this.table_data.forEach((item, index) => {
              item['score'] = res.data.scores[index]
            })
          }
        }
      })
    },
    openDel(row){
      this.delId = row.cid
      this.delDialogVisible = true
    },
    delete_user(){
      let params = [
        this.delId
      ]
      console.log("zzz")
      console.log(params)
      character_delete(params).then(res => {
        if (res.status === 200){
          console.log(res)
          console.log("删除！")
          this.$message.success("删除角色成功！")
          this.get_character()
        }

      })
    },
    openEdit(row){
      this.editDialogVisible = true
      this.editForm.selectedCategory = row.category
      this.editForm.bot_name = row.name
      this.editForm.avatarUrl = row.avatar_url
      this.editForm.id = row.cid
      this.editForm.description = row.description
      console.log(row.avatar_description)
      this.editForm.avatar_description = row.avatar_description
      this.editForm.key = new Date().getTime()
    },
    getAvatarUrl(url, avatarDescription){
      this.editForm.avatarUrl = url
      this.editForm.avatar_description = avatarDescription
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
    tableRowClassName({ row, rowIndex }) {
      if (row['score'] < 50){
        console.log('irrelevance')
        return 'warning-row'
      }
      else {
        return ''
      }
    },
    handleClose(done) {
      this.$confirm('确认关闭？')
        .then(_ => {
          done();
        })
        .catch(_ => {});
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
        this.get_character()
      })
    },
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
