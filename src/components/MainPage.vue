<template>
  <div>
    <el-row>
      <el-menu>
        <el-col :span="6" v-for="(item, index) in character_list" style="">
          <el-menu-item style="width: 100%; height: 100%">
            <div>
              <el-image :src="item.img_url" style="width: 100%; height: 100%">

              </el-image>
              <p>{{item.label}}</p>
            </div>
          </el-menu-item>

        </el-col>
      </el-menu>


    </el-row>

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
      ]
    }
  }
};
</script>

<style scoped>

</style>
