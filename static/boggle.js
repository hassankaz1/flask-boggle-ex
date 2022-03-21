class Boggle {
    /* make a new game at this DOM id */
    constructor(game, time = 60) {
        this.time = time; // game length
        this.score = 0;
        this.words = new Set();
        this.board = $(`#${game}`);

        this.showTimer();
        // every 1000 msec, "tick"
        this.timer = setInterval(this.countdown.bind(this), 1000);
        $(".word-input", this.board).on("submit", this.handleSubmit.bind(this));
    }
    /* show word in list of words */
    showWord(word) {
        $(".words", this.board).append($("<li>", { text: word }).addClass("added"));
    }
    /* show score in html */
    showScore() {
        $(".score", this.board).text(this.score);
    }
    /* show a status message */
    showMessage(msg, cls) {
        $(".msg", this.board)
            .text(msg)
            .removeClass()
            .addClass(`msg ${cls}`);
    }
    /* handle submission of word: if unique and valid, score & show */
    async handleSubmit(evt) {
        evt.preventDefault();
        //from the form get value from user input
        const $word = $(".word", this.board);
        let input = $word.val();

        //if no word inputed return
        if (!input) return;

        //check if user inputted previously used word
        if (this.words.has(input)) {
            this.showMessage(`This word: ${input} has already been used`, "err");
            return;
        }
        // check server for validity
        const resp = await axios.get("/word-check", { params: { input: input } });
        //if not a valid word
        if (resp.data.result === "not-word") {
            this.showMessage(`${input} is not a valid English word`, "err");
        } else if (resp.data.result === "not-on-board") { //not valid word for this board
            this.showMessage(`${input} is not a valid word on this board`, "err");
        } else { //else add word to score and display words
            this.showWord(input);
            this.score += input.length;
            this.showScore();
            this.words.add(input);
            this.showMessage(`Added: ${input}`, "ok");
        }
        $word.val("").focus();
    }
    /* Update timer in DOM */
    showTimer() {
        $(".timer", this.board).text(this.time);
    }
    /* Tick: handle a second passing in game */
    async countdown() {
        this.time -= 1;
        this.showTimer();
        if (this.time === 0) {
            clearInterval(this.timer);
            await this.endGame();
        }
    }
    //end of the game, score the game
    async endGame() {
        console.log("HELLO")
        $(".word-input", this.board).hide();
        console.log($(".play-again", this.board))
        $(".play-again", this.board).show();
        const resp = await axios.post("/end-game", { score: this.score });
        if (resp.data.newRecord) {
            this.showMessage(`New record: ${this.score}`, "ok");
        } else {
            this.showMessage(`Final score: ${this.score}`, "ok");
        }
    }
}

let newGame = new Boggle("game", 60)