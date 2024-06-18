document.addEventListener('DOMContentLoaded', function() {
  // Gives editPost function for each editButton
  const editButtons = document.querySelectorAll('.edit-button');
    editButtons.forEach(editButton => {
    editButton.addEventListener('click', () => {
      let postID = editButton.closest('[data-post-id]').getAttribute('data-post-id');
      editPost(postID);
    })
  });

  // Gives likeToggle function for each likeButton
  const likeButtons = document.querySelectorAll('.like-button');
    likeButtons.forEach(likeButton => {
    likeButton.addEventListener('click', () => {
      let postID = likeButton.closest('[data-post-id]').getAttribute('data-post-id');
      toggleLikes(postID)
    })
  })
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

  
function editPost(ID) {
  // Template tags IDs
  let postViewId = `#post_view_${ID}`;
  let postEditId = `#post_edit_${ID}`;
  let saveButtonId = `#save_button_${ID}`
  let postBodyId = `#post_body_${ID}`

  // Template elements
  let editElement = document.querySelector(postEditId);
  let postElement = document.querySelector(postViewId);
  let saveButton = document.querySelector(saveButtonId);
  let editTextArea = document.querySelector(`${postEditId} textarea`);
  let postBody = document.querySelector(postBodyId)
  
  // Hide post_view and show post_edit
  editElement.className = 'card m-3 border rounded d-flex flex-column'
  editElement.style.display = 'block';
  postElement.className = ''
  postElement.style.display = 'none';

  // Add event listener for each save button to make post request with new post body
  saveButton.addEventListener('click', () => {
    //PUT request
    fetch(`/post/${ID}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')  // Adiciona o token CSRF
      },
      body: JSON.stringify({
          body: editTextArea.value,
      })
    })
    .then(response => response.json())
    .then(result => {
      if(result.success) {
        // Retrive updated post body from view and updates post
        updatedPost = result.post
        postBody.innerText = updatedPost.body

        // Hide post_edit and show post_view
        postElement.className = 'card m-3 border rounded d-flex flex-column'
        postElement.style.display = 'block';
        editElement.className = ''
        editElement.style.display = 'none';

      } else {
        alert("Error updating post:" + result.error) 
      }
    })
    .catch(error => console.error('Error:', error));
  }, { once: true })
}

function toggleLikes(ID){
  // Template ID
  let likeButtonId = `#like_button_${ID}`;

  // Template element
  let likeButton = document.querySelector(likeButtonId);

  // Post request
  fetch(`/post/${ID}/like`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')  
  },
    body: JSON.stringify({
    })
  })
  .then (response => response.json())
  .then (result => {

    if (!result.post.user_liked) {
      likeButton.innerText = `🤍 ${result.post.likes_count}`
      likeButton.title = "Like"
    } else {
      likeButton.innerText = `❤️ ${result.post.likes_count}`
      likeButton.title = "Dislike"
    }
  })
  .catch(error => console.error('Error:', error));
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}