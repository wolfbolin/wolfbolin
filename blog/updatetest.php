<?php
/**
 * Created by PhpStorm.
 * User: wolfbolin
 * Date: 2018/1/15
 * Time: 1:27
 */
exec("python3 md2html-php.py 123.md 2>&1",$arr,$ret);
print_r($arr);
echo "<br>" . $ret . "<br>";   ?>