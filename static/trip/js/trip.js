$(document).ready(function(){
  get_all_trips(0,4);
  $('#search_btn').click(()=>{
    var url = window.location.href;
    var t = url.split('/');
    var user_id = t[3];
    var token = t[4];
    var fcy = $('#from_loc_country').val();
    var fs = $('#from_loc_state').val();
    var fc = $('#from_loc_city').val();
    var tcy = $('#to_loc_country').val();
    var ts = $('#to_loc_state').val();
    var tc = $('#to_loc_city').val();
    $('#from_loc_country').val('');
    $('#from_loc_state').val('');
    $('#from_loc_city').val('');
    $('#to_loc_country').val('');
    $('#to_loc_state').val('');
    $('#to_loc_city').val('');
    search_trips(fcy,fs,fc,tcy,ts,tc,0,4);
  });
});

function join_trip(id){
  var url = window.location.href;
  var t = url.split('/');
  var user_id = t[3];
  var token = t[4];
  id = Number(id);
  $.ajax({
    'url':'/trip/add',
    'type':'POST',
    'data':{
      user_id:user_id,
      token:token,
      trip_id:id
    },
    'success':(data)=>{
      if(data.success){
        $('#exampleModal').modal('hide');
        alert('Added To Trip');
      }else{
        alert('Error: '+data.error);
      }
    },
    'error':(e,rs)=>{
      alert('Error: Please Contact Admin');
    }
  });
}

function search_trips(fcy,fs,fc,tcy,ts,tc,prev,next){
  var url = window.location.href;
  var t = url.split('/');
  var user_id = t[3];
  var token = t[4];
  prev = Number(prev);
  next = Number(next);
  $.ajax({
    url:'/trip/search',
    type:'POST',
    data:{
      user_id:user_id,
      token:token,
      from:prev,
      to:next,
      from_loc_country:fcy,
      from_loc_state:fs,
      from_loc_city:fc,
      to_loc_country:tcy,
      to_loc_state:ts,
      to_loc_city:tc
    },
    success:(data)=>{
      if(data.success){
        $('#trip_data').empty();
        var trips = JSON.parse(data.trip);
        trips.forEach((obj)=>{
          var html = '<tr style="cursor:pointer;" onClick="get_trip('+obj.id+')">';
            html += '<th scope="row">'+obj.date+'</th>';
            html += '<td>'+obj.from_loc_country+'</td>';
            html += '<td>'+obj.from_loc_state+'</td>';
            html += '<td>'+obj.from_loc_city+'</td>';
            html += '<td>'+obj.to_loc_country+'</td>';
            html += '<td>'+obj.to_loc_state+'</td>';
            html += '<td>'+obj.to_loc_city+'</td>';
            html += '<td>'+obj.capacity+'</td>';
          html += '</tr>';
          $('#trip_data').append(html);
        });
        if(Number(prev) - 4>=0){
          prev = Number(prev)-4;
          to = Number(to)-4;
          $('#trip_prev_btn').attr('onClick','search_trips(\''+fcy+'\',\''+fs+'\',\''+fc+'\',\''+tcy+'\',\''+ts+'\',\''+tc+'\',\''+prev+'\',\''+to+'\')');
        }else{
          prev = 0;
          to = 4;
          $('#trip_prev_btn').attr('onClick','search_trips(\''+fcy+'\',\''+fs+'\',\''+fc+'\',\''+tcy+'\',\''+ts+'\',\''+tc+'\',\''+prev+'\',\''+to+'\')');
        }
        to = Number(to) + 4;
        $('#trip_prev_btn').attr('onClick','search_trips(\''+fcy+'\',\''+fs+'\',\''+fc+'\',\''+tcy+'\',\''+ts+'\',\''+tc+'\',\''+(to-4)+'\',\''+to+'\')');
      }else{
        alert('Error: '+data.error);
      }
    },
    error:(re,s)=>{
      alert('Error: Please Contact Admin');
    }
  });
}

function get_trip(id){
  id = parseInt(id);
  var url = window.location.href;
  var t = url.split('/');
  var user_id = t[3];
  var token = t[4];
  $.ajax({
    url:'/trip/details/'+id+'/'+user_id+'/'+token,
    type:'GET',
    success:(data)=>{
      if(data.success){
        $('#modal_from_loc_country').text(data.from_loc_country);
        $('#modal_from_loc_state').text(data.from_loc_state);
        $('#modal_from_loc_city').text(data.from_loc_city);
        $('#modal_to_loc_country').text(data.to_loc_country);
        $('#modal_to_loc_state').text(data.to_loc_state);
        $('#modal_to_loc_city').text(data.to_loc_city);
        $('#modal_capacity').text(data.capacity);
        $('#modal_first_name').text(data.first_name);
        $('#modal_last_name').text(data.last_name);
        $('#modal_email').text(data.email);
        $('#exampleModal').modal('show');
        $('#join_trip_btn').attr('onClick','join_trip(\''+id+'\')');
      }else{
        alert('Error: '+data.error);
      }
    },
    error:(e,rs)=>{
      alert('Error. Please Contact Administrator');
    }
  });
}

function get_all_trips(prev,next){
  prev = parseInt(prev);
  next = parseInt(next);
  var url = window.location.href;
  var t = url.split('/');
  var user_id = t[3];
  var token = t[4];
  $('#trip_data').empty();
  $.ajax({
    url:'/trip/all/'+prev+'/'+next+'/'+user_id+'/'+token,
    type:'GET',
    success:(data)=>{
      if(data.success){
        var trips = JSON.parse(data.trip);
        trips.forEach((obj)=>{
          var html = '<tr style="cursor:pointer;" onClick="get_trip('+obj.id+')">';
            html += '<th scope="row">'+(new Date(obj.date)).toString()+'</th>';
            html += '<td>'+obj.from_loc_country+'</td>';
            html += '<td>'+obj.from_loc_state+'</td>';
            html += '<td>'+obj.from_loc_city+'</td>';
            html += '<td>'+obj.to_loc_country+'</td>';
            html += '<td>'+obj.to_loc_state+'</td>';
            html += '<td>'+obj.to_loc_city+'</td>';
            html += '<td>'+obj.capacity+'</td>';
          html += '</tr>';
          $('#trip_data').append(html);
        });
        if(Number(prev) - 4>=0){
          prev = Number(prev)-4;
          to = Number(to)-4;
          $('#trip_prev_btn').attr('onClick','get_all_trips(\''+prev+'\',\''+to+'\')');
        }else{
          prev = 0;
          to = 4;
          $('#trip_prev_btn').attr('onClick','get_all_trips(\''+prev+'\',\''+to+'\')');
        }
        to = Number(to) + 4;
        $('#trip_prev_btn').attr('onClick','get_all_trips(\''+(to-4)+'\',\''+to+'\')');
      }else{
        alert('Error: '+data.error);
      }
    },
    error:(e,rs)=>{
      alert('Error Please Contact Admin');
    }
  });
}
