<?php 
	require 'url.php';

	$titleimg ="A15.jpg";
	$timestamp = date("Y-m-d H:i:s",time());
//	$filename ="A15-DATA.php";
	$tmpname ="A15-temp.html";
	$tcontent ="";

	
//	$data = json_decode(trim(substr(file_get_contents($filename),15)));	
	
	$data = geturl($titleimg);	


	$timestamp =substr($data->timestamp,0,10);

	ob_start();
	foreach ($data->tenor_group as $v1){
		$currencyname = $v1->currencyname;
		switch (trim($v1->preservable)){
			case "N":
				$preservable =  iconv('GB2312','UTF-8', "非保本");
				break;
			case "Y":
				$preservable = iconv('GB2312','UTF-8', "保本");
				break;	
			default:
				$preservable = "";
		}
		
		$tcontent .=	"<table class=\"table table-condensed\" style=\"font-size:120%;\"><thead><tr><th colspan =\"5\" style=\"text-align:center;\">";
		$tcontent .= $currencyname."<font color=\"#FF6600\"><u>";
		$tcontent .= $preservable."</u></font>".iconv('GB2312','UTF-8', "理财产品收益对比表");
		$tcontent .= "</th></tr><tr><th style=\"text-align:center;width:100px;\">".iconv('GB2312','UTF-8', "期 限");
		$tcontent .= "</th><th style=\"text-align:center;width:150px;\">".iconv('GB2312','UTF-8', "银行名称");
		$tcontent .= "</th><th style=\"text-align:center;width:120px;\">".iconv('GB2312','UTF-8', "近期最高")."<br>".iconv('GB2312','UTF-8', "收益");
		$tcontent .= "<sup><font color=\"red\">1</font></sup></th><th style=\"text-align:center;width:120px;\">".iconv('GB2312','UTF-8', "行业平均");
		$tcontent .= "<sup><font color=\"red\">2</font></sup></th></tr></thead>";
		$tcontent .= "<tbody>";

		foreach ($v1->list as $v2){
			$tcontent .="<tr>";
			$tcontent .="<td style=\"text-align:right;\">".$v2->tenor .iconv('GB2312','UTF-8', "个月")."</td>";	
			$tcontent .= "<td style=\"text-align:center;\">".$v2->issuer_name."</td>";
			$tcontent .= "<td style=\"text-align:center;\">".$v2->expected_highest_yield."</td>";
			$tcontent .= "<td style=\"text-align:center;\">".$v2->average_yield."</td>";
			$tcontent .= "</tr>";
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


 