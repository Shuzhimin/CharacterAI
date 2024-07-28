<template>
  <el-card class="box-card draggable" style="width: 120px; border-radius: 10%"
           :style="{ top: posY + 'px', left: posX + 'px' }"
           @mousedown="startDragging"
           @mousemove="dragging"
           @mouseup="stopDragging">
    <template #header>
      <div class="card-header">
        <span>跳转导航</span>
      </div>
    </template>
    <div v-for="(type, i) in character_type" :key="i" class="text item">
      <a v-if="character_list[i].length !== 0" :href="'#'+i" style="">{{ type }}<br></a>

    </div>
  </el-card>
  <!--    <div-->
  <!--        class="draggable"-->
  <!--        :style="{ top: posY + 'px', left: posX + 'px' }"-->
  <!--        @mousedown="startDragging"-->
  <!--        @mousemove="dragging"-->
  <!--        @mouseup="stopDragging"-->
  <!--    >-->
  <!--        Drag me!-->
  <!--    </div>-->
</template>

<script>
export default {
  name: 'Draggable',
  props: ["character_type", "character_list"],
  data() {
    return {
      draggingFlag: false,  // 是否正在拖拽
      offsetX: 0,  // 鼠标按下时距离元素左上角的偏移
      offsetY: 0,  // 鼠标按下时距禋元素左上角的偏移
      posX: 100,  // 元素左上角相对于父元素的位置
      posY: 200   // 元素左上角相对于父元素的位置
    };
  },
  created() {
    this.posX = window.innerWidth - 250
  },
  methods: {
    startDragging(e) {
      this.draggingFlag = true;
      this.offsetX = e.clientX - this.posX;
      this.offsetY = e.clientY - this.posY;
      console.log("按下")
    },
    dragging(e) {
      if (this.draggingFlag) {
        let posX = e.clientX - this.offsetX;
        let posY = e.clientY - this.offsetY;

        if (posX > 0 && posY > 0) {
          this.posX = posX;
          this.posY = posY;
        }
      }
    },
    stopDragging() {
      this.draggingFlag = false;
    }
  }
};
</script>

<style scoped>
.draggable {
  position: absolute;
  cursor: move;
  border: 1px solid  #f6f7f9;
  padding: 10px;
  background-color:  #f6f7f9;
  transition: transform 0.3s;
  opacity: 0.7;
  z-index: 5000;
}

.draggable.dragging {
  transform: scale(1.1);
}
.fixed-button {
  position: fixed;
  top: 200px;
  right: 100px;
  z-index: 1000; /* 确保按钮位于其他内容之上 */
}
</style>
