
let dynamicFieldCounter = 1;
let num = 0;

function addSubField(button) {
  var parentDiv = button.parentElement;
  var divName = button.parentNode.id;
  // สร้างฟิลด์ลูกใหม่
  var subField = document.createElement("input");
  subField.type = "text";
  subField.name = "sub_field_"+divName;
  subField.setAttribute('required', '');
  console.log(divName)
  subField.placeholder = "หัวข้อย่อย";
  subField.style.width = "100%";
  subField.style.border = "1px solid gray";
  subField.style.paddingTop = "8px";
  subField.style.paddingLeft = "4px";
  subField.style.borderRadius = "0.5rem";
  subField.style.height = "50px";
  // subField.style.height = 'inherit';
  subField.setAttribute("required", "true");

  

  var divName = button.parentNode.className;
  console.log(divName);
  console.log(subField.name);

  // สร้างปุ่มลบฟิลด์ลูก
  var deleteButton = document.createElement("button");
  deleteButton.type = "button";
  deleteButton.className = "delete-sub";
  deleteButton.textContent = "-";
  deleteButton.style.color = "white";
  deleteButton.style.backgroundColor = "rgb(156,163 ,175)";
  deleteButton.style.padding = "1px"
  deleteButton.style.width = "25px";
  deleteButton.style.margin = "2px";
  deleteButton.onclick = function () {
    // ลบฟิลด์ลูกเมื่อคลิกปุ่มลบ
    subField.remove();
    deleteButton.remove();
  };

  // เพิ่มฟิลด์ลูกและปุ่มลบลงในแม่
  parentDiv.querySelector(".subFields").appendChild(subField);
  parentDiv.querySelector(".subFields").appendChild(deleteButton);
  num++;
}

