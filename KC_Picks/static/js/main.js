$(document).ready(function() {

    $('#btn-1').on('click', function(){
        $('#radio-item-1').prop('checked', true);
        $('#compare').submit();
    });

    $('#btn-2').on('click', function(){
        $('#radio-item-2').prop('checked', true);
        $('#compare').submit();
    });

    $("#sidebarCollapse").on('click', function(){
        $("#sidebar").toggleClass('active');
        var className = $('#sidebar').attr('class');
        var containsActive = className.includes("active");
        if(containsActive == true) {
            sessionStorage.setItem('sidebar', 'closed');
            //alert("Closing Sidebar");
        } else {
            //alert("Opening Sidebar");
            sessionStorage.setItem('sidebar', 'open');
        }

        //console.log(sessionStorage.getItem('sidebar'));
        
    });

});

