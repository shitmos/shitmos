document.addEventListener('DOMContentLoaded', () => {
    const traits = {}; // This will hold the trait data

    fetch('trait_counts.json')
        .then(response => response.json())
        .then(data => {
            Object.assign(traits, data);
        });

    const traitTypeCanvas = document.getElementById('trait-type-wheel');
    const traitTypeContext = traitTypeCanvas.getContext('2d');
    const traitCanvas = document.getElementById('trait-wheel');
    const traitContext = traitCanvas.getContext('2d');
    const traitWheelSection = document.getElementById('trait-wheel-section');
    const spinTraitTypeButton = document.getElementById('spin-trait-type-button');
    const spinTraitButton = document.getElementById('spin-trait-button');

    const traitTypes = ['Background', 'Shit', 'Character'];
    const colors = ['#FF5733', '#33FF57', '#3357FF', '#FF33A1', '#F3FF33'];

    let spinning = false;
    let angle = 0;
    let selectedTraitType = '';

    function drawWheel(context, items, centerX, centerY, radius) {
        context.clearRect(0, 0, context.canvas.width, context.canvas.height);
        const arcSize = (2 * Math.PI) / items.length;
        items.forEach((item, index) => {
            context.beginPath();
            context.fillStyle = colors[index % colors.length];
            context.moveTo(centerX, centerY);
            context.arc(centerX, centerY, radius, index * arcSize, (index + 1) * arcSize);
            context.lineTo(centerX, centerY);
            context.fill();
            context.save();
            context.translate(centerX, centerY);
            context.rotate(index * arcSize + arcSize / 2);
            context.textAlign = 'right';
            context.fillStyle = '#000';
            context.font = 'bold 20px Arial';
            context.fillText(item, radius - 10, 10);
            context.restore();
        });
    }

    function spinWheel(context, items, centerX, centerY, radius, onFinished) {
        if (spinning) return;
        spinning = true;
        let velocity = Math.random() * 0.05 + 0.1;
        let lastFrameTime = Date.now();

        function animate() {
            const now = Date.now();
            const delta = now - lastFrameTime;
            lastFrameTime = now;
            angle += velocity * delta;
            velocity *= 0.99;
            context.clearRect(0, 0, 500, 500);
            context.save();
            context.translate(centerX, centerY);
            context.rotate(angle);
            context.translate(-centerX, -centerY);
            drawWheel(context, items, centerX, centerY, radius);
            context.restore();

            if (velocity < 0.001) {
                spinning = false;
                const selectedIdx = Math.floor(((angle % (2 * Math.PI)) / (2 * Math.PI)) * items.length);
                onFinished(items[selectedIdx]);
            } else {
                requestAnimationFrame(animate);
            }
        }

        animate();
    }

    function selectTraitType(selectedType) {
        selectedTraitType = selectedType;
        const traitValues = Object.keys(traits[selectedTraitType]);
        drawWheel(traitContext, traitValues, 250, 250, 250);
        traitWheelSection.style.display = 'block';
    }

    spinTraitTypeButton.addEventListener('click', () => {
        if (!spinning) {
            spinWheel(traitTypeContext, traitTypes, 250, 250, 250, selectTraitType);
        }
    });

    spinTraitButton.addEventListener('click', () => {
        const traitValues = Object.keys(traits[selectedTraitType]);
        if (!spinning && traitValues.length > 0) {
            spinWheel(traitContext, traitValues, 250, 250, 250, (selectedTrait) => {
                alert(`Selected ${selectedTraitType} trait: ${selectedTrait}`);
            });
        }
    });

    traitTypeCanvas.addEventListener('click', (event) => {
        const rect = traitTypeCanvas.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;
        const clickAngle = Math.atan2(y - 250, x - 250) + Math.PI * 2;
        const distance = Math.sqrt((x - 250) ** 2 + (y - 250) ** 2);

        if (distance <= 250 && !spinning) {
            const arcSize = (2 * Math.PI) / traitTypes.length;
            const clickedIndex = Math.floor((clickAngle / arcSize) % traitTypes.length);
            selectTraitType(traitTypes[clickedIndex]);
        }
    });

    // Initial draw of the trait type wheel
    drawWheel(traitTypeContext, traitTypes, 250, 250, 250);
});
