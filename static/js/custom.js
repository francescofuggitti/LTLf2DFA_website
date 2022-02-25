$(document).ready(function() {

    const FUTURE_OPS = new Set(["X", "F", "U", "G", "WX", "R"]);
    const PAST_OPS = new Set(["Y", "O", "S", "H", "WY", "P"]);

    $("#inputFormula").on("keyup", function () {
    $(".spinner-border").hide();
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
      $("#Formula-alert").html("Error: You're typing a formula with both past and future operators.");
      $("#Formula-alert").show();

    }
    else{
      $("#Formula-alert").hide();
      $("#buttonFormula").attr("disabled", false);
    }
    });

    const example_formulas = [
      "X(a)",
      "F(a)",
      "G(a)",
      "a U b",
      "a & F(b)",
      "a & X(F(b & X(F(c))))",
      "G(a -> F(b))",
      "G(F(a))",
      "F(a -> F(b))",
      "(a U b) | G(a)",
      "G(a -> F(b)) & G(a -> X(b))",
      "Y(a)",
      "O(a)",
      "H(a)",
      "a S b",
      "a & O(b)",
      "a & Y(O(b & Y(O(c))))",
      "task & (!area S clean)",
      "t0 -> (battery S charge)",
      "t0 & !(battery S charge)",
      "H(a -> Y(!a S b))"
    ];

    $("#rand-example").click(function () {
      // random select a formula from examples_formulas array
      $("#inputFormula").val(example_formulas[Math.floor(Math.random() * example_formulas.length)]);
      $("#inputFormula").focus();
    });

});
