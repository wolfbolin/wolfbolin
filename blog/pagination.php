<?php
/**
 * Created by PhpStorm.
 * User: wolfbolin
 * Date: 2018/1/16
 * Time: 20:05
 */

/**
 * 需要参数：当前下标$page_index,总页数$page_num
 */
?>
<li>
    <ul class="am-pagination am-pagination-centered">
        <li <?php if($page_index==1)echo "class=\"am-disabled\"";?>>
            <a href="index.php?page=<?php echo $page_index-1?>">&laquo;</a>
        </li>
        <?php
        if($page_index>=4){
            ?><li><span>...</span></li><?php
        }
        if($page_index>=3){
            ?>
            <li><a href="index.php?page=<?php echo $page_index-2?>"><?php echo $page_index-2?></a></li>
            <?php
        }
        if($page_index>=3){
            ?>
            <li><a href="index.php?page=<?php echo $page_index-1?>"><?php echo $page_index-1?></a></li>
            <?php
        }
        ?>
        <li class="am-active"><a href="index.php?page=<?php echo $page_index?>"><?php echo $page_index?></a></li>
        <?php
        if($page_num - $page_index >= 1){
            ?>
            <li><a href="index.php?page=<?php echo $page_index+2?>"><?php echo $page_index+2?></a></li>
            <?php
        }
        if($page_num - $page_index >= 2){
            ?>
            <li><a href="index.php?page=<?php echo $page_index+1?>"><?php echo $page_index+1?></a></li>
            <?php
        }
        if($page_num - $page_index >= 3){
            ?>
            <li><span>...</span></li>
            <?php
        }
        ?>
        <li <?php if($page_index==$page_num)echo "class=\"am-disabled\"";?>>
            <a href="index.php?page=<?php echo $page_index+1?>">&raquo;</a>
        </li>
    </ul>
</li>
