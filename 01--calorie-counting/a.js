const { readFileSync } = require('fs');

const answer = readFileSync('in', 'utf-8')
  .trimEnd()
  .split('\n\n')
  .map(paragraph =>
    paragraph
      .split('\n')
      .map(line => +line)
      .reduce((a, b) => a + b) // sum
  )
  .reduce((a, b) => Math.max(a, b))

console.log(answer);
