$(document).ready(function () {
    $("#loginForm").submit(function (event) {
        event.preventDefault();
        loginFunction($(this));
    });

    function loginFunction(form) {
        const loginData = {
            username: $(form).find("#username").val(),
            password: $(form).find("#password").val(),
        };

        $.ajax({
            url: "http://localhost:8220/login",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify(loginData),
            success: function (response) {
                localStorage.setItem("access_token", response.access_token);
                toast({
                    icon: "success",
                    title: "Inicio de Sesión Exitoso",
                    subtitle: "¡Bienvenido de nuevo!",
                });
            },
            error: function (xhr, status, error) {
                console.error("Error de login:", xhr.responseText);
                toast({
                    icon: "error",
                    title: "Error al intentar Iniciar Sesión",
                    subtitle: "Credenciales incorrectas",
                });
            },
        });
    }

    function toast(options) {
        var settings = $.extend(
            {
                icon: "<i class='ic-solar star-duotone'></i>",
                position: "top",
                time: 5000,
                title: "Título",
                subtitle: "",
                onClose: null,
            },
            options
        );

        const Toast = Swal.mixin({
            toast: true,
            position: settings.position,
            showConfirmButton: false,
            showCloseButton: true,
            timer: settings.time,
            timerProgressBar: true,
            didOpen: (toast) => {
                toast.onmouseenter = Swal.stopTimer;
                toast.onmouseleave = Swal.resumeTimer;
            },
            didClose: () => {
                if (typeof settings.onClose === "function") {
                    settings.onClose();
                }
            },
        });
        Toast.fire({
            icon: settings.icon,
            title: settings.title,
            text: settings.subtitle,
        });
    }
});
