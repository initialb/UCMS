<?php
/**
  * DupliCALL : http://duplicall.sinaapp.com
	Author : BCH 
	Date : 2014.05.27
	Date ：2014.05.28
  */
require_once(dirname(__FILE__).'/'.'utility.php');
require_once(dirname(__FILE__).'/'.'menu.php');
require_once(dirname(__FILE__).'/'.'SaeMysql.php');
require_once(dirname(__FILE__).'/'.'CCInterface.php');

/*
$wechatMenu = new Menu();
$errCode = $wechatMenu->view();
if (0 != $errCode ){
//$wechatMenu->delete();
//$wechatMenu->view();
	$ret = $wechatMenu->create();
	sae_debug($ret);
}
exit;
*/
$wechatObj = new wechatCallbackapiTest();
if(isset($_GET['echostr'])){
	$wechatObj->valid();
}else{
	$wechatObj->responseMsg();
}

//class wechatCallbackapiTest
class wechatCallbackapiTest
{
	public function valid()
    {
        $echoStr = $_GET["echostr"];

        //valid signature , option
        if($this->checkSignature()){
        	echo $echoStr;
        	exit;
        }
    }
	
	private function checkSignature()
	{
        $signature = $_GET["signature"];
        $timestamp = $_GET["timestamp"];
        $nonce = $_GET["nonce"];	
        		
		$token = TOKEN;
		$tmpArr = array($token, $timestamp, $nonce);
		sort($tmpArr, SORT_STRING);
		$tmpStr = implode( $tmpArr );
		$tmpStr = sha1( $tmpStr );
		
		if( $tmpStr == $signature ){
			return true;
		}else{
			return false;
		}
	}

    public function responseMsg()
    {
		//get post data, May be due to the different environments
		$postStr = $GLOBALS["HTTP_RAW_POST_DATA"];

      	//extract post data
		if (!empty($postStr)){
                
              	$postObj = simplexml_load_string($postStr, 'SimpleXMLElement', LIBXML_NOCDATA);
				$RX_TYPE = trim($postObj->MsgType);
				switch ($RX_TYPE){
					case "text":
						$result = $this->receiveText($postObj);
						break;
					case "image":
						$result = $this->receiveImage($postObj);
						break;
					case "voice":
						$result = $this->receiveVoice($postObj);
						break;
					case "video":
						$result = $this->receiveVideo($postObj);
						break;
					case "location":
						$result = $this->receiveLocation($postObj);
						break;
					case "link":
						$result = $this->receiveLink($postObj);
						break;
					case "event":
						$result = $this->receiveEvent($postObj);
						break;
					default:
						$result = "unknown msg type: ". $RX_TYPE;
						break;
				}
				echo $result;
        }else {
        	echo "";
        	exit;
        }
    }
	
