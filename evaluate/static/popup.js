function showDialog(){
    let dialog = document.getElementById('dialog');
    dialog.classList.remove('hidden');
    dialog.classList.add('flex');
    dialog.classList.add('opacity-100');
  }
    function hidedialog(){
      let dialog = document.getElementById("dialog");
      dialog.classList.add("opacity-0");
      dialog.classList.add('hidden');
      dialog.classList.remove('flex');
    
    }