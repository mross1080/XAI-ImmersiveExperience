var meter = new Tone.Meter();
Tone.Master.chain(meter);

currentState = true
var players;
var localURL = "joy.wav"
//var remoteURL = "https://s3.amazonaws.com/impressionexperience/"
//var remoteURL = "http://localhost:5005/"
var remoteURL = "/static/css/"
var meter = new Tone.Meter();
Tone.Master.chain(meter);
var players;
var grainplayer;
var whiteNoiseURL = "WhiteNoiseAmbiance.mp3"
var neutralWobble = "StartupEntrance.mp3"
var startURL = "Pianodrone.mp3"

var previouslyPlaying = "happy"


var lightTargets = {
    "ecstasy": "all",
    "delight": "all",
    "happy": "all",
    "angry": "all",
    "start": "single",
    "rage": "all",
    "amazement": "all",
    "fear": "all",
    "end": "all",
    "sadness": "middle",
    "trust": "all",
    "neutral": "all",
    "darkneutral": "middle",
    "ambiance": "all",
    "neutralcuriosity": "all",
    "tension": "all"
}


var normalLevel = -3;
var extremeLevel = -4

var sampleLevels = {
    "ecstasy": -3,
    "delight": -5,
    "happy": -3,
    "angry": -3,
    "start": -3,
    "rage": -6,
    "amazement": -3,
    "fear": -4,
    "end": -3,
    "sadness": -3,
    "trust": -3,
    "neutral": -4,
    "darkneutral": -4,
    "ambiance": -4,
    "neutralcuriosity": -3,
    "tension": -3
}



var sampleUrls = {
    "ecstasy": remoteURL + "ecstasy.mp3",
    "delight": "/static/css/" + "Delight.mp3",
    "happy": remoteURL + "joy.wav",
    "angry": remoteURL + "anger.wav",
    "start": remoteURL + startURL,
    "rage": remoteURL + "BlurredDrone.mp3",
    "amazement": remoteURL + "anticipation.wav",
    "fear": remoteURL + "fear.wav",
    "sadness": remoteURL + "sad.mp3",
    "trust": remoteURL + "trust.wav",
    "neutral": remoteURL + "neutral1.mp3",
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

            console.log("Done loading Sample Files !")
            for (var i in keys) {
                console.log("setting " + players.get(keys[i]))
                players.get(keys[i]).volume.value = -Infinity
            }



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


function changeVolume(action) {
    if (action == "increase") {
        players.volume.value = players.volume.value + 1


    } else {

        players.volume.value = players.volume.value - 1
    }


}





function controlMic() {
    console.log("changing mic")
    if (!document.getElementById("micControl").checked) {


        console.log("Turning mic on")
        var reverb = new Tone.Freeverb({
            roomSize: 0.7,
            dampening: 3000
        }).toMaster();
        var pitch = new Tone.PitchShift({ "pitch": -60 }).toMaster();



        micInput.open();


        micInput.connect(reverb).connect(pitch).toMaster();
        micInput.toMaster();

        players.volume.value = -4;



    } else {
        console.log("closing mic")
        micInput.close();
        players.volume.value = -1;
    }

}


function targetLights(mood, targetSize) {
    console.log("targeting : " + targetSize)
    console.log("#" + mood + "TargetLabel")

    $("#" + mood + "TargetLabel").text("Targeting : " + targetSize);
    lightTargets[mood] = targetSize

}


var firstTrigger = true

function changeLights(mood) {

    console.log("changing lights to : " + mood)




    if (keys.includes(mood)) {
        if (mood != previouslyPlaying) {

            //Panner object
            //Tone.BufferSource(url).toMaster();

            //var osc = new Tone.LFO(0.5,-1,1).connect(panner.pan)
            //osc.start();
            if (mood != "start") {

            players.get(mood).loop = true;
            } else {
            players.get(mood).loop = false;

            }

            players.get(mood).start();
            players.get(mood).volume = -7;


            //players.get(mood).rampTo(-Infinity,10);


            //        if (!firstTrigger) {

            console.log("Moving from " + previouslyPlaying + " to " + mood)
            var previousVolume = players.get(mood).volume.value;
            var newTrackVolume = -7

            var sampleVolume = sampleLevels[mood]
            players.get(mood).volume.rampTo(sampleVolume, 3);
            players.get(previouslyPlaying).volume.rampTo(-Infinity, 8);

            setTimeout(function() {
                console.log("Stopping : " + previouslyPlaying)
                players.get(previouslyPlaying).stop()

                previouslyPlaying = mood

            }, 7000)
        }


//        else {
//
//        players.get(previouslyPlaying).volume.rampTo(-Infinity, 8);
//
//        setTimeout(function() {
//            console.log("Stopping : " + previouslyPlaying)
//            players.get(previouslyPlaying).stop()
//
//            previouslyPlaying = mood
//
//        }, 7000)
//    }



    }

    if (mood == "musicoff" || mood == "starkwhite") {

        players.stopAll();
    }

    //
    console.log("setting " + lightTargets[mood] + " to " + mood)

    $.get("/changeMood", { "mood": mood, "lightTargets": lightTargets[mood] })
        .done(function(data) {
            console.log(data)
            $("#currentMood").text("Mood currently set to : " + mood);
            $("#scenestatusresponse").text("Scene Successfully changed to : " + mood);
        });
}