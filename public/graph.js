url = "./Maps/ElonMusk/TwitterMap.json"
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
                const fontSize = 12/globalScale * (0.75 + node.followers/100*1.5);
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
        Graph.d3Force('charge').strength(-600);

    })
    .catch(function (err) {
        console.log('error: ' + err);
    });