	private function receiveText($obj){
		$keyword = trim($obj->Content);
		if (is_numeric($keyword) && ($keyword >= 100) && ($keyword < 200)) {
			/*
			$callUri ="http://duplicall.eicp.net:8088/rs/smarttap/calls/info?maxResults=10&sortField=startTime&sortOrder=DESC&targetId=".$keyword;
			$credentials = "admin:admin";
					
			$ch = curl_init();
			curl_setopt($ch,CURLOPT_URL,$SWXurl);
			curl_setopt($ch,CURLOPT_SSL_VERIFYPEER,FALSE);
			curl_setopt($ch,CURLOPT_SSL_VERIFYHOST,FALSE);
			curl_setopt($ch, CURLOPT_HTTPAUTH, CURLAUTH_BASIC);
			curl_setopt($ch, CURLOPT_USERPWD, $credentials);
			curl_setopt($ch,CURLOPT_HTTPHEADER,array("Accept: application/json"));
			curl_setopt($ch,CURLOPT_RETURNTRANSFER,1);
			$output = curl_exec($ch);
			curl_close($ch);	
			*/
			
			//$content ="您发送的是数字文本：" . $keyword;

			$smcValue =SaeMemCache_get($obj->FromUserName."key");
			$content =$smcValue;
			$result = $this->transmitText($obj,$content);		
			
			//if (SaeMemCache_get($obj->FromUserName."key",$obj->FromUserName."Recording");
		}else{
			switch(strtolower($keyword)){
				case "id":
					$access_token = get_Access_Token();
					$result = $this->transmitText($obj,"Access_Token: " . $access_token);
					break;
				case "61":
					$CC = new CCInterface();
					$CC->SendMsg($obj->FromUserName,"【DC测试】六一节快乐 ");
					break;
				case "users":
					$SWXurl = "http://duplicall.eicp.net:8088/rs/smarttap/users/info";
					$credentials = "admin:admin";
					
					$ch = curl_init();
					curl_setopt($ch,CURLOPT_URL,$SWXurl);
					curl_setopt($ch,CURLOPT_SSL_VERIFYPEER,FALSE);
					curl_setopt($ch,CURLOPT_SSL_VERIFYHOST,FALSE);
					curl_setopt($ch, CURLOPT_HTTPAUTH, CURLAUTH_BASIC);
					curl_setopt($ch, CURLOPT_USERPWD, $credentials);
					curl_setopt($ch,CURLOPT_HTTPHEADER,array("Accept: application/json"));
					curl_setopt($ch,CURLOPT_RETURNTRANSFER,1);
					$output = curl_exec($ch);
					curl_close($ch);	
					
					$retArray = json_decode($output,true);
					$userArray =$retArray['usersInfo'];
					usort($userArray,function($a,$b){
						if($a["id"] == $b["id"])
							return 0;
						return ($a["id"] < $b["id"])? -1 :1;
						});
					foreach($userArray as $user){
						//$content .= $user["uri"]."|".$user["id"]."|".$user["displayName"]."|".$user["disabled"]."|".$user["firstName"]."|".$user["lastName"]."|".$user["emailAddress"]."|".$user["alias"]."|".$user["loginId"]."\n";
						$content .= $user["id"].":".$user["firstName"].",".$user["lastName"]."\n";
					}
					$result = $this->transmitText($obj,$content);
					break;
				case "code":
					$appid = APPID;
					$redirect_uri =REDIRECT_URI;
					$auth_url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=".$appid."&redirect_uri=".$redirect_uri."&response_type=code&scope=snsapi_userinfo&state=1#wechat_redirect";
					$content ='DupliCALL UCenter Oauth2.0 <a href="'.$auth_url.'">点击这里进行授权</a>';
					$result = $this->transmitText($obj,$content);
					break;
				case "auth":
					$appid = APPID;
					$appsecret =APPSECRET;
					
					$mysql = new SaeMysql();
						$sql = "SELECT * FROM `gParameters` WHERE `name` ='gAuthCode'";
						$data = $mysql->getLine($sql);
						$authCode = $data["Value"];
					$mysql->closeDb();
					
					$url = "https://api.weixin.qq.com/sns/oauth2/access_token?appid=".$appid."&secret=".$appsecret."&code=".$authCode."&grant_type=authorization_code";
					$result1 = https_request($url);
					$jsoninfo = json_decode($result1,true);
					
					$authAccessToken = $jsoninfo["access_token"];
					$authRefreshToken = $jsoninfo["refresh_token"];
					$authOpenId = $jsoninfo["openid"];
					$authScope = $jsoninfo["scope"];
					
					$userinfo_url ="https://api.weixin.qq.com/sns/userinfo?access_token=".$authAccessToken."&openid=".$authOpenId;
					$userinfo_json = https_request($userinfo_url);
					$userinfo_array = json_decode($userinfo_json,true);
				
					$userOpenid = $userinfo_array["openid"];
					$userNickname = $userinfo_array["nickname"];
					if ($userinfo_array["sex"] == 1){
						$userSex ="先生";
					}else{
						$userSex ="女士";
					}
					$userLanguage =$userinfo_array["language"];
					$userCity = $userinfo_array["city"];
					$userProvince = $userinfo_array["province"];
					$userCountry = $userinfo_array["country"];
					$userImg =$userinfo_array["headimgurl"];
				
					$content1 = "OpenId : ". $userOpenid ."\n Nickname : ". $userNickname ."\n Sex : ".$userSex . "\n Language : ". $userLanguage ."\n Location : ". $userCountry ."/".$userProvince."/".$userCity."\n";
					//$content .= '<img src="'. $userImg.'" >';
				
					$content[] =array("Title"=> $userNickname,
									  "Description"=>$content1,
									  "PicUrl"=>$userImg);
					$result = $this->transmitNews($obj,$content);
					break;
				case "文本":
				case "text":
					$content ="欢迎参加DupliCALL公众号测试｜Welcome to join the test of DupliCALL's Public WX Account";
					$result = $this->transmitText($obj,$content);
					break;
				case "音乐":
				case "music":
					$content = array("Title"=>"最美",
					"Description" => "歌手:羽泉",
					"MusicUrl" =>"http://duplicall.eicp.net:3476/0111.mp3",
					"HQMusicUrl" =>"http://duplicall.eicp.net:3476/0111.mp3");
					$result = $this->transmitMusic($obj,$content);
					break;
				case "图文":
				case "单图文":
					$content = array();
					$content[] =array("Title"=> "DupliCALL 公司介绍",
										"Description"=>"Full-Time Lync Recorder",
										"PicUrl"=>"http://www.ai-logix.com.cn/eng/images/logos/smartworks_box_logo-s.jpg",
										"Url"=>"http://www.ai-logix.com.cn/chs/products.htm");
					$result = $this->transmitNews($obj,$content);
					break;
				case "多图文":
					$content = array();
					$content[] =array("Title"=> "DupliCALL技术支持",
									"Description"=>"在线技术支持",
									"PicUrl"=>"http://www.ai-logix.com.cn/chs/images/support_box.jpg",
									"Url"=>"http://www.ai-logix.com.cn/chs/support.htm");
					$content[] =array("Title"=> "产品资料下载",
									"Description"=>"",
									"PicUrl"=>"http://www.ai-logix.com.cn/chs/images/companypage_banner_large.jpg",
									"Url"=>"http://www.ai-logix.com.cn/chs/support-down-smartworks.htm");
					$content[] =array("Title"=> "Skype在线通话技术支持",
									"Description"=>"使用Skype在线互联网电话软件",
									"PicUrl"=>"http://www.ai-logix.com.cn/chs/images/support.jpg",
									"Url"=>"http://www.ai-logix.com.cn/chs/support-skype.htm");	
					$content[] =array("Title"=> "FAQ技术问答",
									"Description"=>"使用Skype在线互联网电话软件",
									"PicUrl"=>"http://www.ai-logix.com.cn/chs/images/solutions_box.jpg",
									"Url"=>"http://www.ai-logix.com.cn/chs/support-down-faq.htm");	
					$result = $this->transmitNews($obj,$content);
					break;
				default:
					$content ="您发送的是文本消息，内容如下：" . $keyword;
					$result = $this->transmitText($obj,$content);
			}
		
		}
		return $result;
	}
	
