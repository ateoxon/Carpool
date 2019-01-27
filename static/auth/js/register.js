$(document).ready(function(){
  $('#reg_btn').click(function(){
    var first_name = $('#reg_first_name').val();
    var last_name = $('#reg_last_name').val();
    var confirm_password = $('#reg_confirm_password').val();
    var email = $('#reg_email').val();
    var password = $('#reg_password').val();
    $('#reg_email').val('');
    $('#reg_password').val('');
    $('#reg_confirm_password').val('');
    $('#reg_last_name').val('');
    $('#reg_first_name').val('');
    if(first_name=='' || last_name=='' || confirm_password==''
      || email == '' || password==''){
      alert('Fields cant be empty');
    }else if(password!=confirm_password){
      alert('Password do not match');
    }else{
      $.ajax({
        url:'/auth/register',
        type:'POST',
        data:{
          email:email,
          password:password,
          first_name:first_name,
          last_name:last_name
        },
        success:(data)=>{
          console.log(data);
          if(!data.success){
            alert('Error logging in. Error: '+data.error);
          }else{
            alert('logged in');
          }
        },
        error:(rs,e)=>{
          alert('error loggin in. Please contact administrator');
          console.log(rs);
          console.log(e);
        }
      });
    }
  });
});
