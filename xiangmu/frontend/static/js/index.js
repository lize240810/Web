 /* 
    ajax数据请求
    $.ajax({
        url: "/ajax-user-folder-list",
        data: '/',
        dataType: 'json',
        success: function(data) {
            // 显示数据
            console.log(data)
        }
    });*/

/**
 * 渲染目录列表
 * 显示数据
 */
function render_folder_list(data){
    // 获取到页面中的表格
    var $table = $("#user-folder-list");
    // 再获取到表格中的tbody ,然后清空里面的内容
    var $tbody = $table.find('tbody');
    // console.log(data)
    $tbody.empty();
    // 判断通过ajax请求的数据
    if(data.length > 0){
        // 循环数据 使用循环因为是有多个数据 需要依次循环取值 或者依次 添加到页面上
        for (var i = 0 ; i < data.length; i++) {
            var item = data[i] // 获得每一个列
            var path_index = item['path'].lastIndexOf('/') // 取到path  获取到/下标
            var path_name = item['path'].substr(path_index + 1); //从指定位置开始截取
            // 设置str值
            var tr_str=[
                '<tr>',
                    '<td>',
                        '<input type="checkbox" name="ckb-content">',
                    '</td>',
                    '<td> <a href="javascript:;" data-path="', item['path'],'">', path_name, '</a> </td>',
                    '<td>', item['update_time'], '</td>',
                    '<td> <a href="javascript:;"> 重命名 </a> </td>',
                '</tr>'
            ].join('')
            // 添加到tbody表格里面
            $tbody.append(tr_str)
        }
    }else{
        // 为空的话给出提示
        //判断有多少个表头标题
        var $thead = $table.find('thead');
        var th_count = $thead.find("th").length
        //得到标题个数 进行设置空内容提示
        $tbody.html([
            '<tr>',
                '<td colspan="', th_count, '">',
                    '<div class="am-text-center am-link-muted">还没有文件夹,赶快添加一个吧</div>',
                '</td>',
            '</tr>'
        ].join('')) //吧全部内容拼接为一个字符串
    }
}

/**
 * 渲染当前路径
 */
 function render_current_path(path){
    // 面包屑导航 breadcrumb(面包屑)
// 根据html后代选择器获取到面包屑导航  父               子
    var $breadcrumb = $('.path-line > .am-breadcrumb');
    // 清空现有导航
    $breadcrumb.empty()
    // 根据目录分级别
    var path_arr = []
    // 只要目标不符合都全部设置为主目录
    if (path == '/' || path == undefined || path == null || path == "") {
        path = '';
        // 添加数据到path_arr数组
        // push添加元素到数组的方法
        path_arr.push(path)
    }
    else{
        // 目录分解  replace替换  //arguments参数
        // mat匹配到的内容 // /g (全文查找出现的所有匹配字符)
        path.replace(/\//g, function(mat) {
            // arguments[1]  返回/出现的位置
            // arguments[2] 返回截取以后的数据
            // substr  截取 把arguments[2]从(0到/)出现的位置开始截取
            var sub_path = arguments[2].substr(0, arguments[1])
            // 添加到数组中
            path_arr.push(sub_path)
            return mat
        });
        path_arr.push(path)
        console.log(path_arr)
    }
    // 显示到界面上
    for (var i = 0; i < path_arr.length; i++) {
        // 创建一个显示到页面上数组
        var li = [];
        // 当存放目录的数组中没有数据的时候 显示为主目录
        if (i == 0){
            // 只有主目录
            if(path_arr.length == 1){
                // 直接添加 因为在主目录所有不能再点击
                li=[
                    '<li>',
                        '<i class="am-icon-home"></i>主目录',
                    '</li>'
                ];
            }
            else{
                // 不只有根目录的时候
                // 把根目录变为可以点击的目录
                li=[
                    '<li>',
                        '<a href="javascript:;">',
                            '<i class="am-icon-home"></i>主目录',
                        '</a>',
                    '</li>'
                ];
            }
        }
        // 不止有一个目录的时候
        else{
            // 查找/最后出现的位置
            var path_index = path_arr[i].lastIndexOf('/');
            // 根据/最后出现的位置获取文件夹名字
            var path_name = path_arr[i].substr(path_index+1);
            // 长度-1与先循环的长度相等时证明他们现在已经是最地城目录了 不能点击的目录
            if( i == path_arr.length -1){
                // 因为循环从0开始2结束
                li =[
                    '<li class="am-active">',
                        path_name,
                    '</li>'
                ];
            }
            else {
                li = [
                    '<li>',
                        '<a href="javascript:;">',
                            path_name,
                        '</a>',
                    '</li>'
                ];
            }
        }
        // 把上面的li拼接起来转换为jQuery对象
        var $li = $(li.join(''));
        // 遍历查询 查看数组中是否存在空值 有的换转换为根目录 
        if(path_arr[i] == ''){
            // ""全部转换为根目录
            path_arr[i]='/';
        }
        // 额外添加一个属性，用于记录目录跳转目标路径
        $li.attr('data-path', path_arr[i]);
        $breadcrumb.append($li)
    }

}

/**
 * 设置当前路径记录
 */
function set_current_path(path){
// 1. 判断当前路径是否为空
    if(path == '/' || path == undefined || path == null || path ==""){
        // 清空无意义的路径
        $.AMUI.utils.cookie.unset('curren_path')
    }
    else{
        // 设置path 存与cookie中
        $.AMUI.utils.cookie.set('curren_path', path)
    }
}

/**
 * ajax发送请求获取目录列表
 */
function get_folder_list(path){
    var _data = {};
    //当 path未提供参数时,获取当前路径
    if(!path){
        // 从cookie中获取路径
        path = $.AMUI.utils.cookie.get("curren_path")
    }
    //处理path
    if(path == '/' || path === undefined || path == null || path == ""){
        //忽略data
    }
    else{
        _data['path'] = path
    }
    //ajax请求
    $.ajax({
        // views返回了一坨数据 ??
        url : GLOBAL.USER_FOLDER_LIST_URL,
        data : _data,
        dataType : 'json',
        success : function(data) {
            //设置路径
            set_current_path(path);
            //console.log(data);
                // 渲染路径
            render_current_path(path);
            // 显示数据
            render_folder_list(data);
        }
    });
}


/**
 * 绑定click时间,进行目录切换
 */
function bind_path_change(){
    // 元素获取
    var $breadcrumb = $('.path-line > .am-breadcrumb');
    // 获取指定的表格元素
    var $tbody = $('#user-folder-list').find('tbody');
    // 公共click事件
    function a_click(event){
        // 得到当前点击的元素
        var $me = $(this);
        //获取当前元素的data-path
        var path = $me.attr('data-path');
        // 判断当前点击的元素是否是li
        if($me.is('li')){
            // r如果是li 但是没有包含a 就ruturn
            if ($me.find('a').length < 1){
                return;
            }
        }
        // 获取 data-path 的值病调用ajax来查询
        get_folder_list(path);
    }
    //面包屑绑定点击事件  li[data-path]指定元素 
    $breadcrumb.on('click','li[data-path]',a_click);
    // 表格tbody中a标签事件绑定 
    $tbody.on('click','a[data-path]',a_click)
}

/**
 * 实现文件上传按钮绑定
 */
function bind_file_upload() {
    // 初始化文件上传
    // 从div获取 获取文件上传事件
    $('.button-line').fileupload({
        // fileInput:$('#file'),
        // dataType:'json',
    })
}

$(document).ready(function(){
    get_folder_list(); 
    bind_path_change();
    //bind_file_upload()
});

