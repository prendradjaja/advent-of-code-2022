const { readFileSync } = require('fs');

function main(path) {
  const text = readFileSync(path, 'utf-8');
  const lines = text.trimEnd().split('\n');

  const afterHistory = [1];
  for (let line of lines) {
    const x = afterHistory[afterHistory.length - 1];
    if (line === 'noop') {
      afterHistory.push(x);
    } else {
      const v = +line.split(' ')[1];
      afterHistory.push(x);
      afterHistory.push(x + v);
    }
  }

  const answer =
    [20, 60, 100, 140, 180, 220]
      .map(idx => afterHistory[idx - 1] * idx)
      .reduce((a, b) => a + b);

  console.log(answer);
}

main(process.argv[2] || 'in');
