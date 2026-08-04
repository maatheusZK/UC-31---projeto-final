// =====================================================
// FalaAí - JavaScript
// Melhorias de interação da interface
// =====================================================



// =====================================================
// MODO ESCURO
// =====================================================

const botaoTema = document.getElementById("modoTema");


function aplicarTema() {

    const tema = localStorage.getItem("tema");


    if (tema === "escuro") {

        document.body.classList.add("dark-mode");

    }

}



if (botaoTema) {

    botaoTema.addEventListener(
        "click",
        function () {


            document.body.classList.toggle(
                "dark-mode"
            );


            if (
                document.body.classList.contains(
                    "dark-mode"
                )
            ) {

                localStorage.setItem(
                    "tema",
                    "escuro"
                );

            } else {

                localStorage.setItem(
                    "tema",
                    "claro"
                );

            }


        }
    );

}


aplicarTema();



// =====================================================
// CONFIRMAÇÃO DE EXCLUSÃO
// =====================================================

function confirmarExclusao() {


    return confirm(

        "Tem certeza que deseja excluir esta mensagem?"

    );


}



// =====================================================
// ALERTAS AUTOMÁTICOS
// =====================================================

setTimeout(
    function () {


        const alertas =
            document.querySelectorAll(
                ".alert"
            );


        alertas.forEach(
            function(alerta) {


                alerta.style.transition =
                    "opacity .5s";


                alerta.style.opacity =
                    "0";


                setTimeout(
                    function(){

                        alerta.remove();

                    },
                    500
                );


            }
        );


    },
    4000
);



// =====================================================
// CONTADOR DE CARACTERES
// =====================================================

const campoDescricao =
    document.querySelector(
        "textarea[name='descricao']"
    );


if (campoDescricao) {


    const contador =
        document.createElement(
            "small"
        );


    contador.className =
        "text-muted";


    campoDescricao.after(
        contador
    );


    function atualizarContador(){


        contador.textContent =
            campoDescricao.value.length +
            " caracteres";


    }


    campoDescricao.addEventListener(
        "input",
        atualizarContador
    );


    atualizarContador();

}



// =====================================================
// ANIMAÇÃO DOS CARDS
// =====================================================


const cards =
    document.querySelectorAll(
        ".card"
    );


cards.forEach(
    function(card){


        card.addEventListener(
            "mouseenter",
            function(){


                card.style.transition =
                    ".3s";


            }
        );


    }
);



// =====================================================
// SCROLL SUAVE
// =====================================================

document.querySelectorAll(
    "a[href^='#']"
)
.forEach(
    function(link){


        link.addEventListener(
            "click",
            function(e){


                e.preventDefault();


                const destino =
                    document.querySelector(
                        this.getAttribute("href")
                    );


                if(destino){

                    destino.scrollIntoView({

                        behavior:
                            "smooth"

                    });

                }


            }
        );


    }
);