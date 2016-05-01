<?php 
	require 'url.php';

	$titleimg ="B21.jpg";
	$timestamp = date("Y-m-d H:i:s",time());
//	$filename ="B21-DATA.php";
	$tmpname ="B11-temp.html";
	$tcontent ="";

	
//	$data = json_decode(trim(substr(file_get_contents($filename),15)));	

	$data = geturl($titleimg);	


	$timestamp =substr($data->timestamp,0,10);

	ob_start();
	
	switch (trim($data->fundtype)){
		case 1:
//			$titleimg ="B11.jpg";	
			$fundtype = iconv('GB2312','UTF-8', "股票");
			$classtext = iconv('GB2312','UTF-8', "分类");
			break;
		case 2:
//			$titleimg ="B21.jpg";	
			$fundtype = iconv('GB2312','UTF-8', "债券");
			$classtext = iconv('GB2312','UTF-8', "分类");
			break;	
		case 3:
//			$titleimg ="B31.jpg";	
			$fundtype = iconv('GB2312','UTF-8', "平衡");
			$classtext = "";			
			break;	
		case 4:
//			$titleimg ="B41.jpg";	
			$fundtype = iconv('GB2312','UTF-8', "商品");
			$classtext = "";			
			break;					
		default:
			$titleimg ="";	
			$fundtype = "";
			$classtext = "";				
	}

	foreach ($data->sec_group as $v1){
		$tcontent .="<div class=\"row\"><div class=\"col-xs-12 blog-post\"><h4 class=\"blog-post-title\"><strong>";
		$tcontent .=$v1->fund_name . "</strong></h4><p style=\"line-height:0.5;color:#339900;\">" .iconv('GB2312','UTF-8', "年化股息率：");
		$tcontent .=$v1->yield."</p><table class=\"table table-condensed\"><tbody><td rowspan=\"3\" style=\"text-align:center;color:#FF6600;\"><p style=\"font-family:arial;font-size:24px;\"><strong>";
		$tcontent .=$v1->rank."</strong></p><p class=\"text-center\" style=\"color:#FF6600;\"><strong>".iconv('GB2312','UTF-8', "推荐排名")."</strong></p></td>";
		$tcontent .="<tr class=\"success\"><td>".iconv('GB2312','UTF-8', "3个月回报")."</td><td>".iconv('GB2312','UTF-8', "1年回报")."</td><td>".iconv('GB2312','UTF-8', "3年回报")."</td><td>".iconv('GB2312','UTF-8', "5年回报")."</td></tr>";
		$tcontent .="<tr class=\"active\"><td>";
		$tcontent .=str_pad($v1->return3m,8," ", STR_PAD_LEFT)."</td><td>";
		$tcontent .=str_pad($v1->return1y,8," ", STR_PAD_LEFT)."</td><td>";
		$tcontent .=str_pad($v1->return3y,8," ", STR_PAD_LEFT)."</td><td>";
		$tcontent .=str_pad($v1->return5y,8," ", STR_PAD_LEFT)."</td></tr></tbody></table></div></div>";
	}	
		
	
	$fp = fopen($tmpname,"r");
	$htmlresult = fread($fp,filesize($tmpname));
	$htmlresult =str_replace("{ titleimg }",$titleimg,$htmlresult);	
	$htmlresult =str_replace("{ date }",$timestamp,$htmlresult);
	$htmlresult =str_replace("{ fundtype }",$fundtype,$htmlresult);		
	$htmlresult =str_replace("{ classtext }",$classtext,$htmlresult);		
	$htmlresult =str_replace("{ tcontent }",$tcontent,$htmlresult);	
	
//	$content .= str_replace ("{ file }",$file,$content);

	echo $htmlresult;
	
	ob_end_flush();
?>


 