document.addEventListener('DOMContentLoaded', function() {
    const container = document.querySelector('.grid-container');
    const numRows = Math.ceil(window.innerHeight / 32);
    const numCols = Math.ceil(window.innerWidth / 32);

    for (let i = 0; i < numRows * numCols; i++) {
        const tile = document.createElement('div');
        tile.classList.add('tile');
        tile.style.animationDelay = `${Math.random() * 5}s`; // Add a random delay to each tile's animation
        container.appendChild(tile);
    }
});
