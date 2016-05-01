<?php 
	require 'url.php';

	$titleimg ="B12.jpg";
	$timestamp = date("Y-m-d H:i:s",time());
//	$filename ="B12-DATA.php";
	$tmpname ="B12-temp.html";
	$tcontent ="";

	
//	$data = json_decode(trim(substr(file_get_contents($filename),15)));	

	$data = geturl($titleimg);	

	$timestamp =substr($data->timestamp,0,10);

	ob_start();

	foreach ($data->tenor_group as $v1){
		$tcontent .="<h4 class=\"blog-post-title\"><strong>".iconv('GB2312','UTF-8', "最佳表现基金(");
		switch (trim($v1->tenor)){
			case 1:
				$tcontent .=  iconv('GB2312','UTF-8', "1个月");
				break;
			case 3:
				$tcontent .=  iconv('GB2312','UTF-8', "3个月");
				break;	
			case 0:
				$tcontent .=  iconv('GB2312','UTF-8', "年初至今");
				break;	
			case 12:
				$tcontent .=  iconv('GB2312','UTF-8', "1年");
				break;					
			default:
				$tcontent .=  "";
		}
		$tcontent .= ")</strong></h4>";
		$tcontent .= "<table class=\"table table-condensed\"><tbody><tr class=\"success\"><td>".iconv('GB2312','UTF-8', "基金名称")."</td><td style=\"text-align:center;width:80px;\">%<br>(".iconv('GB2312','UTF-8', "基金货币").")</td></tr>";

		foreach ($v1->list as $v2){
			$tcontent .="<tr class=\"active\"><td>".$v2->issuer_name. "</td>";
			$tcontent .="<td style=\"text-align:right;\">".$v2->rate."</td></tr>";
		}
		$tcontent .="</tbody></table>";
		
	}	
		
	
	$fp = fopen($tmpname,"r");
	$htmlresult = fread($fp,filesize($tmpname));
	$htmlresult =str_replace("{ titleimg }",$titleimg,$htmlresult);	
	$htmlresult =str_replace("{ date }",$timestamp,$htmlresult);
	$htmlresult =str_replace("{ tcontent }",$tcontent,$htmlresult);	
	
//	$content .= str_replace ("{ file }",$file,$content);

	echo $htmlresult;
	
	ob_end_flush();
?>


 