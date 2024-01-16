// CSS only !!

// The following JS is a easy way to get checked value with jQuery

var showAlert = true;

document.addEventListener('DOMContentLoaded', function() {
    document.body.classList.add('middle');
});

// for radio
$('input[type="radio"]').on('change', (event) => {
    const name = event.target.name;
    const value = event.target.value;
    if(!showAlert) return;
    // print
    swal({
        title: name,
        type: 'success',
        html: 'value: <strong>' + value + '</strong>',
        confirmButtonText: 'okay'
    })
});

// for checkbox
$('input[type="checkbox"]').on('change', (event) => {
    const name = event.target.name;
    const values = [];
    $('input[name="' + name + '"]:checked').each((index, input) => {
        values.push($(input).val());
    });
    if(!showAlert) return;
    // print
    if(values.length) {
      swal({
          title: event.target.name,
          type: 'success',
          html: 'value: <strong>' + JSON.stringify(values) + '</strong>',
          confirmButtonText: 'okay'
      })
    } else {
      swal({
          title: event.target.name,
          type: 'warning',
          html: 'Please choose a social',
          confirmButtonText: 'okay'
      })
    }
});

// enable / disabled alert
$('#toggle-alert').on('click', ()=> {
    if(showAlert) {
        $('#toggle-alert span').text('ON alert');
    } else {
        $('#toggle-alert span').text('OFF alert');
    }
    showAlert = showAlert ? false : true;
})