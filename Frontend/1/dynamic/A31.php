<?php 
	require 'url.php';
	
	$titleimg ="A31.jpg";
	$timestamp = date("Y-m-d H:i:s",time());
//	$filename ="A31-DATA.php";
	$tmpname ="A31-temp.html";
	$tcontent ="";

	
//	$data = json_decode(trim(substr(file_get_contents($filename),15)));	

	$data = geturl($titleimg);	


	$timestamp =substr($data->timestamp,0,10);
	$currencyname = $data->currencyname .iconv('GB2312','UTF-8', "ծȯ");	

	ob_start();
	foreach ($data->tenor_group as $v1){
		switch ($v1->tenor){
			case 1:
				$tenor =  iconv('GB2312','UTF-8', "����һ�����Ԥ������");
				break;
			case 2:
				$tenor = iconv('GB2312','UTF-8', "�����������Ԥ������");
				break;	
			case 3:
				$tenor = iconv('GB2312','UTF-8', "�����������Ԥ������");
				break;					
			default:
				$tenor = iconv('GB2312','UTF-8', "���Ԥ������");
		}
		
		$tcontent .= "<h4 class=\"blog-post-title\" style=\"text-align:left;\">";
		$tcontent .=$tenor . $currencyname ."</h4>";
		
//		$tcontent .="<div class=\"row\" style=\"margin-top:-25px;\"><div class=\"col-xs-12 blog-post\">";


		foreach ($v1->list as $v2){
			$tcontent .="<div class=\"row\" style=\"margin-top:0.5px;margin-bottom:0.5px\"><div class=\"col-xs-12 blog-post\"><div class=\"col-xs-12\"><table><tbody><tr><td><strong>";
			$tcontent .= $v2->issuer_name."(";
			$tcontent .= $v2->period .iconv('GB2312','UTF-8', "����").")</strong></td><td>&nbsp;</td><td style=\"color:#339900;\">";
			$tcontent .= iconv('GB2312','UTF-8', "ƱϢ:").$v2->rate."</td></tr></tbody></table></div>";
			$tcontent .= "<div class=\"col-xs-3\"><p class=\"text-center\" style=\"font-family:arial;font-size:24px;color:#FF6600;\"><strong>";
			$tcontent .= $v2->rank."</strong></p><p class=\"text-center\" style=\"color:#FF6600;\"><strong>";
			$tcontent .= iconv('GB2312','UTF-8', "��ѡ����")."</strong></p></div><div class=\"col-xs-9\"><table class=\"table table-condensed\"><tbody><tr class=\"active\"><td>".iconv('GB2312','UTF-8', "Ԥ���껯������")."</td><td>";
			$tcontent .= $v2->expected_highest_yield."</td></tr><tr class=\"active\"><td>".iconv('GB2312','UTF-8', "���õȼ�")."</td><td>";
			$tcontent .= $v2->creadit_rank."</td></tr><tr class=\"active\"><td>".iconv('GB2312','UTF-8', "����")."</td><td>";
			$tcontent .= $v2->grading."</td></tr><tr class=\"active\"><td>".iconv('GB2312','UTF-8', "������˾")."</td><td>";
			$tcontent .= $v2->grading_owner."</td></tr><tr class=\"active\"><td>".iconv('GB2312','UTF-8', "������")."</td><td>";
			$tcontent .= $v2->deadline."</td></tr><tr class=\"active\"><td>".iconv('GB2312','UTF-8', "�ο������")."</td><td>";
			$tcontent .= $v2->price."</td></tr><tr class=\"active\"><td>".iconv('GB2312','UTF-8', "ծȯ����")."</td><td>";
			$tcontent .= $v2->bond_code."</td></tr></tbody></table></div></div></div>";	
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


 