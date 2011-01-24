function enableSubmit() {
  document.getElementById("submit_button").disabled = false;
}

function pollSubmitted() {
  document.getElementById("form_div").style.visibility = "hidden";
  document.getElementById("thank_you_div").style.visibility = "visible";
} 
