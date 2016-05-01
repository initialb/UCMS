<?php 
	require 'url.php';

	$titleimg ="A14.jpg";
	$timestamp = date("Y-m-d H:i:s",time());
//	$filename ="A14-DATA.php";
	$tmpname ="A14-temp.html";
	$tcontent ="";
	$flag =true;
	
//	$data = json_decode(trim(substr(file_get_contents($filename),15)));	
	
	$data = geturl($titleimg);	

	$timestamp =substr($data->timestamp,0,10);

	ob_start();
	foreach ($data->tenor_group as $v1){
		$tcontent .=	"<table class=\"table\" ><caption style=\"text-align:left\"><h4><b>";
		$tcontent .= $v1->currencyname;
		$tcontent .= "</b></h4></caption><thead><tr class=\"info\"><th width=\"100px\">".iconv('GB2312','UTF-8', "产 品");
		$tcontent .= "</th><th colspan=\"2\">".iconv('GB2312','UTF-8', " 描  述 ")."</th></tr></thead><tbody>";
		foreach ($v1->list as $v2){
			$tcontent .= "<tr><td rowspan=\"6\" style=\"text-align:center\"><b>";
			$tcontent .= $v2->issuer_name."</b><br>";
			$tcontent .= $v2->prod_name."<br><br>(".iconv('GB2312','UTF-8', "期限");
			$tcontent .= $v2->tenor .iconv('GB2312','UTF-8', "个月").")</td>";
			$tcontent .= "<tr class=\"active\" ><td width=\"110px\">".iconv('GB2312','UTF-8', "预期收益").":<br><small><small><em>(".iconv('GB2312','UTF-8', "上期收益").")</em></small></small></td><td>";
			$tcontent .= $v2->expected_highest_yield ."<br><small><small><em>(";
			$tcontent .= $v2->history_yield.")</em></small></small></td></tr><tr><td><b>";
			$tcontent .= $v2->risk_type. "</b></td><td><b>";
			switch (trim($v2->preservable)){
				case "N":
					$preservable =  iconv('GB2312','UTF-8', "非保本");
					break;
				case "Y":
					$preservable = iconv('GB2312','UTF-8', "保本");
					break;	
				default:
					$preservable = "";
			}			
			$tcontent .= $preservable . $v2->return_type."</b></td></tr><tr><td>".iconv('GB2312','UTF-8', "销售期间").":</td><td>";		
			$tcontent .= $v2->sale_period."</td></tr><tr><td>".iconv('GB2312','UTF-8', "计息期间").":</td><td>";
			$tcontent .= $v2->interest_period."</td></tr><tr><td>".iconv('GB2312','UTF-8', "起购金额").":</td><td>";
			$tcontent .= $v2->starting_amount."</td></tr></tr>";
		}
		$tcontent .="</tbody></table>";
	}	
		
	
	$fp = fopen($tmpname,"r");
	$htmlresult = fread($fp,filesize($tmpname));
//	$htmlresult =str_replace("{ currencyname }",$currencyname,$htmlresult);
//	$htmlresult =str_replace("{ preservable }",$preservable,$htmlresult);	
	$htmlresult =str_replace("{ titleimg }",$titleimg,$htmlresult);	
	$htmlresult =str_replace("{ date }",$timestamp,$htmlresult);
	$htmlresult =str_replace("{ tcontent }",$tcontent,$htmlresult);	
	
//	$content .= str_replace ("{ file }",$file,$content);

	echo $htmlresult;
	
	ob_end_flush();
?>


 