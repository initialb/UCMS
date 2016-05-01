<?php

class CCInterface{

	public function SendMsg($openId,$content){
		$access_token = get_Access_Token();
		$url = "https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=".$access_token;
		$data = '{
			"touser":"' . $openId .'",
			"msgtype":"text",
			"text":
			{
				"content":"' . $content . '" 
			}
		}';
		$ret = https_request($url,$data);
		var_dump($ret);
		sae_debug($ret);
	}	
	
	public function SendNews($openId,$content){
		/*
		$content: [{
					"title": "XXXX",
					"description":"XXXXXXXXXXXXXX",
					"url":"XXXXXX",
					"picturl":"XXXXXXXXXXXX"
					},
					{...}]
		*/
	
		$access_token = get_Access_Token();
		$url = "https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=".$access_token;
		$data = '{
			"touser":"' . $openId .'",
			"msgtype":"news",
			"news":
			{
				"articles":"' . $content . '" 
			}
		}';
		$ret = https_request($url,$data);
		var_dump($ret);
		sae_debug($ret);
	}
	
	public function SendMusic($openId,$musicArray){
			// thumb_media_id : not option!
		$access_token = get_Access_Token();
		$url = "https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=".$access_token;
		$data = '{
			"touser":"' . $openId .'",
			"msgtype":"music",
			"music":
			{
				"title":"' . $musicArray['Title'] . '",
				"description":"' . $musicArray['Description'] . '",
				"musicurl":"' . $musicArray['MusicUrl'] . '",
				"hqmusicurl":"' . $musicArray['HQMusicUrl'] . '",
				"thumb_media_id":"'.$musicArray['Thumb_media_id'] .'"
			}
		}';
		$ret = https_request($url,$data);
		var_dump($ret);
		sae_debug($ret);
	}
	
	public function SendImage($openId,$content){
		$access_token = get_Access_Token();
		$url = "https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=".$access_token;
		$data = '{
			"touser":"' . $openId .'",
			"msgtype":"image",
			"image":
			{
				"media_id":"' . $content . '" 
			}
		}';
		$ret = https_request($url,$data);
		var_dump($ret);
		sae_debug($ret);
	}	
	
	public function SendVoice($openId,$content){
		$access_token = get_Access_Token();
		$url = "https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=".$access_token;
		$data = '{
			"touser":"' . $openId .'",
			"msgtype":"voice",
			"voice":
			{
				"media_id":"' . $content . '" 
			}
		}';
		$ret = https_request($url,$data);
		var_dump($ret);
		sae_debug($ret);
	}	

	public function SendVideo($openId,$videoArray){
			// thumb_media_id : not option!
		$access_token = get_Access_Token();
		$url = "https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=".$access_token;
		$data = '{
			"touser":"' . $openId .'",
			"msgtype":"video",
			"video":
			{
				"title":"' . $videoArray['Title'] . '",
				"description":"' . $videoArray['Description'] . '",
				"media_id":"' . $videoArray['Media_id'] . '"
			}
		}';
		$ret = https_request($url,$data);
		var_dump($ret);
		sae_debug($ret);
	}	
	
}

?>