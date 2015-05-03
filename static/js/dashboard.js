$(function() {
	// give each button tint-toggling power
	$('#repos').find('button').each(function(index, button) {
		var btn = $(button);
		// initialize button color to blue
		btn.css('background-color', 'rgb(20, 100, 250)');
		btn.css('color', 'white');

		// when clicked, ping server and change color to yellow
		btn.click(function(event) {
			btn.css('background-color', 'rgb(250, 250, 0)');
			btn.css('color', 'black');

			$.post('/action', {
				'action': 'toggle-repo',
				'repo': btn.text()
			}, function(reply) {
				// when the server gets back to us, set color to green
				btn.css('background-color', 'rgb(80, 220, 80)');
			});
		});
	});
});
