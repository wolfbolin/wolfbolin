<?php
/**
 * Created by PhpStorm.
 * User: wolfbolin
 * Date: 2018/8/5
 * Time: 18:23
 */
function sayError(){
    return "ERROR";
}
function newline(){
    echo '<br/>';
}

header('Content-Type:text/html;charset= UTF-8');
$rss_url = "https://blog.wolfbolin.com/feed";
$rss = simplexml_load_file($rss_url);
if(!$rss){
    echo sayError();
}
//var_dump($rss);
//foreach ($rss->channel as $key => $value) {
////    echo $value->title . '<br/>';
////    print_r($value);
//    echo json_encode($value);
//}
echo count($rss->channel->item);
newline();
echo $rss->channel->item->description;
//echo json_encode($rss->channel);



