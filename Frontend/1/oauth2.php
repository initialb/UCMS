<?php
 
	if(isset($_GET["code"])){
		$authCode = $_GET["code"];
 
		$mysql = new SaeMysql();
		$sql = "UPDATE `gParameters` SET `Value` ='"  . $authCode . "' WHERE `name` ='gAuthCode'";
		$mysql->runSql( $sql );
		$mysql->closeDb();
		echo "get Code successful!";
	}

?>