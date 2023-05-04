function strokeRoadExterior(ctx, edge) {
  ctx.beginPath();
  ctx.strokeStyle = 'yellow';
  ctx.lineWidth = 3;
  ctx.moveTo(edge[0][0], edge[0][1]);
  ctx.lineTo(edge[1][0], edge[1][1]);
  ctx.stroke();
}

function strokeRoadInterior(ctx, edge) {
  ctx.beginPath();
  ctx.strokeStyle = 'black';
  ctx.lineWidth = 1;
  ctx.moveTo(edge[0][0], edge[0][1]);
  ctx.lineTo(edge[1][0], edge[1][1]);
  ctx.stroke();
}

export function createMap(graphAsEdges, gridSize) {
  const canvas = new OffscreenCanvas(gridSize[0], gridSize[1]);

    const ctx = canvas.getContext('2d');
    for (let edge of graphAsEdges) {
      strokeRoadExterior(ctx, edge)
      strokeRoadInterior(ctx, edge)
    }

  const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
  const pixels = imageData.data;
  let cubes = [];
  for (let i = 0; i < pixels.length; i += 4) {
    console.log(pixels[i], pixels[i + 1], pixels[i + 2], pixels[i + 3]);
    const x = i / 4 % canvas.width;
    const y = Math.floor(i / 4 / canvas.width);
    let color = "green"
    console.log(pixels[i], pixels[i + 1], pixels[i + 2], pixels[i + 3])
    if (pixels[i + 3] !== 0) {
      if (pixels[i] < 200) {
        color = "black"
      }
      else {
        color = "red"
      }
    }
    cubes.push({
      "position": [x, 0, y],
      "color": color,
      "dimensions": [1, 1, 1]
    });
  }
  return cubes;
}