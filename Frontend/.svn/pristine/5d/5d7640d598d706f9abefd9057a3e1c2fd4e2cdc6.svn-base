<?php 
	require 'url.php';
	
	$titleimg ="A32.jpg";
	$timestamp = date("Y-m-d H:i:s",time());
//	$filename ="A32-DATA.php";
	$tmpname ="A32-temp.html";
	$tcontent ="";

	
//	$data = json_decode(trim(substr(file_get_contents($filename),15)));	

	$data = geturl($titleimg);	


	$timestamp =substr($data->timestamp,0,10);

	ob_start();
	foreach ($data->sec_group as $v1){
		
		$tcontent .= "<div class=\"row\">";
		$tcontent .= "<h4 class=\"blog-post-title\" style=\"text-align:left;\"><strong>&nbsp;";
		$tcontent .= iconv('GB2312','UTF-8', " 安全等级 ").$v1->level ."</strong></h4>";		
		$tcontent .="<div class=\"col-xs-12\"><table class=\"table table-condensed text-left\"><tbody><tr class=\"active\"><td style=\"color:#FF6600;width:40%;\">".iconv('GB2312','UTF-8', "排名")."</td><td class=\"text-center\">1</td><td  class=\"text-center\">2</td><td  class=\"text-center\">3</td></tr>";
		

			
		foreach ($v1->list as $v2){
			$vIssuername .="<td  class=\"text-center\">".$v2->issuer_name."</td>";
			$vPeriod .= "<td  class=\"text-center\">".$v2->period."</td>";
			$vRate .= "<td  class=\"text-center\">".$v2->rate."</td>";
			$v12yield .= "<td  class=\"text-center\">".$v2->yield12."</td>";
			$v24yield .= "<td  class=\"text-center\">".$v2->yield24."</td>";
			$v36yield .= "<td  class=\"text-center\">".$v2->yield36."</td>";
			$vDeadline .= "<td  class=\"text-center\">".$v2->deadline."</td>";
			$vPrice .= "<td  class=\"text-center\">".$v2->price."</td>";
			$vBondcode .= "<td  class=\"text-center\"><small>".$v2->bond_code."</small></td>";
		}			
		
		$tcontent .= "<tr><td style=\"color:#FF6600;\">".iconv('GB2312','UTF-8', "发行人")."</td>".$vIssuername."</tr>";
		$tcontent .= "<tr><td style=\"color:#FF6600;\">".iconv('GB2312','UTF-8', "期限")."</td>".$vPeriod."</tr>";
		$tcontent .= "<tr><td style=\"color:#FF6600;\">".iconv('GB2312','UTF-8', "票息")."</td>".$vRate."</tr>";
		$tcontent .= "<tr><td style=\"color:#FF6600;\">".iconv('GB2312','UTF-8', "一年收益")."</td>".$v12yield."</tr>";		
		$tcontent .= "<tr><td style=\"color:#FF6600;\">".iconv('GB2312','UTF-8', "两年年化")."</td>".$v24yield."</tr>";			
		$tcontent .= "<tr><td style=\"color:#FF6600;\">".iconv('GB2312','UTF-8', "三年年化")."</td>".$v36yield."</tr>";			
		$tcontent .= "<tr><td style=\"color:#FF6600;\">".iconv('GB2312','UTF-8', "到期日")."</td>".$vDeadline."</tr>";	
		$tcontent .= "<tr><td style=\"color:#FF6600;\">".iconv('GB2312','UTF-8', "参考买入价")."</td>".$vPrice."</tr>";	
		$tcontent .= "<tr><td style=\"color:#FF6600;\">".iconv('GB2312','UTF-8', "债券代码")."</td>".$vBondcode."</tr>";			
		$tcontent .= "</tbody></table></div></div>";
		
		$vIssuername ="";
		$vPeriod = "";
		$vRate = "";
		$v12yield = "";
		$v24yield = "";
		$v36yield = "";
		$vDeadline = "";
		$vPrice = "";
		$vBondcode = "";		
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


 