const characters = [
  "Miss Scarlett",
  "Colonel Mustard",
  "Mrs. White",
  "Mr. Green",
  "Mrs. Peacock",
  "Professor Plum"
];

const weapons = [
  "Candlestick",
  "Revolver",
  "Rope",
  "Lead Pipe",
  "Knife",
  "Wrench"
];

const rooms = {
  "Kitchen": ["Ballroom", "Dining Room"],
  "Ballroom": ["Kitchen", "Conservatory", "Hall"],
  "Conservatory": ["Ballroom", "Library"],
  "Dining Room": ["Kitchen", "Lounge"],
  "Lounge": ["Dining Room", "Hall"],
  "Hall": ["Lounge", "Ballroom", "Study"],
  "Study": ["Hall", "Library"],
  "Library": ["Study", "Conservatory", "Billiard Room"],
  "Billiard Room": ["Library"]
};

const startingPositions = {
  "Miss Scarlett": "Lounge",
  "Colonel Mustard": "Dining Room",
  "Mrs. White": "Kitchen",
  "Mr. Green": "Conservatory",
  "Mrs. Peacock": "Library",
  "Professor Plum": "Study"
};

let state = {};

function randomChoice(list) {
  return list[Math.floor(Math.random() * list.length)];
}

function shuffle(list) {
  const copy = [...list];
  for (let i = copy.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [copy[i], copy[j]] = [copy[j], copy[i]];
  }
  return copy;
}

function initializeGame() {
  const playerCharacter = characters[0];
  const computerCharacters = characters.slice(1, 4);

  const solution = {
    character: randomChoice(characters),
    weapon: randomChoice(weapons),
    room: randomChoice(Object.keys(rooms))
  };

  const allCards = [...characters, ...weapons, ...Object.keys(rooms)];
  const solutionCards = [solution.character, solution.weapon, solution.room];
  const deck = shuffle(allCards.filter(card => !solutionCards.includes(card)));

  const players = [
    {
      name: "You",
      character: playerCharacter,
      room: startingPositions[playerCharacter],
      hand: [],
      human: true
    },
    ...computerCharacters.map((character, index) => ({
      name: `Computer Player ${index + 1}`,
      character,
      room: startingPositions[character],
      hand: [],
      human: false
    }))
  ];

  deck.forEach((card, index) => {
    players[index % players.length].hand.push(card);
  });

  state = {
    solution,
    players,
    currentRoom: startingPositions[playerCharacter],
    seenCards: new Set(players[0].hand),
    allCards,
    history: [],
    gameOver: false
  };

  setMessage("New game started. Move through the mansion and gather clues.");
  render();
}

function populateSelect(id, options) {
  const select = document.getElementById(id);
  select.innerHTML = "";
  options.forEach(option => {
    const element = document.createElement("option");
    element.value = option;
    element.textContent = option;
    select.appendChild(element);
  });
}

function renderBoard() {
  const board = document.getElementById("board");
  board.innerHTML = "";

  Object.entries(rooms).forEach(([room, connections]) => {
    const div = document.createElement("div");
    div.className = "room" + (room === state.currentRoom ? " active" : "");
    div.innerHTML = `
      <h3>${room}</h3>
      <p><strong>Connects to:</strong> ${connections.join(", ")}</p>
    `;
    board.appendChild(div);
  });
}

function renderStatus() {
  document.getElementById("playerCharacter").textContent = state.players[0].character;
  document.getElementById("currentRoom").textContent = state.currentRoom;

  const handList = document.getElementById("handList");
  handList.innerHTML = "";
  state.players[0].hand.sort().forEach(card => {
    const li = document.createElement("li");
    li.textContent = card;
    handList.appendChild(li);
  });
}

function renderMovement() {
  const movementButtons = document.getElementById("movementButtons");
  movementButtons.innerHTML = "";

  rooms[state.currentRoom].forEach(room => {
    const button = document.createElement("button");
    button.textContent = room;
    button.onclick = () => moveToRoom(room);
    movementButtons.appendChild(button);
  });
}

