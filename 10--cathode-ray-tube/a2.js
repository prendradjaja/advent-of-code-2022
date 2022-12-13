const { readFileSync } = require('fs');

function main(path) {
  const text = readFileSync(path, 'utf-8');
  const lines = text.trimEnd().split('\n');

  let x = 1;
  let adding = false;
  let answer = 0;
  for (let cycle = 1; cycle <= 240; cycle++) {
    if ([20, 60, 100, 140, 180, 220].includes(cycle)) {
      answer += x * cycle;
    }
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
  console.log(answer);
}

main(process.argv[2] || 'in');
