document.getElementById("myForm").addEventListener("submit", function(event) {
    event.preventDefault();  // Evita el envío del formulario por defecto

    var id1 = document.getElementById("id1").value;
    var id2 = document.getElementById("id2").value;

    fetch('/process', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'id1': id1,
            'id2': id2
        })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("result").innerText = data.message;
    });
});
