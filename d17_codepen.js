const DROP_DELAY = 150;
let canvas = document.getElementById('grid'); // we draw on it
let initGrid = canvas.innerHTML.trim().split('\n').map(row => row.split('')); // get it directly from the HTML, keep it for resets
let grid = initGrid.map(row => row.slice()); // an array of arrays of strings
let dropInterval; // main function interval

// button listeners
document.getElementById('start').addEventListener('click', () => start());
document.getElementById('stop').addEventListener('click', () => clearInterval(dropInterval));
document.getElementById('reset').addEventListener('click', () => {
  clearInterval(dropInterval);
  grid = initGrid.map(row => row.slice());
  canvas.innerHTML = initGrid.map(row => row.join('')).join('\n');
});

function start() {

    let visited = new Set(); // set of stringified i,j locations
    let toVisit = [[1, initGrid[0].indexOf('+')]]; // list of [i, j] locations
    let wasModified = false; // detect when to stop

    dropInterval = setInterval(() => {

        if (!toVisit.length) {
            // Create new drop
            visited = new Set();
            toVisit = [[1, initGrid[0].indexOf('+')]];
            wasModified = false;
        }

        let [i, j] = toVisit.pop(); // i, j is the current position of a drop
        visited.add([i, j].toString());
        if (grid[i][j] !== '|') {
          grid[i][j] = '|'; // wet the cell
          wasModified = true;
        }

        // draw current grid
        let gridCopy = grid.map(row => row.slice());
        gridCopy[i][j] = 'o'; // current drop
        canvas.innerHTML = gridCopy.map(row => row.join('')).join('\n');

        let isDropping = false;

        if (i + 1 >= grid.length) {
            // Reached bottom: do nothing (but we probably still want to keep dropping!)
            isDropping = true;
        } else if ('.|'.includes(grid[i + 1][j])) {
            // Can go down..
            toVisit.push([i + 1, j]);
            isDropping = true;
        } else {
          if ('.|'.includes(grid[i][j - 1]) && !visited.has([i, j - 1].toString())) {
            // Can go left and never went..
            toVisit.push([i, j - 1]);
            isDropping = true;
          }
          if ('.|'.includes(grid[i][j + 1]) && !visited.has([i, j + 1].toString())) {
            // Can go right and never went..
            toVisit.push([i, j + 1]);
            isDropping = true;
          }
        }

        if (isDropping) {
            return;
        }

        // Here our drop is stopped (not dropping), but we don't know if we need to accumulate
        // water (i.e. turn it into `~``) or simply keep it flowing.. if there are walls on both
        // sides, it means that we are inside a bucket, thus that water can accumulate.

        // Scan for a wall on the left
        let left = j;
        let leftOpen = true;
        while (grid[i][left] !== '#') {
            left -= 1;
            if (left < 0) {
                break;
            }
        }
        if (left >= 0 && '~#'.includes(grid[i + 1][left + 1])) {
            leftOpen = false;
        }

        // Scan for a wall on the right
        let right = j;
        let rightOpen = true;
        while (grid[i][right] !== '#') {
            right += 1;
            if (right >= grid[0].length) {
                break;
            }
        }
        if (right < grid[0].length && '~#'.includes(grid[i + 1][right - 1])) {
            rightOpen = false;
        }

        if (!leftOpen && !rightOpen && grid[i][j] !== '~') {
            // We are inside a bucket, water can accumulate!
            grid[i][j] = '~';
            wasModified = true;
        }

        if (!wasModified) {
          // Nothing left to do, stop dropping water
          clearInterval(dropInterval);
          canvas.innerHTML = grid.map(row => row.join('')).join('\n');
        }

    }, DROP_DELAY);

}
