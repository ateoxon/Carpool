$(document).ready(function(){
  var url = window.location.href;
  var ar = url.split('/');
  console.log(ar);
  var user_id = ar[3];
  var token = ar[4];
  $.ajax({
    url:'/auth/info/'+user_id+'/'+token,
    type:'GET',
    success:(data)=>{
      if(data.success){
        console.log(data);
        $('#profile_first_name').empty();
        $('#profile_last_name').empty();
        $('#profile_email').empty();
        $('#profile_first_name').val(data.first_name);
        $('#profile_last_name').val(data.last_name);
        $('#profile_email').text(data.email);
      }else{
        alert('Error: '+data.error);
      }
    },
    error:(e,rs)=>{
      alert('Error. Please Contact Admin');
    }
  });

  $('#profile_delete_btn').click(()=>{
    $.ajax({
      url:'/auth/info/delete',
      type:'POST',
      data:{
        user_id:user_id,
        token:token
      },
      success:(data)=>{
        if(data.success){
          window.location.replace('/auth');
        }else{
          alert('Error: '+data.error);
        }
      },
      error:(e,rs)=>{
        alert('Error. Please Contact Admin');
      }
    });
  });

  $('#profile_update_btn').click(()=>{
    var first_name = $('#profile_first_name').val();
    var last_name = $('#profile_last_name').val();
    $.ajax({
      url:'/auth/info/update',
      type:'POST',
      data:{
        user_id:user_id,
        token:token,
        first_name:first_name,
        last_name:last_name
      },
      success:(data)=>{
        if(data.success){
          $('#profile_first_name').empty();
          $('#profile_last_name').empty();
          $('#profile_first_name').val(first_name);
          $('#profile_last_name').val(last_name);
        }else{
          alert('Error: '+data.error);
        }
      },
      error:(e,rs)=>{
        alert('Error. Please Contact Admin');
      }
    });
  });
});
