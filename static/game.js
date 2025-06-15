const tileStyles = {
    0: "tile-0", 2: "tile-2", 4: "tile-4", 8: "tile-8",
    16: "tile-16", 32: "tile-32", 64: "tile-64", 128: "tile-128",
    256: "tile-256", 512: "tile-512", 1024: "tile-1024", 2048: "tile-2048"
};

function renderBoard(board) {
    try {
        console.log("Rendering board:", board);
        const boardDiv = document.getElementById("board");
        if (!boardDiv) {
            console.error("Board div not found!");
            return;
        }
        let html = "<table>";
        for (let row of board) {
            html += "<tr>";
            for (let cell of row) {
                const tileClass = tileStyles[cell] || "tile-0";
                const text = cell !== 0 ? cell : "";
                html += `<td class="${tileClass} ${cell !== 0 ? 'pop' : ''}">${text}</td>`;
            }
            html += "</tr>";
        }
        html += "</table>";
        boardDiv.innerHTML = html;
    } catch (error) {
        console.error("Error rendering board:", error);
        document.getElementById("board").innerHTML = "Error rendering game board. Check console for details.";
    }
}

function updateHighScores() {
    fetch("/high_scores")
        .then(response => response.json())
        .then(scores => {
            const highScoresList = document.getElementById("high-scores");
            highScoresList.innerHTML = scores.map(score => `<li>${score.score} - ${score.date}</li>`).join("");
            const highScoreDiv = document.getElementById("high-score");
            const highestScore = scores.length > 0 ? scores[0].score : 0;
            highScoreDiv.textContent = `High Score: ${highestScore}`;
        })
        .catch(error => console.error("Error fetching high scores:", error));
}

function showOverlay(message) {
    const overlay = document.getElementById("overlay");
    overlay.textContent = message;
    overlay.classList.remove("hidden");
}

function hideOverlay() {
    const overlay = document.getElementById("overlay");
    overlay.classList.add("hidden");
}

// Debounce function to limit how often a move can be triggered
function debounce(func, wait) {
    let timeout;
    return function (...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
    };
}

// Lock to prevent overlapping moves
let isMoveInProgress = false;

function move(direction) {
    if (isMoveInProgress) return; // Prevent overlapping moves
    isMoveInProgress = true;

    fetch(`/move/${direction}`, { method: "POST" })
        .then(response => response.json())
        .then(data => {
            renderBoard(data.board);
            document.getElementById("score").textContent = `Score: ${data.score}`;
            document.getElementById("status").textContent = data.status && !data.status.includes("Score") ? data.status : "";
            updateHighScores();
            if (data.status.includes("Victory") || data.status.includes("Game over")) {
                showOverlay(data.status);
                playSound();
            } else {
                hideOverlay();
            }
        })
        .catch(error => console.error("Error during move:", error))
        .finally(() => {
            isMoveInProgress = false; // Release the lock after the move is complete
        });
}

function resetGame() {
    if (isMoveInProgress) return; // Prevent reset during a move
    isMoveInProgress = true;

    fetch("/reset", { method: "POST" })
        .then(response => response.json())
        .then(data => {
            renderBoard(data.board);
            document.getElementById("score").textContent = `Score: ${data.score}`;
            document.getElementById("status").textContent = data.status && !data.status.includes("Score") ? data.status : "";
            updateHighScores();
            hideOverlay();
        })
        .catch(error => console.error("Error resetting game:", error))
        .finally(() => {
            isMoveInProgress = false;
        });
}

function playSound() {
    const audio = new Audio("/static/sound.mp3");
    audio.play().catch(error => console.log("Audio playback failed:", error));
}

// Initial render
document.addEventListener("DOMContentLoaded", () => {
    try {
        console.log("DOMContentLoaded event fired");
        const boardDiv = document.getElementById("board");
        const initialBoard = JSON.parse(boardDiv.getAttribute("data-board"));
        console.log("Initial board parsed:", initialBoard);
        renderBoard(initialBoard);
        updateHighScores();

        // Keyboard input
        document.addEventListener("keydown", event => {
            const moves = {
                "ArrowUp": "up",
                "ArrowDown": "down",
                "ArrowLeft": "left",
                "ArrowRight": "right"
            };
            const direction = moves[event.key];
            if (direction) {
                move(direction);
                event.preventDefault();
            }
        });

        // Mouse wheel input with debounce
        const debouncedMove = debounce((direction) => {
            move(direction);
        }, 300); // 300ms debounce time

        document.addEventListener("wheel", event => {
            const deltaX = event.deltaX;
            const deltaY = event.deltaY;
            let direction;
            if (Math.abs(deltaX) > Math.abs(deltaY)) {
                direction = deltaX > 0 ? "right" : "left";
            } else {
                direction = deltaY > 0 ? "down" : "up";
            }
            debouncedMove(direction);
            event.preventDefault();
        });

        // Touch swipe input
        let touchStartX, touchStartY;
        document.addEventListener("touchstart", event => {
            touchStartX = event.touches[0].clientX;
            touchStartY = event.touches[0].clientY;
        });

        document.addEventListener("touchmove", event => {
            const touchEndX = event.touches[0].clientX;
            const touchEndY = event.touches[0].clientY;
            const deltaX = touchEndX - touchStartX;
            const deltaY = touchEndY - touchStartY;
            let direction;
            if (Math.abs(deltaX) > Math.abs(deltaY)) {
                direction = deltaX > 0 ? "right" : "left";
            } else {
                direction = deltaY > 0 ? "down" : "up";
            }
            move(direction);
            event.preventDefault();
        });

        // Reset button
        document.getElementById("reset-btn").addEventListener("click", resetGame);
    } catch (error) {
        console.error("Error initializing game:", error);
        document.getElementById("board").innerHTML = "Error initializing game. Check console for details.";
    }
});