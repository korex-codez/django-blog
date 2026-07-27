document.addEventListener("DOMContentLoaded", () => {
  let btn = document.getElementById("likeBtn");

  if (btn) {
    btn.addEventListener("click", () => {
      let id = btn.dataset.id;

      fetch(`/post/${id}/like/`)
        .then((res) => res.json())

        .then((data) => {
          document.getElementById("likeCount").innerHTML = data.count;
        });
    });
  }
});
