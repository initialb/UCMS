<<<<<<< .mine
﻿<?php
/**
  * Cobolii : http://cobolii.sinaapp.com
	Author : BCH 
	Date : 2014.05.22
	Update(Zhuanyangqian) : 2015.12.28
  */

  
require_once(dirname(__FILE__).'/'.'utility.php');
//require_once(dirname(__FILE__).'/'.'menu.php');
require_once(dirname(__FILE__).'/'.'SaeMysql.php');
require_once(dirname(__FILE__).'/'.'CCInterface.php');

//define your token
//define("TOKEN", "Cobolii");
$wechatObj = new wechatCallbackapiTest();
if(isset($_GET['echostr'])){
	$wechatObj->valid();
}else{
	$wechatObj->responseMsg();
}

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
				/*
				$textTpl = "<xml>
				<ToUserName><![CDATA[%s]]></ToUserName>
				<FromUserName><![CDATA[%s]]></FromUserName>
				<CreateTime>%s</CreateTime>
				<MsgType><![CDATA[text]]></MsgType>
				<Content><![CDATA[%s]]></Content>
				</xml>";
				
				$result = sprintf($textTpl,$postObj->FromUserName,$postObj->ToUserName,time(),"您发送的是文本消息，内容如下：".$postObj->Content);
				
				//$result = $this->receiveText($postObj);
				echo $result;
				sae_debug($result);
				
				*/
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
				//$DCMsg = $this->echoDCMsg($postObj);
				//sae_debug($DCMsg);
				//echo $DCMsg;

				
				
        }else {
        	echo "";
        	exit;
        }
    }
	
	private function receiveText($obj){
	//	$content = "您发送的是文本消息，内容如下：" . $obj->Content;
	//$content ="欢迎参加ZYQ公众号测试｜Welcome to join the test of Zhuanyangqian's Public WX Account";
	//		$result = $this->transmitText($obj,$content);
		$keyword = trim($obj->Content);
		
		if(! (strcmp("文本",$keyword) && strcmp("text",$keyword))){
			$content ="欢迎参加ZYQ公众号测试｜Welcome to join the test of Zhuanyangqian's Public WX Account";
			$result = $this->transmitText($obj,$content);
		}elseif(! (strcmp("音乐",$keyword) && strcmp("music",$keyword))){
			$content = array("Title"=>"Are You With Me",
			"Description" => "歌手:Emma Lauwers",
			"MusicUrl" =>"http://cobolii.sinaapp.com/Are.You.With.Me-Emma.Lauwers.mp3",
			"HQMusicUrl" =>"http://cobolii.sinaapp.com/Are.You.With.Me-Emma.Lauwers.mp3");
			$result = $this->transmitMusic($obj,$content);
		}elseif($keyword == "图文" || $keyword == "单图文"){
			$content = array();
			$content[] =array("Title"=> "公司介绍",
				"Description"=>"Zhuanyangqian Introduction",
				"PicUrl"=>"http://cobolii.sinaapp.com/IMG_6747.JPG",
				"Url"=>"http://139.196.16.157/");
			$result = $this->transmitNews($obj,$content);
		}elseif($keyword == "多图文"){
			$content = array();
			
			$content[] =array("Title"=> "美元非保本理财产品收益对比",
				"Description"=>"各银行美元非保本理财产品收益对比",
				"PicUrl"=>"http://cobolii.sinaapp.com/IMG_6747.JPG",
				"Url"=>"http://139.196.16.157/");
			$content[] =array("Title"=> "美元保本理财产品收益对比",
				"Description"=>"各银行美元保本理财产品收益对比",
				"PicUrl"=>"http://cobolii.sinaapp.com/IMG_6747.JPG",
				"Url"=>"http://139.196.16.157/");
			$content[] =array("Title"=> "欧元非保本理财产品收益对比",
				"Description"=>"各银行欧元非保本理财产品收益对比",
				"PicUrl"=>"http://cobolii.sinaapp.com/IMG_6747.JPG",
				"Url"=>"http://139.196.16.157/");	
			$content[] =array("Title"=> "欧元保本理财产品收益对比",
				"Description"=>"各银行欧元保本理财产品收益对比",
				"PicUrl"=>"http://cobolii.sinaapp.com/IMG_6747.JPG",
				"Url"=>"http://139.196.16.157/");	
			$result = $this->transmitNews($obj,$content);
		}else{
			$content ="您发送的是文本消息，内容如下：" . $keyword;
			$result = $this->transmitText($obj,$content);
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
		switch ($obj-Event){
			case "subscribe":
				$content = "欢迎关注赚洋钱微信公众号";
				break;
			case "unsubscribe":
				$content = "";
				break;
		}
		$result = $this->transmitText($obj,$content);
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

||||||| .r108
﻿<?php
/**
  * Cobolii : http://cobolii.sinaapp.com
	Author : BCH 
	Date : 2014.05.22
	Update(Zhuanyangqian) : 2015.12.28
  */

  
require_once(dirname(__FILE__).'/'.'utility.php');
//require_once(dirname(__FILE__).'/'.'menu.php');
require_once(dirname(__FILE__).'/'.'SaeMysql.php');
require_once(dirname(__FILE__).'/'.'CCInterface.php');

//define your token
define("TOKEN", "Cobolii");
$wechatObj = new wechatCallbackapiTest();
if(isset($_GET['echostr'])){
	$wechatObj->valid();
}else{
	$wechatObj->responseMsg();
}

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
				/*
				$textTpl = "<xml>
				<ToUserName><![CDATA[%s]]></ToUserName>
				<FromUserName><![CDATA[%s]]></FromUserName>
				<CreateTime>%s</CreateTime>
				<MsgType><![CDATA[text]]></MsgType>
				<Content><![CDATA[%s]]></Content>
				</xml>";
				
				$result = sprintf($textTpl,$postObj->FromUserName,$postObj->ToUserName,time(),"您发送的是文本消息，内容如下：".$postObj->Content);
				
				//$result = $this->receiveText($postObj);
				echo $result;
				sae_debug($result);
				
				*/
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
				//$DCMsg = $this->echoDCMsg($postObj);
				//sae_debug($DCMsg);
				//echo $DCMsg;

				
				
        }else {
        	echo "";
        	exit;
        }
    }
	
	private function receiveText($obj){
	//	$content = "您发送的是文本消息，内容如下：" . $obj->Content;
	//$content ="欢迎参加ZYQ公众号测试｜Welcome to join the test of Zhuanyangqian's Public WX Account";
	//		$result = $this->transmitText($obj,$content);
		$keyword = trim($obj->Content);
		
		if(! (strcmp("文本",$keyword) && strcmp("text",$keyword))){
			$content ="欢迎参加ZYQ公众号测试｜Welcome to join the test of Zhuanyangqian's Public WX Account";
			$result = $this->transmitText($obj,$content);
		}elseif(! (strcmp("音乐",$keyword) && strcmp("music",$keyword))){
			$content = array("Title"=>"Are You With Me",
			"Description" => "歌手:Emma Lauwers",
			"MusicUrl" =>"http://cobolii.sinaapp.com/Are.You.With.Me-Emma.Lauwers.mp3",
			"HQMusicUrl" =>"http://cobolii.sinaapp.com/Are.You.With.Me-Emma.Lauwers.mp3");
			$result = $this->transmitMusic($obj,$content);
		}elseif($keyword == "图文" || $keyword == "单图文"){
			$content = array();
			$content[] =array("Title"=> "公司介绍",
				"Description"=>"Zhuanyangqian Introduction",
				"PicUrl"=>"http://cobolii.sinaapp.com/IMG_6747.JPG",
				"Url"=>"http://139.196.16.157/");
			$result = $this->transmitNews($obj,$content);
		}elseif($keyword == "多图文"){
			$content = array();
			
			$content[] =array("Title"=> "美元非保本理财产品收益对比",
				"Description"=>"各银行美元非保本理财产品收益对比",
				"PicUrl"=>"http://cobolii.sinaapp.com/IMG_6747.JPG",
				"Url"=>"http://139.196.16.157/");
			$content[] =array("Title"=> "美元保本理财产品收益对比",
				"Description"=>"各银行美元保本理财产品收益对比",
				"PicUrl"=>"http://cobolii.sinaapp.com/IMG_6747.JPG",
				"Url"=>"http://139.196.16.157/");
			$content[] =array("Title"=> "欧元非保本理财产品收益对比",
				"Description"=>"各银行欧元非保本理财产品收益对比",
				"PicUrl"=>"http://cobolii.sinaapp.com/IMG_6747.JPG",
				"Url"=>"http://139.196.16.157/");	
			$content[] =array("Title"=> "欧元保本理财产品收益对比",
				"Description"=>"各银行欧元保本理财产品收益对比",
				"PicUrl"=>"http://cobolii.sinaapp.com/IMG_6747.JPG",
				"Url"=>"http://139.196.16.157/");	
			$result = $this->transmitNews($obj,$content);
		}else{
			$content ="您发送的是文本消息，内容如下：" . $keyword;
			$result = $this->transmitText($obj,$content);
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
		switch ($obj-Event){
			case "subscribe":
				$content = "欢迎关注赚洋钱微信公众号";
				break;
			case "unsubscribe":
				$content = "";
				break;
		}
		$result = $this->transmitText($obj,$content);
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

=======
﻿<?php
/**
  * Cobolii : http://cobolii.sinaapp.com
	Author : BCH 
	Date : 2014.05.22
	Update(Zhuanyangqian) : 2015.12.28
  */

  
require_once(dirname(__FILE__).'/'.'utility.php');
//require_once(dirname(__FILE__).'/'.'menu.php');
require_once(dirname(__FILE__).'/'.'SaeMysql.php');
require_once(dirname(__FILE__).'/'.'CCInterface.php');

//define your token
//define("TOKEN", "Cobolii");

traceHttp();

$wechatObj = new wechatCallbackapiTest();
if(isset($_GET['echostr'])){
	$wechatObj->valid();
}else{
	$wechatObj->responseMsg();
}

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
				/*
				$textTpl = "<xml>
				<ToUserName><![CDATA[%s]]></ToUserName>
				<FromUserName><![CDATA[%s]]></FromUserName>
				<CreateTime>%s</CreateTime>
				<MsgType><![CDATA[text]]></MsgType>
				<Content><![CDATA[%s]]></Content>
				</xml>";
				
				$result = sprintf($textTpl,$postObj->FromUserName,$postObj->ToUserName,time(),"您发送的是文本消息，内容如下：".$postObj->Content);
				
				//$result = $this->receiveText($postObj);
				echo $result;
				sae_debug($result);
				
				*/
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
				//$DCMsg = $this->echoDCMsg($postObj);
				//sae_debug($DCMsg);
				//echo $DCMsg;

				
				
        }else {
        	echo "";
        	exit;
        }
    }
	
	private function receiveText($obj){
	//	$content = "您发送的是文本消息，内容如下：" . $obj->Content;
	//$content ="欢迎参加ZYQ公众号测试｜Welcome to join the test of Zhuanyangqian's Public WX Account";
	//		$result = $this->transmitText($obj,$content);
		$keyword = trim($obj->Content);
		
		if(! (strcmp("文本",$keyword) && strcmp("text",$keyword))){
			$content ="欢迎参加ZYQ公众号测试｜Welcome to join the test of Zhuanyangqian's Public WX Account";
			$result = $this->transmitText($obj,$content);
		}elseif(! (strcmp("音乐",$keyword) && strcmp("music",$keyword))){
			$content = array("Title"=>"Are You With Me",
			"Description" => "歌手:Emma Lauwers",
			"MusicUrl" =>"http://cobolii.sinaapp.com/Are.You.With.Me-Emma.Lauwers.mp3",
			"HQMusicUrl" =>"http://cobolii.sinaapp.com/Are.You.With.Me-Emma.Lauwers.mp3");
			$result = $this->transmitMusic($obj,$content);
		}elseif($keyword == "图文" || $keyword == "单图文"){
			$content = array();
			$content[] =array("Title"=> "公司介绍",
				"Description"=>"Zhuanyangqian Introduction",
				"PicUrl"=>"http://cobolii.sinaapp.com/IMG_6747.JPG",
				"Url"=>"http://139.196.16.157/");
			$result = $this->transmitNews($obj,$content);
		}elseif($keyword == "多图文"){
			$content = array();
			
			$content[] =array("Title"=> "美元非保本理财产品收益对比",
				"Description"=>"各银行美元非保本理财产品收益对比",
				"PicUrl"=>"http://cobolii.sinaapp.com/IMG_6747.JPG",
				"Url"=>"http://139.196.16.157/");
			$content[] =array("Title"=> "美元保本理财产品收益对比",
				"Description"=>"各银行美元保本理财产品收益对比",
				"PicUrl"=>"http://cobolii.sinaapp.com/IMG_6747.JPG",
				"Url"=>"http://139.196.16.157/");
			$content[] =array("Title"=> "欧元非保本理财产品收益对比",
				"Description"=>"各银行欧元非保本理财产品收益对比",
				"PicUrl"=>"http://cobolii.sinaapp.com/IMG_6747.JPG",
				"Url"=>"http://139.196.16.157/");	
			$content[] =array("Title"=> "欧元保本理财产品收益对比",
				"Description"=>"各银行欧元保本理财产品收益对比",
				"PicUrl"=>"http://cobolii.sinaapp.com/IMG_6747.JPG",
				"Url"=>"http://139.196.16.157/");	
			$result = $this->transmitNews($obj,$content);
		}else{
			$content ="您发送的是文本消息，内容如下：" . $keyword;
			$result = $this->transmitText($obj,$content);
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
		switch ($obj-Event){
			case "subscribe":
				$content = "欢迎关注赚洋钱微信公众号";
				break;
			case "unsubscribe":
				$content = "";
				break;
		}
		$result = $this->transmitText($obj,$content);
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

>>>>>>> .r111
?>