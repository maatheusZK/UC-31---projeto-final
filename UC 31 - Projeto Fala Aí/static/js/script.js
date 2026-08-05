document.addEventListener("DOMContentLoaded", () => {

    const botaoDarkMode = document.getElementById("darkMode");

    if (!botaoDarkMode) {
        return;
    }

    const body = document.body;
    const icone = botaoDarkMode.querySelector("i");

    const temaSalvo = localStorage.getItem("tema");

    if (temaSalvo === "dark") {

        body.classList.add("dark");

        icone.classList.remove("bi-moon-stars-fill");
        icone.classList.add("bi-sun-fill");

    }

    botaoDarkMode.addEventListener("click", () => {

        body.classList.toggle("dark");

        if (body.classList.contains("dark")) {

            localStorage.setItem("tema", "dark");

            icone.classList.remove("bi-moon-stars-fill");
            icone.classList.add("bi-sun-fill");

        } else {

            localStorage.setItem("tema", "light");

            icone.classList.remove("bi-sun-fill");
            icone.classList.add("bi-moon-stars-fill");

        }

    });

    

});
