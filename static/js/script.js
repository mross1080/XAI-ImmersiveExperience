var meter = new Tone.Meter();
Tone.Master.chain(meter);

currentState = true
var players;
// var localURL = "https://s3.us-east-2.amazonaws.com/itpcloudassets/vocals.wav"
var localURL = "joy.wav"
//var remoteURL = "https://s3.us-east-2.amazonaws.com/itpcloudassets/chants.wav"
var remoteURL = "https://s3.amazonaws.com/impressionexperience/"



var meter = new Tone.Meter();
Tone.Master.chain(meter);
var players;
var grainplayer;

var sampleUrls = { "happy": remoteURL + "joy.wav", "angry": remoteURL + "anger.wav", "rage": remoteURL + "anger.wav", "amazement": remoteURL + "anticipation.wav", "fear": remoteURL + "fear.wav", "sadness": remoteURL + "sad.mp3", "trust": remoteURL + "trust.wav" }

var micInput = new Tone.UserMedia();

function preload() {

    console.log("loading");
    console.log(sampleUrls)
    try {


        players = new Tone.Players(sampleUrls, function() {

            console.log("Done loading Sample Files ")

        }).toMaster();


    } catch (err) {
        console.log("error in player loading")
        console.log(err)

    }


    var autoWah = new Tone.AutoWah(40, 8, -30).toMaster();
    //opening the input asks the user to activate their mic

    //motu.open().then(function(){
    //  console.log("mic ready")//promise resolves when input is available
    //}).connect(autoWah).toMaster();

}

function setup() {
    document.getElementById("micControl").checked = false
}





function controlMic() {
    console.log("changing mic")
    if (!document.getElementById("micControl").checked) {


        console.log("Turning mic on")
        var autoWah = new Tone.AutoWah(50, 6, -30).toMaster();
        //opening the input asks the user to activate their mic
        micInput.open();
        micInput.connect(autoWah).toMaster();



    } else {
        console.log("closing mic")
        micInput.close();

    }

}



function changeLights(mood) {

    console.log("changing lights to : " + mood)
    //play as soon as the buffer is loaded
    players.stopAll();
    if(mood != "neutral" && mood !="ecstasy" ) {

    players.get(mood).start();
    }

    //

    $.get("/register", { "mood": mood })
        .done(function(data) {
            console.log(data)
            $("#scenestatusresponse").text("Scene Successfully changed to : " + mood);
        });
}