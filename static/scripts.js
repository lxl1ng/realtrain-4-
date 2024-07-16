document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();

    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;

    if (username === 'admin' && password === '123456') {
        alert('登录成功');
    } else {
        alert('用户名或密码错误');
    }
});

document.getElementById('backButton').addEventListener('click', function() {
    window.history.back(); // 返回上一页
});
