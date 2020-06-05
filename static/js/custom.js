$(document).ready(function() {
  $(window).keydown(function(event){
    if(event.keyCode == 13) {
      event.preventDefault();
      return false;
    }
  });
});
function handleClick() {
  let formula = $("#formula").val();
  if (formula != ""){
    let flag = '';
    if ($('#flag').is(":checked")) {
      flag = 'true';
    }
    else{
      flag = 'false';
    }
    //  ajax api request to ltlf2dfa.diag.uniroma1.it/dfa + handle json
    $.ajax({
      type: 'POST',
      url: 'http://ltlf2dfa.diag.uniroma1.it/dfa/'+formula+'/'+flag,
      success: [function (data) {
        let parsed = JSON.parse(data);
        if (parsed.code == "SUCCESS"){
          document.getElementById('dynamic').innerHTML = "<hr /> <p>Automaton corresponding to \"" + parsed.formula + "\"; declare assumption: "+flag+"</p>";
          document.getElementById('dynamic').innerHTML += "<img"+atob(parsed.svg)+"</img>";
        }
        else{
          document.getElementById('dynamic').innerHTML = '<hr /> <p>Request Status: ' + parsed.code + '; Error Text: ' + parsed.error+"</p>";
        }
      }]
    });
  }
}
