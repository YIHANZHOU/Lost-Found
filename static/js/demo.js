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
