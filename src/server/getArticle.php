<?php
/**
 * Created by PhpStorm.
 * User: wolfbolin
 * Date: 2018/8/5
 * Time: 18:23
 * Target: 完成博客RSS数据的解析并以json的形式传给前端
 */
header('Access-Control-Allow-Methods:GET'); #仅允许GET请求
/**
 * 预定义失败信息
 */
$response = [
    'result' => 'WA',
    'card' => []
];
/**
 * 向博客的RSS发起请求
 * 并且尝试解析XML文件
 */
header('Content-Type:text/html;charset= UTF-8');
$rss_url = "https://blog.wolfbolin.com/feed";
$rss = simplexml_load_file($rss_url);
if (!$rss) {
    echo json_encode($response);
    exit();
}
/**
 * 解析成功后读取XML数据
 * 数据类型为对象套对象
 * 获取字符串有一定复杂性
 * 注意同一标签的多次出现
 */
foreach ($rss->channel->item as $item) { #文章的数量由RSS源控制
    $card = [
        'title' => (string)$item->title,#不存在多个标题
        'link' => (string)$item->link
    ];
    $content = urlencode($item->description);
    $content = str_replace('+%5B%26%238230%3B%5D', '...', $content);#令人窒息的符号清除方案
    $content = urldecode($content);
    $card['content'] = $content;
    $date = strtotime($item->pubDate);
    $date = date("Y-m-d H:i:s", $date);
    $card['time'] = $date;
    $category = [];
    foreach ($item->category as $it) {
        $item = [
            'name' => (string)$it,
            'link' => 'https://blog.wolfbolin.com/archives/category/' . $it
        ];
        $category[] = $item;
    }
    $card['category'] = $category;
    $response['card'][] = $card;
}
$response['result'] = 'AC';
echo json_encode($response);