	private function receiveImage($obj){
		//$content = "您发送的是图片消息，地址如下：" . $obj->PicUrl;
		$content =array("MediaId" =>$obj->MediaId);
		$result = $this->transmitImage($obj,$content);
		return $result;
	}
	
	private function receiveVoice($obj){
		//$content = "您发送的是语音消息，MediaID如下：" . $obj->MediaId;
		$content =array("MediaId" =>$obj->MediaId);
		$result = $this->transmitVoice($obj,$content);
		return $result;
	}
	
	private function receiveVideo($obj){
		//$content = "您发送的是视频消息，MediaID如下：" . $obj->MediaId;
		$content =array("MediaId" =>$obj->MediaId,"ThumbMediaId"=>$obj->ThumbMediaId,"Title"=>"","Description"=>"");
		$result = $this->transmitVideo($obj,$content);
		return $result;
	}
	
	private function receiveLocation($obj){
		$content = "您发送的是位置消息：\n 经度 - " . $obj->Location_Y . "\n 纬度 - " .$obj->Location_X . " \n 位置 - ". $obj->Label . " \n Zoom - " .$obj.Scale;
		$result = $this->transmitText($obj,$content);
		return $result;
	}
	
	private function receiveLink($obj){
		$content = "您发送的是链接消息：标题 - " . $obj->Title . " \n 内容 - " .$obj->Description . " \n 链接地址 - ". $obj->Url;
		$result = $this->transmitText($obj,$content);
		return $result;
	}
	
