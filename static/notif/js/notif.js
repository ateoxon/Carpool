$(document).ready(function(){
  get_all_notif(0,4);
});

function get_all_notif(prev,next){
  var url = window.location.href;
  var t = url.split('/');
  var user_id = t[3];
  var token = t[4];
  prev = Number(prev);
  next = Number(next);
  $.ajax({
    'url':'/notif/all/'+prev+'/'+next+'/'+user_id+'/'+token,
    'type':'GET',
    'success':(data)=>{
      if(data.success){
        var notifs = JSON.parse(data.notif);
        $('#notif-holder').empty();
        notifs.forEach((obj)=>{
          var html = '<div class="card" style="width: 18rem;">';
          html+='<div class="card-body">';
          html+='<h5 class="card-title">'+obj.sender__first_name+' '+obj.sender__last_name;
          html+='</h5>';
          html+='<p class="card-text">'+obj.msg+'</p>';
          html+='</div>';
          html+='</div>';
          $('#notif-holder').append(html);
        });
        if(Number(prev) - 4>=0){
          prev = Number(prev)-4;
          to = Number(to)-4;
          $('#notif_prev_btn').attr('onClick','get_all_notif(\''+prev+'\',\''+to+'\')');
        }else{
          prev = 0;
          to = 4;
          $('#notif_prev_btn').attr('onClick','get_all_notif(\''+prev+'\',\''+to+'\')');
        }
        to = Number(to) + 4;
        $('#notif_prev_btn').attr('onClick','get_all_notif(\''+(to-4)+'\',\''+to+'\')');
      }else {
        alert('Error: '+data.error);
      }
    },
    'error':(e,rs)=>{
      alert('Error. Please Contact Admin');
    }
  });
}
