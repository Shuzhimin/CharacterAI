<template>
  <div>
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{path: '/userhome'}" style="color: white">首页</el-breadcrumb-item>
      <el-breadcrumb-item style="color: white">系统管理</el-breadcrumb-item>
      <el-breadcrumb-item style="color: white">账号管理</el-breadcrumb-item>
    </el-breadcrumb>
    <el-card style="margin-top: 15px">
      <el-row :gutter="20" style="padding-bottom: 20px">
        <el-col :span="7">
          <!--  搜索区  -->
          <el-input placeholder="请输入用户名" v-model="username_search" clearable>
            <!--            <el-button slot="append" icon="el-icon-search" @click="getBookList()"></el-button>-->
          </el-input>

        </el-col>

        <el-col :span="2">
          <el-button type="primary" icon="el-icon-search" @click="searchUser">搜索</el-button>
        </el-col>

        <el-col :span="2">
          <el-button type="primary" icon="el-icon-search" @click="addAccount">新增用户</el-button>
        </el-col>

      </el-row>

      <el-table :data="table_data" border fit stripe>
        <el-table-column label="账号ID" prop="uid" align="center"></el-table-column>
        <el-table-column label="账号名" prop="name" align="center"></el-table-column>
        <el-table-column label="账户角色" prop="role" align="center"></el-table-column>
        <el-table-column label="头像描述" prop="avatar_description" align="center"></el-table-column>
        <el-table-column label="头像链接" prop="avatar_url" align="center">
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
        <el-table-column label="操作"  align="center">
          <template slot-scope="scope">
            <el-button size="medium" circle>编辑</el-button>
            <el-button size="medium" @click="delete_user(scope.row)" circle>删除</el-button>
            <el-button size="medium" circle>角色管理</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
        style="padding-top: 20px"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="search_query.pagenum"
        :page-sizes="[1, 2, 5, 10]"
        :page-size="search_query.pagesize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="receive.total">
      </el-pagination>
    </el-card>
    <AddAccountDialog v-if="addAccountDialogVisible" @closeDialog="closeAddAccountDialog" :DialogShowFlag="addAccountDialogVisible"></AddAccountDialog>
  </div>
</template>

<script>
import AddAccountDialog from '@/components/dialog/AddAccountDialog';
import { user_all, user_delete } from '@/api/user';
export default {
  name: 'AccountManagement',
  components: { AddAccountDialog },
  data() {
    return {
      username_search: '',
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
      addAccountDialogVisible: false
    }
  },
  created() {
    this.get_user_all()
  },
  methods: {
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
    },
    // 监听 页码值 改变的时间
    handleCurrentChange (newPage) {
      console.log(newPage)
      this.search_query.pagenum = newPage
    },
    get_user_all(){
      user_all().then(res => {
        if (res.status === 200){
          console.log(res)
          this.table_data = res.data
        }
      })
    },
    delete_user(row){
      let params = [
        row.uid
      ]
      user_delete(params).then(res => {
        this.$message.success("删除成功！")
        this.get_user_all()
      })
    }
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