	private function receiveEvent($obj){
		$content = "";
		
		switch ($obj->Event){
			case "CLICK":
				switch ($obj->EventKey){
					case "calls":
						//$content ="最新的10条录音";
						//$content = dirname(__FILE__).'/'.'test.php';
						//$content ='<a href="'."http://duplicall.sinaapp.com/test.php".'">测试链接</a>';
						$content = SaeMemCache_set($obj->FromUserName."key",$obj->FromUserName."Recording");
						break;
					case "report":
						//$content ="日、周、月报表查看";
						$content ='<a href="'."http://duplicall.sinaapp.com/test.php".'">测试链接</a>';
						break;
					case "users":
						$SWXurl = "http://duplicall.eicp.net:8088/rs/smarttap/users/info";
						/*
						$credentials = "admin:admin";
						
						$ch = curl_init();
						curl_setopt($ch,CURLOPT_URL,$SWXurl);
						curl_setopt($ch,CURLOPT_SSL_VERIFYPEER,FALSE);
						curl_setopt($ch,CURLOPT_SSL_VERIFYHOST,FALSE);
						curl_setopt($ch, CURLOPT_HTTPAUTH, CURLAUTH_BASIC);
						curl_setopt($ch, CURLOPT_USERPWD, $credentials);
						curl_setopt($ch,CURLOPT_HTTPHEADER,array("Accept: application/json"));
						curl_setopt($ch,CURLOPT_RETURNTRANSFER,1);
						$output = curl_exec($ch);
						curl_close($ch);	
						*/
						$output = SWX_Get($SWXurl);
						$retArray = json_decode($output,true);
						$userArray =$retArray['usersInfo'];
						usort($userArray,function($a,$b){
							if($a["id"] == $b["id"])
								return 0;
							return ($a["id"] < $b["id"])? -1 :1;
							});
						$content ="当前用户清单\n";
						foreach($userArray as $user){
							//$content .= $user["uri"]."|".$user["id"]."|".$user["displayName"]."|".$user["disabled"]."|".$user["firstName"]."|".$user["lastName"]."|".$user["emailAddress"]."|".$user["alias"]."|".$user["loginId"]."\n";
							$content .= $user["id"].":".$user["firstName"].",".$user["lastName"]."\n";
						}
						//$result = $this->transmitText($obj,$content);
						//$content ="当前用户清单\n";
						break;
					case "callscount":
						$content ="当前通话数量";
						break;
					case "service":
						$content = array();
						$content[] =array("Title"=> "服务组件状态:","Description"=>"使用Skype在线互联网电话软件","PicUrl"=>"","Url"=>"");
						$SWXurl = "http://duplicall.eicp.net:8088/rs/smarttap/managed_devices/info";
						$output = SWX_Get($SWXurl);
						$retArray = json_decode($output,true);
						$devArray =$retArray['managedDevices'];
						usort($devArray,function($a,$b){
							if($a["id"] == $b["id"])
								return 0;
							return ($a["id"] < $b["id"])? -1 :1;
							});
							
						foreach($devArray as $dev){
							$dev["description"] = str_replace("SmartTAP","DC",$dev["description"]);
							$dev["description"] = str_replace("AudioCodes","DC",$dev["description"]);
							
							$content[]= array("Title"=>"Device ID :". $dev["id"].":".$dev["name"]."\n Address:(".$dev["host"].":".$dev["port"].")\n".$dev["description"],
											"Description"=>$dev["description"],
											"PicUrl"=>"","Url"=>"");
						}
						break;
					case "storage":
						$content ="存储状态";
						break;
					case "alarm":
						$content ="报警信息查看";
						break;
					case "auth":
						$content ="用户授权";
						break;
					case "monitoring":
						$content ="实时监听";
						break;
					case "help":
						$content ="联系管理员";
						break;	
					default:
						break;
				}
				if(is_array($content)){
					$result = $this->transmitNews($obj,$content);
				}else{
					$result = $this->transmitText($obj,$content);
				}
				break;
			case "LOCATION":
			    $MapAk = BDMAPAK;
				
				$url ="http://api.map.baidu.com/geocoder/v2/?ak=".$MapAk."&location=".$obj->Latitude.",".$obj->Longitude."&output=json&coordtype=gcj02ll";
				$output = file_get_contents($url);
				$address = json_decode($output,true);
				$content = "当前位置 ".$obj->Latitude.",".$obj->Longitude.":".$address["result"]["addressComponent"]["province"]." ".$address["result"]["addressComponent"]["city"]." ".$address["result"]["addressComponent"]["district"]." ".$address["result"]["addressComponent"]["street"]." ".$address["result"]["addressComponent"]["street_number"];
				$result = $this->transmitText($obj,$content);
				break;
			case "subscribe":
				$content = "欢迎关注DupliCALL微信公众号";
				$result = $this->transmitText($obj,$content);
				break;
			case "unsubscribe":
				$content = "";
				break;
			default:
				$content = "Unknow Event: ".$obj->Event;
				$result = $this->transmitText($obj,$content);
				break;
		}

		return $result;
		
	}
	
//------------------------------	
	private function transmitText($obj,$content){
		$textTpl = "<xml>
		<ToUserName><![CDATA[%s]]></ToUserName>
		<FromUserName><![CDATA[%s]]></FromUserName>
		<CreateTime>%s</CreateTime>
		<MsgType><![CDATA[text]]></MsgType>
		<Content><![CDATA[DC UCenter :\n %s\n %s]]></Content>
		</xml>";
		
		$result = sprintf($textTpl,$obj->FromUserName,$obj->ToUserName,time(),$content,date("d-M-Y H:i:s"));
		return $result;
	}
	
