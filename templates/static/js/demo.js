function ShowLoginText(){
    layer.open({
        type:1,
        title:"Please enter correct form of number",
        area:["395px","300px"],
        content:$("#loginBox"),
        });
    }
function ShowPostText(){
	layer.open({
		type:1,
		title:"reset your account",
		area:["395px","300px"],
		content:$("#loginBox"),
		});
	}
function Login(){
    var username=$.trim($("#InputUsername").val());//获取用户名trim是去掉空格
    var password=$.trim($("#InputUserPwd").val());//获取密码
    if(username==""||password==""){
        layer.alert("用户名或者密码不能为空!",{
        title:"提示",
        icon:5,
        });
    }
}
function resolve_conflict(){
	name, ext = os.path.splitext(basename)
        count = 0
        while True:
            count = count + 1
            newname = '%s_%d%s' % (name, count, ext)
            if not os.path.exists(os.path.join(target_folder, newname)):
                return newname
}

function uploaded_photos.save(file){
	 var photoUpload = upload.render({
            elem: '#btn_photo'
            , url: '/flask-upload'
            , exts: 'jpg|png|jpeg'
            , size: 5120
            , before: function (obj) {
                obj.preview(function (index, file, result) {
                    $('#photo').attr('src', result);
                    $('#photo').css('width', '300');
                    $('#photo').css('height', '300');
                });
            }
            , done: function (res) {
                if (res.code == 0) {
                    layer.msg(res.filename + '上传成功！');
                    var href = '<a href="' + res.msg + '" style="color:blue; text-decoration: solid;">' + res.msg + '</a>'
                    $('#txt_photo').html(href)
                } else {
                    return layer.msg('上传失败');
                }
            }
            , error: function () {
                var photo = $('#txt_photo');
                photo.html('<span style="color: #FF5722;">上传失败</span> <a class="layui-btn layui-btn-mini demo-reload">重试</a>');
                photo.find('#btn_photo').on('click', function () {
                    photoUpload.upload();
                });
            }
        });
}
