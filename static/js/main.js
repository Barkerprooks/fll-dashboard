document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll('.upload').forEach(upload => {
        
        let input = upload.querySelector('input');
        let span = upload.querySelector('span');
        
        input.addEventListener('change', (event) => {
            let submit = event.target.form.querySelector('.update-submit-button');
            if (event.target.files && event.target.files.length > 0) {
                span.innerText = `Uploading: ${event.target.files[0].name}`;
                submit.disabled = false;
            }
        });
    });
})