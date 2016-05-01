<?php 
define("ZYQURL", "ZYQ-URL.php");
function geturl($filename){	
	$urlfilename = ZYQURL;
	
	$urlfile =json_decode(trim(substr(file_get_contents($urlfilename),15)));

	switch (trim(substr($filename,0,3))){
		case "A11":
			$url = $urlfile->A11;
			break;
		case "A12":
			$url = $urlfile->A12;
			break;	
		case "A13":
			$url = $urlfile->A13;
			break;	
		case "A14":
			$url = $urlfile->A14;
			break;		
		case "A15":
			$url = $urlfile->A15;
			break;	
		case "A21":
			$url = $urlfile->A21;
			break;		
		case "A22":
			$url = $urlfile->A22;
			break;		
		case "A23":
			$url = $urlfile->A23;
			break;		
		case "A24":
			$url = $urlfile->A24;
			break;	
		case "A25":
			$url = $urlfile->A25;
			break;	
		case "A31":
			$url = $urlfile->A31;
			break;		
		case "A32":
			$url = $urlfile->A32;
			break;
		case "B11":
			$url = $urlfile->B11;
			break;		
		case "B12":
			$url = $urlfile->B12;
			break;		
		case "B13":
			$url = $urlfile->B13;
			break;		
		case "B21":
			$url = $urlfile->B21;
			break;		
		case "B23":
			$url = $urlfile->B23;
			break;		
		case "B31":
			$url = $urlfile->B31;
			break;		
		case "B41":
			$url = $urlfile->B41;
			break;		
		case "B43":
			$url = $urlfile->B43;
			break;		
		case "B51":	
			$url = $urlfile->B51;
			break;		
		default:
			$url = "";
	}
	
	$curl = curl_init();
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($curl, CURLOPT_TIMEOUT, 500);
	curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, true);
   curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, true);
    curl_setopt($curl, CURLOPT_URL, $url);
    $res = curl_exec($curl);
    curl_close($curl);
	$redata = json_decode($res);
	return $redata;
}
?>