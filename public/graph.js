function getUrlVars() {
    var vars = {};
    window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
        vars[key] = value;
    });
    return vars;
}

function showMap(url) {

    fetch(url)
        .then(function (response) {
            return response.json();
        })
        .then(function (TwitterMap) {
            const Graph = ForceGraph()
            (document.getElementById('graph'))
                .backgroundColor('#101020')
                .nodeAutoColorBy('followers')
                .linkColor(() => '#484848')
                .nodeCanvasObject((node, ctx, globalScale) => {
                    const label = node.name;
                    const fontSize = 12/globalScale * (0.75 + (node.followers/1000000)/100*1.5);
                    ctx.font = `${fontSize}px Sans-Serif`;
                    const textWidth = ctx.measureText(label).width;
                    const bckgDimensions = [textWidth, fontSize].map(n => n + fontSize * 0.2); // some padding
        
                    ctx.textAlign = 'center';
                    ctx.textBaseline = 'middle';
                    ctx.fillStyle = node.color;
                    ctx.fillText(label, node.x, node.y);
        
                    node.__bckgDimensions = bckgDimensions; // to re-use in nodePointerAreaPaint
                })
                .nodePointerAreaPaint((node, color, ctx) => {
                    ctx.fillStyle = color;
                    const bckgDimensions = node.__bckgDimensions;
                    bckgDimensions && ctx.fillRect(node.x - bckgDimensions[0] / 2, node.y - bckgDimensions[1] / 2, ...bckgDimensions);
                })
                .graphData(TwitterMap);
            Graph.d3Force('charge').strength(-300);

        })
        .catch(function (err) {
            console.log('Error: ' + err);
        });


}

var urlArgs = getUrlVars();

if (urlArgs["map"] === undefined) {
    throw Error("No map has been requested")
}

var url = `./Maps/${urlArgs["map"]}/TwitterMap.json`;

showMap(url)
