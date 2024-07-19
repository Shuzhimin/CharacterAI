<template>
  <div>
    <el-button text @click="dialogVisible = true">{{ bot_name }}</el-button>
    <el-dialog v-model="dialogVisible" :title="bot_name" width="70%" :before-close="handleClose">
      <div style="height: 500px; overflow-y: auto" id="bigBox">
        <div v-for="(item, index) in list" class="msgCss" :style="{textAlign: item.align}">
        <span v-if="item && item.align === 'left'">
<!--          <img-->
<!--            style="width: 50px;height: 50px;vertical-align: middle;border-radius: 50%;padding-right: 10px;"-->
<!--            src="../assets/human1.png"-->
<!--            alt=""-->
<!--          />-->
          <span v-if="item && item.link === ''">{{ item.text }}</span>
          <span v-if="item && item.link">: <a :href="item.link" target="_blank">{{ item.text }}</a></span>
        </span>
          <span v-if="item && item.align === 'right'">
          {{ item.text }}
          <img
            style="width: 50px;height: 50px;vertical-align: middle;border-radius: 50%;padding-right: 10px;padding-left: 10px;"
            src="https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fb-ssl.duitang.com%2Fuploads%2Fitem%2F201803%2F18%2F20180318004321_pwzom.thumb.700_0.jpg&refer=http%3A%2F%2Fb-ssl.duitang.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=auto?sec=1664679186&t=bcd6eae69e52a4d3f3c94aa54cd1b830"
            alt=""
          />
        </span>
        </div>
      </div>
      <div style="margin-top: 15px">
        <el-form-item :inline="true">
          <el-input placeholder="请输入内容" v-model="input_info" class="input-with-select" :autofocus="true"
                    ref="serachBox"
                    style="width: 50%">
          </el-input>
          <el-button :loading="loading" @keydown.enter.native="handleMsg" slot="append" type="primary" @click="handleMsg">
            发送
          </el-button>
        </el-form-item>
      </div>
    </el-dialog>
  </div>

</template>

<script>
import axios from 'axios'
import {ref} from 'vue'


export default {
  name: "HelloWorld",
  setup() {
    const dialogVisible = ref(false)
    return {
      dialogVisible
    }
  },
  data() {
    return {
      visible: false,
      input_info: "",
      list: [],
      loading: false,
      bot_name: "",
      chat_history_list: []
    }
  },
  created() {
    document.addEventListener("keydown", (e) => {
      let key = window.event.keyCode;
      if (key === 13 && !this.loading) {
        // 13是enter键的键盘码 如果等于13 就调用click的登录方法
        this.handleMsg();
      }
    });
  },
  mounted() {
    axios({
      method: "get",
      url: "/api/character_info?bot_name=刘雪峰",
    }).then(res => {
      this.bot_name = res.data.character_info['bot_name'];
    })
  },
  methods: {
    visible11() {
      this.visible = true;
      this.$nextTick(() => {
        this.$refs.serachBox.focus();
      });
    },
    async handleMsg() {
      console.log(this.input_info, "发送信息");
      if (this.input_info !== "") {
        this.loading = true;
        this.list.push({align: "right", text: this.input_info});
        await this.scrollTop11();
        this.getMsg();
        this.input_info = "";
      }
    },
    getMsg() {
      axios({
        method: "put",
        data: JSON.stringify(this.chat_history_list),
        params: {
          bot_name: this.bot_name,
          content: this.input_info,
        },
        url: '/api/chat',
        headers:{
          'content-type': "application/json"
        }
      }).then(async (response) => {
        console.log(response);
        if (response.status === 200) {
          const msg = response.data;
          let listMsg = {
            align: "left",
            text: msg.content,
            link: "",
          };
          this.list.push(listMsg);
          await this.scrollTop11();
          this.chat_history_list.push(...msg.chat_history)
        }
      })
        .catch(function (error) {
          console.log(error);
        });
      this.loading = false;
    },
    // 处理滚动条一直保持最上方
    scrollTop11() {
      let div = document.getElementById("bigBox");
      div.scrollTop = div.scrollHeight;
    },
  },
}
</script>

<style scoped>
.dialog-footer button:first-child {
  margin-right: 10px;
}

.msgCss {
  font-size: 16px;
  font-weight: 500;
}
</style>
