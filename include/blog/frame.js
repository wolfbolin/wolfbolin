$(function() {
    function wf_alert(content) {
        document.getElementById("wf-alert-text").innerHTML=content;
        $('#wf-alert').modal();
    }
    function wf_loading(content){
        document.getElementById("wf-loading-text").innerHTML=content;
        $('#wf-loading').modal();
    }
    $('#logout-btn').on('click', function() {
        $.ajax({
            type:"POST",
            url:"login.php",
            dataType:"json",
            data:{
                "action":"logout"
            },
            beforeSend:function(){
                wf_loading('登出中...');
            },
            success:function(msg){
                console.log(msg);
                if(msg.result === 'success'){
                    window.location.reload();
                }else{
                    $('#wf-loading').modal('close');
                    wf_alert('请勿尝试非法操作。');
                }
            },
            error:function(){
                $('#login-loading').modal('close');
                wf_alert('网络异常');
            }
        })
    });
    $('#login-modal-btn').on('click', function() {
        $('#login-modal').modal({
            relatedTarget: this,
            onConfirm: function(e) {
                if(e.data.length !== 2){
                    wf_alert("数据异常");
                    return;
                }
                var accountID = e.data[0];
                var password = e.data[1];
                var account_regex = /^[A-Za-z0-9._]{5,20}$/
                var password_regex = /^[A-Za-z0-9`~!@#$%^&*-=+,.]{5,30}$/
                if(!account_regex.test(accountID)){
                    wf_alert("用户名格式不符合规范");
                    return;
                }
                if(!password_regex.test(password)){
                    wf_alert("密码格式不符合规范");
                    return;
                }
                $.ajax({
                    type:"POST",
                    url:"login.php",
                    dataType:"json",
                    data:{
                        "action":"login",
                        "accountID":accountID,
                        "password":password
                    },
                    beforeSend:function(){
                        wf_loading('登陆中...');
                    },
                    success:function(msg){
                        console.log(msg);
                        $('#wf-loading').modal('close');
                        if(msg.result === 'success'){
                            window.location.reload();
                        }else if(msg.result === 'authentication failure'){

                            wf_alert('帐号或密码错误，请检查后重试。');
                        }else{
                            wf_alert('请勿尝试非法操作。');
                        }
                    },
                    error:function(){
                        $('#wf-loading').modal('close');
                        wf_alert('网络异常');
                    }
                })
            }
        });
    });
});