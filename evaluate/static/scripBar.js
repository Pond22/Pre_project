// dropdown bar จัดการข้อมูล
document.addEventListener('DOMContentLoaded', function () {
    const button = document.getElementById('navbar-toggle');
    const menu = document.getElementById('navbar-dropdown');

    const dropdownButton = document.getElementById('dropdownNavbarLink');
    const dropdownMenu = document.getElementById('dropdownNavbar');

    dropdownButton.addEventListener('click', () => {
        dropdownMenu.classList.toggle('hidden');
    });

    button.addEventListener('click', function () {
        menu.classList.toggle('hidden');
    });
    });

// dropdown bar จัดการข้อมูล
const dropdown = document.getElementById('userDropdown');
// รับอ้างอิงไปยัง element ของปุ่มหรืออื่นๆ ที่ใช้ในการเปิด/ปิด dropdown
const toggleButton = document.getElementById('avatarButton'); // สมมติว่ามีปุ่มที่ใช้ในการเปิด/ปิด dropdown 
// เพิ่ม event listener เมื่อคลิกที่ปุ่มเพื่อเปิด/ปิด dropdown
toggleButton.addEventListener('click', function() {
        // ถ้า dropdown ไม่มี class "hidden" ให้เพิ่ม class "hidden" เข้าไป
    if (!dropdown.classList.contains('hidden')) {
        dropdown.classList.add('hidden');
    } else {
        // ถ้า dropdown มี class "hidden" ให้ลบ class "hidden" ออก
        dropdown.classList.remove('hidden');
        }
});
    