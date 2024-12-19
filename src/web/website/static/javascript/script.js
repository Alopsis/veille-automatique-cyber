function isNumber(value) {
    return typeof value === 'number';
}
var timeline;

function getDataFromFrise(friseId) {
    $.ajax({
        type: "POST",
        url: "http://127.0.0.1:5000/recup/data/frise",
        data: {
            friseId: friseId,
        },
        success: function success(data) {
            var container = document.getElementById("frise");
            var items = new vis.DataSet();
            data.forEach((element, index) => {
                items.add({
                    id: index + 1,
                    content: element.valeur,
                    start: element.date,
                });
            });

            if (timeline) {
                timeline.setItems(items);
            } else {
                var options = {
                };

                timeline = new vis.Timeline(container, items, options);
                timeline.on("click", function (properties) {
                    if (properties.item) {
                        var item = items.get(properties.item);
                        console.log(item);
                    }
                });
            }
        },
        error: function error(xhr, status, error) {
            console.error("Erreur lors de la récupération des données :", error);
        },
    });
}


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

                data = getDataFromFrise(friseId);
        
                
                            
            },
            error: function error(xhr, status,error){
                console.log("ko");
            }
        })


    })
    $(document).on("click", "#btn-ajout-frise-item", function () {
        let date = $('#date-value').val();
        let value = $('#add-item-frise-value').val();
        let idfrise = $(this).data("value");
        if (value !== "" && date !== "") {
            console.log("Les champs ont été correctement remplis.");
            $.ajax({
                type:"POST",
                url: "http://127.0.0.1:5000/add/frise/item",
                data:{
                    idfrise: idfrise,
                    date: date,
                    value:value,
                },
                success: function success(response){
                    console.log("Reussi ! ");
                    getDataFromFrise(idfrise);
                }, 
                error: function error(xhr, status, error){
                    console.log("Ko");
                }
            })
        } else {
            console.error("Veuillez remplir tous les champs.");
        }
    });
    
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

