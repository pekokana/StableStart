async function init() {
    await fetch('/init', { method: 'POST' });
    alert("initialized");
}

async function run() {
    const res = await fetch('/run_year', { method: 'POST' });
    const data = await res.json();
    document.getElementById("out").innerText =
        JSON.stringify(data, null, 2);
}

async function loadHorses() {
    const res = await fetch('/horses');
    show(await res.json());
}

async function loadRaces() {
    const res = await fetch('/races');
    show(await res.json());
}

async function loadResults() {
    const year = document.getElementById("year").value;
    const res = await fetch(`/results?year=${year}`);
    show(await res.json());
}

async function loadStats() {
    const year = document.getElementById("year").value;
    const res = await fetch(`/stats/year/${year}`);
    show(await res.json());
}

function show(data) {
    document.getElementById("data").innerText =
        JSON.stringify(data, null, 2);
}