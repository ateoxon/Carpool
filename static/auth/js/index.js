$(document).ready(function(){
  $('#profile_btn').click(()=>{
    $('#index_container').empty();
    $.get('/static/auth/html/profile.html',function(result){
      $('#index_container').append(result);
    });
  });
  $('#notif_btn').click(()=>{
    $('#index_container').empty();
    $.get('/static/notif/html/notif.html',function(result){
      $('#index_container').append(result);
    });
  });
  $('#trip_btn').click(()=>{
    $('#index_container').empty();
    $.get('/static/trip/html/trip.html',function(result){
      $('#index_container').append(result);
    });
  });
  $('#my_trip_btn').click(()=>{
    $('#index_container').empty();
    $.get('/static/trip/html/my_trip.html',function(result){
      $('#index_container').append(result);
    });
  });
  $('#logout_btn').click(()=>{
    var url = window.location.href;
    var ar = url.split('/');
    var user_id = ar[3];
    var token = ar[4];
    $.ajax({
      url:'/auth/logout',
      type:'POST',
      data:{
        token:token,
        user_id:user_id
      },
      success:(data)=>{
        console.log(data);
        if(data.success){
          window.location.replace('/auth');
        }else{
          alert('Error Loggin Out. Error: '+data.error);
        }
      },
      error:(rs,e)=>{
          alert('Error, Please Contact Administrator');
      }
    });
  });
});
