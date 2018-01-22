$(document).ready(function() {
  const fileInput = $('#tos-file-input');
  fileInput.change(function() {
    this.form.submit();
    $('body').addClass('loading');
  });
  fileInput.click(function () {
    this.value = '';
  });
});
