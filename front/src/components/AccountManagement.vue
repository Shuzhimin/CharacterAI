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
        <el-table-column label="账号ID" prop="id" align="center"></el-table-column>
        <el-table-column label="账号名" prop="username" align="center"></el-table-column>
        <el-table-column label="账户角色" prop="user_character" align="center"></el-table-column>
        <el-table-column label="账户状态" prop="active" align="center"></el-table-column>
        <el-table-column label="头像" prop="avatar" align="center">
          <template slot-scope="scope">
            <div>
              <el-image
                style="width: 100px; height: 100px"
                :src="scope.row.avatar"
                :preview-src-list="[scope.row.avatar]">
              </el-image>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="注册时间" prop="register_time" align="center"></el-table-column>
        <el-table-column label="更新时间" prop="update_time" align="center"></el-table-column>
        <el-table-column label="操作"  align="center">
          <template slot-scope="scope">
            <el-button size="medium" circle>编辑</el-button>
            <el-button size="medium" circle>删除</el-button>
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
export default {
  name: 'AccountManagement',
  components: { AddAccountDialog },
  data() {
    return {
      username_search: '',
      table_data: [
        {
          id: 1,
          username: 'admin',
          user_character: '管理员',
          active: '生效中',
          avatar: 'https://lingyou-1302942961.cos.ap-beijing.myqcloud.com/lingyou/16790385261248df6fb83-63b0-4497-826e-b5f2cfbe97a3.jpg',
          register_time: '2024-03-01 12:00',
          update_time: '2024-03-01 12:00'
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
