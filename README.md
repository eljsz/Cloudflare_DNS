# Cloudflare_DNS 抓取网站优选ip,并且自动更改cf的dns

启动的时候需要关闭代理

配置文件注释:
{
"auth_email": "", // 你的CloudFlare注册账户邮箱
"auth_key": "", // 你的CloudFlare账户key，位置在域名概述页面点击右下角获取api key。
"zone_name": "", // 修改为你的主域名
"record_name": "cf", // 自动更新的二级域名前缀，例如cloudflare的cdn用cf，gcore的cdn用gcore，后面是数字，程序会自动添加。
"set_url_config": 1, // 需要爬取的网站 1: https://stock.hostmonit.com/CloudFlareYes   2: http://cdn.fastwork.cc/cf/
"record_count": 3, // 二级域名个数，例如配置5个，则域名分别是cf1、cf2、cf3、cf4、cf5。后面的信息均不需要修改，让它自动运行就好了。
"record_type": "A" // DNS记录类型
}

电报 https://t.me/+vTwBHA9RbtMwYzA9
