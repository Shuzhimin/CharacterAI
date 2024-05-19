const { defineConfig } = require('@vue/cli-service')
// module.exports = defineConfig({
//   transpileDependencies: true
// })

module.exports = {
  transpileDependencies: [],
  devServer: {
    host: "0.0.0.0",
    port: 8900,
    open: true,
  }
}
