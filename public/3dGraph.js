data = "./McNasty/TwitterMutualMap.json"

const Graph = ForceGraph3D()
    (document.getElementById('graph'))
    .jsonUrl(data)
    .nodeAutoColorBy('followers')
    .linkColor(() => '#FFFFFF')
    .nodeThreeObject(node => {
        const sprite = new SpriteText(node.name);
        sprite.material.depthWrite = false; // make sprite background transparent
        sprite.color = node.color;
        sprite.textHeight = (4 + node.followers/100*25);
        return sprite;
    })

Graph.d3Force('charge').strength(-300);


