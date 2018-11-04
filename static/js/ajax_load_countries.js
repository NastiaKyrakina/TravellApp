$(document).ready(function () {
    load_countrues();
});

function load_countrues(status = '1') {

    dataList = $("#countries");

    $.ajax({
        type: 'GET',
        async: true,
        url: '/load_countries/',
        data: "qc=" + status,
        success: function (data) {

            for (var i in data['dict']) {
                var option = document.createElement('option');
                option.value = data['dict'][i]['name'];
                dataList.append(option)
            }
        },
        dataType: 'json',
    });
}