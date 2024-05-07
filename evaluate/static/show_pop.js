function show_Dialog(){
  let dialog = document.getElementById('dialog1');
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
    function hide_dialog(){
      document.getElementById("dialog1").style.display='none'
      let dialog = document.getElementById("dialog1");
      dialog.classList.add("opacity-0");
      dialog.classList.add('hidden');
      dialog.classList.remove('flex');
      
    }

    document.addEventListener('DOMContentLoaded', function() {
      document.getElementById('csv_file').addEventListener('change', event => {
          const fileInput = event.target;
          const file = event.target.files[0];
          const reader = new FileReader();
  
          reader.onload = function(e) {
              const text = e.target.result;
              const rows = processCSV(text); // ประมวลผลข้อมูล CSV

              //ลบข้อมูลเก่า
              const showCsv = document.getElementById('show_csv');
              while (showCsv.firstChild) {
                  showCsv.removeChild(showCsv.firstChild);
            }
              // สร้าง input text 
              rows.forEach((row, index) => {
                // ข้ามแถวแรกที่เป็นหัวข้อคอลัมน์
                if (index !== 0) {
                    const dataRow = document.createElement('div');
                    dataRow.className = 'data-row';
                    Object.entries(row).forEach(([key, value], columnIndex) => {
                        const input = document.createElement('input');
                        input.setAttribute('type', 'text');
                        input.setAttribute('value', value);
                        
                        // ตั้งชื่อของ input ตาม index ของคอลัมน์
                        if (columnIndex === 0) {
                            input.setAttribute('name', 'stu_num_list[]');
                        } else if (columnIndex === 1) {
                            input.setAttribute('name', 'stu_name_list[]');
                        }
                        
                        dataRow.appendChild(input);
                    });
                    document.getElementById('show_csv').appendChild(dataRow);
                }
            });
  
              document.getElementById('show_csv').style.display = 'flex';
              document.getElementById('show_csv').style.flexDirection = 'column';
          };
  
          reader.readAsText(file);
      });
  
      function processCSV(text) {
          // Split the text into an array of lines
          const lines = text.trim().split('\n');
  
      
          //lines.shift();
  
          // Create an array to store the rows of data
          const rows = [];
  
          // Split each line into an array of columns and create an object for each row
          lines.forEach(line => {
              const columns = line.split(',');
              const rowData = {};
              columns.forEach((column, index) => {
                  rowData[index] = column.trim(); // Trim whitespace from the columns
              });
              rows.push(rowData);
          });
  
          // Return the array of rows
          return rows;
      }
  });
  