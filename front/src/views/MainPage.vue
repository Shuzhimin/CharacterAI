<template>
  <el-input
      v-model="character_name"
      style=";padding-right: 20px; padding-top: 10px;width: 50%"
      placeholder="请输入智能体名"
      clearable
      @input="getCharacter">
    <template #append>
      <el-button slot="append" @click="getCharacter">
        <el-icon><Search /></el-icon>
      </el-button>
    </template>

  </el-input>
  <draggable :character_type="character_type" :character_list="character_list"></draggable>
  <el-scrollbar >
    <div style="height: 100%; background-color: white;margin-top: 20px">
      <el-card style="background-color: #f6f7f9; border: 0;height: 100%">
        <!--                <el-button type="primary" class="fixed-button" @click="scrollTo()" circle size="large">回到顶部</el-button>-->
        <!--                <el-card class="box-card fixed-button" style="width: 150px">-->
        <!--                    <template #header>-->
        <!--                        <div class="card-header">-->
        <!--                            <span>跳转导航</span>-->
        <!--                        </div>-->
        <!--                    </template>-->
        <!--                    <div v-for="(type, i) in character_type" :key="i" class="text item">-->
        <!--                        <a v-if="character_list[i].length !== 0" :href="'#'+i">{{ type }}<br></a>-->

        <!--                    </div>-->
        <!--                </el-card>-->

        <!--      <el-row>-->

        <div v-if="character_num === 0" style="display: flex;flex-direction: column;justify-content: center;align-items: center;margin-top: 10%">
          <span style="color: black;font-size: large" @click="$router.push('/createrole')">快去创建你的第一个智能体吧！点击即可跳转！</span>
        </div>
        <template v-for="(type, i) in character_type">
          <el-row :id="i">
            <div v-if="character_list[i].length !== 0" style="padding-top: 20px; background-color: transparent;width: 100%">
              <div>
                <!--            <i class="el-icon-s-opportunity" style="font-weight: 50;font-size: 30px; color: white"></i>-->
                <el-icon size="30px" color="#409efc"><Opportunity /></el-icon>
                <span style="font-size: 30px; color: black">{{type}}</span>
              </div>

              <div class="zs-adv">
                <a title="上一页" :href="'#'" class="adv-pre" @click="scroll(i, 'left')" style="width: 5%">
                  <el-icon style="font-size: 30px;"><ArrowLeft /></el-icon>
                  <!--                          <el-icon><ArrowLeftBold /></el-icon>-->
                </a>
                <div id="adv-pad-scroll" :class="`category-${i}`" style="width: 80%; height: 250px">
                  <div class="adv-pad" >
                    <!--                            <div style="width: 100%; height: 100%; background-color: transparent; " v-for="(item) in character_list[i]" @click="selectRole(item)">-->
                    <!--                            <img-->
                    <!--                                v-for="(item, itemIndex) in character_list[i]"-->
                    <!--                                :key="`${i}-${itemIndex}`"-->
                    <!--                                class="adv-pad-item"-->
                    <!--                                :src="item.src"-->
                    <!--                                :alt="item.alt || ''"-->
                    <!--                                @click="selectRole(item)"-->
                    <!--                            />-->
                    <div
                        v-for="(item, itemIndex) in character_list[i]"
                        :key="`${i}-${itemIndex}`"
                        class="image-container"
                        @click="selectRole(item)"
                    >
                      <el-image class="avatar-item adv-pad-item" :src="item.img_url" style="width: 200px; height: 200px;border-radius: 0%"></el-image>
                      <!--                              <img-->
                      <!--                                  class="adv-pad-item"-->
                      <!--                                  :src="item.src"-->
                      <!--                                  :alt="item.alt || ''"-->
                      <!--                              />-->
                      <div class="image-label">{{ item.name || '图片名称' }}</div>
                    </div>
                    <!--                            <p class="adv-pad-item" style="color: black">{{item.name}}</p>-->
                    <!--                          </div>-->
                  </div>
                </div>
                <a title="下一页" :href="'#'" class="adv-next" @click="scroll(i, 'right')" style="width: 5%">
                  <el-icon style="font-size: 30px;"><ArrowRight /></el-icon>
                </a>
              </div>

            </div>
          </el-row>

        </template>




        <!--      </el-row>-->
      </el-card>

    </div>
  </el-scrollbar>

