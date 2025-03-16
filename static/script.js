document.addEventListener('DOMContentLoaded', async () => {
    try {
        
        // Fetch data from the server
        const response = await fetch('/check-connection');
        const data = await response.json();

        if (data.status === 'connected') {
            // Extract the result array from the response
            const resultArray = data.result_array; // Should be [1, 20]
            const greenTime = resultArray[1] * 1000; // Convert seconds to milliseconds
            const directionIndex = resultArray[0]; // 0 for B, 1 for C, 2 for D, 3 for E
            const c=parseInt(greenTime);
            setTimeout(function(){
                window.location.reload(1);
            }, c);
            // Map indices to junction IDs
            const junctions = ['junction-b', 'junction-c', 'junction-d', 'junction-e'];
            const greenJunction = junctions[directionIndex]; // Determine which junction to turn green

            // Yellow light duration (2 seconds)
            const yellowDuration = 2000;

            function setLight(junction, color) {
                const trafficLights = {
                    'junction-b': {
                        red: document.getElementById('red-b'),
                        yellow: document.getElementById('yellow-b'),
                        green: document.getElementById('green-b'),
                        countdown: document.getElementById('countdown-b'),
                    },
                    'junction-c': {
                        red: document.getElementById('red-c'),
                        yellow: document.getElementById('yellow-c'),
                        green: document.getElementById('green-c'),
                        countdown: document.getElementById('countdown-c'),
                    },
                    'junction-d': {
                        red: document.getElementById('red-d'),
                        yellow: document.getElementById('yellow-d'),
                        green: document.getElementById('green-d'),
                        countdown: document.getElementById('countdown-d'),
                    },
                    'junction-e': {
                        red: document.getElementById('red-e'),
                        yellow: document.getElementById('yellow-e'),
                        green: document.getElementById('green-e'),
                        countdown: document.getElementById('countdown-e'),
                    },
                };

                // Remove 'active' class from all lights in the junction
                Object.keys(trafficLights[junction]).forEach(light => {
                    trafficLights[junction][light].classList.remove('active');
                });
                // Add 'active' class to the specified light color
                trafficLights[junction][color].classList.add('active');
            }

            function updateCountdown(junction, time) {
                const countdownElement = document.getElementById(`countdown-${junction.slice(-1).toLowerCase()}`);
                let remainingTime = time / 1000; // Convert milliseconds to seconds
                countdownElement.textContent = `${remainingTime}s`;

                const intervalId = setInterval(() => {
                    remainingTime -= 1;
                    countdownElement.textContent =`${remainingTime}s`;

                    if (remainingTime <= 0) {
                        clearInterval(intervalId);
                        countdownElement.textContent = '0s';
                    }
                }, 1000);
            }

            async function cycleLights() {
                const junctionOrder = ['junction-b', 'junction-c', 'junction-d', 'junction-e'];

                // Set green for the specific junction, red for others
                for (let i = 0; i < junctionOrder.length; i++) {
                    const currentJunction = junctionOrder[i];

                    if (currentJunction === greenJunction) {
                        setLight(currentJunction, 'green');
                        updateCountdown(currentJunction, greenTime);

                        // Wait for green light duration
                        await new Promise(resolve => setTimeout(resolve, greenTime));

                        // Set yellow light
                        setLight(currentJunction, 'yellow');
                        await new Promise(resolve => setTimeout(resolve, yellowDuration));

                        // After yellow, set red for this junction and continue
                        setLight(currentJunction, 'red');
                    } else {
                        setLight(currentJunction, 'red');
                    }
                }
            }

            // Start the cycle of traffic lights for the specific junction
            cycleLights();

        } else {
            console.error('Node A not found or error occurred');
        }
    } catch (error) {
        console.error('Error fetching data from server:', error);
    }
    // Function to refresh the page every 10 seconds
    // Call autoRefresh function when the page loads
});