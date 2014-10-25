$(document).ready(function() {
	//alert("called");
$("#refresh_requests").button({ icons: { primary: "ui-icon-refresh"} }).mouseup(function(){loadrequests();});
$("#refresh_friendlist").button({ icons: { primary: "ui-icon-refresh"} }).mouseup(function(){getAllfriends();});
$("#refresh_posts").button({ icons: { primary: "ui-icon-refresh"} }).mouseup(function(){getAllPosts();});

getAllfriends();
getAllPosts();
loadrequests();
function getAllPosts(){
	$.get('/get_all_posts/',function(data){
		$('#post_area').html('');
		$.each(data,function(key,value){
			//alert(data[key]);
			//alert(key + " " + value);
			var htmldata = '';
			data_items = value.toString().split(",");
			htmldata += "<div class=\"post_thread\"><div class=\"post_top\"><div class=\"post_name\"><font color=\'WHITE\'><strong>" + data_items[1] + "</strong></font></div><div class=\"post_datetime\"><font color=\'WHITE\'><strong>" + data_items[2] + "</strong></font></div></div><div class=\"post_message\" style=\'overflow:hidden;\'><font color=\'#6AA7F7\'>" + data_items[0] + "</font></div></div><div><br><div>"
			$('#post_area').prepend(htmldata);
		});
	});

}

function loadrequests(){
	$.get('/get_friend_requests/',function(data){
		var items=[];
		if(data == "No request"){
			$('#request_names').html("No new requests");
		}else{
		    $('#request_names').html('');
			$.each(data,function(key,value){
				//alert(key + " " + value);
				$('#request_names').append("<div id=\""+key+"_dv\" style=\"border:1px solid #6AA7F7;border-radius:5px\"></div>")
				$('#'+key+'_dv').append("<p><strong>" + value + "</strong> has sent a friend request</p>").append($('<button/>',{
						text:'Accept',
						id:key,
						click:function(event){
							$.get('/accept_request/',{id:this.id},function(data){
									alert("You are now friend with " + data);
									getAllPosts();
									getAllfriends();
								});
							$('#'+key+'_dv').remove();
						}
					})).append($('<button/>',{
						text:'Reject',
						id:key,
						click:function(){
							$.get('/reject_request/',{id:this.id},function(data){
								});
							$('#'+key+'_dv').remove();
						}
					}));
					});
				}
			});
		}

function getAllfriends(){
	$.get('/get_all_friends/',function(data){
		flist = "<ul>"
		$.each(data,function(key,value){
			flist += "<li>" + value + "</li>"
		});
		flist += "</ul>"
		$('#friend_names').html(flist)
	});
}

$("#friend_request_name").autocomplete({
    source: '/autocompleteusers_name',
    select: function( event, ui ) {
            $("#friend_request_name").val(ui.item.label);
        },
        focus: function( event, ui ) {
            $("#friend_request_name").val(ui.item.label);
        },
    minLength: 1,
    delay:0,
  });
 $("#friend_request_email").autocomplete({
    source: '/autocompleteusers_email',
    select: function( event, ui ) {
            $("#friend_request_email").val(ui.item.label);
        },
        focus: function( event, ui ) {
            $("#friend_request_email").val(ui.item.label);
        },
    minLength: 1,
    delay:0,
  });
$('#request_name').mouseup(function(){
	var friendname = $("#friend_request_name").val()
	if(friendname != ""){
		$.get('/send_request/',{friendname:friendname},function(data){
			$('#name_search_result').html(data);
		});
	}
});
$('#request_email').mouseup(function(){
	var email = $("#friend_request_email").val()
	var emailregex = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
	if(!(emailregex.test(email))){
		$('#email_search_result').html("Email id is not valid");
		return false;
	}
	if(email != ""){
		$.get('/send_request/',{email:email},function(data){
			$('#email_search_result').html(data);
		});
	}
});
setInterval(refreshPage,120000);
function refreshPage(){
	loadrequests();
	getAllfriends();
	getAllPosts();
}
});
