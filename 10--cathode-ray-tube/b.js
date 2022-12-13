const { readFileSync } = require('fs');

function main(path) {
  const text = readFileSync(path, 'utf-8');
  const lines = text.trimEnd().split('\n');

  let pixelOrder = [];
  for (let r = 0; r < 6; r++) {
    for (let c = 0; c <= 39; c++) {
      pixelOrder.push([r, c]);
    }
  }

  let x = 1;
  let adding = false;
  let answer = 0;
  let activePixel;
  const grid = {};
  for (let cycle = 1; cycle <= 240; cycle++) {
    activePixel = pixelOrder.shift();
    const [r, c] = activePixel;
    const lit = [x-1, x, x+1].includes(c);
    grid[[r, c]] = lit ? '#' : ' ';

    if (lines[0] == 'noop') {
      lines.shift();
    } else if (!adding && lines[0].startsWith('addx')) {
      adding = true;
    } else if (adding) {
      const line = lines.shift();
      const v = +line.split(' ')[1];
      x += v;
      adding = false;
    }
  }

  for (let r = 0; r < 6; r++) {
    for (let c = 0; c <= 39; c++) {
      process.stdout.write(grid[[r, c]]);
    }
    console.log();
  }
}

main(process.argv[2] || 'in');
