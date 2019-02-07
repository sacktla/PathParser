let study_select = document.getElementById('study')
let category_select = document.getElementById('category')
let value_select    = document.getElementById('value')
//searching display is a little off. need to take into account all parameter
//upstream frmo change to ensure that the downstream only displays
//the parameters upstream
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

category_select.onchange = function(){
  category_id = category_select.value;
  fetch('/value/' + category_id).then(function(response){
    response.json().then(function(data){
      let optionHTML = '';
      for (let value of data.values){
        optionHTML += '<option value="' + value.id + '">' + value.value + '</option>';
      }

      value_select.innerHTML = optionHTML;
    });
  });
}
