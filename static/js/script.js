
function changeLights(mood) {



$.get( "/register", { "mood": mood } )
  .done(function( data ) {
    console.log(data)
     $( "#scenestatusresponse" ).text("Scene Successfully changed to : " + mood);
  });
}