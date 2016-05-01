<?php
require_once(dirname(__FILE__).'/'.'jssdk.php'); 
$jssdk = new JSSDK("APPID", "APPSECRET");
$signPackage = $jssdk->GetSignPackage();
?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
     <link href="bootstrap/css/bootstrap.min.css" rel="stylesheet">
    <!-- link href="../bootstrap/css/style.css" rel="stylesheet" -->
	<link rel="stylesheet" href="bootstrap/weui-master/dist/style/weui.min.css"/>
	<link rel="stylesheet" href="css/zhuanyangqian.css" />
  <title>World Money JS testing</title>
</head>
<body>
    <div class="container-fluid">
	<article class="weui_article" style="margin-top:-25px">
		<p>This is Wechat JS SDK testing~</p>
			<h3 id="menu-device">设备信息接口</h3>
			<span class="desc">获取网络状态接口</span>
			<button class="btn btn_primary" id="getNetworkType">getNetworkType</button>  
			<br><br>
			<span class="desc">图片预览</span>
			<button class="btn btn_primary" id="previewImage">previewImage</button> 			
	</article>
	</div>
</body>
<script src="http://res.wx.qq.com/open/js/jweixin-1.0.0.js"></script>
<script>
  /*
   * 注意：
   * 1. 所有的JS接口只能在公众号绑定的域名下调用，公众号开发者需要先登录微信公众平台进入“公众号设置”的“功能设置”里填写“JS接口安全域名”。
   * 2. 如果发现在 Android 不能分享自定义内容，请到官网下载最新的包覆盖安装，Android 自定义分享接口需升级至 6.0.2.58 版本及以上。
   * 3. 常见问题及完整 JS-SDK 文档地址：http://mp.weixin.qq.com/wiki/7/aaa137b55fb2e0456bf8dd9148dd613f.html
   *
   * 开发中遇到问题详见文档“附录5-常见错误及解决办法”解决，如仍未能解决可通过以下渠道反馈：
   * 邮箱地址：weixin-open@qq.com
   * 邮件主题：【微信JS-SDK反馈】具体问题
   * 邮件内容说明：用简明的语言描述问题所在，并交代清楚遇到该问题的场景，可附上截屏图片，微信团队会尽快处理你的反馈。
   */
  wx.config({
    debug: false,
    appId: '<?php echo $signPackage["appId"];?>', 
    timestamp: <?php echo $signPackage["timestamp"];?>,
    nonceStr: '<?php echo $signPackage["nonceStr"];?>',
    signature: '<?php echo $signPackage["signature"];?>',
    jsApiList: [
      // 所有要调用的 API 都要加到这个列表中
	  'getNetworkType',
	  'previewImage'
    ]
  });
  wx.ready(function () {
    // 在这里调用 API
	
	document.querySelector('#getNetworkType').onclick = function () {
		wx.getNetworkType({
			success: function (res) {
				alert(res.networkType);
			},
			fail: function (res) {
				alert(JSON.stringify(res));
			}
		});
  }		
	document.querySelector('#previewImage').onclick = function () {		
		wx.previewImage({
			current: 'http://zhuanyangqian.applinzi.com/img/logo.jpg',
			urls: ['http://zhuanyangqian.applinzi.com/img/A10.jpg','http://zhuanyangqian.applinzi.com/img/A11.jpg','http://zhuanyangqian.applinzi.com/img/A12.jpg',]

		});
	};
  });
</script>
    <script src="bootstrap/js/bootstrap.min.js"></script>
</html>
