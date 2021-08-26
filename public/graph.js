function get_url_vars() {
    // Function get_url_args
    // This funtion gets the arguments passed throught the url and returns them as a dictionary
    var vars = {};
    window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
        vars[key] = value;
    });
    return vars;
}

function show_map_2D(url) {

    // show_map_2D
    // This function fetches the twitter map and then displays it in
    // a force-graph (2D version)

    fetch(url)
        .then(function (response) {
            return response.json();
        })
        .then(function (twitter_map) {
            const Graph = ForceGraph()
            (document.getElementById('graph'))
                .backgroundColor('#101020')
                .nodeAutoColorBy('followers') //Random colour
                .linkColor(() => '#484848') //Link colour
                .nodeCanvasObject((node, ctx, globalScale) => { //Controls text
                    const label = node.name;
                    const fontSize = 12/globalScale * (0.75 + node.followers/100000000*1.5); // Text size
                    ctx.font = `${fontSize}px Sans-Serif`;
                    const textWidth = ctx.measureText(label).width;
                    const bckgDimensions = [textWidth, fontSize].map(n => n + fontSize * 0.2); // some padding
                    

                    ctx.textAlign = 'center';
                    ctx.textBaseline = 'middle';
                    ctx.fillStyle = node.color;
                    ctx.fillText(label, node.x, node.y);
        
                    node.__bckgDimensions = bckgDimensions; // to re-use in nodePointerAreaPaint
                })
                .nodePointerAreaPaint((node, color, ctx) => { // Area where mouse hovers over to activate txt box
                    ctx.fillStyle = color;
                    const bckgDimensions = node.__bckgDimensions;
                    bckgDimensions && ctx.fillRect(node.x - bckgDimensions[0] / 2, node.y - bckgDimensions[1] / 2, ...bckgDimensions);
                })
                .graphData(twitter_map);
            Graph.d3Force('charge').strength(-300); // Power between nodes

        })
        .catch(function (err) {
            console.log('Error: ' + err);
        });
}

function show_map_3D(url) {

    // Function show_map_3D
    // This function fetches the twitter map and then displays it in
    // a force-graph (3D graph)

    const Graph = ForceGraph3D()
        (document.getElementById('graph'))
        .jsonUrl(url) // Load twitter map
        .nodeAutoColorBy('followers') // Random colour
        .linkColor(() => '#FFFFFF') // Link colour
        .nodeThreeObject(node => {
            const sprite = new SpriteText(node.name);
            sprite.material.depthWrite = false; // make sprite background transparent
            sprite.color = node.color;
            sprite.textHeight = (4 + node.followers/100000000*25); // Size of text
            return sprite;
        })

    Graph.d3Force('charge').strength(-300); // Power between nodes
}


var urlArgs = get_url_vars();

if (urlArgs["map"] === undefined) { // If no map passed through url arguments
    throw Error("No map has been requested")
}


var url = `./Maps/${urlArgs["map"]}/TwitterMap.json`;
if (urlArgs["version"] == "3D") { // If 3D version specified
    show_map_3D(url)
} else {
    show_map_2D(url)
}