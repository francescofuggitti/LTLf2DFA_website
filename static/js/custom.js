$(document).ready(function() {

  const FUTURE_OPS = new Set(["X", "F", "U", "G", "WX", "R"]);
  const PAST_OPS = new Set(["Y", "O", "S", "H"]);

  $("#inputFormula").on("keyup", function () {
    var typed_formula = $("#inputFormula").val().split("");
    var upper_case = [];
    for (var i=0; i<typed_formula.length; i++){
      if (typed_formula[i] == typed_formula[i].toUpperCase())
        upper_case.push(typed_formula[i]);
    }
    var found_future = false;
    var found_past = false;
    for (var i=0; i<upper_case.length; i++){
      if (FUTURE_OPS.has(upper_case[i]))
        found_future = true;
      if (PAST_OPS.has(upper_case[i]))
        found_past = true;
    }
    if (found_future && found_past){
      $("#buttonFormula").attr("disabled", true);
      $("#mixFormula-alert").show();

    }
    else{
      $("#mixFormula-alert").hide();
      $("#buttonFormula").attr("disabled", false);
    }
  });




  //
  // $("#buttonFormula").click( function() {
  //   if ($("#inputFormula").val() !== ''){
  //     $("#buttonFormula").attr("disabled", true);
  //
  //     $.ajax({
  //       url: "/dfa",
  //       type: "POST",
  //       data: {
  //         inputFormula: $('#inputFormula').val()
  //       },
  //       success: function(response) {
  //         if (response.code === "SUCCESS"){
  //           $("#inputFormula").html(response.formula);
  //           $("#row-result").html(atob(response.svg))
  //           $("#buttonFormula").attr("disabled", false);
  //         }
  //       },
  //       error: function(xhr) {
  //         alert(xhr.code+": "+xhr.error)
  //       }
  //     });
  //   }
  //
  // });


});
