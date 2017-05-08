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
	})
})
