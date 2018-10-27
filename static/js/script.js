window.onload = function () {

     let menu = document.getElementsByClassName('menu')[0];

    document.onclick = function (e) {
        let parentItem = e.target.parentElement;
        let cl1 = parentItem.classList.contains('submenu');
        let cl2 = parentItem.classList.contains('has-sub');
        let c13 = !!parentItem.childElementCount > 1;

        if (!cl1 && !cl2 && !c13){
            closeAllMenu()
        }
    };

    menu.onclick = function (e) {
        let parentItem = e.target.parentElement;
        let icon;
        if (e.target.tagName === 'I') {
            icon = e.target;
        } else {
            icon = e.target.nextElementSibling;
        }

        if ((parentItem.classList.contains('submenu') || parentItem.classList.contains('has-sub')) && parentItem.childElementCount > 1){

            let targetParrent = parentItem.querySelector('ul');
            let firstParrent = parentItem.parentElement;
            let secondParrent = firstParrent.parentElement;
            let sub_left = secondParrent.classList.contains('has-sub');

            closeOpenedMenu(targetParrent, sub_left);

            if (typeof targetParrent != null) {
               if (targetParrent.classList.contains('show')) {
                   targetParrent.classList.remove('show');
                   if (icon.tagName === 'I') {
                    // icon.classList.remove('toggledown');
                    icon.classList.remove('fa-minus-circle');
                    // icon.classList.add('toggleup');
                    icon.classList.add('fa-plus-circle');

                   }
                   if (sub_left) {
                     targetParrent.classList.remove('sub-left')
                   }
               } else {
                   targetParrent.classList.add('show');
                   if (icon.tagName === 'I') {
                       // icon.classList.remove('toggleup');
                       icon.classList.remove('fa-plus-circle');
                       // icon.classList.add('toggledown');
                       icon.classList.add('fa-minus-circle');
                   }
                   if (sub_left) {
                     targetParrent.classList.add('sub-left')
                   }
               }
            }


        } else {
            return false
        }

    };


    function closeOpenedMenu(tp, sp) {
        let showedItems = document.getElementsByClassName('show');

        for (let i=0; i<showedItems.length; i++) {
            if (showedItems[i] !== tp && sp === false) {
                let parrent_i = showedItems[i].previousElementSibling;

                if (parrent_i.tagName === 'I') {
                    // parrent_i.classList.remove('toggledown');
                    parrent_i.classList.remove('fa-minus-circle');
                    // parrent_i.classList.add('toggleup');
                    parrent_i.classList.add('fa-plus-circle');
                }
                showedItems[i].classList.remove('show');
            }
        }
    }

    function closeAllMenu() {
       let showedItems = document.getElementsByClassName('show'),
           showedLeftItems = document.getElementsByClassName('sub-left'),
           iconToggleDown = document.getElementsByClassName('fa-minus-circle');

       for (let i=0; i<showedItems.length; i++) {
           showedItems[i].classList.remove('show')
        }

       for (let i=0; i<showedLeftItems.length; i++) {
           showedLeftItems[i].classList.remove('sub-left')
        }

        for (let i=0; i<iconToggleDown.length; i++) {
           // iconToggleDown[i].classList.remove('toggledown');
            //
           iconToggleDown[i].classList.add('fa-plus-circle');
           iconToggleDown[i].classList.remove('fa-minus-circle');
        }
    }

};