function addMainField() {
  // สร้างฟิลด์แม่ใหม่
  var parentDiv = document.getElementById("parent");
  var mainFieldDiv = document.createElement("div");
  mainFieldDiv.id  = "main_field" + dynamicFieldCounter;
  mainFieldDiv.classList.add("main_field" + dynamicFieldCounter);

  var mainField = document.createElement("input");
  mainField.type = "text";
  mainField.name = "main_field" + dynamicFieldCounter;
  mainField.className = "mainField";
  mainField.id = "main_field" + dynamicFieldCounter
  mainField.placeholder = "Main Field";

//แต่ง
  mainField.type = "text";
  mainField.name = "main_field" + dynamicFieldCounter;
  // mainField.className = "main_field" + dynamicFieldCounter;
  mainField.id = "main_field" + dynamicFieldCounter
  mainField.placeholder = "หัวข้อหลัก";
  mainField.style.width = "80%";
  mainField.style.border = "1px solid gray";  
  mainField.style.height = "50px";
  mainField.style.backgroundColor = "rgb(249,250 ,251)";
  mainField.style.marginTop = "8px";
  mainField.style.borderRadius = "0.5rem";
  mainField.style.paddingLeft = "4px";
  console.log(dynamicFieldCounter);

  var addButton = document.createElement("button");
  addButton.type = "button";
  addButton.textContent = "+ เพิ่มหัวข้อย่อย";
  addButton.style.border = "1px solid gray";
  addButton.style.backgroundColor = "rgb(59, 130, 246)"
  addButton.style.color = "white";
  addButton.style.width = "auto";
  addButton.style.padding = "6px";
  addButton.style.margin = "2px"
  addButton.style.borderRadius = "0.5rem"
  addButton.onclick = function () {
    addSubField(addButton);
  };

  var subFieldsDiv = document.createElement("div");
  subFieldsDiv.classList.add("subFields");

  //ทำปุ่มลบฟิลด์แม่
  var deleteButton = document.createElement("button");
  deleteButton.type = "button";
  deleteButton.textContent = "ลบหัวข้อหลัก";
  deleteButton.style.color = "white";
  deleteButton.style.border = "1px solid gray";
  deleteButton.style.backgroundColor = "rgb(185 ,28 ,28)";
  deleteButton.style.padding = "2px";
  deleteButton.style.borderRadius = "0.5rem";
  deleteButton.style.width = "100px";
  deleteButton.style.marginBottom = "3px"
  deleteButton.onclick = function () {
    mainField.remove();
    deleteButton.remove();
  };
  // ทำปุ่มแสดง popup
  /*
  var popupButton = document.createElement("button");
  popupButton.type = "button";
  popupButton.textContent = "เลือกแม่แบบ";
  popupButton.onclick = function () {
    showPopup(mainField.id);
  };*/

  // เพิ่มฟิลด์แม่และปุ่มเพิ่มฟิลด์ลูกลงในแม่
  mainFieldDiv.appendChild(mainField);
  //mainFieldDiv.appendChild(popupButton);
  mainFieldDiv.appendChild(addButton);
  mainFieldDiv.appendChild(subFieldsDiv);
  parentDiv.insertBefore(mainFieldDiv, parentDiv.lastElementChild);

  //ทำปุ่มลบฟิลด์แม่
  var deleteButton = document.createElement("button");
  deleteButton.type = "button";
  deleteButton.textContent = "ลบทั้งหมด";
  deleteButton.style.color = "white";
  deleteButton.style.border = "1px solid gray";
  deleteButton.style.backgroundColor = "rgb(185 ,28 ,28)";
  deleteButton.style.padding = "6px";
  deleteButton.style.borderRadius = "0.5rem";
  deleteButton.style.width = "100px";
  deleteButton.style.marginBottom = "3px"
  deleteButton.onclick = function () {
    //สำคัญสำหรับการลบ ห้ามแก้ ถ้าไม่มีมันตอนกด - ชื่อของฟิลด์ตอนหลังบ้านรับ POST จะผิด

    thename = mainField.name;
    mainFieldDiv.remove();
    var number = thename.match(/\d+$/)[0]; // ดึงตัวเลขข้างหลังสุดออกมา
    var value = number;
    var tem = number;
    tem++;

    for (v = tem; v < dynamicFieldCounter; v++) {
      //หาclass

      console.log("ค่า v" + value);
      var nextField = document.querySelector(".main_field" + v);
      console.log("ชื่อมัน" + nextField.className);
      var subclass = nextField.querySelector(".subFields");
      //console.log(subclass.className);

      if (nextField) {
        var inputElement = nextField.querySelector("input"); // เลือก input ภายใน div
        console.log("ste", value);
        var name = "main_field" + value;
        var name_sub = "sub_field_main_field" + value;
        var subFields = subclass.querySelectorAll("input");
        console.log(subFields);

        nextField.className = name; // แก้ชื่อ div
        console.log("แก้ชื่อ" + nextField.className);

        inputElement.setAttribute("name", name); // แก้ชื่อ
        inputElement.setAttribute("class", name); // แก้คลาส

        // วนลูปทุก subField และตั้งค่า name ของแต่ละตัว
        for (var i = 0; i < subFields.length; i++) {
          subFields[i].setAttribute("name", name_sub); // แก้ชื่อ sub
        }
        //mainFieldDiv.remove();
      }
      hiddenInput.value = value;
      value++;
    }
    if (tem == dynamicFieldCounter) {
      tem -= 2;
      console.log("ค่าที่ควรเป็น " + tem);
      hiddenInput.value = tem;
    }
    document.getElementById("main").appendChild(hiddenInput);
    dynamicFieldCounter--;
    //mainFieldDiv.remove();
  }; //สำคัญสำหรับการลบ ห้ามแก้ //สำคัญสำหรับการลบ ห้ามแก้//สำคัญสำหรับการลบ ห้ามแก้//สำคัญสำหรับการลบ ห้ามแก้//สำคัญสำหรับการลบ ห้ามแก้//สำคัญสำหรับการลบ ห้ามแก้
  //สำคัญสำหรับการลบ ห้ามแก้//สำคัญสำหรับการลบ ห้ามแก้//สำคัญสำหรับการลบ ห้ามแก้//สำคัญสำหรับการลบ ห้ามแก้//สำคัญสำหรับการลบ ห้ามแก้//สำคัญสำหรับการลบ ห้ามแก้//สำคัญสำหรับการลบ ห้ามแก้
  mainFieldDiv.appendChild(deleteButton);

  var hiddenInput = document.createElement("input");
  hiddenInput.type = "hidden";
  hiddenInput.name = "length"; // ตั้งชื่อฟิลด์
  hiddenInput.value = dynamicFieldCounter; // กำหนดค่าจาก dynamicFieldCounter

  // เพิ่ม hiddenInput ลงใน form
  document.getElementById("main").appendChild(hiddenInput);

  document
    .getElementById("main")
    .addEventListener("change", function (event) {
      // กันคนแก้ไขจากหน้า html
      if (event.target.name === "length") {
        // หากมีการแก้ไขฟิลด์ hidden ให้สร้าง hidden input ใหม่
        var newHiddenInput = document.createElement("input");
        newHiddenInput.type = "hidden";
        newHiddenInput.name = "length";
        newHiddenInput.value = dynamicFieldCounter;

        // ลบอันเก่าออก
        event.target.parentNode.removeChild(event.target);

        // เพิ่มใหม่
        document.getElementById("main").appendChild(newHiddenInput);
      }
    });

  dynamicFieldCounter++;
}




//จัดการทั่วไป
//pop-up

function showTemplateDetails() {
  // โค้ดที่แสดงข้อมูลแม่แบบ
  var templateDetailsDiv = document.getElementById("template_details");
  templateDetailsDiv.innerHTML = "<p>ข้อมูลแม่แบบที่เลือก</p>";
  templateDetailsDiv.style.display = "block";
}


