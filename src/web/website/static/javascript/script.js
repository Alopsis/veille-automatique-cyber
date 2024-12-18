



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
    $('#valider').on("click",function(){
        console.log("on click")
        let sources = [];
        $('.source-checkbox').each(function() {
            if ($(this).is(":checked") == false) { 
                const value = $(this).val(); 
                if (!sources.includes(value)) { 
                    sources.push(value); 
                }
            }
        });
        
        console.log(sources)
        $.ajax({
            url: "http://127.0.0.1:5000/valider",
            type:"POST",
            data:{
                sources: sources
            },
            success: function(response){
                console.log(response);
                $('#super-container').html(response);
            },
            error: function(xhr, status,error){
                console.error("Ko");
            }
        })
    })
    $('#add-frise').on("click",function(){
        let nom = $("#frise-input-name").val();
        console.log(nom);
        if (nom == ""){
            return; 
        }
        $.ajax({
            url: "http://127.0.0.1:5000/add/frise",
            type: "POST",
            data:{
                nom: nom
            },
            success: function(response){
                console.log(response);
            },
            error: function(xhr, status, error){
                
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

