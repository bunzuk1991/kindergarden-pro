function formatDate(date) {

  var dd = date.getDate();
  if (dd < 10) dd = '0' + dd;

  var mm = date.getMonth() + 1;
  if (mm < 10) mm = '0' + mm;

  var yy = date.getFullYear();
  if (yy < 10) yy = '0' + yy;

  return yy + '-' + mm + '-' + dd;
}


function previewFile() {

  let preview = document.querySelector('.img-container .img-wrapper img');
  let file    = document.querySelector('#add-photo').files[0];
  let reader  = new FileReader();

  reader.onloadend = function () {
    preview.src = reader.result;
  };

  if (file) {
    reader.readAsDataURL(file);
  } else {
    preview.src = "";
  }
}


function daysBar() {
    let items = $(".percent-data");

    items.each(function (i, elem) {

        current_item = $(this);
        let percent = current_item.attr('data-percent');
        current_item.css('width', percent + '%')

    });
}


function clearForm() {
    let form_ = $('#form-parent');
    let form_input = form_.find('input[type="text"], input[type="date"], input[type="phone"]');
    let form_textarea = form_.find('textarea');

    form_textarea.val('');


    form_input.each(function (i, elem) {
        $(this).attr('value', '');
        $(this).val('');
    })
};


function convertDate(textDate) {
    let text = "" + textDate;
    let date = new Date(text.replace(/(\d+).(\d+).(\d+)/, '$3/$2/$1'));

    return date;
};

function returnParentHtml(id, name, date_of_birth, type, phone, work, posada, newitem){

    let textHtml = '';

    let textHtml_prev = '<div class="lst-name">'
                +   '<p>' + name + '</p>'
                + '</div>'
                + '<div class="lst-date-birth">'
                +   '<p>' + date_of_birth + '</p>'
                + '</div>'
                + '<div class="lst-type">'
                +   '<p>' + type + '</p>'
                + '</div>'
                + '<div class="lst-phone">'
                +   '<p>' + phone + '</p>'
                + '</div>'
                + '<div class="lst-work">'
                +   '<p>' + work + '</p>'
                + '</div>'
                + '<div class="lst-posada">'
                +   '<p>' + posada + '</p>'
                + '</div>'
                + '<div class="lst-change">'
                +   '<p><a href="#" class="change-parent-info">Змінити</a></p>'
                +   '<p><a href="#" class="delete-parent-info">Вилучити</a></p>'
                + '</div>';

    if (newitem) {
        textHtml =  '<li class="lst-parent" id="' + id + '" data-operation="added"  data-delete="">' + textHtml_prev + '</li>';
    } else {
        textHtml = textHtml_prev;
    }

    return textHtml;
}

function tabsToggle() {
    $('.tabs-content .tab:not(":first-of-type")').hide();

    $('.tabs-titles ul li').each(function (i) {
        $(this).attr('data-tab', 'tab' + i)
    });

    $('.tabs-content .tab').each(function (i) {
        $(this).attr('data-tab', 'tab' + i)
    });
    
    $('.tabs-titles ul li').on('click', function (e) {
        let DataThis = $(this);
        let Wrapper = $(this).closest('.line-parents');

        Wrapper.find('.tabs-titles ul li').removeClass('active-tab');
        $(this).addClass('active-tab');

        Wrapper.find('.tabs-content .tab').hide();
        Wrapper.find('.tabs-content .tab[data-tab=' + DataThis.data('tab') + ']').show();

    })
}

