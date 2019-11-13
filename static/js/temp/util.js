window.onscroll = function() {scroll()};


function scroll() {
    var header = document.getElementById("Title");
    var sticky = header.offsetTop;

    if (window.pageYOffset > sticky) {
      header.classList.add("sticky");
    } else {
      header.classList.remove("sticky");
    }
}


function submitQuestion() {
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
        for (var index = 1; index <= Object.keys(response).length; index++){
            document.getElementById("A" + index).value = response["ans" + index];
        }

      },
      error: function(xhr){
        alert("An error occured: " + xhr.status + " " + xhr.statusText);
      }
    })
}