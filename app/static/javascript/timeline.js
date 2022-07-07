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

const delform = document.getElementById("delete");

delform.addEventListener('submit', e => {
    e.preventDefault();
    const id = new FormData(delform);
    fetch('/api/timeline_post', {
        method: 'DELETE',
        body: id,
    })
    .then(res => res.text())
    .then(data => {
        console.log(data);
        location.reload();
    });
})