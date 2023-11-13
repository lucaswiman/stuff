class TicTacToe extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
        this.setupBoard(this);
    }

    connectedCallback() {
      this.render();
    }

    render() {
        this.shadowRoot.innerHTML = `
            <style>
              #board {
                  display: grid;
                  grid-template-columns: repeat(3, 1fr); /* Creates 3 columns */
                  grid-template-rows: repeat(3, 1fr);    /* Creates 3 rows */
                  gap: 10px;                             /* Space between cells */
                  max-width: 300px;                      /* Max width of the board */
                  margin: auto;                          /* Center the board */
              }

              .cell {
                  display: flex;
                  justify-content: center;
                  align-items: center;
                  border: 1px solid black; /* Border for each cell */
                  font-size: 24px;         /* Font size for X and O */
                  aspect-ratio: 1;         /* Makes each cell a square */
              }
              .winning-cell {
                  background-color: lightgreen;
              }
            </style>
            <h2 id="player">${this.outcome === null ? 'Current Player: ' + this.currentPlayer : this.outcome}</h2>
            <div id="board">
                ${this.gameState.map((cell, index) => `
                    <div class="cell ${this.winningSquares.includes(index) ? 'winning-cell' : ''}" data-index="${index}">
                        ${cell ? cell : ''}
                    </div>
                `).join('')}
            </div>
            <button id="new-game">New Game</button>
        `;

        this.shadowRoot.querySelectorAll('.cell').forEach(cell => {
            cell.addEventListener('click', () => this.makeMove(cell));
        });
      	let btn = this.shadowRoot.querySelector('button#new-game');
        console.log(btn)
        const board = this;
        const resetBoard = () => {
          board.setupBoard(board);
          board.render();
        }
      	btn.addEventListener('click', resetBoard);

    }

    setupBoard(board) {
      board.gameState = Array(9).fill(null);
      board.winningSquares = [];
      board.currentPlayer = 'X';
      board.isGameOver = false;
      board.outcome = null;
    }

    makeMove(cell) {
        const index = cell.dataset.index;
        if (this.gameState[index] || this.isGameOver) {
            return;
        }
        this.gameState[index] = this.currentPlayer;
        const outcome = this.checkForWinner();
        this.outcome = outcome.outcome;
        this.winningSquares = outcome.winningSquares;
        if (this.outcome !== null) {
          this.isGameOver = true;
        } else {
          this.currentPlayer = this.currentPlayer === 'X' ? 'O' : 'X';
        }
        this.render();
    }

    checkForWinner() {
        const lines = [
          [0, 1, 2],
          [3, 4, 5],
          [6, 7, 8],
          [0, 3, 6],
          [1, 4, 7],
          [2, 5, 8],
          [0, 4, 8],
          [2, 4, 6],
        ];

        for (let i = 0; i < lines.length; i++) {
            const [a, b, c] = lines[i];
            if (this.gameState[a] && this.gameState[a] === this.gameState[b] && this.gameState[a] === this.gameState[c]) {
              this.isGameOver = true;
              return {
                outcome: `Winner: ${this.gameState[a]}`,
                winningSquares: lines[i],
              };
            }
        }

        // Check for draw or continue the game
        if (!this.gameState.includes(null)) {
          this.isGameOver = true;
          return {
            outcome: 'Draw',
            winningSquares: [],
          };
        }

        return {
          outcome: null,
          winningSquares: [],
        };
    }
}

customElements.define('tic-tac-toe', TicTacToe);