</template>

<script>
import { character_select } from '@/api/character';
import {
  Check,
  Delete,
  Edit,
  Message,
  Search,
  Star,
  Plus,
  Opportunity,
  ArrowRight,
  ArrowLeft,
  ArrowLeftBold,

} from '@element-plus/icons-vue'
import Draggable from '@/components/Draggable';
export default {
  name: 'MainPage',
  components: { Draggable },
  data() {
    return {
      maxClickNum: 0, // 最大点击次数
      lastLeft: 0, // 上次滑动距离
      clickNum: 0, // 点击次数
      scrollStates: {}, // 用来记录每个分类的滚动状态
      character_list : [
        // 美食
        [],
        // 旅游
        [
          // {
          // id: 5,
          // img_url: 'https://aitopia-1302942961.cos.ap-beijing.myqcloud.com/lingyou/1688809087917a4bed63a-5757-48d5-b6a9-1b6d4c81be00.png?imageView2/1/w/300/h/300',
          // label: 'test5',
          // description: 'test5'
          // },{
          //   id: 6,
          //   img_url: 'https://aitopia-1302942961.cos.ap-beijing.myqcloud.com/lingyou/1688809087917a4bed63a-5757-48d5-b6a9-1b6d4c81be00.png?imageView2/1/w/300/h/300',
          //   label: 'test6',
          //   description: 'test6'
          // },
        ],
        // 科技
        [],
        // 健康
        [],
        // 法律
        [],
        // 文档分析
        [],
        // 智能报表
        [],
        // 其他
        [],

      ],
      character_num: 0,
      character_name: '',
      character_type: [
        '美食',
        '旅游',
        '科技',
        '健康',
        '法律',
        '文档分析',
        '智能报表',
        '其他'
      ],
      character_code: {
        'food': 0,
        'travel': 1,
        'tech': 2,
        'health': 3,
        'law': 4,
        'doc_rag': 5,
        'reporter': 6,
        'other': 7
      },
    }
  },
  created() {
    this.$emit('updateParentValue', '/mainpage')
    this.getCharacter()
  },
  methods: {
    scroll(categoryIndex, direction) {
      if (!this.scrollStates[categoryIndex]) {
        this.scrollStates[categoryIndex] = { lastLeft: 0, clickNum: 0 };
      }

      const itemsInCategory = this.character_list[categoryIndex];
      const currentItem = document.querySelector(`.category-${categoryIndex} .adv-pad`);
      const itemWidth = currentItem.children[0].offsetWidth;

      if (direction === 'left' && this.scrollStates[categoryIndex].clickNum > 0) {
        currentItem.style.marginLeft = `${this.scrollStates[categoryIndex].lastLeft + itemWidth}px`;
        this.scrollStates[categoryIndex].lastLeft += itemWidth;
        this.scrollStates[categoryIndex].clickNum--;
      } else if (direction === 'right' && this.scrollStates[categoryIndex].clickNum < itemsInCategory.length - 1) {
        currentItem.style.marginLeft = `${-itemWidth + this.scrollStates[categoryIndex].lastLeft}px`;
        this.scrollStates[categoryIndex].lastLeft -= itemWidth;
        this.scrollStates[categoryIndex].clickNum++;
      }
    },
    scrollTo(){
      window.location.href = '#5'
    },

    selectRole(roleMess){
      console.log(roleMess)
      localStorage.setItem('roleCategory', roleMess.category)
      localStorage.setItem('roleMess_name', roleMess.name)
      localStorage.setItem('roleMess_avatar_url', roleMess.img_url)
      localStorage.setItem('roleMess_id', roleMess.cid)
      localStorage.setItem('roleMess_description', roleMess.description)
      localStorage.setItem('roleMess_avatar_description', roleMess.avatar_description)
      this.$router.push('/dialogue')
    },
    getCharacter(){
      // this.character_list.forEach((item, index) => {


      let params = {
        // "cid": window.localStorage.getItem('uid'),
        // "category": this.character_code[0],
        "query": this.character_name
      }
      console.log(this.character_list)
      character_select(params).then(res => {

        if (res.status === 200){
          // for (var i=0;i<this.character_list.length;i++){
          //   this.character_list[i] = []
          // }
          let cl = [
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            []
          ]
          this.character_num = res.data.total
          for (var i=0;i<res.data.characters.length;i++){
            let d = {
              cid: res.data.characters[i].cid,
              img_url: res.data.characters[i].avatar_url,
              name: res.data.characters[i].name,
              description: res.data.characters[i].description,
              avatar_description: res.data.characters[i].avatar_description,
              category: res.data.characters[i].category
            }
            if (d.img_url === ""){
              d.img_url = "https://aitopia-1302942961.cos.ap-beijing.myqcloud.com/lingyou/1688809087917a4bed63a-5757-48d5-b6a9-1b6d4c81be00.png?imageView2/1/w/300/h/300"
            }
            if (this.character_code[d.category] === undefined){
              // if (d.category === ""){
              d.category = "other"
            }
            cl[this.character_code[d.category]].push(d)

            // this.character_list[5].push(d)
          }
          this.character_list = cl
          console.log('zzz')
          console.log(this.character_list)

        }
      })
      // })

    }
  }
};
</script>

