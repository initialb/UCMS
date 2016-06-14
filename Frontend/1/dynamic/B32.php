<?php 
	require 'url.php';

	$titleimg ="B32.jpg";
	$timestamp = date("Y-m-d H:i:s",time());
	$filename ="B32-DATA.php";
	$tmpname ="B02-temp.html";
	$tcontent ="";

	
//	$data = json_decode(trim(substr(file_get_contents($filename),15)));	

	$data = geturl($titleimg);	

	$timestamp =substr($data->timestamp,0,10);

	ob_start();
	
	$releasedate = $data->releasedate;	
	
	switch (trim($data->fundtype)){
		case 1:
//			$titleimg ="B11.jpg";	
			$fundtype = iconv('GB2312','UTF-8', "股票");
			$titlecolor ="#548DD4";
			$tablecolor ="#C6D9F1";
			$imgprefix ="B90";
			break;
		case 2:
//			$titleimg ="B21.jpg";	
			$fundtype = iconv('GB2312','UTF-8', "债券");
			$titlecolor ="#FFC000";
			$tablecolor ="#FFC000";
			$imgprefix ="B92";			
			break;	
		case 3:
//			$titleimg ="B31.jpg";	
			$fundtype = iconv('GB2312','UTF-8', "平衡");
			$titlecolor ="#33CC33";
			$tablecolor ="#92D050";	
			$imgprefix ="B91";			
			break;	
		case 4:
//			$titleimg ="B41.jpg";	
			$fundtype = iconv('GB2312','UTF-8', "商品");
			$titlecolor ="";
			$tablecolor ="";
			$imgprefix ="";			
			break;					
		default:
			$titleimg ="";	
			$fundtype = "";
			$titlecolor ="";
			$tablecolor ="";
			$imgprefix ="";
	}	

	foreach ($data->tenor_group as $v1){
		$tcontent .="<div class=\"row\" style=\"margin-top:-25px\"><div class=\"col-xs-12 blog-post\"><h4 class=\"blog-post-title\" style=\"font-size:18px;\">".iconv('GB2312','UTF-8', "最佳表现基金(");
		switch (trim($v1->tenor)){
			case 1:
				$tcontent .=  iconv('GB2312','UTF-8', "1个月");
				break;
			case 3:
				$tcontent .=  iconv('GB2312','UTF-8', "3个月");
				break;	
			case 6:
				$tcontent .=  iconv('GB2312','UTF-8', "6个月");
				break;	
			case 12:
				$tcontent .=  iconv('GB2312','UTF-8', "1年");
				break;					
			default:
				$tcontent .=  "";
		}
		$tcontent .= ")</h4>";
		$tcontent .= "<table class=\"table table-condensed\"><tbody><tr style=\"background-color:";
		$tcontent .= $tablecolor . ";text-align:center;\"><td width=\"50%\"><strong>".iconv('GB2312','UTF-8', "基金名称") . "</strong></td><td width=\"20%\"><strong>" .iconv('GB2312','UTF-8', "表现(%)") . "</strong></td><td width=\"30%\"><strong>" . iconv('GB2312','UTF-8', "基金分组/ISIN") . "</strong></td></tr>";

		foreach ($v1->list as $v2){
			$tcontent .= "<tr class=\"active\"><td rowspan=\"2\" style=\"text-align:left;vertical-align:middle;\">";
			$tcontent .= $v2->fund_name . "</td>";
			$tcontent .= "<td rowspan=\"2\" style=\"text-align:center;vertical-align:middle;\">";
			$tcontent .= str_pad($v2->return,8," ", STR_PAD_LEFT) . "</td>";
			$tcontent .="<td style=\"text-align:center;border-bottom:0px;margin-bottom:0px;padding-bottom:0px;vertical-align:bottom;\">";
			$tcontent .= $v2->group_type . "</td></tr>";
			$tcontent .="<tr class=\"active\"><td style=\"text-align:center;border-top:0px;margin-top:0px;padding-top:0px;vertical-align:top;\">";
			$tcontent .= $v2->isin . "</td></tr>";
		}
		$tcontent .="</tbody></table></div></div>";
		
	}	
		
	
	$fp = fopen($tmpname,"r");
	$htmlresult = fread($fp,filesize($tmpname));
	$htmlresult =str_replace("{ titleimg }",$titleimg,$htmlresult);	
	$htmlresult =str_replace("{ date }",$timestamp,$htmlresult);
	$htmlresult =str_replace("{ fundtype }",$fundtype,$htmlresult);		
	$htmlresult =str_replace("{ releasedate }",$releasedate,$htmlresult);
	$htmlresult =str_replace("{ titlecolor }",$titlecolor,$htmlresult);		
	$htmlresult =str_replace("{ tcontent }",$tcontent,$htmlresult);	
	
//	$content .= str_replace ("{ file }",$file,$content);

	echo $htmlresult;
	
	ob_end_flush();
?>


 