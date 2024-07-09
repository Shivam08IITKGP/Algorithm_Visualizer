const algorithms = {
    graph: [
        { name: 'Articulation Point', value: 'Articulation Point' },
        { name: 'Bridges', value: 'Bridges' },
        { name: 'Dijkstra\'s Algorithm', value: "Dijkstra's Algorithm" },
        { name: 'DFS', value: 'DFS' },
        { name: 'BFS', value: 'BFS' },
        { name: 'Kruskal MST', value: 'Kruskal MST' },
        { name: 'Prim MST', value: 'Prims MST' },
        { name: 'Random Traversal', value: 'Random Traversal' },
    ],
    strings: [
        { name: 'KMP Algorithm', value: 'KMP' },
        { name: 'Z Array Algorithm', value: 'Z-Array' },
        { name: 'Suffix Array Algorithm', value: 'Suffix Array' },
    ],
    sorting: [
        { name: 'Quick Sort', value: 'Quick Sort' },
        { name: 'Merge Sort', value: 'Merge Sort' },
        { name: 'Bubble Sort', value: 'Bubble Sort' },
        { name: 'Insertion Sort', value: 'Insertion Sort' },
    ],
    dynamic_programming: [
        { name: '0/1 Knapsack', value: '0/1 Knapsack' },
        { name: 'Duplicate Knapsack', value: 'Duplicate Knapsack' },
        { name: 'Longest Common Subsequence', value: 'Longest Common Subsequence' },
        { name: 'Longest Palindromic Subsequence', value: 'Longest Palindromic Subsequence' },
        { name: 'Longest Common Substring', value: 'Longest Common Substring' },
    ],
    trees: [
        { name:'Level Order Traversal', value: 'Level Order Traversal' },
        { name:'ZigZag Order Traversal', value: 'Zig Zag Order Traversal' },
        { name:'Lazy Propagation', value: 'Segment Tree'},
    ],
};

function updateAlgorithmList() {
    const category = document.getElementById('algorithm-category').value;
    const algorithmSelect = document.getElementById('algorithm');
    algorithmSelect.innerHTML = '<option value="">--Select Algorithm--</option>';

    if (category && algorithms[category]) {
        algorithms[category].forEach(algorithm => {
            const option = document.createElement('option');
            option.value = algorithm.value;
            option.textContent = algorithm.name;
            algorithmSelect.appendChild(option);
        });
    }
}

function toggleCustomInput() {
    const testCase = document.getElementById('test_case').value;
    const customInputBox = document.getElementById('custom-input-box');
    if (testCase === 'Custom') {
        customInputBox.style.display = 'block';
    } else {
        customInputBox.style.display = 'none';
    }
}

function updatePlaceholder() {
    const customInput = document.getElementById('custom_input');
    const algorithm = document.getElementById('algorithm').value;

    let placeholderText = '';

    if (algorithm === "Dijkstra's Algorithm" || algorithm === 'Kruskal MST' || algorithm === 'Prims MST') {
        placeholderText = `Write Directed or Undirected\nWrite the edges in format \nu v w\nFor edge (u->v weight w)\nSeparated by new lines\n(Don't write total nodes and total edges)`;
    } else if (['Articulation Point', 'Bridges', 'DFS', 'BFS', 'Random Traversal'].includes(algorithm)) {
        placeholderText = `Write Directed or Undirected\nWrite the edges in format \nu v\nFor edge (u->v) separated by new lines\n(Don't write total nodes and total edges)`;
    } else if (algorithm === 'Quick Sort' || algorithm === 'Merge Sort' || algorithm === 'Bubble Sort' || algorithm === 'Insertion Sort') {
        placeholderText = `Write the array separated by commas\nNo spaces\nExample: 1,2,3,4,5`;
    } else if (algorithm ==='KMP' || algorithm === 'Z-Array' || algorithm === 'Longest Palindromic Subsequence') {
        placeholderText = `Write the string`;
    } else if (algorithm === '0/1 Knapsack' || algorithm === 'Duplicate Knapsack') {
        placeholderText = `Write the Weights array\nWrite the Profit array\nWrite the Total Capacity\nWrite the arrays without spaces separated by commas\nExample: 1,2,3,4,5\nExample: 1,2,3,4,5\nExample: 10`;
    } else if (algorithm === 'Longest Common Subsequence' || algorithm === 'Longest Common Substring') {
        placeholderText = `Write the first string\nWrite the second string`;
    } else if (algorithm === 'Level Order Traversal' || algorithm === 'Zig Zag Order Traversal'){
        placeholderText = `No custom input for this algorithm\nSorry!`;
        // isInputDisabled = true;
    } else if (algorithm === 'Segment Tree'){
        placeholderText = `Write the array separated by commas\nNo spaces\nExample: 1,2,3,4,5\nWrite the queries in format\nl,r,val (1 based indexing)\nfor updation\nl,r\nfor query\nSeparated by new lines\n(Don't write total queries and total elements)\nThe random test case will take queries as 2,5,5 for updation\n2,4 and 1,4 for query`;
    }

    customInput.placeholder = placeholderText;
}

document.addEventListener('DOMContentLoaded', (event) => {
    const customInput = document.getElementById('custom_input');
    const algorithmSelect = document.getElementById('algorithm');
    const runButton = document.getElementById('run-button');
    const loadingIcon = document.getElementById('loading-icon');

    updatePlaceholder(); // Initial placeholder setup

    algorithmSelect.addEventListener('change', updatePlaceholder);
    customInput.addEventListener('focus', () => { customInput.placeholder = ''; });
    customInput.addEventListener('blur', updatePlaceholder);

    // Add event listener for the "Run" button
    const icons = ['🏃‍♀️', '🏊‍♀️', '🚴‍♀️']; // Running, swimming, and cycling woman emojis
    let iconIndex = 0;
    let interval;

    runButton.addEventListener('click', function () {
        // Clear any existing interval
        if (interval) clearInterval(interval);

        // Unhide the loading icon and start the cyclic rotation
        loadingIcon.style.display = 'inline-block';
        iconIndex = 0; // Reset to the first icon
        loadingIcon.textContent = icons[iconIndex];

        interval = setInterval(() => {
            iconIndex = (iconIndex + 1) % icons.length;
            loadingIcon.textContent = icons[iconIndex];
        }, 500); // Change image every 500ms
    });

    // Initially hide the loading icon
    loadingIcon.style.display = 'none';
});

