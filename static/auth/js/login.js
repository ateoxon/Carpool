$(document).ready(function(){
  $('#login_btn').click(function(){
    var email = $('#login_email').val();
    var password = $('#login_password').val();
    $('#login_email').val('');
    $('#login_password').val('');
    $.ajax({
      url:'/auth/login',
      type:'POST',
      data:{
        email:email,
        password:password
      },
      success:(data)=>{
        console.log(data);
        if(!data.success){
          alert('Error loggin in. Error: '+data.error);
        }else{
          window.location.replace('/'+data.user_id+'/'+data.token);
        }
      },
      error:(rs,e)=>{
        console.log(rs);
        console.log(e);
      }
    });
  });
});
