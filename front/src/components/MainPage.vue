<template>
  <div>

    <el-card>
      <el-row>
        <el-input
          v-model="character_name"
          style="padding-left: 20px;padding-right: 20px; padding-top: 20px;width: 50%;"
          placeholder="请输入角色名"
          clearable>
          <el-button slot="append" icon="el-icon-search"></el-button>
        </el-input>
        <el-menu style="padding-top: 20px">
          <el-col :span="6" v-for="(item, index) in character_list" style="">
            <el-menu-item style="width: 100%; height: 100%" @click="selectRole(item)">
              <div>
                <el-image :src="item.img_url" style="width: 100%; height: 100%">

                </el-image>
                <p>{{item.label}}</p>
              </div>
            </el-menu-item>

          </el-col>
        </el-menu>


      </el-row>
    </el-card>


  </div>
</template>

<script>
export default {
  name: 'MainPage',
  data() {
    return {
      character_list : [
        {
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
        },{
          id: 5,
          img_url: 'https://aitopia-1302942961.cos.ap-beijing.myqcloud.com/lingyou/1688809087917a4bed63a-5757-48d5-b6a9-1b6d4c81be00.png?imageView2/1/w/300/h/300',
          label: 'test5',
          description: 'test5'
        },{
          id: 6,
          img_url: 'https://aitopia-1302942961.cos.ap-beijing.myqcloud.com/lingyou/1688809087917a4bed63a-5757-48d5-b6a9-1b6d4c81be00.png?imageView2/1/w/300/h/300',
          label: 'test6',
          description: 'test6'
        },{
          id: 7,
          img_url: 'https://aitopia-1302942961.cos.ap-beijing.myqcloud.com/lingyou/1688809087917a4bed63a-5757-48d5-b6a9-1b6d4c81be00.png?imageView2/1/w/300/h/300',
          label: 'test7',
          description: 'test7'
        },
      ],
      character_name: ''
    }
  },
  methods: {
    selectRole(roleMess){
      console.log(roleMess)
      localStorage.setItem('roleMess_label', roleMess.label)
      localStorage.setItem('roleMess_img_url', roleMess.img_url)
      localStorage.setItem('roleMess_id', roleMess.id)
      localStorage.setItem('roleMess_description', roleMess.description)
      this.$router.push('/dialogue')
    }
  }
};
</script>

<style scoped>
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
</style>
