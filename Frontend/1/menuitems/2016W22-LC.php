<?php  
header("content-type:text/html; charset=utf-8");
//require_once('../utility.php');
//require_once('../SaeMysql.php');

	$mysql = new SaeMysql();
	$sql = "INSERT INTO `WM_Log` (`page`) VALUES('2016W21-LC')";
	$mysql->runSql($sql);
	$mysql->closeDb();		
?> 

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=10, user-scalable=yes">

    <title>外汇理财周报(2016.05.16-2016.05.22)</title>

    <meta name="description" content="Release by WorldMoney 2016.01.01">
    <meta name="author" content="WorldMoney">

    <link href="../bootstrap/css/bootstrap.min.css" rel="stylesheet">
    <!-- link href="../bootstrap/css/style.css" rel="stylesheet" -->
	<link rel="stylesheet" href="../bootstrap/weui-master/dist/style/weui.min.css"/>
	<link rel="stylesheet" href="../css/zhuanyangqian.css" />
	<link rel="stylesheet" href="../css/A5.css" />		
  </head>
  <body>

    <div class="container-fluid">
	<br>
	<div class="media">
		<div class="media-left">
			<a href="#">
				<img class="media-object" src="../img/A4-20160430-000.jpg" alt="..." height="64" width="64">
				</a>
		</div>
		<div class="media-body" style="vertical-align:middle;">
			<h4 class="media-heading"><strong>外汇理财周报</strong><br>(2016.05.16-2016.05.22)
			</h4>

		</div>
	</div>
	<br>	
		<div class ="col-xs-8" style="text-align:left;line-height:0.5;">
			<p class="blog-post-meta">2016-05-23  <a href="weixin://profile/gh_5a211fd0cbf2">赚洋钱</a></p>
		</div>
		<div class ="col-xs-4" style="text-align:right;line-height:0.5;">		
			<a style="text-align:right;" id="translateLink"></a>
		</div>
	
	<hr>	
	
	<article class="weui_article" style="margin-top:-25px;font-size:120%;">
		<blockquote style="font-family:arial;">
				<h4>国内美元理财产品一周收益分析
				</h4>	
		</blockquote>	
		<div  class="orange" style="border:2px solid #E6E6E6;">
				<p>本周市场利率方面并不平静。</p>
				<p>美联储在周三晚间公布了4月份会议纪要，大多数美联储成员认为美国当前的经济情况支持6月份加息。加息预期提前而至，美国10期国债收益率一周连续上升6.7个基点，报收于1.8430%。10年期国债收益率1个月上升8.9个基点，3个月上升9.5个基点。</p>
				<p>上周的G7会议上，各国财长及央行对于采取财政刺激的政策发生分歧。日本以及多数G7国家倾向于采取进一步的财政刺激计划，但德国对此表示强烈反对，原因在于德国目前具有良好的债务水平，并且经济的结构性调整到目前为止进展顺利。而日本并无像德国这样的转型计划，日本政府一方面有意逐步降低看似并不成功的量化政策，另一方面希望继续加大财政刺激。尽管分歧存在，但是比较明确的信号是：未来G7利率政策的向下空间已经关闭。</p>
				<p>英国10年期政府债收益率继续受益于上周央行维持利率不变的政策，一周上升7.5个基点，报收于1.454%。德国10年期政府债收益率一周上升4个基点，报收于0.168%。法国10年期政府债收益率一周上升3.2个基点，报收于0.509%。</p>
				<p>澳大利亚10年期政府债收益率一周微涨2.8个基点，报收于2.314%。</p>
				<p>日本10期政府债利率本周从最高收益率-0.065%跌至-0.113%。</p>
		</div>
		<br>
		
		<p>在刚结束的一周，国内各家银行总计发售31个美元理财产品，比上一周发行的数量再次加少。产品发售还是集中在6个月及1年期。短期产品发售频率再次下降。</p>
		<p>兴业银行的美元非保本理财产品在三个不同期限上（6个月、9个月与12个月）明显处于领先地位。尤其在6个月与12个月期限上，比同期限最低预期收益的银行高出将近100%！招商银行在1个月及3个月期限的美元理财产品上的收益比上周大幅提升。原因可能在于美联储6月加息的预期推高美元短期债券的收益率。</p>
		<p>在美联储加息预期强烈的背景下，投资者可适当规避长期限美元理财产品，预期不久后美元6个月以上理财产品的收益会上升。</p>
		<figure>
			<a class="imggroup" rel="imggallery" href="../img/weekly/20160523/2016W22-LC-001.JPG"><img alt="Image Preview" src="../img/weekly/20160523/2016W22-LC-001.JPG" width="100%" height="100%"></a>
		</figure>
		<font size="2" color="#6495ED">数据来源：“赚洋钱”外汇理财数据统计表，截止于2016/5/22</font><br>
		<br>		

		<figure>
			<a class="imggroup" rel="imggallery" href="../img/weekly/20160523/2016W22-LC-002.JPG"><img alt="Image Preview" src="../img/weekly/20160523/2016W22-LC-002.JPG" width="100%" height="100%"></a>
		</figure>	
		<font size="2" color="#6495ED">数据来源：“赚洋钱”外汇理财数据统计表，截止于2016/5/22</font><br>
		<br>		
		
		<blockquote style="font-family:arial;">
				<h4>海外基金投资排行榜
				</h4>	
		</blockquote>			
		<div  class="orange" style="border:2px solid #E6E6E6;">
				<p>从今年迄今的收益排行榜看，尽管贵金属价格本周受美联储6月加息预期的影响一度快速下滑，黄金价格一周收跌1.56%，但贵金属股票基金仍然一枝独秀。新兴市场股票基金在贵金属与商品能源的带动下，今年迄今收益表现突出。这代表着市场风险偏好仍然倾向于较高风险的资产。另一个让人瞩目的是，债券基金首次上今年迄今收益的排行榜。</p>
				<p>从本周收益排名看，在经历今年比较大幅度下跌后，生物科技行业股票基金升幅明显。欧洲股票基金在本周排行榜上录得多个席位。总体而言，本周基金市场表现平平。</p>
		</div>	
		<br>
		<p>分类股票基金排名：</p>
		<figure>
			<a class="imggroup" rel="imggallery" href="../img/weekly/20160523/2016W22-LC-003.JPG"><img alt="Image Preview" src="../img/weekly/20160523/2016W22-LC-003.JPG" width="100%" height="100%"></a>
		</figure>
		<font size="2" color="#6495ED">数据来源：MorningStar，截止于2016/5/20</font><br>		
		<br>
		<p>股票基金一周排名(美元累积)</p>	
		<figure>
			<a class="imggroup" rel="imggallery" href="../img/weekly/20160523/2016W22-LC-004.JPG"><img alt="Image Preview" src="../img/weekly/20160523/2016W22-LC-004.JPG" width="100%" height="100%"></a>
		</figure>
		<font size="2" color="#6495ED">数据来源：MorningStar，截止于2016/5/20</font><br>		
		<br>
		<p style="color:#FF6600;">相关阅读:<a href="http://zhuanyangqian.applinzi.com/menuitems/C31.html"><u>“如何识别外汇理财产品的收益与风险”</u></a>	</p>	
	</article>
	
	<hr>
	<div class="col-xs-12" style="text-align:center;">
		<img alt="Image Preview" src="../img/following.jpg" width="100%" height="100%"><br>
		<img alt="Image Preview" src="../img/qrcode.jpg" width="40%" height="40%">
	</div> 
