export function simulateCreateCharacter(createForm) {
  // 模拟处理数据并返回响应
  const responseData1 = {
    success: true,
    message: '角色创建成功',
    data: {
      // 可以根据需要添加模拟的返回数据
      characterId: '1',
      createForm,
    }
  };
  return responseData1;
}

export function simulateAvatar(createForm) {
  // 模拟处理数据并返回响应
  const responseData2 = {
    success: true,
    message: '头像生成成功',
    data: {
      AvatarUrl: 'https://aitopia-1302942961.cos.ap-beijing.myqcloud.com/lingyou/1688809087917a4bed63a-5757-48d5-b6a9-1b6d4c81be00.png?imageView2/1/w/300/h/300',
    }
  };
  return responseData2;
}
