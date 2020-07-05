$(document).ready(function () {
    // a script for reports.html
    $(".open-modals").on("click", function () {
        const r_id = $(this).attr("data-url");
        $("#report_id").val(r_id);
        console.log(r_id);
    });

    // a script for home.html
    $('#div_id_production_line').on("change", function () {
        const pl = $('#id_production_line option:selected').text();
        $('#prod_line').val(pl);
    });

    // datepicker
    $(function () {
        $('.datepicker').datepicker({
            "dateFormat": 'yy-mm-dd'
        }).val();
    });


});