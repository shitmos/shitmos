document.addEventListener('DOMContentLoaded', () => {
    const wheelCanvas = document.getElementById('wheel');
    const wheelContext = wheelCanvas.getContext('2d');
    const spinButton = document.getElementById('spin-button');
    const loadDataButton = document.getElementById('load-data-button');
    const snapshotDateInput = document.getElementById('snapshot-date');
    const layerNameInput = document.getElementById('layer-name');
    const numberOfSpinsInput = document.getElementById('number-of-spins');
    const winnersList = document.getElementById('winners-list');
    const wheelSection = document.getElementById('wheel-section');
    const winnersSection = document.getElementById('winners-section');

    let participants = []; // This will hold the wallet addresses
    let spinning = false;
    let angle = 0;
    let spinsLeft = 0;
    const colors = ['#FF5733', '#33FF57', '#3357FF', '#FF33A1', '#F3FF33'];
    const selectedWinners = new Set();

    function drawWheel(context, items, centerX, centerY, radius) {
        context.clearRect(0, 0, context.canvas.width, context.canvas.height);
        const arcSize = (2 * Math.PI) / items.length;
    
        items.forEach((item, index) => {
            // Draw the slice
            context.beginPath();
            context.fillStyle = colors[index % colors.length];
            context.moveTo(centerX, centerY);
            context.arc(centerX, centerY, radius, index * arcSize, (index + 1) * arcSize);
            context.closePath();
            context.fill();
    
            // Save the context state
            context.save();
    
            // Move to the center of the wheel
            context.translate(centerX, centerY);
    
            // Rotate to the middle of the slice
            const angle = index * arcSize + arcSize / 2;
    
            // Adjust font size based on your preference
            const fontSize = 10; // Set font size to 10px
            context.font = `bold ${fontSize}px Arial`;
    
            // Set text alignment and color
            context.textAlign = 'center';
            context.fillStyle = '#000';
    
            // Calculate the position for the text
            const textRadius = radius / 2; // Position text at half the radius
    
            // Calculate text position
            const xPos = textRadius * Math.cos(angle - Math.PI / 2);
            const yPos = textRadius * Math.sin(angle - Math.PI / 2);
    
            // Rotate the context to keep text horizontal
            context.rotate(angle);
    
            // Draw the full wallet address horizontally
            context.fillText(item, 0, -textRadius);
    
            // Restore the context state
            context.restore();
        });
    }

    function spinWheel(context, items, centerX, centerY, radius, onFinished) {
        if (spinning) return;
        spinning = true;
        let velocity = Math.random() * 0.02 + 0.07;
        let lastFrameTime = Date.now();

        function animate() {
            const now = Date.now();
            const delta = now - lastFrameTime;
            lastFrameTime = now;
            angle += velocity * delta;
            velocity *= 0.98; // Damping
            context.clearRect(0, 0, context.canvas.width, context.canvas.height);
            context.save();
            context.translate(centerX, centerY);
            context.rotate(angle);
            context.translate(-centerX, -centerY);
            drawWheel(context, items, centerX, centerY, radius);
            context.restore();

            if (velocity < 0.001) {
                spinning = false;
                const totalSegments = items.length;
                const normalizedAngle = angle % (2 * Math.PI);
                const selectedIdx = (totalSegments - Math.floor((normalizedAngle / (2 * Math.PI)) * totalSegments)) % totalSegments;
                onFinished(items[selectedIdx]);
            } else {
                requestAnimationFrame(animate);
            }
        }

        animate();
    }

    function updateWinnersList(winner) {
        const listItem = document.createElement('li');
        listItem.textContent = winner;
        winnersList.appendChild(listItem);
    }

    loadDataButton.addEventListener('click', () => {
        const snapshotDate = snapshotDateInput.value;
        const layerName = layerNameInput.value.trim();
        const numberOfSpins = parseInt(numberOfSpinsInput.value, 10);

        if (!snapshotDate || !layerName || isNaN(numberOfSpins) || numberOfSpins < 1) {
            alert('Please enter valid snapshot date, layer name, and number of spins.');
            return;
        }

        // Construct the JSON file path based on snapshot date and layer name
        const formattedDate = snapshotDate; // Assuming the date is in yyyy-mm-dd format
        const dataFilePath = `snapshots/${formattedDate}/filtered_${layerName}.json`;

        fetch(dataFilePath)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                // Extract owner addresses from the data
                participants = data.map(entry => entry.owner_addr);
                if (participants.length === 0) {
                    alert('No participants found for the given snapshot date and layer name.');
                    return;
                }
                spinsLeft = numberOfSpins;
                selectedWinners.clear();
                winnersList.innerHTML = '';
                wheelSection.style.display = 'block';
                winnersSection.style.display = 'block';
                drawWheel(wheelContext, participants, 250, 250, 250);
            })
            .catch(error => {
                console.error('Error loading data:', error);
                alert('Failed to load data. Please check the snapshot date and layer name.');
            });
    });

    spinButton.addEventListener('click', () => {
        if (!spinning && spinsLeft > 0 && participants.length > 0) {
            spinWheel(wheelContext, participants, 250, 250, 250, (selectedParticipant) => {
                if (selectedWinners.has(selectedParticipant)) {
                    alert('Participant already won. Spinning again.');
                    spinButton.click(); // Spin again
                } else {
                    selectedWinners.add(selectedParticipant);
                    updateWinnersList(selectedParticipant);
                    spinsLeft--;
                    if (spinsLeft === 0) {
                        alert('All spins completed.');
                    }
                }
            });
        } else if (spinsLeft === 0) {
            alert('No spins left.');
        }
    });
});
