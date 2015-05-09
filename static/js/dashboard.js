$(function() {
	$('#repos').find('button').each(function(index, button) {
		var btn = $(button);

		// when clicked, ping server and change color to yellow
		btn.click(function(event) {
			btn.removeClass('tinted untinted');
			btn.addClass('toggling');

			$.post('/action', {
				'action': 'toggle-repo',
				'repo': btn.text()
			}, function(reply) {
				btn.removeClass('toggling');

				// change color to reflect new state
				if (reply == 'tinted') {
					btn.addClass('tinted');
				} else if (reply == 'untinted') {
					btn.addClass('untinted');
				}
			});
		});

		// check repo tint-state
		$.post('/action', {
			'action': 'get-repo-state',
			'repo': btn.text()
		}, function(reply) {
			if (reply == 'tinted') {
				btn.removeClass('tinted untinted toggling');
				btn.addClass('tinted');
			} else if (reply == 'untinted') {
				btn.removeClass('tinted untinted toggling');
				btn.addClass('untinted');
			}
		});
	});
});
