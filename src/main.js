$(document).ready(function () {
    $("#createMovie").on("click", function () {
        insertarPelicula();
    })
    $("#createLevel").on("click", function () {
        insertarClasificacion();
    })

    function insertarPelicula() {
        const peliculaData = {
            Nombre: "Inception",
            Director: "Christopher Nolan",
            Duracion: "148 min",
            Genero: "Ciencia ficción",
            FechaLanzamiento: "2010-07-16",
            ClasificacionId: 2, // Mayores de 14
        };

        $.ajax({
            url: "http://localhost:8220/insert_movie",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify(peliculaData),
            success: function (response) {
                console.log("Película insertada:", response);
                alert("Película insertada correctamente");
            },
            error: function (xhr, status, error) {
                console.error("Error al insertar película:", xhr.responseText);
                alert("Error al insertar película");
            },
        });
    }

    function insertarClasificacion() {
        const nivelData = {
            ClasificacionDesc: "Mayores de 18",
        };

        $.ajax({
            url: "http://localhost:8220/insert_level",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify(nivelData),
            success: function (response) {
                console.log("Clasificación insertada:", response);
                alert("Clasificación insertada correctamente");
            },
            error: function (xhr, status, error) {
                console.error("Error al insertar clasificación:", xhr.responseText);
                alert("Error al insertar clasificación");
            },
        });
    }

});
