module.exports = {
    devServer: {
        proxy: 'http://127.0.0.1:8000',
        port: 9090,
        disableHostCheck: true,
    },
    publicPath: './',
    chainWebpack: config => {
        // 修复HMR
        config.resolve.symlinks(true)
    },
}
