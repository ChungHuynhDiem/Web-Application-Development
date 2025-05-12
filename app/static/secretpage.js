// Khi người dùng nhấn nút "View"
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".view-btn").forEach((button) => {
        button.addEventListener("click", function () {
            const userId = this.getAttribute("data-id");
            console.log(userId);
            fetch(`/user_details/${userId}`)
                .then((response) => response.json())
                .then((data) => {
                    console.log(data);
                    // Gán giá trị vào các input
                    document.querySelector("#View_id").value = data.id;
                    document.querySelector("#View_UserName").value = data.UserName;
                    document.querySelector("#View_PassWord").value = data.PassWord;
                    document.querySelector("#View_FullName").value = data.FullName;
                    document.querySelector("#View_UserRole").value = data.UserRole;
                    document.querySelector("#View_CreatedAt").value = data.CreatedAt;
                    document.querySelector("#View_UpdatedAt").value = data.UpdatedAt;
                })
                .catch((error) => {
                    console.error("Error fetching user details:", error);
                });
        });
    });
});

// Khi người dùng nhấn nút "Edit"
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".edit-btn").forEach((button) => {
        button.addEventListener("click", function () {
            const userId = this.getAttribute("data-id");
            console.log(userId);
            fetch(`/user_details/${userId}`)
                .then((response) => response.json())
                .then((data) => {
                    console.log(data);
                    // Gán giá trị vào các input
                    document.querySelector("#Edit_id").value = data.id;
                    document.querySelector("#Edit_UserName").value = data.UserName;
                    document.querySelector("#Edit_PassWord").value = data.PassWord;
                    document.querySelector("#Edit_FullName").value = data.FullName;
                    document.querySelector("#Edit_UserRole").value = data.UserRole;
                    document.querySelector("#Edit_CreatedAt").value = data.CreatedAt;
                    document.querySelector("#Edit_UpdatedAt").value = data.UpdatedAt;
                })
                .catch((error) => {
                    console.error("Error fetching user details:", error);
                });
        });
    });
});

//cập nhật thông tin user
document.getElementById("EditForm").addEventListener("submit", function (e) {
    e.preventDefault(); // Ngăn form reload trang
    const editForm = document.getElementById("EditForm");
    const payload = {
        id: document.getElementById("Edit_id").value,
        UserName: document.getElementById("Edit_UserName").value,
        PassWord: document.getElementById("Edit_PassWord").value,
        FullName: document.getElementById("Edit_FullName").value,
        UserRole: document.getElementById("Edit_UserRole").value,
    };
    const formData = new FormData(editForm);
    console.log(formData);
    fetch("/update_user", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
    })
        .then((response) => {
            if (response.ok) {
                location.reload(); // Reload để cập nhật bảng
            } else {
                alert("Cập nhật thất bại!");
            }
        })
        .catch((err) => {
            console.error("Lỗi cập nhật:", err);
        });
});

// Khi người dùng nhấn nút "Delete"
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".delete-btn").forEach((button) => {
        button.addEventListener("click", function () {
            const userId = this.getAttribute("data-id");
            console.log(userId);
            fetch(`/user_details/${userId}`)
                .then((response) => response.json())
                .then((data) => {
                    console.log(data);
                    document.querySelector("#delete-acc").textContent = data.UserName;
                })
                .catch((error) => {
                    console.error("Error fetching user details:", error);
                });
            document.getElementById("DeleteUser").setAttribute("data-id", userId);
            document.getElementById("delete-acc").textContent = userId; // Hoặc tên
        });
    });
});

// xóa user
document.addEventListener("DOMContentLoaded", function () {
    const deleteBtn = document.getElementById("DeleteUser");

    deleteBtn.addEventListener("click", function () {
        const userId = this.getAttribute("data-id");
        console.log(userId);
        if (!userId) return;

        fetch(`/delete_user/${userId}`, {
            method: "DELETE",
        })
            .then((response) => response.json())
            .then((data) => {
                console.log("Deleted:", data);
                // Reload lại danh sách hoặc xóa dòng khỏi bảng
                location.reload();
            })
            .catch((err) => console.error("Error deleting user:", err));
    });
});


//tao accout user moi
document.getElementById("CreateForm").addEventListener("submit", function (e) {
    e.preventDefault(); // Ngăn form reload trang
    const editForm = document.getElementById("CreateForm");
    const payload = {
      Create_UserName: document.getElementById("Create_UserName").value,
      Create_PassWord: document.getElementById("Create_PassWord").value,
      Create_FullName: document.getElementById("Create_FullName").value,
      Create_UserRole: document.getElementById("Create_UserRole").value,
    };
    const formData = new FormData(editForm);
    console.log(formData);
    fetch("/CreateAcc", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    })
      .then((response) => {
        if (response.ok) {
          location.reload(); // Reload để cập nhật bảng
        } else {
          alert("tao acc thất bại!");
        }
      })
      .catch((err) => {
        console.error("Lỗi tao acc:", err);
      });
});