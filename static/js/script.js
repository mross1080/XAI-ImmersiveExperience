
function changeLights(mood) {

//   $.ajax({
//  url: "/register",
//  context: document.body,
//   data: {
//        "VarA": VarA,
//        "VarB": VarB,
//        "VarC": VarC
//    },
//}).done(function(data) {
//    console.log(data)
//  $( this ).addClass( "done" );
//});
//
//

$.get( "/register", { "mood": mood } )
  .done(function( data ) {
    console.log(data)
  });
}