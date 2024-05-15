
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

function add_user(form_id, type) {
    const inputContainer = document.getElementById('input-container');
    const newInput = document.createElement('input');
    newInput.type = 'text';
    newInput.placeholder ="กรุณาใส่รหัสนักศึกษา 10 หลัก";
    newInput.onblur = function() {
        if (this.value.trim() === '') { // ถ้าช่องว่าง
            /* alert('กรุณาใส่รหัสนักศึกษา 10 หลัก'); // แสดงป็อปอัพ */
            /* this.focus(); // ให้โฟกัสกลับไปที่ช่องอินพุตนี้ */
        } else if (this.value.trim().length !== 10) { // ตรวจสอบว่ามี 10 หลักหรือไม่
            /* this.focus(); // ให้โฟกัสกลับไปที่ช่องอินพุตนี้
            this.scrollIntoView();  */
        } else {
            saveData_user(this, form_id); // ถ้าข้อมูลถูกต้อง, บันทึกข้อมูล
        }
    };
  
    inputContainer.appendChild(newInput); // เพิ่มอินพุตใหม่เข้าไปในคอนเทนเนอร์
    newInput.scrollIntoView(); 
    newInput.focus(); 
  }

  function saveData_user(inputElement, form_id) {
    const value = inputElement.value;
    const apiUrl = '/manage_AuthorizedUser/'; 

    fetch(apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json', 
            'X-CSRFToken': getCookie('csrftoken') 
        },
        body: JSON.stringify({
            form_id: form_id,
            student_code: value 
        })
    })
    .then(response => {
        console.log('Status:', response.status);
        if (!response.ok) {
            console.error('Error:', error)
        }
        return response.json(); 
    })
    .then(data => {
        console.log('Success:', data);
        location.reload(); 
    })
    .catch(error => {
        console.error('Error:');
        location.reload(); 
    });
}

document.addEventListener('DOMContentLoaded', function() {
    const formElement = document.getElementById('editForm');
    const formFields = formElement.querySelectorAll('input, select, textarea');
    
    const saveFormData = () => {
        const formData = new FormData(formElement);
        const data = Object.fromEntries(formData.entries());
        localStorage.setItem('formData', JSON.stringify(data));
    };
    

    const loadFormData = () => {
        const savedData = JSON.parse(localStorage.getItem('formData'));
        if (savedData) {
            Object.keys(savedData).forEach(key => {
                const field = formElement.querySelector(`[name="${key}"]`);
                if (field) {
                    field.value = savedData[key];
                }
            });
        }
    };

    formFields.forEach(field => {
        field.addEventListener('input', saveFormData);
    });

    loadFormData();


    const popupStatus = localStorage.getItem('popupStatus');
    const popup = document.getElementById("popup1");
    if (popupStatus === 'open') {
        popup.style.display = "block";
    } else {
        popup.style.display = "none";
    }
});

function togglePopup() {
    const popup = document.getElementById("popup1");
    if (popup.style.display === "none" || popup.style.display === "") {
        popup.style.display = "block";
        localStorage.setItem('popupStatus', 'open');
    } else {
        popup.style.display = "none";
        localStorage.setItem('popupStatus', 'closed');
    }
}

function delete_user(id){
    fetch('/manage_AuthorizedUser/', {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json', 
            'X-CSRFToken': getCookie('csrftoken') 
        },
        body: JSON.stringify({
            aut_id : id,
        })
    })
    .then(response => {
        console.log('Status:', response.status);
        /* var userRow = document.getElementById('user_' + id).closest('.user-row');
        if (userRow) {
            userRow.remove();
        } */
        location.reload();
        if (!response.ok) {
            console.error('Error:', error)
        }
        return response.json(); 
    })
}


/* async function updateForm(formId) {
    const formElement = document.getElementById('editForm');
    const formData = new FormData(formElement);
    const data = Object.fromEntries(formData.entries());
    
    const response = await fetch(`/update_form_api/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: JSON.stringify({
            form_id: formId,
            data: data
        })
    });
    
    const result = await response.json();
    if (response.ok) {
        alert('Form updated successfully');
        // Redirect or update the page as needed
    } else {
        console.error(result);
        alert('Error updating form');
    }
}
 */
