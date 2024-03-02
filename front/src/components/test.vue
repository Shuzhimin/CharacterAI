<template>
  <div class="container">
    <el-row>
      <el-scrollbar wrap-class="horizontal-scroll" :native="false">
        <!-- 这里放置需要横向排列的内容 -->
        <div v-for="item in items" :key="item.id" class="content">{{ item }}</div>
      </el-scrollbar>
    </el-row>

  </div>
</template>

<script>
export default {
  name: 'test',
  data() {
    return {
      items: [
        'Item 1',
        'Item 2',
        'Item 3',
        'Item 3',
        'Item 3',
        'Item 3',
        'Item 3',
        'Item 3',
        'Item 3',
        'Item 3',
        'Item 3',
        'Item 3',
        'Item 3',
        'Item 3',
        'Item 3',
        'Item 3',
        'Item 3',
      ] // 数据源
    }
  },
};
</script>

<style scoped>
.container {
  width: 500px; /* 设定容器宽度 */
  overflow-x: auto; /* 开启水平溢出自动显示滚动条 */
  display: flex;
}

.horizontal-scroll::v-deep .el-scrollbar__wrap {
  display: flex; /* 将子元素横向排列 */
}

.content {
  margin-right: 50px; /* 调整每个内容之间的间距 */
  display: flex;
}
.el-scrollbar .el-scrollbar__wrap .el-scrollbar__view{
  white-space: nowrap;
}
</style>
