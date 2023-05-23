
document.getElementById("myForm").addEventListener("submit", async function(event) {
    event.preventDefault(); 
    const id1 = document.getElementById("id1").value;
    const id2 = document.getElementById("id2").value;

    const response = await fetch("/api/function1", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ id1, id2 }) 
    });

    if (response.ok) {
        const data = await response.json();
        console.log(data); // Hacer algo con la respuesta del backend
    } else {
        // Hubo un error en la solicitud
        console.error("Error en la solicitud:", response.status);
    }
});