var meter = new Tone.Meter();
Tone.Master.chain(meter);

currentState = true
var players;
var localURL = "joy.wav"
var remoteURL = "https://s3.amazonaws.com/impressionexperience/"

var meter = new Tone.Meter();
Tone.Master.chain(meter);
var players;
var grainplayer;

var sampleUrls = {"ecstasy": remoteURL + "ecstasy.mp3","delight": remoteURL + "Delight.mp3", "happy": remoteURL + "joy.wav", "angry": remoteURL + "anger.wav", "start":remoteURL + "StartupEntrance.mp3",
"rage": remoteURL + "BlurredDrone.mp3", "amazement": remoteURL + "anticipation.wav", "fear": remoteURL + "fear.wav","end":remoteURL + "ShutdownExit.mp3",
"sadness": remoteURL + "sad.mp3", "trust": remoteURL + "trust.wav","neutral":remoteURL + "WhiteNoiseAmbiance.mp3","ambiance":remoteURL + "Pianodrone.mp3", }
var keys = Object.keys(sampleUrls);

var micInput = new Tone.UserMedia();

function preload() {

    console.log("loading");
    console.log(sampleUrls)
    try {


        players = new Tone.Players(sampleUrls, function() {

            console.log("Done loading Sample Files ")
             $("#loadingModal").remove()
        }).toMaster();


    } catch (err) {
        console.log("error in player loading")
        console.log(err)
        $("#scenestatusresponse").text("Errors in loading audio : " + err);

    }



}

function setup() {
    document.getElementById("micControl").checked = false
}





function controlMic() {
    console.log("changing mic")
    if (!document.getElementById("micControl").checked) {


        console.log("Turning mic on")
        var autoWah = new Tone.AutoWah(50, 6, -30).toMaster();
        var reverb =new Tone.JCReverb(0.4).toMaster();
var pitch = new Tone.PitchShift({"pitch":-16}).toMaster();

var phaser = new Tone.Phaser({
	"frequency" : 15,
	"octaves" : 5,
	"baseFrequency" : 1000
}).toMaster();
        //opening the input asks the user to activate their mic
        micInput.open();
        micInput.connect(autoWah).connect(reverb).connect(phaser).connect(pitch).toMaster();
        players.volume.value = -4;



    } else {
        console.log("closing mic")
        micInput.close();
        players.volume.value = -1;
    }

}



function changeLights(mood) {

    console.log("changing lights to : " + mood)
    //play as soon as the buffer is loaded
    players.stopAll();
    if(keys.includes(mood) ) {

    players.get(mood).start();
    }

    //

    $.get("/changeMood", { "mood": mood })
        .done(function(data) {
            console.log(data)
             $("#currentMood").text("Mood currently set to : " + mood);
            $("#scenestatusresponse").text("Scene Successfully changed to : " + mood);
        });
}