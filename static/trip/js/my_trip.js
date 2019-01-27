$(document).ready(function(){
  get_my_trips(0,4);
  var url = window.location.href;
  var t = url.split('/');
  var user_id = t[3];
  var token = t[4];
  $('#create_trip_btn').click(()=>{
    var fcy = $('#from_loc_country').val();
    var fs = $('#from_loc_state').val();
    var fc = $('#from_loc_city').val();
    var tcy = $('#to_loc_country').val();
    var ts = $('#to_loc_state').val();
    var tc = $('#to_loc_city').val();
    var cap = $('#capacity').val();
    $.ajax({
      url:'/trip/create',
      type:'POST',
      data:{
        user_id:user_id,
        token:token,
        from_loc_country:fcy,
        from_loc_state:fs,
        from_loc_city:fc,
        to_loc_country:tcy,
        to_loc_state:ts,
        to_loc_city:tc,
        capacity:cap
      },
      success:(data)=>{
        if(data.success){
          $('#from_loc_country').val('');
          $('#from_loc_state').val('');
          $('#from_loc_city').val('');
          $('#to_loc_country').val('');
          $('#to_loc_state').val('');
          $('#to_loc_city').val('');
          $('#exampleModal').modal('hide');
          alert('Trip Created');
        }else{
          alert('Error: '+data.error);
        }
      },
      error:(e,rs)=>{
        alert('Error Please Contact Admin');
      }
    });
  });
});

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
        $('#trip_details_modal').modal('show');
        var tm = JSON.parse(data.trip_members);
        var html = '<label>Trip Members</label>';
        $('#trip_member_holder').empty();
        $('#trip_member_holder').append(html);
        html = '';
        tm.forEach((obj)=>{
          var html = '<label class="form-control">';
          html+= ''+obj.member__first_name + ' '+obj.member__last_name + ' '+obj.member__email;
          html+='</label>';
          $('#trip_member_holder').append(html);
        });
      }else{
        alert('Error: '+data.error);
      }
    },
    error:(e,rs)=>{
      alert('Error. Please Contact Administrator');
    }
  });
}

function get_my_trips(prev,next){
  prev = parseInt(prev);
  next = parseInt(next);
  var url = window.location.href;
  var t = url.split('/');
  var user_id = t[3];
  var token = t[4];
  $('#trip_data').empty();
  $.ajax({
    url:'/trip/user/'+prev+'/'+next+'/'+user_id+'/'+token,
    type:'GET',
    success:(data)=>{
      if(data.success){
        var trips = JSON.parse(data.trips);
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
          $('#trip_prev_btn').attr('onClick','get_my_trips(\''+prev+'\',\''+to+'\')');
        }else{
          prev = 0;
          to = 4;
          $('#trip_prev_btn').attr('onClick','get_my_trips(\''+prev+'\',\''+to+'\')');
        }
        to = Number(to) + 4;
        $('#trip_prev_btn').attr('onClick','get_my_trips(\''+(to-4)+'\',\''+to+'\')');
      }else{
        alert('Error: '+data.error);
      }
    },
    error:(e,rs)=>{
      alert('Error Please Contact Admin');
    }
  });
}
