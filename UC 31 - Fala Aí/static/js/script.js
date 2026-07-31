// =============================
// MODO ESCURO
// =============================

const botaoDark = document.getElementById("darkMode");

if (localStorage.getItem("tema") === "dark") {
    document.body.classList.add("dark-mode");
    alterarIcone(true);
}

if (botaoDark) {
    botaoDark.addEventListener("click", () => {

        document.body.classList.toggle("dark-mode");

        const ativo = document.body.classList.contains("dark-mode");

        localStorage.setItem("tema", ativo ? "dark" : "light");

        alterarIcone(ativo);

    });
}

function alterarIcone(dark) {

    if (!botaoDark) return;

    botaoDark.innerHTML = dark
        ? '<i class="bi bi-sun-fill"></i>'
        : '<i class="bi bi-moon-fill"></i>';
}


// =============================
// ANIMAÇÃO DOS CARDS
// =============================

const cards = document.querySelectorAll(".card");

cards.forEach((card, index) => {

    card.style.opacity = "0";
    card.style.transform = "translateY(20px)";

    setTimeout(() => {

        card.style.transition = ".5s";

        card.style.opacity = "1";
        card.style.transform = "translateY(0)";

    }, index * 100);

});


// =============================
// CONFIRMAÇÃO DE EXCLUSÃO
// =============================

const formulariosExcluir = document.querySelectorAll("form");

formulariosExcluir.forEach(form => {

    if (form.action.includes("excluir")) {

        form.addEventListener("submit", function (e) {

            if (!confirm("Deseja realmente excluir esta manifestação?")) {

                e.preventDefault();

            }

        });

    }

});