function selectTemplate(id, text, event) {
  if (event) {
      event.stopPropagation();  // ป้องกัน event bubbling
  }
  var templateDetailsDiv = document.getElementById("template_details");
  templateDetailsDiv.innerHTML = "<p>แม่แบบที่เลือก: " + text + "</p>";
  templateDetailsDiv.style.display = "block";

  // โอนข้อความไปยังฟิลด์
  var targetInput = document.getElementById('Plo_div');

  var newInput = document.createElement('input');
  newInput.type = 'text';
  newInput.value = text;  
  newInput.id = 'main_item_form_template';  
  newInput.className = 'main_item_form_template';
  
  var hiddenInput = document.createElement('input');
  hiddenInput.type = 'hidden';
  hiddenInput.name = 'main_item_form_template_id';  // ตั้งชื่อฟิลด์ที่ต้องการส่งไปยังหลังบ้าน
  hiddenInput.value = id;  // ใส่ค่าไอดีที่ต้องการส่ง
  hiddenInput.id = 'main_item_form_template_id';

  console.log(targetInput);
  if (targetInput) {
    targetInput.querySelector(".Main_item").appendChild(newInput);
    targetInput.querySelector(".Main_item").appendChild(hiddenInput);
  }
}

let sub_count = 0;

function set_subField(id, text, event) {
event.stopPropagation(); // ป้องกัน event bubbling

var parentDiv = document.getElementById('Plo_div'); // หา div หลัก

var newInput = document.createElement('input');
newInput.type = 'text';
newInput.value = text;
newInput.id = 'sub_item_form_template_' + id;
newInput.className = 'sub_item_form_template';

var hiddenInput = document.createElement('input');
hiddenInput.type = 'hidden';
hiddenInput.name = 'sub_item_form_template_id';  // ตั้งชื่อฟิลด์ที่ต้องการส่งไปยังหลังบ้าน
hiddenInput.value = id;  // ใส่ค่าไอดีที่ต้องการส่ง
hiddenInput.id = 'main_item_form_template_id';

if (parentDiv) {
  parentDiv.querySelector(".subFields").appendChild(newInput);
  parentDiv.querySelector(".subFields").appendChild(hiddenInput);  
}
}

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


function confirmSelection() {
  var checkedBoxes = document.querySelectorAll('input[name="template_choice"]:checked');

  if (checkedBoxes.length > 0) {
      console.log("การเลือกข้อมูลเสร็จสิ้น");

      var Plo_div = document.getElementById("Plo_div");
      Plo_div.innerHTML = ""; // Clear
      var count = 0;
      var parents = {}; // Object to store references to parent divs
      var parentCounts = {}; // Object to store the counts used for parent divs

      checkedBoxes.forEach(function(checkbox) {
          var item = {
              id: checkbox.value,
              text: checkbox.nextElementSibling.textContent.trim(),
              isSub: checkbox.getAttribute('data-is-sub') === 'true',
              parentId: checkbox.getAttribute('data-parent-id')
          };

          var inputField = document.createElement('input');
          inputField.type = 'text';
          inputField.value = item.text;

          // Create hidden input for storing the item.id
          var hiddenInput = document.createElement('input');
          hiddenInput.type = 'hidden';
          hiddenInput.value = item.id;

          if (!item.isSub) {
              // Main item
              inputField.name = 'plo_main_' + count;
              hiddenInput.name = 'id_main_' + count;

              if (!parents[item.id]) {
                  var mainDiv = document.createElement('div');
                  mainDiv.id = 'div_' + count;
                  mainDiv.appendChild(inputField);
                  mainDiv.appendChild(hiddenInput); // Add hidden input to the same div
                  Plo_div.appendChild(mainDiv);
                  parents[item.id] = mainDiv;
                  parentCounts[item.id] = count; // Store count for sub-items to use
                  count++;
              } else {
                  parents[item.id].appendChild(inputField);
                  parents[item.id].appendChild(hiddenInput); // Add hidden input to the existing div
              }
          } else {
              // Sub-item
              inputField.name = 'plo_sub_' + parentCounts[item.parentId];
              hiddenInput.name = 'id_sub_' + parentCounts[item.parentId];

              if (!parents[item.parentId]) {
                  var parentDiv = document.createElement('div');
                  parentDiv.id = 'div_' + parentCounts[item.parentId];
                  Plo_div.appendChild(parentDiv);
                  parents[item.parentId] = parentDiv;
              }
              parents[item.parentId].appendChild(inputField);
              parents[item.parentId].appendChild(hiddenInput); // Add hidden input to the parent div
          }
      });

      closePopup();
  } else {
      alert("โปรดเลือกข้อมูล");
  }
}