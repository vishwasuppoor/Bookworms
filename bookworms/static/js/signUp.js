$(function(){
	$('button').click(function(){
		var user = $('#inputUsername').val();
		var pass = $('#inputPassword').val();
		$.ajax({
			url: '/signUpUser',
			data: $('form').serialize(),
			type: 'POST',
			dataType: 'JSON',
			success: function(response){
				console.log(response);
				document.getElementById('placeholder').innerHTML = "Congratulations on registering for CSE6242, " + response.user + "! Redirecting you to the course homepage...";
				$('form').get(0).reset();
				setTimeout(function() {
					window.location.href = "http://poloclub.gatech.edu/cse6242/2018spring/";
				}, 3000);
				
			},
			error: function(error){
				console.log(error);
			}
		});
//		
		
	});
});
