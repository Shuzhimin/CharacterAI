<template>
  <div style="height: 100%; background-color: #242949">
    <el-card style="background-color: #212529; border: 0">
      <el-row>
        <el-input
          v-model="character_name"
          style="padding-left: 20px;padding-right: 20px; padding-top: 20px;width: 50%;"
          placeholder="请输入角色名"
          clearable>
          <el-button slot="append" icon="el-icon-search"></el-button>
        </el-input>
        <div v-for="(type, i) in character_type" v-if="character_list[i].length !== 0" style="padding-top: 20px; background-color: transparent">
          <div>
            <i class="el-icon-s-opportunity" style="font-weight: 50;font-size: 30px; color: white"></i>
            <span style="font-size: 30px; color: white">{{type}}</span>
          </div>

          <el-menu style="padding-top: 20px; background-color: transparent">
            <el-col :span="3" v-for="(item, index) in character_list[i]" style="background-color: transparent;">
              <el-menu-item style="width: 100%; height: 100%; background-color: transparent" @click="selectRole(item)">
                <div>
                  <el-image :src="item.img_url" style="width: 100%; height: 100%">

                  </el-image>
                  <p class="clabel" style="color: white">{{item.label}}</p>
                </div>
              </el-menu-item>

            </el-col>
          </el-menu>
        </div>



      </el-row>
    </el-card>
<!--    <div class="color"></div>-->
<!--    <div class="color"></div>-->
<!--    <div class="color"></div>-->
<!--    <div class="box">-->
<!--      <div class="square" style="&#45;&#45;i:0;"></div>-->
<!--      <div class="square" style="&#45;&#45;i:1;"></div>-->
<!--      <div class="square" style="&#45;&#45;i:2;"></div>-->
<!--      <div class="square" style="&#45;&#45;i:3;"></div>-->
<!--      <div class="square" style="&#45;&#45;i:4;"></div>-->
<!--    </div>-->

  </div>
</template>

<script>
import { character_select } from '@/api/character';
export default {
  name: 'MainPage',
  data() {
    return {
      character_list : [
        // 美食
        [{
          id: 1,
          img_url: 'https://aitopia-1302942961.cos.ap-beijing.myqcloud.com/lingyou/1688809087917a4bed63a-5757-48d5-b6a9-1b6d4c81be00.png?imageView2/1/w/300/h/300',
          label: 'test1',
          description: 'test1'
        },{
          id: 2,
          img_url: 'https://aitopia-1302942961.cos.ap-beijing.myqcloud.com/lingyou/1688809087917a4bed63a-5757-48d5-b6a9-1b6d4c81be00.png?imageView2/1/w/300/h/300',
          label: 'test2',
          description: 'test2'
        },{
          id: 3,
          img_url: 'https://aitopia-1302942961.cos.ap-beijing.myqcloud.com/lingyou/1688809087917a4bed63a-5757-48d5-b6a9-1b6d4c81be00.png?imageView2/1/w/300/h/300',
          label: 'test3',
          description: 'test3'
        },{
          id: 4,
          img_url: 'https://aitopia-1302942961.cos.ap-beijing.myqcloud.com/lingyou/1688809087917a4bed63a-5757-48d5-b6a9-1b6d4c81be00.png?imageView2/1/w/300/h/300',
          label: 'test4',
          description: 'test4'
        },],
        // 旅游
        [{
          id: 5,
          img_url: 'https://aitopia-1302942961.cos.ap-beijing.myqcloud.com/lingyou/1688809087917a4bed63a-5757-48d5-b6a9-1b6d4c81be00.png?imageView2/1/w/300/h/300',
          label: 'test5',
          description: 'test5'
        },{
          id: 6,
          img_url: 'https://aitopia-1302942961.cos.ap-beijing.myqcloud.com/lingyou/1688809087917a4bed63a-5757-48d5-b6a9-1b6d4c81be00.png?imageView2/1/w/300/h/300',
          label: 'test6',
          description: 'test6'
        },],
        // 科技
        [],
        // 健康
        [{
          id: 7,
          img_url: 'https://aitopia-1302942961.cos.ap-beijing.myqcloud.com/lingyou/1688809087917a4bed63a-5757-48d5-b6a9-1b6d4c81be00.png?imageView2/1/w/300/h/300',
          label: 'test7',
          description: 'test7'
        },],
        // 法律
        [{
          id: 8,
          img_url: 'https://aitopia-1302942961.cos.ap-beijing.myqcloud.com/lingyou/1688809087917a4bed63a-5757-48d5-b6a9-1b6d4c81be00.png?imageView2/1/w/300/h/300',
          label: 'test8',
          description: 'test8'
        },{
          id: 9,
          img_url: 'https://aitopia-1302942961.cos.ap-beijing.myqcloud.com/lingyou/1688809087917a4bed63a-5757-48d5-b6a9-1b6d4c81be00.png?imageView2/1/w/300/h/300',
          label: 'test9',
          description: 'test9'
        },],
        // 其他
        [],

      ],
      character_name: '',
      character_type: [
        '美食',
        '旅游',
        '科技',
        '健康',
        '法律',
        '其他'
      ]
    }
  },
  created() {
    this.getCharacter()
  },
  methods: {
    selectRole(roleMess){
      console.log(roleMess)
      localStorage.setItem('roleMess_label', roleMess.label)
      localStorage.setItem('roleMess_img_url', roleMess.img_url)
      localStorage.setItem('roleMess_id', roleMess.id)
      localStorage.setItem('roleMess_description', roleMess.description)
      this.$router.push('/dialogue')
    },
    getCharacter(){
      let params = {
        "skip": 1,
        "limit": 20
      }
      character_select(params).then(res => {
        if (res.status === 200){
          console.log(res)
        }
      })
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
</style>
