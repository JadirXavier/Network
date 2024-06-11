  function goToPage() {
    let input = document.getElementById("page_input");
    let page = parseInt(input.value);
    let maxPage = {{ page_obj.paginator.num_pages }};

    if (page >= 1 && page <= maxPage) {
        window.location.href = "?page=" + page;
    } else {
        alert("Please enter a valid page number between 1 and " + maxPage);
    }
  }

