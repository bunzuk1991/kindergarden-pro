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
  let file    = document.querySelector('#id_child-image').files[0];
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
}

function convertDate(textDate) {
    let text = "" + textDate;
    let dd = text.indexOf(".");
    let date_converted;
    if (dd !== -1) {
        date_converted = new Date(text.replace(/(\d+).(\d+).(\d+)/, '$3/$2/$1'));
    } else {
        date_converted = new Date(text);
    }

    return date_converted;
}

function returnParentHtml(id, name, date_of_birth, phone, work, posada, relations, address, parent_id, newitem){

    let textHtml = '';
    let id_num = id.replace(/lst-/g, "");
    let prefix = 'parent-' + id_num + '-';
    let text_replace;

    if (newitem) {
        text_replace = '';
    } else {
        text_replace = ' value="' + parent_id + '"';
    }

    let textHtml_prev = '<div class="field-container">'
             +   '<div class="top-line">'
             +       '<input type="text" name="' + prefix + 'fullname" value="' + name + '" readonly maxlength="200" class="input-wrp" id="id_' + prefix + 'fullname">'
             +       '<input type="hidden" name="' + prefix + 'id"' + text_replace + ' class="input-wrp" id="id_' + prefix + 'id">'
             +   '</div>'
             +   '<div class="bottom-line">'
             +      '<div class="lst-date-birth">'
             +           '<input type="text" name="' + prefix + 'date_of_birth" value="' + date_of_birth + '" readonly class="input-wrp" id="id_' + prefix + 'date_of_birth">'
             +       '</div>'
             +       '<div class="lst-phone">'
             +           '<input type="text" name="' + prefix + 'phone" value="' + phone + '" readonly maxlength="40" class="input-wrp" id="id_' + prefix + 'phone">'
             +       '</div>'
             +   '</div>'
             +'</div>'
             + '<div class="field-container">'
             +   '<div class="top-line">'
             +       '<div class="lst-type">'
             +           relations
             +       '</div>'
             +   '</div>'
             +   '<div class="bottom-line">'
             +       '<div class="lst-posada">'
             +           '<input type="text" name="' + prefix + 'workplace" value="' + posada + '" readonly maxlength="90" class="input-wrp" id="id_' + prefix + 'workplace">'
             +       '</div>'
             +  '</div>'
             + '</div>'
             + '<div class="field-container">'
             +   '<div class="lst-work">'
             +       '<textarea name="' + prefix + 'work" cols="None" rows="None" readonly maxlength="250" class="input-wrp" id="id_' + prefix + 'work">' + work + '</textarea>'
             +   '</div>'
             + '</div>'
             + '<div class="field-container hidden">'
             +   '<div class="lst-address">'
             +       '<textarea name="' + prefix + 'address" cols="40" rows="10" readonly maxlength="250" class="input-wrp" id="id_' + prefix + 'address">' + address + '</textarea>'
             +   '</div>'
             + '</div>'
             + '<div class="field-container">'
             +   '<div class="lst-change">'
             +       '<a href="#" class="change-parent-info">Змінити</a>'
             +       '<a href="#" class="delete-parent-info">Вилучити</a>'
             +       '<input type="checkbox" name="' + prefix + 'DELETE" id="id_' + prefix + 'DELETE">'
             +   '</div>'
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

function get_ajax_data(json_def, target_element) {
        let child_slug = $('#child-slug').attr('data-slug');

        let data = {
            json_query: true,
            json_def: json_def
        };

        let returned_data = {};

        $.ajax({
            type: "GET",
            url: '/child/' + child_slug + '/',
            dataType: 'json',
            data: data,
            success: function (data) {
                if (data) {
                    let target_items = $('.' + target_element),
                    $item_ul    = $('<ul class="select">'),
                    $item_select_value = $('<div class="select-value" data-value="">Оберіть відношення</div>'),
                    $item_select_wrapper = $('<div class="select-item-wrapper">'),
                    ajax_list = data.list;

                    for (let i=0; i<ajax_list.length; i++) {
                        let current_elem = ajax_list[i];
                        $('<li class="select-item"></li>').attr("value", current_elem["id"]).text(current_elem["name"]).appendTo($item_select_wrapper);
                    }

                    $item_ul.append($item_select_value).append($item_select_wrapper);
                    target_items.empty();
                    target_items.append($item_ul);
                    // for (let i=0; i<target_items.length; i++) {
                    //     target_items[i].append($item_ul);
                    // }
                }
            }
        });

        return returned_data;
    }

// function get_relation_list(target_element) {
//     let target_item = $('.' + target_element),
//         $item_ul    = $('<ul class="select" data-value="">'),
//         $item_select_value = $('<div class="select-value">Оберіть відношення</div>'),
//         $item_select_wrapper = $('<div class="select-item-wrapper">'),
//         ajax_list = get_ajax_data('relations');
//
//
//     for (var i=0; i<ajax_list.length; i++) {
//         let current_elem = ajax_list[i]
//         $('<li class="select-item"></li>').attr("value", current_elem["id"]).text(current_elem["name"]).appendTo($item_select_wrapper);
//     }
//
//     $item_ul.appendTo($item_select_value).appendTo($item_select_wrapper);
//     target_item.empty();
//     target_item.appendTo($item_ul);
//
// }


$( document ).ready(function() {

    daysBar();
    tabsToggle();
    get_ajax_data('relations', 'select-div');
    $('.cl-date-picker').datepicker();

    $(".birth-wrapper").birthdaypicker(options={"wrapper":"birth-wrapper"});

    $('.select-div').on('click', '.select', function (e) {
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
           last_id = 0;
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

        let form = $('#form-parent'),
            id = form.find('input[name="form-id"]').val(),
            select_value = $('.select-value').attr('data-value'),
            select_option = $('.select-item'),
            total_forms_tag = $('#id_parent-TOTAL_FORMS'),
            total_forms_val = +total_forms_tag.val() + 1,
            textHtml = '<select name="parent-' + id.replace(/lst-/g, "") + '-relation">';

        for (i=0; i<select_option.length; i++) {
           let current_elem = select_option[i];
           let current_value = current_elem.getAttribute('value');
           if (current_value === select_value) {
               textHtml += '<option value="' + current_value + '" selected>' + current_elem.innerText + '</option>'
           } else {
               textHtml += '<option value="' + current_value + '">' + current_elem.innerText + '</option>'
           }
        }

        textHtml += '</select>';

        let name = form.find('input[name="name"]').val(),
            date_of_birth = form.find('#birthdate').val(),
            phone = form.find('input[name="phone"]').val(),
            address = form.find('textarea[name="address"]').val(),
            work = form.find('textarea[name="work"]').val(),
            place = form.find('input[name="position"]').val(),
            operation_type = form.find('#operation-type').attr('data-type'),
            oper_numb = 0,
            parent_id = form.find('input[name="parent_id"]').val(),
            modal = $('.modal');

        if (operation_type === '1') {

            let new_item = returnParentHtml(id, name, date_of_birth, phone, work, place, textHtml, address, parent_id, true);
            $('.list-parents').append(new_item);
            total_forms_tag.attr('value', total_forms_val);
        } else {
            let new_item = returnParentHtml(id, name, date_of_birth, phone, work, place, textHtml, address, parent_id, false);
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

    $('.select-div').on('click', '.select-item', function (e) {

        let current = $(this);
        let radio_selected = $('.select-value');

        radio_selected.text(current.text());
        radio_selected.attr("data-value", current.attr("value"));

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
            relation = current_element.find('#' + 'id_parent-' + num_id + '-relation option:selected'),
            phone = current_element.find('#' + 'id_parent-' + num_id + '-phone').val(),
            address = current_element.find('#' + 'id_parent-' + num_id + '-address').val(),
            work = current_element.find('#' + 'id_parent-' + num_id + '-work').val(),
            workplace = current_element.find('#' + 'id_parent-' + num_id + '-workplace').val(),
            parent_id = current_element.find('#' + 'id_parent-' + num_id + '-id').val();


        clearForm();

        let form = $('#form-parent');
        let date_from_p = convertDate(date_of_birth);

        form.find('input[name="name"]').attr('value', fullname);
        form.find('input[name="name"]').val(fullname);
        form.find('#birthdate').attr('value', formatDate(date_from_p));
        form.find('#birthdate').val(formatDate(date_from_p));
        $(".birth-wrapper").birthdaypicker(options={"wrapper":"birth-wrapper", "defaultDate": formatDate(date_from_p)});
        form.find('input[name="phone"]').attr('value', phone);
        form.find('input[name="phone"]').val(phone);
        form.find('.select-value').attr('data-value', relation.val()).text(relation[0].innerText).addClass('value-inserted');
        form.find('textarea[name="work"]').val(work);
        form.find('input[name="position"]').attr('value', workplace);
        form.find('input[name="position"]').val(workplace);
        form.find('input[name="form-id"]').attr('value', id_parent);
        form.find('input[name="form-id"]').val(id_parent);
        form.find('input[name="parent_id"]').val(parent_id);
        form.find('input[name="parent_id"]').attr('value', parent_id);
        form.find('#operation-type').attr('data-type', '2');


         $('.modal').addClass('opened');


    });

    $('.list-parents').on('click', '.delete-parent-info',  function (e) {
        e.preventDefault();
        let current_element = $(this).closest('.lst-parent'),
            total_forms_tag = $('#id_parent-TOTAL_FORMS'),
            total_forms_val = +total_forms_tag.val() - 1;
        if (current_element.attr("data-operation") === "added") {
            total_forms_tag.val(total_forms_val);
        }
        current_element.find('input[id$=DELETE]').prop('checked', true);
        current_element.addClass('parent-deleted');
        current_element.attr('data-delete', 'true');
    });

    $('.button-wrapper').on('change', '#id_child-image', function (e) {
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


    // $('#save-child').on('click', function (e) {
    //     e.preventDefault();
    //
    //
    // });



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