function login(){
    var src = [
        '<div class="am-g">',
            '<form method="post" class="am-form" action="{{ url_for('+"view_login"+') }}">',
                '<label for="email">用户名:</label>',
                '<input type="text" name="username" id="email" value="">',
                '<br>',
                '<label for="password">密码:</label>',
                '<input type="password" name="password" id="password" value="">',
                '<br>',
                '<label for="remember-me">',
                    '<input id="remember-me" type="checkbox">记住密码</label>',
                '<br />',
                '<div class="am-cf">',
                    '<input type="submit" name="" value="登 录" class="am-btn am-btn-primary am-btn-sm am-fl">',
                    '<input type="submit" name="" value="忘记密码 ^_^? " class="am-btn am-btn-default am-btn-sm am-fr">',
                '</div>',
            '</form>',
        '</div>',
    ].join('')
    $(".am-panel-bd").empty()
    $(".am-panel-bd").append(src)
}
function singin(){
    var src = [
        '<div class="am-g">',
            '<form method="post" class="am-form" action="{{ url_for('+"view_login"+') }}">',
                '<label for="username">用户名:</label>',
                '<input type="text" name="username" id="username" value="">',
                '<br>',
                '<label for="email">电子邮件:</label>',
                '<input type="email" name="email" id="email" value="">',
                '<br>',
                '<label for="password">密码:</label>',
                '<input type="password" name="password" id="password" value="">',
                '<br>',
                '<label for="confpassword">确认密码:</label>',
                '<input type="password" name="confpassword" id="confpassword" value="">',
                '<br>',
                '<label for="remember-me">',
                    '<input id="remember-me" type="checkbox">我已同意</label>',
                '<br />',
                '<div class="am-cf">',
                    '<input type="submit" name="" value="注册" class="am-btn am-btn-primary am-btn-sm am-fl">',
                '</div>',
            '</form>',
        '</div>',
    ].join('')
    $(".am-panel-bd").empty()
    $(".am-panel-bd").append(src)
}


$(function(){
    $("button.am-btn:nth-child(1)").click(login);
    $("button.am-btn:nth-child(2)").click(singin);
})