$( document ).ready(function() {

    daysBar();
    tabsToggle();

    $(".birth-wrapper").birthdaypicker(options={"wrapper":"birth-wrapper"});


    $('.select').on('click', function (e) {
        e.preventDefault();

        let lists = $(this).find('.select-item-wrapper');
        lists.toggleClass('show-select');

    });

    $('#add-parent').on('click', function (e) {
        e.preventDefault();
        clearForm();

        let last_element = $('.lst-parent:last-child');
        let last_id = 0;

        if (last_element.length === 0) {
           last_id = 1;
        } else {
            last_id = +last_element.attr('id').replace(/lst-/g, "");
            last_id += 1;
            // last_id = last_element.length + 1;
        }

        let modal = $('.modal');
        let form_id = modal.find('input[name="form-id"]');
        let oper_type = modal.find('#operation-type');

        form_id.attr('value', 'lst-' + last_id);
        form_id.val('lst-' + last_id);
        oper_type.attr('data-type', '1');
        modal.addClass('opened');
    });

    $('#modal-parent-save').on('click', function (e) {
        e.preventDefault();

        let form = $('#form-parent');

        let name = form.find('input[name="name"]').val();
        let date_of_birth = form.find('input[name="date-of-birth"]').val();
        let phone = form.find('input[name="phone"]').val();
        let type = form.find('.select-value')[0].innerText;
        let work = form.find('textarea[name="work"]').val();
        let place = form.find('input[name="position"]').val();
        let id = form.find('input[name="form-id"]').val();
        let operation_type = form.find('#operation-type').attr('data-type');
        let oper_numb = 0;
        let modal = $('.modal');

        if (operation_type === '1') {
            let new_item = returnParentHtml(id, name, date_of_birth, type, phone, work, place, true);
            $('.list-parents').append(new_item);
        } else {
            let new_item = returnParentHtml(id, name, date_of_birth, type, phone, work, place, false);
            let elem = $("#" + id);
            if (elem.attr('data-operation') === '') {
                elem.attr('data-operation', 'change')
            }
            elem.children().remove();
            elem.append(new_item);
        }

        modal.removeClass('opened');

        clearForm();

    });

    $('.select-item').on('click', function (e) {

        let current = $(this).text();
        let radio_selected = $('.select-value');

        radio_selected.text(current);
        if (!radio_selected.hasClass('value-inserted')) {
            radio_selected.addClass('value-inserted');
        }
    });

    $('.list-parents').on('click', '.change-parent-info',  function (e) {
        e.preventDefault();
        let current_element = $(this).closest('.lst-parent');
        let id_parent = current_element.attr('id');
        let num_id = id_parent.replace(/lst-/g, "");

        let fullname = current_element.find('#' + 'id_parent-' + num_id + '-fullname').val(),
            date_of_birth = current_element.find('#' + 'id_parent-' + num_id + '-date_of_birth').val(),
            relation = current_element.find('#' + 'id_parent-' + num_id + '-relation:selected').val(),
            phone = current_element.find('#' + 'id_parent-' + num_id + '-phone').val(),
            address = current_element.find('#' + 'id_parent-' + num_id + '-address').val(),
            work = current_element.find('#' + 'id_parent-' + num_id + '-work').val(),
            workplace = current_element.find('#' + 'id_parent-' + num_id + '-workplace').val();


        clearForm();

        let form = $('#form-parent');
        let date_from_p = convertDate(date_of_birth);

        form.find('input[name="name"]').attr('value', fullname);
        form.find('input[name="name"]').val(fullname);
        form.find('input[name="date-of-birth"]').attr('value', formatDate(date_from_p));
        form.find('input[name="date-of-birth"]').val(formatDate(date_from_p));
        form.find('input[name="phone"]').attr('value', phone);
        form.find('input[name="phone"]').val(phone);
        // form.find('.select-value').text(type);
        form.find('textarea[name="work"]').val(work);
        form.find('input[name="position"]').attr('value', workplace);
        form.find('input[name="position"]').val(workplace);
        form.find('input[name="form-id"]').attr('value', id_parent);
        form.find('input[name="form-id"]').val(id_parent);
        form.find('#operation-type').attr('data-type', '2');


         $('.modal').addClass('opened');


    });

    $('.list-parents').on('click', '.delete-parent-info',  function (e) {
        e.preventDefault();
        let current_element = $(this).closest('.lst-parent');


        current_element.addClass('parent-deleted');
        current_element.attr('data-delete', 'true');

    });

    $('#add-photo').on('change', function (e) {
        previewFile();
    });

    $('.close-modal .fa').on('click', function (e) {
        $('.modal').removeClass('opened');
        clearForm();
    });

    $('#usi-toggle').on('click', function (e) {
        e.preventDefault();
        let current = $('.user-info');


        if (current.hasClass( "usi-open" )) {
        	current.removeClass('usi-open');
        	current.addClass('usi-close');
        } else {
        	current.removeClass('usi-close');
        	current.addClass('usi-open');
        }
    });


    $('.toggle-hidden-menu').on('click', function (e) {
        e.preventDefault();
        let current = $(this).find('+ .menu-hidden');
        let menu_hidden = $(".menu-hidden");
        let act_a = $(".active-hidden-a");
        let current_a = $(this);

        act_a.each(function(i, elem) {
            if (elem !== current_a[0]) {
                $(this).removeClass("active-hidden-a")
            }
        });

        menu_hidden.each(function(i, elem) {
            if (elem !== current[0]) {
                $(this).removeClass("menu-hidden-open")
            }
        });

        $(this).toggleClass('active-hidden-a');
        current.toggleClass("menu-hidden-open");
    });


    $('#save-child').on('click', function (e) {
        e.preventDefault();
        let child_slug = $('#child-slug').attr('data-slug');

        let data = {
            json_query: true,
            json_def: 'relations'
        };

        $.ajax({
            type: "GET",
            url: '/child/' + child_slug + '/',
            dataType: 'json',
            data: data,
            success: function (data) {
                console.log(data)
            }
        })
    });


    $(window).mouseup(function (e) {
    // **** клік поза межами #usi-toggle та .user-info
        let usi = $(".user-info");
        let usi_toggle = $('#usi-toggle');

        if (usi.has(e.target).length === 0 && usi_toggle.has(e.target).length === 0 && e.target.id !== 'usi-toggle'){
            usi.removeClass('usi-open');
            usi.addClass('usi-close');
        }
     // **** клік поза межами #usi-toggle та .user-info


        // **** клік поза межами #menu-hidden
        let menu_hidden = $(".menu-hidden");
        let act_a = $('.toggle-hidden-menu');
        let tar_a_parrent;

        let tar_a = e.target.classList.contains("toggle-hidden-menu");


        if (e.target.tagName === 'HTML') {
           tar_a_parrent = false;
        } else {
           tar_a_parrent = e.target.parentElement.classList.contains("toggle-hidden-menu");
        }



        let missed = tar_a_parrent || tar_a;

        if (menu_hidden.has(e.target).length === 0 && !e.target.classList.contains('menu-hidden') && !missed){
            menu_hidden.removeClass('menu-hidden-open');
            act_a.removeClass("active-hidden-a");

        }
        // **** клік поза межами #menu-hidden

        let select = $('.select-item-wrapper');

        if (select.has(e.target).length === 0 && !e.target.classList.contains('select-item-wrapper') && !e.target.classList.contains('select-value')){
            select.removeClass('show-select');
        }
    });
});