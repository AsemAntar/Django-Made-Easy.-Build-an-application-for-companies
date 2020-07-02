$(document).ready(function () {
    $(".open-modals").on("click", function () {
        const r_id = $(this).attr("data-url");
        $("#report_id").val(r_id);
        console.log(r_id);
    });
});