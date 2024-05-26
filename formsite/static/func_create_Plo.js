let dynamicFieldCounter = 1;
  let num = 0;

  function addSubField(button) {
    var parentDiv = button.parentElement;
    var divName = button.parentNode.className;
    // สร้างฟิลด์ลูกใหม่
    var subField = document.createElement("input");
    subField.type = "text";
    subField.name = "sub_field_"+divName;
    subField.setAttribute('required', '');
    console.log(divName)
    subField.placeholder = "หัวข้อย่อย";
    subField.style.width = "50%";
    subField.style.border = "1px solid gray";
    subField.style.paddingTop = "2px";
    subField.style.paddingLeft = "4px";
    subField.style.borderRadius = "0.5rem";
    subField.style.height = "40px";
    //subField.setAttribute("required", "true");

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
    mainField.className = "main_field" + dynamicFieldCounter;
    mainField.id = "main_field" + dynamicFieldCounter
    mainField.placeholder = "Main Field";

 //แต่ง
    mainField.type = "text";
    mainField.name = "main_field" + dynamicFieldCounter;
    mainField.className = "main_field" + dynamicFieldCounter;
    mainField.id = "main_field" + dynamicFieldCounter
    mainField.placeholder = "หัวข้อหลัก";
    mainField.style.width = "33.333%";
    mainField.style.border = "1px solid gray";
    mainField.style.height = "50px";
    mainField.style.backgroundColor = "rgb(249,250 ,251)";
    mainField.style.marginTop = "8px";
    mainField.style.borderRadius = "0.25rem";
    mainField.style.paddingLeft = "4px";
    console.log(dynamicFieldCounter);

    var addButton = document.createElement("button");
    addButton.type = "button";
    addButton.textContent = "+ เพิ่มหัวข้อย่อย";
    // addButton.style.border = "1px solid gray";
    addButton.style.backgroundColor = "rgb(59, 130, 246)"
    addButton.style.color = "white";
    addButton.style.width = "auto";
    addButton.style.padding = "10px";
    addButton.style.margin = "8px"
    addButton.style.borderRadius = "0.5rem"
    addButton.style.fontSize="16px"
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
    deleteButton.textContent = "ลบหัวข้อหลัก";
    deleteButton.style.border="1px solid gray";
    deleteButton.style.width="115px";
    deleteButton.style.height="40px";
    deleteButton.style.backgroundColor="rgb(239,68,68)";
    deleteButton.style.marginBottom="5px";
    deleteButton.style.color="white";
    deleteButton.style.fontSize="16px";
    deleteButton.style.borderRadius="0.5rem";
    deleteButton.style.padding="5px 5px";
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

  