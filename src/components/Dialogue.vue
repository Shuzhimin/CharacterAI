<template>
  <div style="height: 100%">
    <el-card style="height: 100%; min-height: 100%">
      <el-container style="height: 100%">
        <el-header>Header</el-header>
        <el-main>
          <div v-for="(item, index) in history_message" class="msgCss" :style="{textAlign: item.align}">
            <el-row style="padding-top: 20px">
              <div v-if="item.owner === 'bot'" class="block">
                <el-avatar :size="50" :src="item.avatar_url"></el-avatar>
                <span class="content">{{item.content}}</span>
              </div>
              <div v-if="item.owner === 'user'" class="block" style="float: right">
                <span class="content">{{item.content}}</span>
                <el-avatar :size="50" :src="item.avatar_url"></el-avatar>
              </div>
            </el-row>

          </div>
        </el-main>
        <el-footer>
          <el-input
            v-model="input_message"
            style=""
            placeholder="请输入"
            clearable>
            <el-button slot="append" icon="el-icon-s-promotion button-icon" ></el-button>
          </el-input>
        </el-footer>
      </el-container>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'Dialogue',
  data() {
    return{
      input_message: '',
      history_message: [
        {
          content: '我是你的专属AI角色，请跟我聊天吧！',
          owner: 'bot',
          avatar_url: 'https://lingyou-1302942961.cos.ap-beijing.myqcloud.com/lingyou/16790385261248df6fb83-63b0-4497-826e-b5f2cfbe97a3.jpg',
        },{
          content: '你好，很高兴认识你，你能告诉我中国有哪些有名的小吃吗？',
          owner: 'user',
          avatar_url: '',
        },{
          content: '中国的小吃有很多，例如胡辣汤、油条、粽子等。',
          owner: 'bot',
          avatar_url: 'https://lingyou-1302942961.cos.ap-beijing.myqcloud.com/lingyou/16790385261248df6fb83-63b0-4497-826e-b5f2cfbe97a3.jpg',
        },
      ]
    }
  }
};
</script>

<style scoped>
.el-header {
  background-color: #242949;
  height: 10%;
  border-radius: 10px;
}
.el-main {
  height: 70%;
  background-color: #212529;
  border-radius: 10px;
}
.el-footer {
  height: 20%;
  background-color: #212529;
  display: flex;
  justify-content: center; /* 水平居中 */
  align-items: center;     /* 垂直居中 */
  border-radius: 95px;
}
.el-card {
  background-color: #212529;
}
/*搜索组件最外层div */
.el-input {
  background-color: #242949;
  width: 100%;
  height: 100%;
  margin-right: 15px;
  border-radius: 95px;
  display: flex;
  justify-content: center; /* 水平居中 */
  align-items: center;     /* 垂直居中 */
  color: white;
}
/*搜索input框 */
:deep(.el-input__inner) {
  background-color: transparent;
  border-radius: 95px;
  /*-moz-border-radius-topright: 95px;*/
  border: 0;
  box-shadow: 0 0 0 0px;
  color: white;
}
/*搜索button按钮 */
:deep(.el-input-group__append) {
  width: 60px;
  background-color: transparent;
  border-radius: 95px;
  border: 0;
  box-shadow: 0 0 0 0px;
  font-size: 50px;
  float: right;
}
.msgCss {
  font-size: 16px;
  font-weight: 500;
}
.block {
  display: flex;
  align-items: center;     /* 垂直居中 */
}
.content {
  color: white;
  padding-left: 20px;
  padding-right: 20px;
}
:deep(.el-card__body) {
  height: 100%;
}
</style>
