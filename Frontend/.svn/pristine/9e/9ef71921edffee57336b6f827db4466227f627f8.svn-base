<?php
header("content-type:text/html; charset=utf-8");
/**
  * Cobolii : http://zhuanyangqian.sinaapp.com
	Author : BCH 
	Date : 2016.02.22
  */

require_once(dirname(__FILE__).'/'.'utility.php');
require_once(dirname(__FILE__).'/'.'menu.php');
require_once(dirname(__FILE__).'/'.'SaeMysql.php');
require_once(dirname(__FILE__).'/'.'CCInterface.php');

//define your token
//define("TOKEN", "ZhuanYangQian");



$wechatMenu = new Menu();
//$wechatMenu->delete();
$errCode = $wechatMenu->view();
if (0 != $errCode ){
//$wechatMenu->delete();
//$wechatMenu->view();
	$ret = $wechatMenu->create();
	sae_debug($ret);
	exit; 
}
//exit;


$wechatObj = new wechatCallbackapiTest();

if(isset($_GET['echostr'])){

	$wechatObj->valid();
}else{
    sae_debug("responseMsg ok!");
	$wechatObj->responseMsg();
}

class wechatCallbackapiTest
{
	public function valid()
    {
        $echoStr = $_GET["echostr"];

        //valid signature , option
        if($this->checkSignature()){
            //sae_debug("echostr:".$echoStr);
            //sae_debug("GET-echostr:".$_GET["echostr"]);
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
        // sae_debug($token);
		$tmpArr = array($token, $timestamp, $nonce);
		sort($tmpArr, SORT_STRING);
		$tmpStr = implode( $tmpArr );
		$tmpStr = sha1( $tmpStr );
        sae_debug("tempstr : ".$tmpStr);
        sae_debug("signature: ".$signature);
		
		if( $tmpStr == $signature ){
            //echo $_GET["echostr"];
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
		$content = "您发送的是文本消息，内容如下：" . $obj->Content;
		$content ="欢迎参加赚洋钱服务号测试｜Welcome to join the test of Zhuanyangqian's Service Wechat Account";
		$result = $this->transmitText($obj,$content);
		$keyword = trim($obj->Content);
		
		switch ($keyword){
			case "文本":
			case "text":
				$content ="欢迎参加赚洋钱服务号测试｜Welcome to join the test of Zhuanyangqian's Service Wechat Account";
				$result = $this->transmitText($obj,$content);	
				break;
			case "音乐":
			case "music":
				$content = array("Title"=>"Are You With Me",
				"Description" => "歌手:Emma Lauwers",
				"MusicUrl" =>"http://cobolii.sinaapp.com/Are.You.With.Me-Emma.Lauwers.mp3",
				"HQMusicUrl" =>"http://cobolii.sinaapp.com/Are.You.With.Me-Emma.Lauwers.mp3");
				$result = $this->transmitMusic($obj,$content);				
				break;
			case "多图文":
				$content = array();
				$content[] =array("Title"=> "在售外汇理财产品信息",
					"Description"=>"00head20160101.html",
					"PicUrl"=>"http://cobolii.sinaapp.com/img/head.jpg",
					"Url"=>"http://cobolii.sinaapp.com/bootstrap/00head20160101.html");
				$content[] =array("Title"=> "央妈干预，离岸人民币大涨700点（附各主要银行人民币汇率牌价）",
					"Description"=>"附各主要银行人民币汇率牌价",
					"PicUrl"=>"http://cobolii.sinaapp.com/img/titel01.png",
					"Url"=>"http://cobolii.sinaapp.com/bootstrap/01titel20160101.html");
				$content[] =array("Title"=> "联储加息，意欲何为？非农就业数据为你解答",
					"Description"=>"非农就业数据为你解答",
					"PicUrl"=>"http://cobolii.sinaapp.com/img/titel02.png",
					"Url"=>"http://cobolii.sinaapp.com/bootstrap/02titel20160101.html");
				$content[] =array("Title"=> "全球性熊市的来临 一图让你看懂全球资产收益的下跌",
					"Description"=>"一图让你看懂全球资产收益的下跌",
					"PicUrl"=>"http://cobolii.sinaapp.com/img/titel03.png",
					"Url"=>"http://cobolii.sinaapp.com/bootstrap/03titel20160101.html");	
				$content[] =array("Title"=> "如何识别外汇理财产品的收益与风险",
					"Description"=>"如何识别外汇理财产品的收益与风险",
					"PicUrl"=>"http://cobolii.sinaapp.com/img/titel04.png",
					"Url"=>"http://cobolii.sinaapp.com/bootstrap/04titel20160101.html");	
				$result = $this->transmitNews($obj,$content);				
				break;
			case "图文":
			case "单图文":
				$content = array();
				$content[] =array("Title"=> "公司介绍",
					"Description"=>"Zhuanyangqian Introduction",
					"PicUrl"=>"http://cobolii.sinaapp.com/IMG_6747.JPG",
					"Url"=>"http://139.196.16.157/");
				$result = $this->transmitNews($obj,$content);
				break;
			case "000":
				$content = array();
				$content[] =array("Title"=> "美元理财产品收益比较(2016.01.01)",
					"Description"=>"更多美元理财产品收益比较",
					"PicUrl"=>"http://cobolii.sinaapp.com/img/head.jpg",
					"Url"=>"http://cobolii.sinaapp.com/bootstrap/000.html");
				$result = $this->transmitNews($obj,$content);			
				break;
			case "011":
				$content = array();
				$content[] =array("Title"=> "在售美元保本理财产品(2016.01.01)",
					"Description"=>"更多在售美元保本理财产品",
					"PicUrl"=>"http://cobolii.sinaapp.com/img/head.jpg",
					"Url"=>"http://cobolii.sinaapp.com/bootstrap/011.html");
				$result = $this->transmitNews($obj,$content);			
				break;	
			case "012":
				$content = array();
				$content[] =array("Title"=> "在售美元非保本理财产品(2016.01.01)",
					"Description"=>"更多在售美元非保本理财产品",
					"PicUrl"=>"http://cobolii.sinaapp.com/img/head.jpg",
					"Url"=>"http://cobolii.sinaapp.com/bootstrap/012.html");
				$result = $this->transmitNews($obj,$content);			
				break;		

			case "101":
				$content = array();
				$content[] =array("Title"=> "精选在售外汇理财产品",
					"Description"=>"menuitems/A11.html",
					"PicUrl"=>"http://".WEB_SITE."/img/A11.jpg",
					"Url"=>WEB_SITE."/menuitems/A11.html");
				$result = $this->transmitNews($obj,$content);	
				break;
			case "102":
				$content = array();			
				$content[] =array("Title"=> "在售美元非保本理财产品信息",
					"Description"=>"menuitems/A12.html",
					"PicUrl"=>"http://".WEB_SITE."/img/A12.jpg",
					"Url"=>WEB_SITE."/menuitems/A12.html");
				$result = $this->transmitNews($obj,$content);					
				break;				
			case "103":
				$content = array();	
				$content[] =array("Title"=> "在售美元保本理财产品信息",
					"Description"=>"menuitems/A13.html",
					"PicUrl"=>"http://".WEB_SITE."/img/A13.jpg",
					"Url"=>WEB_SITE."/menuitems/A13.html");				
				$result = $this->transmitNews($obj,$content);			
				break;
			case "104":
				$content = array();	
				$content[] =array("Title"=> "在售非美元理财产品信息",
					"Description"=>"menuitems/A14.html",
					"PicUrl"=>"http://".WEB_SITE."/img/A14.jpg",
					"Url"=>WEB_SITE."/menuitems/A14.html");				
				$result = $this->transmitNews($obj,$content);			
				break;
			case "105":
				$content = array();	
				$content[] =array("Title"=> "美元理财产品收益比较",
					"Description"=>"menuitems/A15.html",
					"PicUrl"=>"http://".WEB_SITE."/img/A15.jpg",
					"Url"=>WEB_SITE."/menuitems/A15.html");				
				$result = $this->transmitNews($obj,$content);			
				break;
			case "201":
				$content = array();		
				$content[] =array("Title"=> "美元兑人民币实时牌价",
					"Description"=>"提供国内主要银行美元兑人民币实时牌价",
					"PicUrl"=>"http://".WEB_SITE."/img/A21.jpg",
					"Url"=>WEB_SITE."/dynamic/A21.php");				
				$result = $this->transmitNews($obj,$content);			
				break;
			case "202":
				$content = array();	
				$content[] =array("Title"=> "英镑兑人民币实时牌价",
					"Description"=>"提供国内主要银行英镑兑人民币实时牌价",
					"PicUrl"=>"http://".WEB_SITE."/img/A22.jpg",
					"Url"=>WEB_SITE."/dynamic/A22.php");				
				$result = $this->transmitNews($obj,$content);			
				break;
			case "203":
				$content = array();
				$content[] =array("Title"=> "欧元兑人民币实时牌价",
					"Description"=>"提供国内主要银行欧元兑人民币实时牌价",
					"PicUrl"=>"http://".WEB_SITE."/img/A23.jpg",
					"Url"=>WEB_SITE."/dynamic/A23.php");				
				$result = $this->transmitNews($obj,$content);			
				break;
			case "204":
				$content = array();	
				$content[] =array("Title"=> "澳元兑人民币实时牌价",
					"Description"=>"提供国内主要银行澳元兑人民币实时牌价",
					"PicUrl"=>"http://".WEB_SITE."/img/A24.jpg",
					"Url"=>WEB_SITE."/dynamic/A24.php");					
				$result = $this->transmitNews($obj,$content);			
				break;
			case "205":
				$content = array();					
				$content[] =array("Title"=> "日元兑人民币实时牌价",
					"Description"=>"提供国内主要银行日元兑人民币实时牌价",
					"PicUrl"=>"http://".WEB_SITE."/img/A25.jpg",
					"Url"=>WEB_SITE."/dynamic/A25.php");
				$result = $this->transmitNews($obj,$content);					
				break;					
			case "301":
				$content = array();	
				$content[] =array("Title"=> "\"赚洋钱\"最高预期收益外债精选",
					"Description"=>"menuitems/A31.html",
					"PicUrl"=>"http://".WEB_SITE."/img/A31.jpg",
					"Url"=>WEB_SITE."/menuitems/A31.html");					
				$result = $this->transmitNews($obj,$content);			
				break;
			case "302":
				$content = array();		
				$content[] =array("Title"=> "\"赚洋钱\"各安全等级外币债券推荐",
					"Description"=>"menuitems/A32.html",
					"PicUrl"=>"http://".WEB_SITE."/img/A32.jpg",
					"Url"=>WEB_SITE."/menuitems/A32.html");					
				$result = $this->transmitNews($obj,$content);			
				break;
			case "411":
				$content = array();	
				$content[] =array("Title"=> "海外最佳表现股票基金(综合评价)",
					"Description"=>"menuitems/B11.html",
					"PicUrl"=>"http://".WEB_SITE."/img/B11.jpg",
					"Url"=>WEB_SITE."/menuitems/B11.html");			
				$result = $this->transmitNews($obj,$content);			
				break;
			case "412":
				$content = array();	
				$content[] =array("Title"=> "当月海外最佳表现股票基金(实际收益)",
					"Description"=>"menuitems/B12.html",
					"PicUrl"=>"http://".WEB_SITE."/img/B12.jpg",
					"Url"=>WEB_SITE."/menuitems/B12.html");			
				$result = $this->transmitNews($obj,$content);			
				break;
			case "413":
				$content = array();		
				$content[] =array("Title"=> "\"赚洋钱\"推荐股票基金",
					"Description"=>"menuitems/B13.html",
					"PicUrl"=>"http://".WEB_SITE."/img/B13.jpg",
					"Url"=>WEB_SITE."/menuitems/B13.html");			
				$result = $this->transmitNews($obj,$content);			
				break;
			case "421":
				$content = array();	
				$content[] =array("Title"=> "海外最佳表现债券基金(综合评价)",
					"Description"=>"menuitems/B21.html",
					"PicUrl"=>"http://".WEB_SITE."/img/B21.jpg",
					"Url"=>WEB_SITE."/menuitems/B21.html");				
				$result = $this->transmitNews($obj,$content);			
				break;
			case "423":
				$content = array();					
				$content[] =array("Title"=> "'赚洋钱'推荐债券基金",
					"Description"=>"menuitems/B23.html",
					"PicUrl"=>"http://".WEB_SITE."/img/B23.jpg",
					"Url"=>WEB_SITE."/menuitems/B23.html");	
				break;
			case "431":
				$content = array();					
				$content[] =array("Title"=> "海外最佳表现平衡基金(综合评价)",
					"Description"=>"menuitems/B31.html",
					"PicUrl"=>"http://".WEB_SITE."/img/B31.jpg",
					"Url"=>WEB_SITE."/menuitems/B31.html");	
				break;		
			case "441":
				$content = array();	
				$content[] =array("Title"=> "海外最佳表现商品基金(综合评价)",
					"Description"=>"menuitems/B41.html",
					"PicUrl"=>"http://".WEB_SITE."/img/B41.jpg",
					"Url"=>WEB_SITE."/menuitems/B41.html");	
				break;
			case "443":
				$content = array();	
				$content[] =array("Title"=> "\"赚洋钱\"推荐商品基金",
					"Description"=>"menuitems/B43.html",
					"PicUrl"=>"http://".WEB_SITE."/img/B43.jpg",
					"Url"=>WEB_SITE."/menuitems/C5.html");	
				break;					
			case "500":
				$content = array();		
				$content[] =array("Title"=> "\"赚洋钱\"投资组合",
					"Description"=>"menuitems/B50.html",
					"PicUrl"=>"http://".WEB_SITE."/img/B50.jpg",
					"Url"=>WEB_SITE."/menuitems/C5.html");					
				$result = $this->transmitNews($obj,$content);			
				break;
			case "900":
				$content = array();
				$content[] =array("Title"=> "在售外汇理财(A.T.)",
					"Description"=>"栏目介绍",
					"PicUrl"=>"http://".WEB_SITE."/img/A10.jpg",
					"Url"=>WEB_SITE."/menuitems/A10.html");
				$content[] =array("Title"=> "精选在售外汇理财产品(A.T.)",
					"Description"=>"menuitems/A11.html",
					"PicUrl"=>"http://".WEB_SITE."/img/A11.jpg",
					"Url"=>WEB_SITE."/dynamic/A11.php");
				$content[] =array("Title"=> "在售美元非保本理财产品信息(A.T.)",
					"Description"=>"menuitems/A12.html",
					"PicUrl"=>"http://".WEB_SITE."/img/A12.jpg",
					"Url"=>WEB_SITE."/dynamic/A12.php");
				$content[] =array("Title"=> "在售美元保本理财产品信息(A.T.)",
					"Description"=>"menuitems/A13.html",
					"PicUrl"=>"http://".WEB_SITE."/img/A13.jpg",
					"Url"=>WEB_SITE."/dynamic/A13.php");
				$content[] =array("Title"=> "在售非美元理财产品信息(A.T.)",
					"Description"=>"menuitems/A14.html",
					"PicUrl"=>"http://".WEB_SITE."/img/A14.jpg",
					"Url"=>WEB_SITE."/dynamic/A14.php");	
				$content[] =array("Title"=> "美元理财产品收益比较(A.T.)",
					"Description"=>"menuitems/A15.html",
					"PicUrl"=>"http://".WEB_SITE."/img/A15.jpg",
					"Url"=>WEB_SITE."/dynamic/A15.php");	
				$result = $this->transmitNews($obj,$content);		
				break;	
			case "901":
				$content = array();	
				$content[] =array("Title"=> "海外债券",
					"Description"=>"栏目介绍",
					"PicUrl"=>"http://".WEB_SITE."/img/A30.jpg",
					"Url"=>WEB_SITE."/menuitems/A30.html");				
				$content[] =array("Title"=> "最高预期收益外债精选(A.T.)",
					"Description"=>"dynamic/A31.php",
					"PicUrl"=>"http://".WEB_SITE."/img/A31.jpg",
					"Url"=>WEB_SITE."/dynamic/A31.php");
				$content[] =array("Title"=> "各安全等级外币债券推荐(A.T.)",
					"Description"=>"dynamic/A32.php",
					"PicUrl"=>"http://".WEB_SITE."/img/A32.jpg",
					"Url"=>WEB_SITE."/dynamic/A32.php");					
				$result = $this->transmitNews($obj,$content);			
				break;	
			case "902":
				$content = array();
				$content[] =array("Title"=> "海外基金(A.T.)",
					"Description"=>"栏目介绍",
					"PicUrl"=>"http://".WEB_SITE."/img/B10.jpg",
					"Url"=>WEB_SITE."/menuitems/B10.html");			
				$content[] =array("Title"=> "海外股票基金分类综合评价(A.T.)",
					"Description"=>"menuitems/B11.html",
					"PicUrl"=>"http://".WEB_SITE."/img/B11.jpg",
					"Url"=>WEB_SITE."/dynamic/B11.php");
				$content[] =array("Title"=> "海外股票基金最佳表现优选(A.T.)",
					"Description"=>"menuitems/B12.html",
					"PicUrl"=>"http://".WEB_SITE."/img/B12.jpg",
					"Url"=>WEB_SITE."/dynamic/B12.php");
				$content[] =array("Title"=> "\"赚洋钱\"推荐股票基金(A.T.)",
					"Description"=>"menuitems/B13.html",
					"PicUrl"=>"http://".WEB_SITE."/img/B13.jpg",
					"Url"=>WEB_SITE."/dynamic/B13.php");	
				$content[] =array("Title"=> "海外债券基金分类综合评价(A.T.)",
					"Description"=>"menuitems/B21.html",
					"PicUrl"=>"http://".WEB_SITE."/img/B21.jpg",
					"Url"=>WEB_SITE."/dynamic/B21.php");
				$content[] =array("Title"=> "'赚洋钱'推荐债券基金(A.T.)",
					"Description"=>"menuitems/B23.html",
					"PicUrl"=>"http://".WEB_SITE."/img/B23.jpg",
					"Url"=>WEB_SITE."/dynamic/B23.php");
				$content[] =array("Title"=> "海外最佳表现平衡基金(综合评价)(A.T.)",
					"Description"=>"menuitems/B31.html",
					"PicUrl"=>"http://".WEB_SITE."/img/B31.jpg",
					"Url"=>WEB_SITE."/dynamic/B31.php");
				$content[] =array("Title"=> "海外最佳表现商品基金(综合评价)(A.T.)",
					"Description"=>"menuitems/B41.html",
					"PicUrl"=>"http://".WEB_SITE."/img/B41.jpg",
					"Url"=>WEB_SITE."/dynamic/B41.php");
				$content[] =array("Title"=> "\"赚洋钱\"推荐商品基金",
					"Description"=>"menuitems/B43.html",
					"PicUrl"=>"http://".WEB_SITE."/img/B43.jpg",
					"Url"=>WEB_SITE."/menuitems/C5.html");					
				$result = $this->transmitNews($obj,$content);				
				break;	
			case "903":
				$content = array();		
				$content[] =array("Title"=> "2016年全球投资展望：控制住你的热情",
					"Description"=>"menuitems/A5-20160422S.html",
					"PicUrl"=>"http://".WEB_SITE."/img/A5-20160422S-000.jpg",
					"Url"=>WEB_SITE."/menuitems/A5-20160422S.html");	
				$content[] =array("Title"=> "透过美联储的加息困境看美国经济前景",
					"Description"=>"menuitems/A4-20160424.html",
					"PicUrl"=>"http://".WEB_SITE."/img/A4-20160424-000.jpg",
					"Url"=>WEB_SITE."/menuitems/A4-20160424.html");		
				$content[] =array("Title"=> "一周市场综述(2016.04.18-2016.04.24)",
					"Description"=>"menuitems/A4-20160424.html",
					"PicUrl"=>"http://".WEB_SITE."/img/weeklyhead.jpg",
					"Url"=>WEB_SITE."/menuitems/2016W18.html");						
				$result = $this->transmitNews($obj,$content);			
				break;			
			case "999":
				$content = array();		
				$content[] =array("Title"=> "JS测试",
					"Description"=>"weixinjs.html",
					"PicUrl"=>"http://".WEB_SITE."/img/B50.jpg",
					"Url"=>WEB_SITE."/sample.php");					
				$result = $this->transmitNews($obj,$content);			
				break;
			default:
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
		switch ($obj->Event){
			case "subscribe":
				$content = "欢迎关注赚洋钱微信服务号";
				$result = $this->transmitText($obj,$content);
				break;
			case "unsubscribe":
				$content = "";
				$result = $this->transmitText($obj,$content);
				break;
			case "VIEW":
				break;
			case "CLICK":
//				sae_debug($obj->Event);
//				sae_debug($obj->EventKey);				
//				$content = $obj->EventKey;
				$result = $this->responseMenu($obj);
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
		<Content><![CDATA[赚洋钱微信服务号 :\n %s\n %s]]></Content>
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
		$result = sprintf($textTpl,$obj->FromUserName,$obj->ToUserName,time(),"赚洋钱微信服务号");
		return $result;
	}
	
	private function responseMenu($obj){
		switch ($obj->EventKey){
			case "A1":
				$content = array();
				$content[] =array("Title"=> "在售外汇理财",
					"Description"=>"栏目介绍",
					"PicUrl"=>"http://".WEB_SITE."/img/A10.jpg",
					"Url"=>WEB_SITE."/menuitems/A10.html");
				$content[] =array("Title"=> "精选在售外汇理财产品",
					"Description"=>"menuitems/A11.html",
					"PicUrl"=>"http://".WEB_SITE."/img/A11.jpg",
					"Url"=>WEB_SITE."/dynamic/A11.php");
				$content[] =array("Title"=> "在售美元非保本理财产品信息",
					"Description"=>"menuitems/A12.html",
					"PicUrl"=>"http://".WEB_SITE."/img/A12.jpg",
					"Url"=>WEB_SITE."/dynamic/A12.php");
				$content[] =array("Title"=> "在售美元保本理财产品信息",
					"Description"=>"menuitems/A13.html",
					"PicUrl"=>"http://".WEB_SITE."/img/A13.jpg",
					"Url"=>WEB_SITE."/dynamic/A13.php");
				$content[] =array("Title"=> "在售非美元理财产品信息",
					"Description"=>"menuitems/A14.html",
					"PicUrl"=>"http://".WEB_SITE."/img/A14.jpg",
					"Url"=>WEB_SITE."/menuitems/A14.html");	
				$content[] =array("Title"=> "美元理财产品收益比较",
					"Description"=>"menuitems/A15.html",
					"PicUrl"=>"http://".WEB_SITE."/img/A15.jpg",
					"Url"=>WEB_SITE."/menuitems/A15.html");	
				$result = $this->transmitNews($obj,$content);
				break;
			case "A2":
				$content = array();
				$content[] =array("Title"=> "外汇实时牌价",
					"Description"=>"栏目介绍",
					"PicUrl"=>"http://".WEB_SITE."/img/A20.jpg",
					"Url"=>WEB_SITE."/menuitems/A20.html");			
				$content[] =array("Title"=> "美元兑人民币实时牌价",
					"Description"=>"menuitems/A21.html",
					"PicUrl"=>"http://".WEB_SITE."/img/A21.jpg",
					"Url"=>WEB_SITE."/dynamic/A21.php");
				$content[] =array("Title"=> "英镑兑人民币实时牌价",
					"Description"=>"menuitems/A22.html",
					"PicUrl"=>"http://".WEB_SITE."/img/A22.jpg",
					"Url"=>WEB_SITE."/dynamic/A22.php");
				$content[] =array("Title"=> "欧元兑人民币实时牌价",
					"Description"=>"menuitems/A23.html",
					"PicUrl"=>"http://".WEB_SITE."/img/A23.jpg",
					"Url"=>WEB_SITE."/dynamic/A23.php");
				$content[] =array("Title"=> "澳元兑人民币实时牌价",
					"Description"=>"menuitems/A24.html",
					"PicUrl"=>"http://".WEB_SITE."/img/A24.jpg",
					"Url"=>WEB_SITE."/dynamic/A24.php");
				$content[] =array("Title"=> "日元兑人民币实时牌价",
					"Description"=>"menuitems/A25.html",
					"PicUrl"=>"http://".WEB_SITE."/img/A25.jpg",
					"Url"=>WEB_SITE."/dynamic/A25.php");					
				$result = $this->transmitNews($obj,$content);
				break;
			case "A3":
				$content = array();
				$content[] =array("Title"=> "海外债券",
					"Description"=>"栏目介绍",
					"PicUrl"=>"http://".WEB_SITE."/img/A30.jpg",
					"Url"=>WEB_SITE."/menuitems/A30.html");		
				$content[] =array("Title"=> "\"赚洋钱\"最高预期收益外债精选",
					"Description"=>"menuitems/A31.html",
					"PicUrl"=>"http://".WEB_SITE."/img/A311.jpg",
					"Url"=>WEB_SITE."/menuitems/A31.html");		
				$content[] =array("Title"=> "\"赚洋钱\"各安全等级外币债券推荐",
					"Description"=>"menuitems/A32.html",
					"PicUrl"=>"http://".WEB_SITE."/img/A321.jpg",
					"Url"=>WEB_SITE."/menuitems/A32.html");						
				$result = $this->transmitNews($obj,$content);	
				break;
			case "A4":
				$content = array();
				$content[] =array("Title"=> "一周市场综述(2016.04.18-2016.04.24)",
					"Description"=>"一周市场综述",
					"PicUrl"=>"http://".WEB_SITE."/img/weeklyhead.jpg",
					"Url"=>WEB_SITE."/menuitems/2016W18.html");
				$content[] =array("Title"=> "2016-04-24•透过美联储的加息困境看美国经济前景",
					"Description"=>"menuitems/A4-20160424.html",
					"PicUrl"=>"http://".WEB_SITE."/img/A4-20160424-000.jpg",
					"Url"=>WEB_SITE."/menuitems/A4-20160424.html");					
				$content[] =array("Title"=> "2016-04-17•科比退役后如何管理他的财富？",
					"Description"=>"menuitems/A4-20160416.html",
					"PicUrl"=>"http://".WEB_SITE."/img/A4-20160416-000.jpg",
					"Url"=>WEB_SITE."/menuitems/A4-20160416.html");
				$content[] =array("Title"=> "2016-03-26•一波未平一波又起-穿过布鲁塞尔的硝烟看欧美市场",
					"Description"=>"menuitems/A46.html", 
					"PicUrl"=>"http://".WEB_SITE."/img/A46.jpg",
					"Url"=>WEB_SITE."/menuitems/A46.html");					
				$content[] =array("Title"=> "2016-03-19•维持现行利率不变 - 美联储为何犹豫？",
					"Description"=>"menuitems/A45.html",
					"PicUrl"=>"http://".WEB_SITE."/img/A45.jpg",
					"Url"=>WEB_SITE."/menuitems/A45.html");					
				$result = $this->transmitNews($obj,$content);					
				break;
			case "A5":	
				$content = array();
				$content[] =array("Title"=> "2016年1季度全球基金投资季刊",
					"Description"=>"重点推荐",
					"PicUrl"=>"http://".WEB_SITE."/img/weekly/20160411/2016S01.Report/2016S01-title.jpg",
					"Url"=>WEB_SITE."/menuitems/2016S01.html");	
				$content[] =array("Title"=> "2016-04-22•2016年全球投资展望：控制住你的热情",
					"Description"=>"menuitems/A5-20160422S.html",
					"PicUrl"=>"http://".WEB_SITE."/img/A5-20160422S-000.jpg",
					"Url"=>WEB_SITE."/menuitems/A5-20160422S.html");						
				$content[] =array("Title"=> "2016-04-22•黄金是否值得你一直持有？",
					"Description"=>"menuitems/A5-20160422.html",
					"PicUrl"=>"http://".WEB_SITE."/img/A5-20160422-000.jpg",
					"Url"=>WEB_SITE."/menuitems/A5-20160422.html");						
				$content[] =array("Title"=> "2016-04-16•债券投资可能会给你超越期望的回报",
					"Description"=>"menuitems/A5-20160416.html",
					"PicUrl"=>"http://".WEB_SITE."/img/A5-20160416-000.jpg",
					"Url"=>WEB_SITE."/menuitems/A5-20160416.html");						
				$content[] =array("Title"=> "2016-04-14•能源还会给你机会-请抓住!",
					"Description"=>"menuitems/A53.html",
					"PicUrl"=>"http://".WEB_SITE."/img/A53.jpg",
					"Url"=>WEB_SITE."/menuitems/A53.html");						

				$result = $this->transmitNews($obj,$content);
				break;				
			case "B1":
				$content = array();
				$content[] =array("Title"=> "股票基金精选",
					"Description"=>"栏目介绍",
					"PicUrl"=>"http://".WEB_SITE."/img/B10.jpg",
					"Url"=>WEB_SITE."/menuitems/B10.html");			
				$content[] =array("Title"=> "海外股票基金分类综合评价",
					"Description"=>"menuitems/B11.html",
					"PicUrl"=>"http://".WEB_SITE."/img/B11.jpg",
					"Url"=>WEB_SITE."/menuitems/B11.html");
				$content[] =array("Title"=> "海外股票基金最佳表现优选(更新于2016.04.20)",
					"Description"=>"menuitems/B12.html",
					"PicUrl"=>"http://".WEB_SITE."/img/B12.jpg",
					"Url"=>WEB_SITE."/menuitems/B12.html");
				$content[] =array("Title"=> "\"赚洋钱\"推荐股票基金",
					"Description"=>"menuitems/B13.html",
					"PicUrl"=>"http://".WEB_SITE."/img/B13.jpg",
					"Url"=>WEB_SITE."/menuitems/B13.html");
				$result = $this->transmitNews($obj,$content);				
				break;
			case "B2":
				$content = array();
				$content[] =array("Title"=> "债券基金精选",
					"Description"=>"栏目介绍",
					"PicUrl"=>"http://".WEB_SITE."/img/B20.jpg",
					"Url"=>WEB_SITE."/menuitems/B20.html");				
				$content[] =array("Title"=> "海外债券基金分类综合评价",
					"Description"=>"menuitems/B21.html",
					"PicUrl"=>"http://".WEB_SITE."/img/B21.jpg",
					"Url"=>WEB_SITE."/menuitems/B21.html");
				$content[] =array("Title"=> "'赚洋钱'推荐债券基金",
					"Description"=>"menuitems/B23.html",
					"PicUrl"=>"http://".WEB_SITE."/img/B23.jpg",
					"Url"=>WEB_SITE."/menuitems/B23.html");
				$result = $this->transmitNews($obj,$content);				
				break;
			case "B3":	
				$content = array();
				$content[] =array("Title"=> "平衡基金精选",
					"Description"=>"栏目介绍",
					"PicUrl"=>"http://".WEB_SITE."/img/B30.jpg",
					"Url"=>WEB_SITE."/menuitems/B30.html");					
				$content[] =array("Title"=> "海外最佳表现平衡基金(综合评价)",
					"Description"=>"menuitems/B31.html",
					"PicUrl"=>"http://".WEB_SITE."/img/B31.jpg",
					"Url"=>WEB_SITE."/menuitems/B31.html");
				$result = $this->transmitNews($obj,$content);				
				break;
			case "B4":	
				$content = array();
				$content[] =array("Title"=> "商品基金精选",
					"Description"=>"栏目介绍",
					"PicUrl"=>"http://".WEB_SITE."/img/B40.jpg",
					"Url"=>WEB_SITE."/menuitems/B40.html");			
				$content[] =array("Title"=> "海外最佳表现商品基金(综合评价)",
					"Description"=>"menuitems/B41.html",
					"PicUrl"=>"http://".WEB_SITE."/img/B41.jpg",
					"Url"=>WEB_SITE."/menuitems/B41.html");
				$content[] =array("Title"=> "\"赚洋钱\"推荐商品基金",
					"Description"=>"menuitems/B43.html",
					"PicUrl"=>"http://".WEB_SITE."/img/B43.jpg",
					"Url"=>WEB_SITE."/menuitems/C5.html");				
				$result = $this->transmitNews($obj,$content);			
				break;
			case "B5":
				$content = array();
				$content[] =array("Title"=> "\"赚洋钱\"投资组合",
					"Description"=>"栏目介绍",
					"PicUrl"=>"http://".WEB_SITE."/img/B50.jpg",
					"Url"=>WEB_SITE."/menuitems/B50.html");				

				$result = $this->transmitNews($obj,$content);				
				break;
//			case "C1":
//				$content = array();
//				$content[] =array("Title"=> "公司及团队",
//					"Description"=>"团队介绍",
//					"PicUrl"=>"http://".WEB_SITE."/img/C10.jpg",
//					"Url"=>WEB_SITE."/menuitems/C1.html");
//				$result = $this->transmitNews($obj,$content);				
//				break;
			case "C2":	
				$content = array();
				$content[] =array("Title"=> "公司动态",
					"Description"=>"栏目介绍",
					"PicUrl"=>"http://".WEB_SITE."/img/C20.jpg",
					"Url"=>WEB_SITE."/menuitems/C5.html");
				$result = $this->transmitNews($obj,$content);				
				break;
			case "C3":
				$content = array();
				$content[] =array("Title"=> "理财课堂",
					"Description"=>"栏目介绍",
					"PicUrl"=>"http://".WEB_SITE."/img/C30.jpg",
					"Url"=>WEB_SITE."/menuitems/C30.html");
				$content[] =array("Title"=> "如何识别外汇理财产品的收益与风险",
					"Description"=>"menuitems/C31.html",
					"PicUrl"=>"http://".WEB_SITE."/img/C31.jpg",
					"Url"=>WEB_SITE."/menuitems/C31.html");
				$result = $this->transmitNews($obj,$content);			
				break;
			case "C4":	
				$content = array();
				$content[] =array("Title"=> "您的问题与需求",
					"Description"=>"栏目介绍",
					"PicUrl"=>"http://".WEB_SITE."/img/C40.jpg",
					"Url"=>WEB_SITE."/menuitems/C4.html");
				$result = $this->transmitNews($obj,$content);				
				break;
			case "C5":		
				$content[] =array("Title"=> "联系我们",
					"Description"=>"栏目介绍",
					"PicUrl"=>"http://".WEB_SITE."/img/C50.jpg",
					"Url"=>WEB_SITE."/menuitems/C5.html");
				$result = $this->transmitNews($obj,$content);		
				break;
		}
		return $result;
	}
}

?>