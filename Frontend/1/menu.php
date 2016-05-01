<?php
//require_once(dirname(__FILE__).'/'.'utility.php');

class Menu{
	
	public function create(){
		$jsonmenu ='{
			"button":[
			{
				"name":"外汇理财",
				"sub_button":[
				{
					"type":"click",
					"name":"在售外汇理财",
					"key":"A1"
				},
				{
					"type":"click",
					"name":"外汇实时牌价",
					"key":"A2"
				},
				{
					"type":"click",
					"name":"海外债券",
					"key":"A3"
				},				
				{
					"type":"click",
					"name":"市场热点",
					"key":"A4"
				},
				{
					"type":"click",
					"name":"投资策略",
					"key":"A5"
				}]
			},
			{
				"name":"海外基金",
				"sub_button":[
				{
					"type":"click",
					"name":"股票基金精选",
					"key":"B1"
				},
				{
					"type":"click",
					"name":"债券基金精选",
					"key":"B2"
				},
				{
					"type":"click",
					"name":"平衡基金精选",
					"key":"B3"
				},
				{
					"type":"click",
					"name":"商品基金精选",
					"key":"B4"
				},
				{
					"type":"click",
					"name":"\"赚洋钱\"投资组合",
					"key":"B5"
				}]
			},
			{
				"name":"关于我们",
				"sub_button":[
				{
					"type":"view",
					"name":"公司及团队",
					"url":"http://zhuanyangqian.applinzi.com/menuitems/C1.html"
				},
				{
					"type":"click",
					"name":"公司动态",
					"key":"C2"
				},
				{
					"type":"click",
					"name":"理财课堂",
					"key":"C3"
				},
				{
					"type":"view",
					"name":"您的问题与需求",
					"url":"http://zhuanyangqian.applinzi.com/menuitems/C4.html"
				},
				{
					"type":"click",
					"name":"联系我们",
					"key":"C5"
				}]
			}]
		}';
		$access_token = get_Access_Token();
		sae_debug("menu:accessToken = ".$accessToken);		
		$url = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=".$access_token;
		$result =https_request($url,$jsonmenu);
		$jsoninfo = json_decode($result,true);
		$errCode = $jsoninfo["errcode"];
		return $errCode;
		sae_debug("Create Menu Return Code : " .$errCode);
	}
	
	public function view(){
		$access_token = get_Access_Token();
		$url = "https://api.weixin.qq.com/cgi-bin/menu/get?access_token=".$access_token;
		$result =https_request($url,$jsonmenu);
		$jsoninfo = json_decode($result,true);
		$errCode = $jsoninfo["errcode"];
		return $errCode;
		sae_debug("View Menu Return Code : " .$errCode);
	
	}
	 
	public function delete(){		
		$access_token = get_Access_Token();
		$url = "https://api.weixin.qq.com/cgi-bin/menu/delete?access_token=".$access_token;
		$result =https_request($url,$jsonmenu);
		$jsoninfo = json_decode($result,true);
		$errCode = $jsoninfo["errcode"];
		return $errCode;
		sae_debug("Delete Menu Return Code : " .$errCode);
	}
}
?>