// document.getElementById('csv_file').addEventListener('change', event => {
//     const file = event.target.files[0];
//     const reader = new FileReader();
  
//     reader.onload = function(e) {
//       const text = e.target.result;
//       processCSV(text);
//     };
  
//     reader.readAsText(file);
//   });
  


//   function processCSV(text) {
//     const lines = text.split('\n');
//     const tbody = document.querySelector('#csv-table tbody');
    
//     lines.forEach(line => {
//       const columns = line.split(',');
//       const row = document.createElement('tr');
        
//       columns.forEach(column => {
//         const cell = document.createElement('td');
//         cell.textContent = column;
//         row.appendChild(cell);
//       });
  
//       tbody.appendChild(row);
//     });
//   }

document.getElementById('csv_file').addEventListener('change', event => {
  const fileInput = event.target;
  const file = event.target.files[0];
  const reader = new FileReader();

  reader.onload = function(e) {
    const text = e.target.result;
    const rows = processCSV(text); // ประมวลผลข้อมูล CSV
    
    // เพิ่มแถวลงในตาราง
    const tableBody = document.getElementById('data-csv');
    // tableBody.innerHTML = ''; // Clear เนื้อหาที่มีอยู่ก่อนหน้า

    rows.forEach((row, index) => {
      // ไม่แสดงแถวแรก (header) และแถวที่ว่าง
      if (index !== 0 && row.length > 0) {
        const rowElement = document.createElement('tr');
        row.forEach(cell => {
          // ตรวจสอบว่าค่าในเซลล์ไม่ใช่ undefined ก่อนที่จะแทรกลงใน HTML
          if (cell !== undefined && cell.trim() !== '') {
            const cellElement = document.createElement('td');
            cellElement.textContent = cell;
            rowElement.appendChild(cellElement);
          }
        });
        // เพิ่มปุ่ม Delete ในแถว
        const deleteCell = document.createElement('td');
        if (index !== rows.length - 1) { // ไม่เพิ่มปุ่ม delete ในแถวสุดท้าย
        const deleteButton = document.createElement('button');
        deleteButton.className = 'delete-btn-csv';
        deleteButton.textContent = 'Delete';
        deleteButton.addEventListener('click', () => {
          rowElement.remove(); // ลบแถวเมื่อปุ่มถูกคลิก
        });
        deleteCell.appendChild(deleteButton);
      }
        rowElement.appendChild(deleteCell);
        tableBody.appendChild(rowElement);
      }
    });
   
    const deleteAllButton = document.createElement('button');
    deleteAllButton.className ='delete-all-csv'
    deleteAllButton.textContent = 'Delete All';
    deleteAllButton.addEventListener('click', () => {
      tableBody.innerHTML = ''; // ลบทุกแถวเมื่อปุ่มถูกคลิก
      deleteAllButton.remove(); // ลบปุ่ม delete all เมื่อคลิก
      fileInput.value = '';
    });
    tableBody.parentNode.appendChild(deleteAllButton);
  // เพิ่มปุ่มลบทั้งหมด
  
};

  reader.readAsText(file);
});

function processCSV(text) {
  // Split the text into an array of lines
  const lines = text.split('\n');

  // Split each line into an array of columns
  const rows = lines.map(line => line.split(','));

  return rows;
}

