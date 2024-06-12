document.addEventListener('DOMContentLoaded', function() {
  // Seleciona todos os botões de edição
  const editButtons = document.querySelectorAll('.edit-button');
  
  // Adiciona um event listener a cada botão de edição
  editButtons.forEach(button => {
    button.addEventListener('click', () => {
      // Obtém o ID do post a partir do atributo data-post-id
      const postId = button.getAttribute('data-post-id');
      const postViewId = `#post_view_${postId}`;
      const postEditId = `#post_edit_${postId}`;
      
      // Chama a função edit_post com os IDs apropriados
      edit_post(postEditId, postViewId);
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
  function edit_post(edit, post) {
    const editElement = document.querySelector(edit);
    const postElement = document.querySelector(post);
    
    editElement.className = 'card m-3 border rounded d-flex flex-column'
    editElement.style.display = 'block';
    postElement.className = ''
    postElement.style.display = 'none';

  }
