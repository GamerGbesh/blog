document.addEventListener("DOMContentLoaded", function () {
    // Navbar toggle animation
    const navbarToggler = document.querySelector(".navbar-toggler");
    const navbarCollapse = document.querySelector("#navbarNav");
    
    if (navbarToggler) {
        navbarToggler.addEventListener("click", function () {
            navbarCollapse.classList.toggle("show");
        });
    }

    // Smooth scrolling for pagination links
    document.querySelectorAll(".pagination a").forEach(link => {
        link.addEventListener("click", function (e) {
            e.preventDefault();
            window.scrollTo({ top: 0, behavior: "smooth" });
            window.location.href = this.href;
        });
    });

    // Form validation for login and signup
    const loginForm = document.querySelector("form[action*='login']");
    const signupForm = document.querySelector("form[action*='signup']");
    
    function validateForm(event) {
        const inputs = event.target.querySelectorAll("input");
        let valid = true;
        inputs.forEach(input => {
            if (!input.value.trim()) {
                input.classList.add("is-invalid");
                valid = false;
            } else {
                input.classList.remove("is-invalid");
            }
        });
        if (!valid) event.preventDefault();
    }
    
    if (loginForm) loginForm.addEventListener("submit", validateForm);
    if (signupForm) signupForm.addEventListener("submit", validateForm);

    // Modal for generated blog preview (if applicable)
    const blogTextArea = document.querySelector("textarea.form-control");
    if (blogTextArea) {
        blogTextArea.addEventListener("click", function () {
            const modal = document.createElement("div");
            modal.classList.add("modal", "fade", "show");
            modal.style.display = "block";
            modal.innerHTML = `
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">Generated Blog</h5>
                            <button type="button" class="close" onclick="this.parentElement.parentElement.parentElement.remove();">&times;</button>
                        </div>
                        <div class="modal-body">
                            <p>${blogTextArea.value}</p>
                        </div>
                    </div>
                </div>
            `;
            document.body.appendChild(modal);
        });
    }

    // Show loading spinner when generating AI blog
    const blogForm = document.querySelector("form[action='']");
    if (blogForm) {
        const submitButton = blogForm.querySelector("button[type='submit']");
        const loader = document.createElement("div");
        loader.classList.add("loading-spinner");
        loader.style.display = "none";
        loader.innerHTML = `
            <div style="position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); z-index: 1050; background: rgba(255, 255, 255, 0.9); padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.3);">
                <div class="spinner-border text-primary" role="status" style="width: 3rem; height: 3rem;">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <p style="margin-top: 10px; font-weight: bold; color: #007bff;">Generating Blog...</p>
            </div>
        `;
        document.body.appendChild(loader);

        blogForm.addEventListener("submit", function () {
            loader.style.display = "block";
            submitButton.disabled = true;
        });
    }
});
