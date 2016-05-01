 <?php
 $ua = $_SERVER['HTTP_USER_AGENT'];
 if(!strpos($ua, 'MicroMessenger')){
     $weixin = "不是微信浏览器";
 }else{
     $preg = "/MicroMessenger\/(.+)/";
     preg_match_all($preg, $ua, $new_cnt);
     $weixin = "".$new_cnt[1][0]."\n";
 }
 if(strpos($ua, 'Android')){
     $phone = "Android";
 }else if(strpos($ua, 'iPhone OS')){
     $phone = "iOS";
 }else{
     $phone = "其他";
 }
 ?>
 <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
 <HTML>
   <HEAD>
     <TITLE>赚洋钱</TITLE>
     <META charset=utf-8>
     <META name=viewport content="width=device-width, user-scalable=no, initial-scale=1">
     <link rel="stylesheet" href="http://code.jquery.com/mobile/1.4.2/jquery.mobile-1.4.2.min.css" />
     <script src="http://code.jquery.com/jquery-1.9.1.min.js"></script>
     <script src="http://code.jquery.com/mobile/1.4.2/jquery.mobile-1.4.2.min.js"></script>
   </HEAD>
   <BODY>
     <div data-role="page" id="page1">
       <div data-role="content">
         <UL data-role="listview" data-inset="true">
           <LI>
             <P>
               <div class="fieldcontain">
                 <label for="userid">微信版本</label>
                 <input name="userid" id="userid" value="<?php echo $weixin;?>" type="text" >
               </div>
               <div class="fieldcontain">
                 <label for="openid">手机系统</label>
                 <input name="openid" id="openid" value="<?php echo $phone;?>" type="text" >
               </div>
             </P>
           </LI>
         </UL>
       </div>
       <div data-theme="b" data-role="footer" data-position="fixed">
         <h3>赚洋钱</h3>
       </div>
     </div>
   </BODY>
 </HTML>
