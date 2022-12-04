// I wrote this because I didn't like the fact that my Python solution has
// this repetition: `l = int(l); r = int(r)`
//
// I wanted to see if I liked this better in JS (in which .map() is a very
// concise operation, unlike Python).
//
// The result: This... is not really any better.

const { readFileSync } = require('fs');

function main() {
  const answer = readFileSync('in', 'utf-8')
    .trimEnd()
    .split('\n')
    .map(
      line =>
        line.split(',')
          .map(
            pair =>
              pair.split('-').map(n => +n)
          )
    )
    .filter(
      ([pair1, pair2]) =>
        contains(pair1, pair2) || contains(pair2, pair1)
    )
    .length;

  console.log(answer);
};

function contains(small, big) {
  return (
    big[0] <= small[0] &&
    big[1] >= small[1]
  );
}

main();
