// window.onscroll = function() {scroll()};
  

// function scroll() {
//     var header = document.getElementById("Title");
//     var sticky = header.offsetTop;

//     if (window.pageYOffset > sticky) {
//       header.classList.add("sticky");
//     } else {
//       header.classList.remove("sticky");
//     }
// }


function submitQuestion() {
  $("#main").css("display", "none");
  $("#loader").css("display","block");

    $.ajax({
      url: '/process',
      data: {
        para: $('#Paragraph').val(),
        Q1: $('#Q1').val(),
        Q2: $('#Q2').val(),
        Q3: $('#Q3').val()
      },
      type: "POST",
      success: function(response) {
	console.log(response);
        $("#main").css("display", "block");
        $("#loader").css("display","none");
            
        for (var index = 1; index <= Object.keys(response).length; index++){
            document.getElementById("A" + index.toString()).value ="Answer: " + response["ans" + index.toString()];
            $(".ansContainer").css("display", "block");
        }

      },
      error: function(xhr){
        alert("An error occured: " + xhr.status + " " + xhr.statusText);
  	$("#main").css("display", "block");
        $("#loader").css("display","none");
      }
    })
  }

  function clearInput() {
    document.getElementById('Paragraph').value = "";
    document.getElementById('Q1').value = "";
    document.getElementById('Q2').value = "";
    document.getElementById('Q3').value = "";
    document.getElementById('A1').value = "";
    document.getElementById('A2').value = "";
    document.getElementById('A3').value = "";
    $(".ansContainer").css("display", "none");

  }
