function open_Dialog(){
    let dialog = document.getElementById('dialog2');
      if (dialog.style.display === 'block' || dialog.classList.contains('flex')) {
          // ถ้า dialog กำลังแสดงอยู่ให้ซ่อน
          dialog.style.display = 'none';
          dialog.classList.add('hidden');
          dialog.classList.remove('flex');
          dialog.classList.remove('opacity-100');
      } else {
          // ถ้า dialog ถูกซ่อนอยู่ให้แสดง
          dialog.style.display = 'block';
          dialog.classList.remove('hidden');
          dialog.classList.add('flex');
          dialog.classList.add('opacity-100');
      }
  }
      function close_Dialog(){
        document.getElementById("dialog2").style.display='none'
        let dialog = document.getElementById("dialog2");
        dialog.classList.add("opacity-0");
        dialog.classList.add('hidden');
        dialog.classList.remove('flex');
        
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

    function add_new_member(department) {
        const form = document.getElementById('addTeacherForm');
        const formData = new FormData(form);
        const csrftoken = getCookie('csrftoken');

        formData.append('department', department);
                                                                                    
        fetch('/add_teacher/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                close_Dialog();
                location.reload();
            } else {
                alert("เกิดข้อผิดพลาดในการเพิ่มอาจารย์");
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
    