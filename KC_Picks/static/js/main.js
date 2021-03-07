$(document).ready(function() {

    $('#btn-1').on('click', function(){
        $('#radio-item-1').prop('checked', true);
        $('#compare').submit();
    });

    $('#btn-2').on('click', function(){
        $('#radio-item-2').prop('checked', true);
        $('#compare').submit();
    });

});