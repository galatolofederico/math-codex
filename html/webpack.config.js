const glob = require("glob");
const HtmlWebpackPlugin = require("html-webpack-plugin")
const CopyWebpackPlugin = require("copy-webpack-plugin");
const LoadingScreenPlugin = require('loading-screen')

module.exports = {
  entry: glob.sync("./src/js/*.js"),
  mode: "development",
  output: {
    path: __dirname + "/dist",
    filename: "bundle.js"
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: "src/index.html"
    }),
    new CopyWebpackPlugin({
      patterns: [
          { from: "assets", to: "assets" }
      ]
  }),
    new LoadingScreenPlugin()
  ],
  devtool: 'inline-source-map',
  devServer: {
    static: './dist',
    hot: true,
    allowedHosts: ['.ngrok.io']
  },
  module: {
    rules: [
      {
        test: /\.(scss)$/,
        use: [
          {
            loader: 'style-loader'
          },
          {
            loader: 'css-loader'
          },
          {
            loader: 'postcss-loader',
            options: {
              postcssOptions:{
                plugins: function () {
                  return [
                    require('autoprefixer')
                  ];
                }
              }
            }
          },
          {
            loader: 'sass-loader'
          }
        ]
      }
    ]
  }
}