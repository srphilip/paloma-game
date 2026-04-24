const gameData = [
    { palavra: "Abelha", letra: "A", imagem: "images/abelha.jpg", som: "sounds/abelha.mp3" },
    { palavra: "Bola", letra: "B", imagem: "images/bola.png", som: "sounds/bola.mp3" },
    { palavra: "Gato", letra: "G", imagem: "images/gato.png", som: "sounds/gato.mp3" },
    { palavra: "Sapo", letra: "S", imagem: "images/sapo.png", som: "sounds/sapo.mp3" }
];

let score = 0;
let totalItems = 3;
let currentItems = [];

// Variáveis para controlar a seleção por toque
let letraSelecionada = null;
let cardSelecionadoElement = null;

const dropZoneContainer = document.getElementById('drop-zone-container');
const lettersContainer = document.getElementById('letters-container');
const scoreDisplay = document.getElementById('score');
const feedbackMessage = document.getElementById('feedback-message');
const restartBtn = document.getElementById('restart-btn');
const somAcerto = document.getElementById('som-acerto');
const somErro = document.getElementById('som-erro');

function initGame() {
    score = 0;
    letraSelecionada = null;
    cardSelecionadoElement = null;
    
    scoreDisplay.innerText = score;
    feedbackMessage.innerText = "Toque em uma letra e depois no quadro vazio!";
    feedbackMessage.style.color = "#ff9f43";
    restartBtn.classList.add('hidden');
    dropZoneContainer.innerHTML = '';
    lettersContainer.innerHTML = '';

    currentItems = shuffleArray([...gameData]).slice(0, totalItems);
    let letras = currentItems.map(item => item.letra);
    letras = shuffleArray(letras);

    currentItems.forEach(item => {
        const itemBox = document.createElement('div');
        itemBox.classList.add('item-box');
        
        // Se a imagem não for encontrada, mostra um quadrado com o nome
        itemBox.innerHTML = `
            <img src="${item.imagem}" alt="${item.palavra}" class="item-image" onerror="this.outerHTML='<div class=\\'fallback-text\\'>${item.palavra}</div>'">
            <div class="drop-zone" data-letra="${item.letra}"></div>
        `;
        dropZoneContainer.appendChild(itemBox);
    });

    letras.forEach(letra => {
        const letterCard = document.createElement('div');
        letterCard.classList.add('letra-card');
        letterCard.innerText = letra;
        
        // Evento de toque na carta
        letterCard.addEventListener('click', () => selecionarLetra(letra, letterCard));
        lettersContainer.appendChild(letterCard);
    });

    const dropZones = document.querySelectorAll('.drop-zone');
    dropZones.forEach(zone => {
        // Evento de toque no espaço vazio
        zone.addEventListener('click', () => tentarPosicionar(zone));
    });
}

function selecionarLetra(letra, elemento) {
    const todasCartas = document.querySelectorAll('.letra-card');
    todasCartas.forEach(carta => carta.classList.remove('selecionada'));

    elemento.classList.add('selecionada');
    letraSelecionada = letra;
    cardSelecionadoElement = elemento;
}

function tentarPosicionar(zonaAlvo) {
    // Retorna se nada foi selecionado ou se a zona já foi preenchida
    if (!letraSelecionada || zonaAlvo.classList.contains('dropped')) return;

    const letraCorreta = zonaAlvo.getAttribute('data-letra');

    if (letraSelecionada === letraCorreta) {
        // Acerto
        tocarSom(somAcerto);
        
        const itemObj = currentItems.find(i => i.letra === letraCorreta);
        if(itemObj && itemObj.som) {
             const somPalavra = new Audio(itemObj.som);
             setTimeout(() => tocarSom(somPalavra), 600);
        }

        zonaAlvo.innerText = letraSelecionada;
        zonaAlvo.classList.add('dropped', 'acerto-animacao');
        zonaAlvo.style.fontSize = "3rem";
        zonaAlvo.style.fontWeight = "bold";
        zonaAlvo.style.color = "#2ecc71";
        zonaAlvo.style.backgroundColor = "#e8f8f5";
        zonaAlvo.style.borderColor = "#2ecc71";
        
        if (cardSelecionadoElement) {
            cardSelecionadoElement.remove(); 
        }
        
        letraSelecionada = null;
        cardSelecionadoElement = null;
        
        score++;
        scoreDisplay.innerText = score;
        feedbackMessage.innerText = "Muito bem! Você acertou!";
        feedbackMessage.style.color = "#2ecc71";

        verificarFimDeJogo();

    } else {
        // Erro
        tocarSom(somErro);
        
        zonaAlvo.classList.add('erro-animacao');
        feedbackMessage.innerText = "Ops! Tente novamente!";
        feedbackMessage.style.color = "#e74c3c";
        
        setTimeout(() => {
            zonaAlvo.classList.remove('erro-animacao');
        }, 400);

        if (cardSelecionadoElement) {
            cardSelecionadoElement.classList.remove('selecionada');
        }
        letraSelecionada = null;
        cardSelecionadoElement = null;
    }
}

function tocarSom(audioElement) {
    if (audioElement && audioElement.readyState >= 2) {
        audioElement.currentTime = 0;
        audioElement.play().catch(() => console.log("Áudio bloqueado até a primeira interação."));
    }
}

function verificarFimDeJogo() {
    if (score === totalItems) {
        setTimeout(() => {
            feedbackMessage.innerText = "Parabéns! Você completou tudo!";
            restartBtn.classList.remove('hidden');
        }, 500);
    }
}

function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
}

restartBtn.addEventListener('click', initGame);

window.onload = initGame;