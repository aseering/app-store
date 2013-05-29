// Assumes jQuery is included already

function search(txt) {
    $(".app_list_elt").each(function(index, elt) {
	if (elt.innerHTML.indexOf(txt) >= 0) {
	    $(elt).show();
	} else {
	    $(elt).hide();
	}
    });
}

$(document).ready(function() {
    $("#search_field").bind("keyup input paste", function() {
	if ($(this).val().length > 3 || $(this).val().length == 0) {
	    search($(this).val());
	}
    });
    $("#search_field").change(function() {
	search($(this).val());
    });
    $("#search_btn").click(function() {
	search($("#search_field").val());
    });
});
