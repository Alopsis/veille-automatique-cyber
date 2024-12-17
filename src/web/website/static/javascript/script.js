



$(document).ready(function() {


    $("#refresh").on("click",function(){
        $.ajax({
            url: "http://127.0.0.1:5000/refresh/articles",
            type: "POST",
            success: function(response) {
                console.log("Les articles ont bien été recuperés.")
            },
            error: function(xhr, status, error){
                console.log("Une erreur est apparue lors de la récuperation des derniers articles.")
            }
        })
    })
    /*$(".generateSubDomain").on("click", function() {
        companyName = $(this).val()
        $.ajax({
            url: "http://127.0.0.1:5000/company/subdomains/"+companyName,
            type: "POST", 
            data: {
            },
            success: function(response) {
                console.log(response);
                printSubDomainGraph(response,companyName)

            },
            error: function(xhr, status, error) {
                console.error("Ko");
            },
        });
    });
    */

});