	private function transmitMusic($obj,$musicArray){
		$itemTpl = "<Music>
		<Title><![CDATA[%s]]></Title>
		<Description><![CDATA[%s]]></Description>
		<MusicUrl><![CDATA[%s]]></MusicUrl>
		<HQMusicUrl><![CDATA[%s]]></HQMusicUrl>
		</Music>";
		
		$itemStr =sprintf($itemTpl,$musicArray['Title'],$musicArray['Description'],$musicArray['MusicUrl'],$musicArray['HQMusicUrl']);
	
		$textTpl = "<xml>
		<ToUserName><![CDATA[%s]]></ToUserName>
		<FromUserName><![CDATA[%s]]></FromUserName>
		<CreateTime>%s</CreateTime>
		<MsgType><![CDATA[music]]></MsgType>
		$itemStr
		</xml>";
		
		$result = sprintf($textTpl,$obj->FromUserName,$obj->ToUserName,time());
		return $result;
	}
	
	
	private function transmitImage($obj,$imageArray){
		$itemTpl = "<Image>
		<MediaId><![CDATA[%s]]></MediaId>
		</Image>";
		
		$itemStr =sprintf($itemTpl,$imageArray['MediaId']);
	
		$textTpl = "<xml>
		<ToUserName><![CDATA[%s]]></ToUserName>
		<FromUserName><![CDATA[%s]]></FromUserName>
		<CreateTime>%s</CreateTime>
		<MsgType><![CDATA[image]]></MsgType>
		$itemStr
		</xml>";
		
		$result = sprintf($textTpl,$obj->FromUserName,$obj->ToUserName,time());
		return $result;
	}
	
