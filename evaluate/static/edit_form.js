
//จัดการทั่วไป
//pop-up

function openPopup() {
var popup = document.getElementById("popup");
popup.style.display = "block";
}

function closePopup() {
var popup = document.getElementById("popup");
popup.style.display = "none";
}

function checkboxHandle(checkboxId, id, text, event, status) {
if (event) {
  event.stopPropagation();  // ป้องกัน event bubbling
}

console.log(status)
var checkbox = document.getElementById(checkboxId);
console.log(checkboxId)
if (checkbox.checked && status == 'main') {
  selectTemplate(id, text, event);
}
else if (checkbox.checked && status == 'sub') {
  set_subField(id, text, event);
}
else if (!checkbox.checked && status == 'main'){
  var targetInput = document.getElementById('main_item_form_template');
  var targetInput2 = document.getElementById('main_item_form_template_id');
  targetInput.parentNode.removeChild(targetInput);
  targetInput2.parentNode.removeChild(targetInput2);
  
}
else if (!checkbox.checked && status == 'sub'){
  var targetInput = document.getElementById('sub_item_form_template_'+ id);
  targetInput.parentNode.removeChild(targetInput);

}
}

function toggleSections() {
var uploadCsvSection = document.getElementById("upload-csv-section");
var container = document.getElementById("Main_display_page");

if (uploadCsvSection.style.display === "none") {
  uploadCsvSection.style.display = "block";
  container.style.display = "none";
  uploadCsvSection.scrollIntoView({ behavior: "smooth" });
} else {
  uploadCsvSection.style.display = "none";
  container.style.display = "block";
  container.scrollIntoView({ behavior: "smooth" });
}
}

function confirmSelection(formId) {
    var checkedBoxes = document.querySelectorAll('input[name="template_choice"]:checked');

    if (checkedBoxes.length > 0) {
        var selectedItems = [];

        checkedBoxes.forEach(function(checkbox) {
            selectedItems.push({
                template_select_id: checkbox.value,
                text: checkbox.nextElementSibling.textContent.trim(),
                isSub: checkbox.getAttribute('data-is-sub') === 'true',
                parentId: checkbox.getAttribute('data-parent-id')
            });
        });

        // Send the selected items to the server
        fetch('/save-new-items/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                form_id: formId,
                items: selectedItems
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('New items saved successfully');
                location.reload();
                closePopup();
            } else {
                console.error('Failed to save new items:', data.error);
            }
        })
        .catch(error => console.error('Error:', error));
    } else {
        alert("โปรดเลือกข้อมูล");
    }
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

