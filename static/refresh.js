let study_select = document.getElementById('study')
let category_select = document.getElementById('category')
let value_select    = document.getElementById('value')

study_select.onchange = function(){
  study_id = study_select.value;
  fetch('/category/' + study_id).then(function(response){
    response.json().then(function(data){
      let optionHTML = '';
      for(let category of data.categories){
        optionHTML += '<option value="' + category.id + '">' + category.category + '</option>';
      }
      category_select.innerHTML = optionHTML;
    });
  });
}
