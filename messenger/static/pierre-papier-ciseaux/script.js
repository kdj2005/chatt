const choices = document.querySelectorAll('.choice');
const playerScoreEl = document.getElementById('player-score');
const computerScoreEl = document.getElementById('computer-score');
const playerChoiceEl = document.querySelector('.player-choice');
const computerChoiceEl = document.querySelector('.computer-choice');
const finalResultEl = document.querySelector('.final-result');

let playerScore = 0;
let computerScore = 0;

const gameRules = {
    pierre: { beats: 'ciseaux' },
    papier: { beats: 'pierre' },
    ciseaux: { beats: 'papier' }
};

choices.forEach(choice => {
    choice.addEventListener('click', () => {
        const playerChoice = choice.dataset.choice;
        const computerChoice = getComputerChoice();
        
        playerChoiceEl.textContent = getEmoji(playerChoice);
        computerChoiceEl.textContent = getEmoji(computerChoice);
        
        const result = determineWinner(playerChoice, computerChoice);
        
        if (result === 'win') {
            playerScore++;
            finalResultEl.textContent = 'Vous gagnez!';
        } else if (result === 'lose') {
            computerScore++;
            finalResultEl.textContent = 'Vous perdez!';
        } else {
            finalResultEl.textContent = 'Égalité!';
        }
        
        playerScoreEl.textContent = playerScore;
        computerScoreEl.textContent = computerScore;
    });
});

function getComputerChoice() {
    const choices = ['pierre', 'papier', 'ciseaux'];
    const randomIndex = Math.floor(Math.random() * 3);
    return choices[randomIndex];
}

function determineWinner(player, computer) {
    if (player === computer) return 'draw';
    return gameRules[player].beats === computer ? 'win' : 'lose';
}

function getEmoji(choice) {
    const emojis = {
        pierre: '✊',
        papier: '✋',
        ciseaux: '✌️'
    };
    return emojis[choice];
}