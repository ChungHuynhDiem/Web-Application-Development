// fetch("/ChangePassWord", {
//   method: "POST",
//   headers: {
//     "Content-Type": "application/json",
//   },
//   body: JSON.stringify({
//     old_password,
//     new_password,
//     confirm_password,
//   }),
// })
//   .then(async (res) => {
//     if (res.status === 200) {
//       return res.json();
//     } else if (res.status === 400) {
//       const errorData = await res.json();
//       throw new Error(errorData.message);
//     } else {
//       throw new Error("Unexpected response");
//     }
//   })
//   .then((data) => {
//     const flash = document.getElementById("flash-message");
//     flash.innerHTML = `<div class="alert alert-${data.status}">${data.message}</div>`;

//     if (data.status === "success" && data.redirect) {
//       setTimeout(() => (window.location.href = data.redirect), 1500);
//     }
//   })
//   .catch((err) => {
//     const flash = document.getElementById("flash-message");
//     flash.innerHTML = `<div class="alert alert-danger">${err.message}</div>`;
//   });

document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("changePasswordForm");
  const flashContainer = document.getElementById("ajax-flash-message");
  const submitBtn = document.getElementById("submit-btn");
  const submitText = document.getElementById("submit-text");
  const spinner = document.getElementById("spinner");

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    // Show loading state
    submitText.textContent = "Обработка...";
    spinner.style.display = "inline-block";
    submitBtn.disabled = true;

    // Clear previous messages
    flashContainer.style.display = "none";
    flashContainer.innerHTML = "";

    const formData = {
      old_password: document.getElementById("old_password").value,
      new_password: document.getElementById("new_password").value,
      confirm_password: document.getElementById("confirm_password").value,
    };

    fetch("/ChangePassWord", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    })
      .then((response) => {
        if (response.ok) {
          return response.json();
        }
        return response.json().then((err) => {
          throw err;
        });
      })
      .then((data) => {
        // Show success message
        flashContainer.innerHTML = `
                <div class="alert alert-${data.status} alert-dismissible fade show">
                    ${data.message}
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
            `;
        flashContainer.style.display = "block";

        if (data.status === "success") {
          // Reset form on success
          form.reset();

          // Redirect if needed
          if (data.redirect) {
            setTimeout(() => {
              window.location.href = data.redirect;
            }, 1500);
          }
        }
      })
      .catch((error) => {
        // Show error message
        const message =
          error.message || "Произошла ошибка. Пожалуйста, попробуйте снова.";
        flashContainer.innerHTML = `
                <div class="alert alert-danger alert-dismissible fade show">
                    ${message}
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
            `;
        flashContainer.style.display = "block";
      })
      .finally(() => {
        // Reset button state
        submitText.textContent = "Сменить пароль";
        spinner.style.display = "none";
        submitBtn.disabled = false;
      });
  });
});