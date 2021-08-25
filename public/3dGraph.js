function getUrlVars() {
    var vars = {};
    window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
        vars[key] = value;
    });
    return vars;
}

function showMap(url) {
    const Graph = ForceGraph3D()
        (document.getElementById('graph'))
        .jsonUrl(url)
        .nodeAutoColorBy('followers')
        .linkColor(() => '#FFFFFF')
        .nodeThreeObject(node => {
            const sprite = new SpriteText(node.name);
            sprite.material.depthWrite = false; // make sprite background transparent
            sprite.color = node.color;
            sprite.textHeight = (4 + (node.followers/1000000)/100*25);
            return sprite;
        })

    Graph.d3Force('charge').strength(-300);
}

var urlArgs = getUrlVars();

if (urlArgs["map"] === undefined) {
    throw Error("No map has been requested")
}

var url = `./Maps/${urlArgs["map"]}/TwitterMap.json`;

showMap(url)

