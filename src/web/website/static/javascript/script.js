



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
    $('.btn-afficher-frise').on("click",function(){
        console.log("test");
        friseId = $(this).val();
        console.log(friseId);
        // ajax 
        $.ajax({
            url: "http://127.0.0.1:5000/affiche/frise",
            type:"POST",
            data:{
                friseId:friseId,
            },
            success: function success(response){
                $('#super-container').html(response);
                var container = document.getElementById("frise");
                var items = new vis.DataSet([
                    { id: 1, content: "item 1", start: "2014-04-20" },
                    { id: 2, content: "item 2", start: "2014-04-14" },
                    { id: 3, content: "item 3", start: "2014-04-18" },
                    { id: 4, content: "item 4", start: "2014-04-16", end: "2014-04-19" },
                    { id: 5, content: "item 5", start: "2014-04-25" },
                    { id: 6, content: "item 6", start: "2014-04-27", type: "point" },
                ]);
                var options = {};
                var timeline = new vis.Timeline(container, items, options);
                            
            },
            error: function error(xhr, status,error){
                console.log("ko");
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