<style scoped lang="less">
/*搜索组件最外层div */
.input_box {
  width: 300px;
  margin-right: 15px;
  border-radius: 95px
}
/*搜索input框 */
:deep(.el-input__inner) {
  /*background-color: transparent;!*覆盖原背景颜色，设置成透明 *!*/
  border-radius: 95px;
  /*-moz-border-radius-topright: 95px;*/
  /*border: 0;*/
  box-shadow: 0 0 0 0px;
}
/*搜索button按钮 */
:deep(.el-input-group__append) {
  border-radius: 95px;
  border: 0;
  box-shadow: 0 0 0 0px;
}
.el-menu-item:hover{
  /*border-left:#33A2EF solid 6px !important;*/
  background-color: #666e74 !important;
  color: #38B2FF !important;
}
.avatar-item:hover{
  transform: scale(1.2);
  transition: all 0.3s ease-in-out;
}

.fixed-button {
  position: fixed;
  top: 200px;
  right: 100px;
  z-index: 1000; /* 确保按钮位于其他内容之上 */
}

.zs-adv {
  margin: 50px auto 0;
  width: 100%;
  //width: 1272px;
  height: 120px;
  a {
    margin-top: 58px;
    width: 16px;
    height: 24px;
    opacity: 0.8;
  }
  a:hover {
    opacity: 1;
  }
  .adv-pre {
    float: left;
    margin-right: 20px;
  }
  .adv-next {
    float: right;
    //margin-right: 20px;

  }
  #adv-pad-scroll {
    float: left;
    //width: 1200px;
    width: 95%;
    overflow: hidden;
    .adv-pad {
      width: 2400px;
      height: 280px;
      .image-container {
        position: relative; /* 为容器设置相对定位，以便子元素可以绝对定位 */
        display: inline-block; /* 保证图片容器与其他元素适当地排列 */
      }
      .adv-pad-item {
        padding: 20px 10px 0px 10px;
        width: 200px;
        height: 200px;
        cursor: pointer;
        animation: all 1.5s;
      }
      .image-label {
        text-align: center;
        //position: absolute;
        //bottom: 0;
        //left: 0;
        //background-color: rgba(0, 0, 0, 0.5);
        //color: white;
        ////padding: 3px 5px;
        ////margin: 0 5px 5px 0; /* 外边距，防止遮挡图片内容，可调整 */
        ////font-size: 12px;
        ////white-space: nowrap; /* 确保文本不换行 */
        ////overflow: hidden; /* 隐藏超出部分，可选 */
        ////text-overflow: ellipsis; /* 超出部分显示省略号，需与上面的overflow配合使用 */
        //padding: 3px 5px;
        //margin: 0; /* 移除外边距，避免影响背景色的宽度 */
        //font-size: 12px;
        //white-space: nowrap;
        //overflow: hidden;
        //text-overflow: ellipsis;
        //display: flex; /* 使用flex布局 */
        //align-items: center; /* 垂直居中文本 */
      }

      .adv-pad-item:hover {
        padding: 10px 5px 0px 10px;
      }
    }
  }
}
</style>
