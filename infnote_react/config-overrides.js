/* eslint-env node */
/* eslint no-unused-vars: 'off'*/
const webpack = require('webpack')
// const UglifyEsPlugin = require('uglify-es-webpack-plugin')

module.exports = function override(config, env) {
    //do stuff with the webpack config...

    // https://github.com/facebook/create-react-app/pull/3776
    // 根据上面的提示修改配置，让 create-react-app 可以编译没有 precompile ES6 to ES5 的 modules
    // 注意这个会拖慢编译速度，而且开发模式本身也不需要配合这个编译
    if (env === 'production') {
        config.module.rules[1].oneOf.push({
            test: /\.js$/,
            loader: require.resolve('babel-loader'),
            options: {
                babelrc: false,
                compact: false,
                presets: [require.resolve('./dependencies')],
                cacheDirectory: true,
            },
        })
        config.plugins.forEach(function(item) {
            if (item instanceof webpack.optimize.UglifyJsPlugin) {
                item.options.mangle = false
                item.options.sourceMap = false
            }
        })

        // https://github.com/bitcoinjs/bitcoinjs-lib/issues/959
        // error: filename is not defined
        // config.plugins = config.plugins.map(function(item) {
        //     if (item instanceof webpack.optimize.UglifyJsPlugin) {
        //         return new UglifyEsPlugin({
        //             mangle: {
        //                 reserved: ['Buffer', 'BigInteger','Point', 'ECPubKey', 'ECKey', 'sha512_asm', 'asm', 'ECPair', 'HDNode']
        //             }
        //         })
        //     }
        //     return item
        // })
    }

    return config
}