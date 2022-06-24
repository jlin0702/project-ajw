const form = document.getElementById("timeline-form");

form.addEventListener('submit', e => {
    e.preventDefault();
    const timeline = new FormData(form);
    fetch('/api/timeline_post', {
        method: 'POST',
        body: timeline,
    })
    .then(res => res.json())
    .then(data => {
        console.log(data);
        location.reload();
    });
})