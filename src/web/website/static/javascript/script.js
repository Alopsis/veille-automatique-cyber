function containsOnlyLetters(str) {
    return /^[a-zA-Z]+$/.test(str);
}



$(document).ready(function() {
    $(".generateSubDomain").on("click", function() {
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

    $('#btn-add-company').on("click",function(){
        if(containsOnlyLetters){
            companyName = $('#company-value').val()
            console.log(companyName)
            $.ajax({
                url: "http://127.0.0.1:5000/company/generate/"+companyName,
                type:"POST",
                data: {
                    companyName: companyName
                },
                success: function(response){
                    console.log("Ok");
                },
                error: function(xhr, status, error){
                    console.error("Ko");
                }
            })
        }

    })

    var nodes = new vis.DataSet([
        {id: 1, label: 'Node 1'},
        {id: 2, label: 'Node 2'},
        {id: 3, label: 'Node 3'},
        {id: 4, label: 'Node 4'},
        {id: 5, label: 'Node 5'}
    ]);
    var edges = new vis.DataSet([
        {from: 1, to: 3},
        {from: 1, to: 2},
        {from: 2, to: 4},
        {from: 2, to: 5}
    ]);
    var container = document.getElementById('mynetwork');
    var data = {
        nodes: nodes,
        edges: edges
    };
    var options = {};
    var network = new vis.Network(container, data, options);
    network.on('click', function (params) {
        alert('Clique sur un élément : ' + params.nodes);
    });
    
});



function printSubDomainGraph(subDomains, apexName) {
    // Création des nœuds
    let nodes = new vis.DataSet();
    let edges = new vis.DataSet();

    // Ajouter le nœud principal pour le domaine apex
    nodes.add({ id: apexName, label: apexName });

    // Ajouter les sous-domaines comme nœuds et relier au domaine apex
    subDomains.forEach((subDomain, index) => {
        nodes.add({ id: subDomain, label: subDomain });
        edges.add({ from: subDomain, to: apexName }); // Chaque sous-domaine pointe vers le domaine apex
    });

    // Conteneur HTML où le graphe sera rendu
    var container = document.getElementById('mynetwork');

    // Données du graphe
    var data = {
        nodes: nodes,
        edges: edges
    };

    // Options pour le graphe
    var options = {
        interaction: { hover: true },
        nodes: {
            shape: 'dot',
            size: 16,
            font: {
                size: 14
            },
            borderWidth: 2
        },
        edges: {
            width: 2,
            color: {
                color: '#848484',
                highlight: '#848484',
                hover: '#848484'
            },
            arrows: {
                to: { enabled: true, scaleFactor: 1 }
            }
        }
    };

    var network = new vis.Network(container, data, options);

    network.on('click', function (params) {
        if (params.nodes.length > 0) {
            alert('Clique sur le nœud : ' + params.nodes[0]);
        }
    });
}