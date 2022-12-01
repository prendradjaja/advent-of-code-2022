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
  .sort((a, b) => b - a) // sort descending
  .slice(0, 3)
  .reduce((a, b) => a + b) // sum

console.log(answer);
