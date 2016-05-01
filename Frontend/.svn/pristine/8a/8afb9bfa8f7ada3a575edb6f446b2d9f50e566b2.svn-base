<?php 
	require 'url.php';
	
	$titleimg ="A23.jpg";
	$tmpname ="A21-temp.html";
	$tcontent ="<tbody>";
	$flag = false;
	
	//$data = json_decode(trim(substr(file_get_contents($filename),15)));	

	$data = geturl($titleimg);	

	ob_start();
	foreach ($data->list as $v1){
		if ($flag) {
			$tcontent .= "<tr>";
		}else{
			$tcontent .= "<tr class=\"active\">";
		}
		$flag = !$flag;		
			
		$tcontent .= "<td style=\"text-align:left;width:80px;\">".$v1->bank."</td>";
		
		$tcontent .= "<td style=\"text-align:center;\">";
		if (!(strcasecmp("*",substr($v1->remitbid,0,1)))){
			$tcontent .= "<font color=\"red\"><b>".substr($v1->remitbid,1)."</b></font></td>";
		}else{
			$tcontent .= $v1->remitbid."</td>";
		}
		
		$tcontent .= "<td style=\"text-align:center;\">";
		if (!(strcasecmp("*",substr($v1->remitask,0,1)))){
			$tcontent .= "<font color=\"red\"><b>".substr($v1->remitask,1)."</b></font></td>";
		}else{
			$tcontent .= $v1->remitask."</td>";
		}

		$tcontent .= "<td style=\"text-align:center;\">";
		if (!(strcasecmp("*",substr($v1->cashbid,0,1)))){
			$tcontent .= "<font color=\"red\"><b>".substr($v1->cashbid,1)."</b></font></td>";
		}else{
			$tcontent .= $v1->cashbid."</td>";
		}

		
		$tcontent .= "<td style=\"text-align:center;\">";
		if (!(strcasecmp("*",substr($v1->cashask,0,1)))){
			$tcontent .= "<font color=\"red\"><b>".substr($v1->cashask,1)."</b></font></td>";
		}else{
			$tcontent .= $v1->cashask."</td>";
		}

		$tcontent .="</tr>";
	}
	$tcontent .= "</tbody>";
	
	
	$fp = fopen($tmpname,"r");
	$htmlresult = fread($fp,filesize($tmpname));
	$htmlresult =str_replace("{ currencyname }",$data->currencyname,$htmlresult);
	$htmlresult =str_replace("{ titleimg }",$titleimg,$htmlresult);	
	$htmlresult =str_replace("{ timestamp }",$data->timestamp,$htmlresult);
	$htmlresult =str_replace("{ tcontent }",$tcontent,$htmlresult);	
	
//	$content .= str_replace ("{ file }",$file,$content);

	echo $htmlresult;
	
	ob_end_flush();
?>


 