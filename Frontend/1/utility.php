<?php

//define your token
define("TOKEN", "ZhuanYangQian");
define("APPID","wx0203ddfd9811dede");
define("APPSECRET","ed6eb8122f6cec5384449e1094b30ae9");  // management testing account

define("REDIRECT_URI","http%3A%2F%2Fzhuanyangqian.applinzi.com%2Foauth2.php");

//BAIDU MAP AK
define("BDMAPAK","80f1638282beadcd3d3902cb91b35bf4");


define("SAE_ACCESSKEY","z1yxm51x52");
define("SAE_SECRETKEY","4w00hl1yzm2z5i355zzzxzwj3l0w3w002y2zzkj0");

define("WEB_SITE","zhuanyangqian.applinzi.com");

//$gTokenTime =0;
//$gAccessToken ="";
//此两项，需要手工在数据库中添加！


function traceHttp($str = null){
	if(empty($str)){
		$content = date('Y-m-d H:i:s'). "\nREMOTE_ADDR:".$_SERVER["REMOTE_ADDR"]."\nQUERY_STRING:".$_SERVER["QUERY_STRING"]."\n\n";
	
		if (isset($_SERVER['HTTP_APPNAME'])){
			sae_set_display_errors(false);
			sae_debug(trim($content));
			sae_set_display_errors(true);
		}else{	
			$max_size = 10000;
			$log_filename = "log.xml";
			if(file_exists($log_filename) and (abs(filesize($log_filename)) > $max_size)){
				unlink($log_filename);
			}
			file_put_contents($log_filename,$content,FILE_APPEND);
		}
	}else{
		$log_filename = "log.xml";
		file_put_contents($log_filename,$str,FILE_APPEND);
	}
	
}

function PrintErrorMsg($ErrCode,$ErrMsg){
	//	$content = date('Y-m-d H:i:s'). "\nERROR_CODE: ". $ErrCode . "\nERROR_MSG: " .$ErrMsg;
	//	$log_filename = "log.xml";
	//	file_put_contents($log_filename,$content,FILE_APPEND);
	sae_debug("ErrCode : " . $ErrCode . " ErrMsg : " . $ErrMsg);
}


//Function Https_request
function https_request($url,$data = null){
	$ch = curl_init();
	curl_setopt($ch,CURLOPT_URL,$url);
	curl_setopt($ch,CURLOPT_SSL_VERIFYPEER,FALSE);
	curl_setopt($ch,CURLOPT_SSL_VERIFYHOST,FALSE);
	if(!empty($data)){
		curl_setopt($ch,CURLOPT_POST,1);
		curl_setopt($ch,CURLOPT_POSTFIELDS,$data);
	}
	curl_setopt($ch,CURLOPT_RETURNTRANSFER,1);
	$output = curl_exec($ch);
	curl_close($ch);
	return $output;
}

function get_Access_Token(){
	$appid = APPID;
	$appsecret = APPSECRET;
	$nowTime = time();
	$mysql = new SaeMysql();
	$sql = "SELECT * FROM `gParameters` WHERE `name` ='gAccessToken'";
	$data = $mysql->getLine($sql);
	$accessToken = $data["Value"];
//	sae_debug("accessToken = ".$accessToken);
	$sql = "SELECT * FROM `gParameters` WHERE `name` ='gTokenTime'";
	$data = $mysql->getLine($sql);
	$tokenTime = $data["Value"];
	
	if(($nowTime - $tokenTime) > 7000){ 
		$url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=".$appid."&secret=".$appsecret;
		$outputToken = https_request($url);
		$jsoninfo = json_decode($outputToken,true);
		$accessToken = $jsoninfo["access_token"];
		$sql = "UPDATE `gParameters` SET `Value` ='"  . $accessToken . "' WHERE `name` ='gAccessToken'";
		$mysql->runSql( $sql );
		$sql = "UPDATE `gParameters` SET `Value` ='"  . $nowTime . "' WHERE `name` ='gTokenTime'";
		$mysql->runSql( $sql );

	}
	$mysql->closeDb();
	return $accessToken;

}

function get_JS_Access_Token(){
	$appid = APPID;
	$appsecret = APPSECRET;
	$nowTime = time();
	$mysql = new SaeMysql();
	$sql = "SELECT * FROM `gParameters` WHERE `name` ='gJSAccessToken'";
	$data = $mysql->getLine($sql);
	$JSAccessToken = $data["Value"];
//	sae_debug("accessToken = ".$accessToken);
	$sql = "SELECT * FROM `gParameters` WHERE `name` ='gJSTokenTime'";
	$data = $mysql->getLine($sql);
	$JSTokenTime = $data["Value"];
	
	if(($nowTime - $JSTokenTime) > 7000){ 
		$accessToken = get_Access_Token();
		$url = "https://api.weixin.qq.com/cgi-bin/ticket/getticket?type=jsapi&access_token=".$accessToken;

		$outputToken = https_request($url);
		$jsoninfo = json_decode($outputToken,true);
		
		$JSAccessToken = $jsoninfo["ticket"];
		$sql = "UPDATE `gParameters` SET `Value` ='"  . $JSAccessToken . "' WHERE `name` ='gJSAccessToken'";
		$mysql->runSql( $sql );
		$sql = "UPDATE `gParameters` SET `Value` ='"  . $nowTime . "' WHERE `name` ='gTokenTime'";
		$mysql->runSql( $sql );

	}
	$mysql->closeDb();
	return $JSAccessToken;	
}


function SWX_Get($swxUrl){
	$credentials = "admin:admin";
						
	$ch = curl_init();
	curl_setopt($ch,CURLOPT_URL,$swxUrl);
	curl_setopt($ch,CURLOPT_SSL_VERIFYPEER,FALSE);
	curl_setopt($ch,CURLOPT_SSL_VERIFYHOST,FALSE);
	curl_setopt($ch, CURLOPT_HTTPAUTH, CURLAUTH_BASIC);
	curl_setopt($ch, CURLOPT_USERPWD, $credentials);
	curl_setopt($ch,CURLOPT_HTTPHEADER,array("Accept: application/json"));
	curl_setopt($ch,CURLOPT_RETURNTRANSFER,1);
	$output = curl_exec($ch);
	curl_close($ch);
	return $output;
}


/*
Pharse XML file:
$apistr = file_get_contents($geourl);
$apiobj = simplexml_load_string($apistr);
$addstr = $apiobj -> results -> result[0] -> name;


*/

/*SAE MemCache Utility Examples
*/

function SaeMemCache_set($openid,$data){
	$smc = memcache_init();
	if($smc == true){
		memcache_set($smc,$openid,$data,60);
		return "Please enter Recording UserID:";
	}else{
		return "MemCache is not ready!";
	}
}

function SaeMemCache_get($openid){
	$smc = memcache_init();
	if($smc == true){
		$result = memcache_get($smc,$openid);
		if (!empty($result)){
			return $result;
		}else{
			return "data empty";
		}
	}else{
		return "MemCache is not ready!";
	}
}



?>