const { readFileSync } = require('fs');

const interpret = {
  'A': 'R',
  'B': 'P',
  'C': 'S',
  'X': 'R',
  'Y': 'P',
  'Z': 'S',
};

function main() {
  const answer = readFileSync('in', 'utf8')
    .trimEnd()
    .split('\n')
    .map(
      line => {
        let [l, r] = line.split(' ');
        l = interpret[l];
        r = choose(l, r);
        const choicePoints = {'R': 1, 'P': 2, 'S': 3}[r];
        const resultPoints = play(l, r);
        return choicePoints + resultPoints;
      }
    )
    .reduce((a, b) => a + b)

  console.log(answer);
}

function succ(x) {
  const RPS = 'RPS';
  return RPS[(RPS.indexOf(x) + 1) % 3];
}

function play(l, r) {
  if (l === r) {
    return 3;
  } else if (succ(l) === r) {
    return 6;
  } else {
    return 0;
  }
}

function choose(l, r) {
  if (r === 'X') {
    return succ(succ(l));
  } else if (r === 'Y') {
    return l;
  } else {
    return succ(l);
  }
}

main();
