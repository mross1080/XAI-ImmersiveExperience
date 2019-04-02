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
var whiteNoiseURL = "WhiteNoiseAmbiance.mp3"
var neutralWobble = "StartupEntrance.mp3"
var startURL = "Pianodrone.mp3"

var previouslyPlaying = "happy"

var sampleUrls = {
    "ecstasy": remoteURL + "ecstasy.mp3",
    "delight": remoteURL + "Delight.mp3",
    "happy": remoteURL + "joy.wav",
    "angry": remoteURL + "anger.wav",
    "start": remoteURL + startURL,
    "rage": remoteURL + "BlurredDrone.mp3",
    "amazement": remoteURL + "anticipation.wav",
    "fear": remoteURL + "fear.wav",
    "end": remoteURL + "ShutdownExit.mp3",
    "sadness": remoteURL + "sad.mp3",
    "trust": remoteURL + "trust.wav",
    "neutral": remoteURL + neutralWobble,
    "darkneutral": remoteURL + neutralWobble,
    "ambiance": remoteURL + whiteNoiseURL,
    "neutralcuriosity": remoteURL + "NeutralCuriosity.mp3",
    "tension": remoteURL + "Tension.mp3"
}
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
        //var autoWah = new Tone.AutoWah(50, 6, -30).toMaster();
        var reverb = new Tone.JCReverb(0.7).toMaster();
        var pitch = new Tone.PitchShift({ "pitch": -40 }).toMaster();

        //var phaser = new Tone.Phaser({
        //  "frequency" : 15,
        //  "octaves" : 5,
        //  "baseFrequency" : 1000
        //}).toMaster();
        //opening the input asks the user to activate their mic



        micInput.open();


        //        micInput.connect(reverb).connect(pitch).toMaster();
        micInput.toMaster();
        players.volume.value = -4;



    } else {
        console.log("closing mic")
        micInput.close();
        players.volume.value = -1;
    }

}


var firstTrigger = true
function changeLights(mood) {

    console.log("changing lights to : " + mood)




    if (keys.includes(mood)) {


//Panner object
//Tone.BufferSource(url).toMaster();

//var osc = new Tone.LFO(0.5,-1,1).connect(panner.pan)
//osc.start();
        players.get(mood).loop = true;
        players.get(mood).start();
        players.get(mood).volume = -7;



        //players.get(mood).rampTo(-Infinity,10);


//        if (!firstTrigger) {

            console.log("Moving from " + previouslyPlaying + " to " + mood)
            var previousVolume = players.get(mood).volume.value;
            var newTrackVolume = -7

            setTimeout(function() {
                console.log("Stopping : " + previouslyPlaying)
                players.get(previouslyPlaying).stop()

                previouslyPlaying = mood

            }, 5000)

            setTimeout(function() {
                console.log("setting new track volume to : " + newTrackVolume)
                players.get(mood).volume.value = newTrackVolume++;
                players.get(previouslyPlaying).volume.value = previousVolume -= 2;


                setTimeout(function() {
                    console.log("setting new track volume to : " + newTrackVolume)
                    players.get(mood).volume.value = newTrackVolume += 2;
                    players.get(previouslyPlaying).volume.value = previousVolume -= 3;


                    setTimeout(function() {
                        console.log("setting new track volume to : " + newTrackVolume)
                        players.get(mood).volume.value = newTrackVolume += 2;
                        players.get(previouslyPlaying).volume.value = previousVolume -= 4;



                    }, 2000)
                }, 1500)
            }, 1000)


//         firstTrigger = false



    }

    if (mood=="musicoff") {

        players.stopAll();
    }

    //

    $.get("/changeMood", { "mood": mood })
        .done(function(data) {
            console.log(data)
            $("#currentMood").text("Mood currently set to : " + mood);
            $("#scenestatusresponse").text("Scene Successfully changed to : " + mood);
        });
}