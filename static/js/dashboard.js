$(function() {
	var BTN_UNTINTED = 'rgb(20, 100, 250)';
	var BTN_TOGGLING = 'rgb(250, 250, 0)';
	var BTN_TINTED = 'rgb(80, 220, 80)';

	$('#repos').find('button').each(function(index, button) {
		var btn = $(button);
		// initialize button color to blue
		btn.css('background-color', BTN_UNTINTED);
		btn.css('color', 'white');

		// when clicked, ping server and change color to yellow
		btn.click(function(event) {
			btn.css('background-color', BTN_TOGGLING);
			btn.css('color', 'black');

			$.post('/action', {
				'action': 'toggle-repo',
				'repo': btn.text()
			}, function(reply) {
				// when the server gets back to us, set color to green
				if (reply == 'tinted') {
					btn.css('background-color', BTN_TINTED);
					btn.css('color', 'black');
				} else if (reply == 'untinted') {
					btn.css('background-color', BTN_UNTINTED);
					btn.css('color', 'white');
				}
			});
		});

		// check repo tint-state
		$.post('/action', {
			'action': 'get-repo-state',
			'repo': btn.text()
		}, function(reply) {
			if (reply == 'tinted') {
				btn.css('background-color', BTN_TINTED);
				btn.css('color', 'black');
			} else if (reply == 'untinted') {
				btn.css('background-color', BTN_UNTINTED);
				btn.css('color', 'white');
			}
		});
	});
});