function renderNotebook() {
  const seenCards = document.getElementById("seenCards");
  seenCards.innerHTML = "";
  Array.from(state.seenCards).sort().forEach(card => {
    const li = document.createElement("li");
    li.textContent = card;
    seenCards.appendChild(li);
  });

  const unknownCards = document.getElementById("unknownCards");
  unknownCards.innerHTML = "";
  state.allCards
    .filter(card => !state.seenCards.has(card))
    .sort()
    .forEach(card => {
      const li = document.createElement("li");
      li.textContent = card;
      unknownCards.appendChild(li);
    });

  const historyList = document.getElementById("historyList");
  historyList.innerHTML = "";

  if (state.history.length === 0) {
    historyList.textContent = "No suggestions have been made yet.";
    return;
  }

  state.history.forEach((item, index) => {
    const div = document.createElement("div");
    div.className = "history-item";
    div.innerHTML = `
      <strong>${index + 1}. ${item.suggester}</strong><br>
      Suggested: ${item.character} with the ${item.weapon} in the ${item.room}<br>
      Refuted by: ${item.refuter || "No one"}<br>
      Card shown: ${item.shownCard || "None/Unknown"}
    `;
    historyList.appendChild(div);
  });
}

function render() {
  renderBoard();
  renderStatus();
  renderMovement();
  renderNotebook();

  populateSelect("suspectSelect", characters);
  populateSelect("weaponSelect", weapons);
  populateSelect("accuseSuspectSelect", characters);
  populateSelect("accuseWeaponSelect", weapons);
  populateSelect("accuseRoomSelect", Object.keys(rooms));
}

function setMessage(message) {
  document.getElementById("messageBox").textContent = message;
}

function moveToRoom(room) {
  if (state.gameOver) return;

  if (!rooms[state.currentRoom].includes(room)) {
    setMessage("Invalid move. You can only move to connected rooms.");
    return;
  }

  state.currentRoom = room;
  state.players[0].room = room;
  setMessage(`You moved to the ${room}.`);
  render();
}

function makeSuggestion() {
  if (state.gameOver) return;

  const character = document.getElementById("suspectSelect").value;
  const weapon = document.getElementById("weaponSelect").value;
  const room = state.currentRoom;
  const suggestionCards = [character, weapon, room];

  let refuter = null;
  let shownCard = null;

  for (let i = 1; i < state.players.length; i++) {
    const player = state.players[i];
    const matches = player.hand.filter(card => suggestionCards.includes(card));

    if (matches.length > 0) {
      refuter = player;
      shownCard = randomChoice(matches);
      state.seenCards.add(shownCard);
      break;
    }
  }

  state.history.push({
    suggester: "You",
    character,
    weapon,
    room,
    refuter: refuter ? refuter.name : null,
    shownCard
  });

  if (refuter) {
    setMessage(
      `You suggested ${character} with the ${weapon} in the ${room}.\n` +
      `${refuter.name} refuted your suggestion and showed: ${shownCard}.`
    );
  } else {
    setMessage(
      `You suggested ${character} with the ${weapon} in the ${room}.\n` +
      `No one could refute this suggestion. This may be important evidence.`
    );
  }

  render();
}

function makeAccusation() {
  if (state.gameOver) return;

  const character = document.getElementById("accuseSuspectSelect").value;
  const weapon = document.getElementById("accuseWeaponSelect").value;
  const room = document.getElementById("accuseRoomSelect").value;

  const correct =
    character === state.solution.character &&
    weapon === state.solution.weapon &&
    room === state.solution.room;

  if (correct) {
    state.gameOver = true;
    setMessage(
      `Correct accusation!\n` +
      `The solution was ${character} with the ${weapon} in the ${room}.\n` +
      `You win!`
    );
  } else {
    state.gameOver = true;
    setMessage(
      `Incorrect accusation. Game over.\n` +
      `Correct solution: ${state.solution.character} with the ${state.solution.weapon} in the ${state.solution.room}.`
    );
  }

  render();
}

document.getElementById("newGameBtn").addEventListener("click", initializeGame);
document.getElementById("suggestBtn").addEventListener("click", makeSuggestion);
document.getElementById("accuseBtn").addEventListener("click", makeAccusation);

initializeGame();
