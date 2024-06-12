document.addEventListener('DOMContentLoaded', function() {
  const editButtons = document.querySelectorAll('.edit-button');
  editButtons.forEach(button => {
    button.addEventListener('click', () => {
      const postID = button.getAttribute('data-post-id');
      edit_post(postID);
    });
  });
});

// Pagination
function goToPage(maxPage) {
  let input = document.getElementById("page_input");
  let page = parseInt(input.value);

  if (page >= 1 && page <= maxPage) {
      window.location.href = "?page=" + page;
  } else {
      alert("Please enter a valid page number between 1 and " + maxPage);
  }
}

  //Hide post_view and show post_edit
  function edit_post(ID) {
    let postViewId = `#post_view_${ID}`;
    let postEditId = `#post_edit_${ID}`;
    let saveButtonId = `#save_button_${ID}`

    console.log (postViewId, postEditId, saveButtonId);

    let editElement = document.querySelector(postEditId);
    let postElement = document.querySelector(postViewId);
    let saveButton = document.querySelector(saveButtonId);
    let textArea = document.querySelector(`#post_edit_${ID} textarea`);
    
    editElement.className = 'card m-3 border rounded d-flex flex-column'
    editElement.style.display = 'block';
    postElement.className = ''
    postElement.style.display = 'none';


    saveButton.addEventListener('click', () => {
        fetch(`/post/${ID}`, {
            method: 'PUT',
            body: JSON.stringify({
                body: textArea.innerHTML,
            })
        })
    })


    
  }
