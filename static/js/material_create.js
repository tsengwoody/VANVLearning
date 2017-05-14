$(document).ready(function() {
	$("#radioType2").on("click", function() {
		$("#titleForm").removeClass("hidden");
		$("#contentForm").addClass("hidden");
		$("#trueFalseForm").removeClass("hidden");
	});

	$("#radioType1").on("click", function() {
		$("#titleForm").removeClass("hidden");
		$("#contentForm").removeClass("hidden");
		$("#trueFalseForm").addClass("hidden");
	});

	$("#radioType3").on("click", function() {
		console.log('3rd radio is clicked');
		$.ajax({
			url: 'http://localhost:8000/MaterialADocument/get_form_info/TextForm',
		})
		.done(function(data) {
			console.log('ajax success, data is: ', data);
		})
		.fail(function(err) {
			console.log('ajax fail', err);
		})
	});
})
