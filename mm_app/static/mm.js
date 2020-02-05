
const max_guess_count = 10;   //allowable turns to solve mystery pegs
let   guess_count = 0;
const pegs = [];              //current guess pegs    
let   result = [];            //resultant match from guess  
let   game_id;                //game being played  

const max_colors = 11;        //number of color pegs to choose from
const colors = [];

function start_game(number_of_pegs, number_of_colors) {
    const start = {
        number_of_pegs: number_of_pegs, 
        number_of_colors : number_of_colors
    };

    $.post('/start', start)
    .done( (data, status) => {
        game_id = JSON.parse(data);
        console.log(`started game[${game_id}]`);
        console.log(`status = [${status}]`);
    })
    .fail( (data, status) => {
        console.log(`fail - start_game: data[${data}]`);
        console.log(`fail - start_game: status = [${status}]`);
    });
}

function gameMessage() {
    const numRight = result.reduce((a, b) => a + b, 0);
    const remaining = max_guess_count - guess_count;
    let msg = "";
    if(numRight == pegs.length) {
        msg = `congrats you have guessed the secret pegs in ${guess_count} ${guess_count==1 ? 'guess':'guesses'}`;
        end_game();
    } else if(remaining <= 0) {
        msg = `sorry you lose, no more guesses available`;
        end_game();
    } else {
        msg = `there are a maximum of ${max_guess_count} guesses.`;
        msg += ` you have ${remaining} ${remaining==1 ? 'guess':'guesses'} left`;
    }

    $('#game-msg').text(msg);
}

function end_game() {
    $("#guess-btn").hide(100);
    $("#guess .pegs").hide(100);
    $("#replay-btn").slideDown(400);
    $.post("/end", {game_id : game_id})
    .done( (data, status) => {
        game_id = JSON.parse(data);
        console.log(`game[${game_id}] was removed`);
        console.log(`status = [${status}]`);
    })
    .fail( (data, status) => {
        console.log(`fail - end_game: data[${data}]`);
        console.log(`fail - end_game: status = [${status}]`);
    });
}

function new_game() {
    //reuse arrays
    guess_count = 0;
    pegs.length = 0; 
    result.length = 0; 

    //set 1st guess set to a random color pick
    $("#guess .peg").each(function() {
        let colorIndex = Math.floor(Math.random()*colors.length);
        pegs.push(colorIndex);
        $( this ).css( "background-color", colors[colorIndex]);
    });

    start_game(pegs.length, colors.length);
    gameMessage();
}



function init() {
    let h = Math.floor(Math.random()*10);
    let s = Math.floor(Math.random()*25)+75;
    let l = Math.floor(Math.random()*25)+50;
    let a = (Math.floor(Math.random()*50)+50)/100; //.50 - .99
    const step = Math.floor(360 / max_colors);
    for(let i=0; i < max_colors; i++) {
        colors.push(`hsla(${h},${s}%,${l}%,${a})`);
        h = (h + step) % 361;
        s = Math.floor(Math.random()*25)+75;
        l = Math.floor(Math.random()*25)+50;
        a = (Math.floor(Math.random()*50)+50)/100; 
    }

    //show current color set in header
    for(color of colors) {
        $('<div class="peg"></div>')
        .css( "background-color", color)
        .appendTo(".swatch");
    }

    //hide replay button
    $("#replay-btn").hide();
    
    new_game();
}

init();

$("#guess .peg").on("click", function() {
    const index = $("#guess .peg").index($(this));

    //increment color index for this peg
    let colorIndex = pegs[index]; 
    colorIndex++;
    if(colorIndex >= colors.length) colorIndex = 0;
    pegs[index] = colorIndex;
    
    $( this ).css( "background-color", colors[colorIndex]);
});

$("#guess").on("submit", function(e) {
    e.preventDefault();
    let guessed =`<div class="guess-count">${++guess_count}</div>`;
    if(guess_count <= max_guess_count) {
        $.post("/guess",{ game_id : game_id, pegs: JSON.stringify(pegs) }) 
        .done( (data, status) => {
            result = JSON.parse(data);
            console.log(`result = [${result}]`);
            console.log(`status = [${status}]`);
            //console.log(result);
            let match = $('<div class="matches"></div>');
            let guess = $("#guess .pegs").clone().prepend(guessed);;
            for(r of result) {
                if(r==1) {
                    $(`<div class="exact-match"></div>`).appendTo(match);
                } else if(r==0) {
                    $(`<div class="color-match"></div>`).appendTo(match);
                }
            }
            $("#guess-btn").fadeOut(100).fadeIn(100);
            match.appendTo(guess);
            guess.prependTo(".board").hide().slideDown(600);
    
            gameMessage();
        })
        .fail( (data, status) => {
            console.log(`fail - guess: status = [${status}]`);
            console.log(`fail - guess: data[${data}]`);
            console.log('data');
            --guess_count; //reverse guess_count post
        });
    }

});

$("#replay-btn").on("click", function() {
    $("#replay-btn").slideUp(300);
    $(".board .pegs").fadeOut(300).remove();
    $("#guess-btn").slideDown(300);
    $("#guess .pegs").slideDown(300);
    new_game();
});