</div>



    <!-- script src="../bootstrap/js/jquery.min.js"></script -->
    <script src="../bootstrap/js/bootstrap.min.js"></script>
    <!-- script src="../bootstrap/js/scripts.js"></script -->
	<script src="../bootstrap/js/chinese_convert.js"></script>
	<script>
		var defaultEncoding = 2; // 預設語言：1-繁體中文 | 2-简体中文
		var translateDelay = 0;
		var cookieDomain = "http://zhuanyangqian.applinzi.com";	// 修改爲你的部落格地址
		var msgToTraditionalChinese = "轉繁體";	// 簡轉繁時所顯示的文字
		var msgToSimplifiedChinese = "转简体"; 	// 繁转简时所显示的文字
		var translateButtonId = "translateLink";	// 「轉換」<A>鏈接標籤ID
		translateInitilization();
	</script>	
	<script src="../bootstrap/fancybox/jquery.fancybox.pack.js"></script>	
	<!-- script>
		$(document).ready(function() {
			$("a.imggroup").fancybox({
				'transitionIn'	:	'elastic',
				'transitionOut'	:	'elastic',
				'speedIn'		:	600, 
				'speedOut'		:	200, 
				'overlayShow'	:	false,
				'minWidth' 		:	100,
				'maxWidth' 		:	500,				
			});
		});
	</script -->	
  </body>
</html>