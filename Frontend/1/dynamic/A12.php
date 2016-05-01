<?php 
	require 'url.php';

	$titleimg ="A12.jpg";
	$timestamp = date("Y-m-d H:i:s",time());
	$tmpname ="A12-temp.html";
	$urlname ="ZYQ-URL.php";	
	$tcontent ="";
	$flag1 =true;
	$flag2 =true;
	$flag3 =true;
	$flag4 =true;
	
	$data = geturl($titleimg);	

	$currencyname = $data->currencyname;
	switch (trim($data->preservable)){
		case "N":
			$preservable =  iconv('GB2312','UTF-8', "非保本");
			break;
		case "Y":
			$preservable = iconv('GB2312','UTF-8', "保本");
			break;	
		default:
			$preservable = "";
	}
	$timestamp =substr($data->timestamp,0,10);

	ob_start();
	foreach ($data->tenor_group as $v1){
		$tcontent .=	"<table class=\"table\" ><caption style=\"text-align:left\"><h4><b>";
		$tcontent .= $currencyname;
		$tcontent .= $preservable.iconv('GB2312','UTF-8', "在售");
		$tcontent .= $v1->tenor.iconv('GB2312','UTF-8', "个月")."</b><br><small>(".iconv('GB2312','UTF-8', "近1个月行业平均预期收益");
		if ($flag1){
			$tcontent .= "<sup>1</sup>";
			$flag1=!$flag1;
		}
		$tcontent .= ": ".$v1->industry_1m_avg_yield.")</small></h4></caption>";
		$tcontent .=	"<thead><tr class=\"info\"><th width=\"100px\">".iconv('GB2312','UTF-8', "产品")."</th><th colspan=\"2\">".iconv('GB2312','UTF-8', " 描  述 ")."</th></tr></thead><tbody>";
		foreach ($v1->list as $v2){
			$tcontent .=	"<tr><td rowspan=\"5\" style=\"text-align:center\"><b>";	
			$tcontent .= $v2->issuer_name."</b><br>";
			$tcontent .= $v2->prod_name."</td>";
			$tcontent .= "<tr class=\"active\" ><td width=\"110px\">".iconv('GB2312','UTF-8', "预期收益").":<br><small><small><em>(".iconv('GB2312','UTF-8', "上期收益");
			if ($flag2){
				$tcontent .= "<sup>2</sup>";
				$flag2=!$flag2;				
			}
			$tcontent .=")</em></small></small></td><td>";
			$tcontent .=$v2->expected_highest_yield."<br><small><small><em>(";
			$tcontent .=$v2->history_yield.")</em></small></small></td></tr><tr><td><b>";
			$tcontent .=$v2->return_type."</b></td><td><b>";
			$tcontent .=$v2->risk_type;			
			if ($flag4){
				$tcontent .= "<sup>4</sup>";
				$flag4=!$flag4;				
			}	
			$tcontent .="</b></td></tr><tr><td>".iconv('GB2312','UTF-8', "销售期间").":</td><td>";
			$tcontent .=$v2->sale_period."</td></tr><tr><td>".iconv('GB2312','UTF-8', "计息期间");			
			if ($flag3){
				$tcontent .= "<sup>3</sup>";
				$flag3=!$flag3;				
			}			
			$tcontent .=":</td><td>";
			$tcontent .=$v2->interest_period."</td></tr></tr>";
		}
		$tcontent .="</tbody></table>";
	}	
		
	
	$fp = fopen($tmpname,"r");
	$htmlresult = fread($fp,filesize($tmpname));
	$htmlresult =str_replace("{ currencyname }",$currencyname,$htmlresult);
	$htmlresult =str_replace("{ preservable }",$preservable,$htmlresult);	
	$htmlresult =str_replace("{ titleimg }",$titleimg,$htmlresult);	
	$htmlresult =str_replace("{ date }",$timestamp,$htmlresult);
	$htmlresult =str_replace("{ tcontent }",$tcontent,$htmlresult);	
	
//	$content .= str_replace ("{ file }",$file,$content);

	echo $htmlresult;
	
	ob_end_flush();
?>


 