	private function transmitVoice($obj,$voiceArray){
		$itemTpl = "<Voice>
		<MediaId><![CDATA[%s]]></MediaId>
		</Voice>";
		
		$itemStr =sprintf($itemTpl,$voiceArray['MediaId']);
	
		$textTpl = "<xml>
		<ToUserName><![CDATA[%s]]></ToUserName>
		<FromUserName><![CDATA[%s]]></FromUserName>
		<CreateTime>%s</CreateTime>
		<MsgType><![CDATA[voice]]></MsgType>
		$itemStr
		</xml>";
		
		$result = sprintf($textTpl,$obj->FromUserName,$obj->ToUserName,time());
		return $result;
	}
	
	
	private function transmitVideo($obj,$videoArray){
		$itemTpl = "<Video>
		<MediaId><![CDATA[%s]]></MediaId>
		<ThumbMediaId><![CDATA[%s]]></ThumbMediaId>
		<Title><![CDATA[%s]]></Title>
		<Description><![CDATA[%s]]></Description>
		</Video>";
		
		$itemStr =sprintf($itemTpl,$videoArray['MediaId'],$videoArray['ThumbMediaId'],$videoArray['Title'],$videoArray['Description']);
	
		$textTpl = "<xml>
		<ToUserName><![CDATA[%s]]></ToUserName>
		<FromUserName><![CDATA[%s]]></FromUserName>
		<CreateTime>%s</CreateTime>
		<MsgType><![CDATA[video]]></MsgType>
		$itemStr
		</xml>";
		
		$result = sprintf($textTpl,$obj->FromUserName,$obj->ToUserName,time());
		return $result;
	}
	
	private function transmitNews($obj,$arr_item){
	
		if(!is_array($arr_item))
			return;
			
		$itemTpl = "<item>
		<Title><![CDATA[%s]]></Title>
		<Description><![CDATA[%s]]></Description>
		<PicUrl><![CDATA[%s]]></PicUrl>
		<Url><![CDATA[%s]]></Url>
		</item>";
				
		$itemStr = "";
		foreach ($arr_item as $item)
			$itemStr .= sprintf($itemTpl,$item['Title'],$item['Description'],$item['PicUrl'],$item['Url']);
	
		$newsTpl = "<xml>
		<ToUserName><![CDATA[%s]]></ToUserName>
		<FromUserName><![CDATA[%s]]></FromUserName>
		<CreateTime>%s</CreateTime>
		<MsgType><![CDATA[news]]></MsgType>
		<Content><![CDATA[]]></Content>
		<ArticleCount>%s</ArticleCount>
		<Articles>$itemStr</Articles>
		</xml>";
		
		$result = sprintf($newsTpl,$obj->FromUserName,$obj->ToUserName,time(),count($arr_item));
		return $result;
	}
	
	private function echoDCMsg($obj){
		$textTpl = "<xml>
		<ToUserName><![CDATA[%s]]></ToUserName>
		<FromUserName><![CDATA[%s]]></FromUserName>
		<CreateTime>%s</CreateTime>
		<MsgType><![CDATA[text]]></MsgType>
		<Content><![CDATA[%s]></Content>
		</xml>";
		$result = sprintf($textTpl,$obj->FromUserName,$obj->ToUserName,time(),"DC UCenter");
		return $result;
	}
	
	

}


?>