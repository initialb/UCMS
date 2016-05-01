<?php 
	require 'url.php';

	$titleimg ="A11.jpg";
	$timestamp = date("Y-m-d H:i:s",time());
//	$filename ="A11-DATA.php";
	$tmpname ="A11-temp.html";
	$urlname ="ZYQ-URL.php";
	$tcontent = "";
	$ReplyMsg = "";
	$MaxReturn = "";
	 
	$flag1 = true;
	$flag2 = true;
	$flag3 = true;
	$flag4 = true;
	
//	$data = json_decode(trim(substr(file_get_contents($filename),15)));	
	
//	$url = geturl($titleimg);
//	$url="http://139.196.16.157:5000/ucms/api/v1.0/weixin/selectedwmp/USD";
//	$curl = curl_init();
//    curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
//    curl_setopt($curl, CURLOPT_TIMEOUT, 500);
//	curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, true);
//    curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, true);
//    curl_setopt($curl, CURLOPT_URL, $url);
//    $res = curl_exec($curl);
//	sae_debug($data);
//    curl_close($curl);
//	$data = json_decode($res);
	
	$data = geturl($titleimg);		

	$currencyname = $data->currencyname;
	$MaxReturn = $data->max_return;
	$timestamp =substr($data->timestamp,0,10);

	ob_start();
	foreach ($data->tenor_group as $v1){
		switch (trim($v1->preservable)){
			case "N":
				$preservable =  iconv('GB2312','UTF-8', "非保本");
				$ReplyMsg = "<div class=\"row\"><div class=\"col-xs-12\"><table class=\"table table-condensed table-bordered\"><thead><tr class=\"warning\"><th>".iconv('GB2312','UTF-8', "回复")."<strong>102</strong>".iconv('GB2312','UTF-8', "获取更多在售美元非保本理财产品")."</th></tr></thead></table></div></div><hr>";
				break;
			case "Y":
				$preservable = iconv('GB2312','UTF-8', "保本");
				$ReplyMsg = "<div class=\"row\"><div class=\"col-xs-12\"><table class=\"table table-condensed table-bordered\"><thead><tr class=\"warning\"><th>".iconv('GB2312','UTF-8', "回复")."<strong>103</strong>".iconv('GB2312','UTF-8', "获取更多在售美元保本理财产品")."</th></tr></thead></table></div></div><hr>";
				break;	
			default:
				$preservable = "";
				$ReplyMsg = "";
		}		
		
		foreach ($v1->list as $v2){
			$tcontent .= "<div class=\"row\" style=\"margin-top:-25px\"><div class=\"col-xs-12 blog-post\"><h4 class=\"blog-post-title\"><strong>";
			$tcontent .= $v2->issuer_name."&middot;";
			$tcontent .= $v2->prod_name;
			$tcontent .= $preservable;
			$tcontent .= $v2->return_type."</strong></h4><h4 style=\"line-height:0.5;color:#339900;\"><small>".iconv('GB2312','UTF-8', "发售时间").":&nbsp;&nbsp;</small>";
			$tcontent .= $v2->sale_period."</h4><div class=\"row\"><div class=\"col-xs-4\"><br><p class=\"text-center\" style=\"font-family:arial;font-size:24px;color:#FF6600;\"><strong>";
			$tcontent .= $v2->expected_highest_yield."</strong></p><p class=\"text-center\" style=\"color:#FF6600;\">".iconv('GB2312','UTF-8', "预期年化收益率")."</p>";
			$tcontent .= "</div><div class=\"col-xs-8\" ><table class=\"table table-condensed\"><tbody><tr class=\"success\"><td>".iconv('GB2312','UTF-8', "起购金额")."</td><td>";
			$tcontent .= $v2->starting_amount."</td></tr><tr class=\"success\"><td>".iconv('GB2312','UTF-8', "产品期限")."</td><td>";
			$tcontent .= $v2->deposit_period.iconv('GB2312','UTF-8', "个月")."</td></tr><tr class=\"active\"><td>".iconv('GB2312','UTF-8', "当月行业平均")."</td><td>";
			$tcontent .= $v2->industry_1m_avg_yield."</td></tr><tr class=\"active\"><td>";
			$tcontent .= $currencyname;
			$tcontent .= $v2->deposit_period.iconv('GB2312','UTF-8', "个月定存")."</td><td>";
			$tcontent .= $v2->usd_rate."</td></tr></tbody></table></div></div></div></div>";
		}
		
		$tcontent .= $ReplyMsg;
		$tcontent .="<hr>";
	}	
		
	
	$fp = fopen($tmpname,"r");
	$htmlresult = fread($fp,filesize($tmpname));
	$htmlresult =str_replace("{ currencyname }",$currencyname,$htmlresult);
	$htmlresult =str_replace("{ maxreturn }",$MaxReturn,$htmlresult);	
	$htmlresult =str_replace("{ titleimg }",$titleimg,$htmlresult);	
	$htmlresult =str_replace("{ date }",$timestamp,$htmlresult);
	$htmlresult =str_replace("{ tcontent }",$tcontent,$htmlresult);	
	
//	$content .= str_replace ("{ file }",$file,$content);

	echo $htmlresult;
	
	ob_end_flush();
?>


 