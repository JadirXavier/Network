document.addEventListener('DOMContentLoaded', function() {
  //Gives editPost function for each editButton
  const editButtons = document.querySelectorAll('.edit-button');
  editButtons.forEach(editButton => {
    editButton.addEventListener('click', () => {
      const postID = editButton.getAttribute('data-post-id');
      editPost(postID);
    });
  });
});

//Pagination
function goToPage(maxPage) {
  let input = document.getElementById("page_input");
  let page = parseInt(input.value);

  if (page >= 1 && page <= maxPage) {
      window.location.href = "?page=" + page;
  } else {
      alert("Please enter a valid page number between 1 and " + maxPage);
  }
}

  
  function editPost(ID) {
    //Template tags IDs
    let postViewId = `#post_view_${ID}`;
    let postEditId = `#post_edit_${ID}`;
    let saveButtonId = `#save_button_${ID}`
    let postBodyId = `#post_body_${ID}`

    //Template elements
    let editElement = document.querySelector(postEditId);
    let postElement = document.querySelector(postViewId);
    let saveButton = document.querySelector(saveButtonId);
    let editTextArea = document.querySelector(`${postEditId} textarea`);
    let postBody = document.querySelector(postBodyId)
    
    //Hide post_view and show post_edit
    editElement.className = 'card m-3 border rounded d-flex flex-column'
    editElement.style.display = 'block';
    postElement.className = ''
    postElement.style.display = 'none';

    //PUT request
    saveButton.addEventListener('click', () => {
        fetch(`/post/${ID}`, {
            method: 'PUT',
            body: JSON.stringify({
                body: editTextArea.value,
            })
        })
        .then(response => response.json())
        .then(result => {
          if(result.success) {
            //Retrive updated post body with serialize() from update_post funcion from view
            updatedPost = result.post
            postBody.innerText = updatedPost.body

            //Hide post_edit and show post_view
            postElement.className = 'card m-3 border rounded d-flex flex-column'
            postElement.style.display = 'block';
            editElement.className = ''
            editElement.style.display = 'none';

          } else {
            alert("Error updating post:" + result.error) 
          }
        })
        .catch(error => console.error('Error:', error));
    })
  }
