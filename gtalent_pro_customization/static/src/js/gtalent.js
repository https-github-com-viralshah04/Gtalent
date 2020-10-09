odoo.define('gtalent_pro_customization.gtalent', function (require) {
    var rpc = require('web.rpc');
    $(document).ready(function(){

//    console.log("In js")
       $('#btnAdd').on('click', function(event){
             var ddl = document.getElementById("degree");
       var option = document.createElement("OPTION");
       option.innerHTML = document.getElementById("degree_name").value;
       ddl.options.add(option);
       value = {
       'degree_name': document.getElementById("degree_name").value
       }
       $.ajax({
            url : '/add/degree/name',
            data : value
            })
})

$('#btnAdd_educational_institute').on('click', function(event){
             var educational_institute = document.getElementById("institute");
       var option_education = document.createElement("OPTION");
       console.log("educational_institute: ",educational_institute)
       console.log("option: ",option_education)

  option_education.innerHTML = document.getElementById("educational_institute").value;
       educational_institute.options.add(option_education);
       value = {
       'educational_institute': document.getElementById("educational_institute").value
       }
       $.ajax({
            url : '/add/educational/institute',
            data : value
            })
})

    $('#candidatetype').on('change', function() {
      if (this.value == 'fresher')
      {
        $(".workexp").hide();
      }
      else
      {
        $(".workexp").show();
      }
    });


     $('.degree').change(function(event)
         {
            var degree = document.getElementById("degree")
         })

    $('#job_application_form,#job_application_form2').click(function(event) {

		    var job_id = event.currentTarget.attributes.custom_job_id.value

            $.ajax({
                   url: '/check_login',
                   data: {},
                   success: function(data){
                        var res = JSON.parse(data) ;
                        if (res['is_user_logged_in'] == false)
                        {

                            swal({
                                  title: "Warning",
                                  text: "Sorry you won't be able to apply for this job without registration!",
                                  icon: "warning",
                                  buttons: true,
                                  dangerMode: true,
                                },(willDelete) => {
                                  if (willDelete) {
                                    window.location = '/web/login'
                                  }
                                })
                        }
                        else if (res['is_user_logged_in'] == true)
                        {
                            window.location = '/jobs/apply/' + job_id
                        }
                   }
            });

        });



if (window.location.href.indexOf('/applicant/profile') > 0)
{
    $.ajax({
            url: '/get_applicant_details',
            data: {},
            success: function(data)
            {
                var result = JSON.parse(data);
                if(result)
                {
                    $("#gender").val(result['gender'])
                    $("#nationality").val(result['nationality'])
                    $("#candidate_type").val(result['candidate_type'])
//                    $("#category").val(result['category'])
                    $("#blood_group").val(result['blood_group'])
                }
            }
    });
    
    $("#employment_start_date, #employment_end_date").datepicker({
        changeMonth: true,
        changeYear: true,
        firstDay: 1,
        dateFormat: 'dd/mm/yy',
    })

    $("#employment_start_date").datepicker({ dateFormat: 'dd-mm-yy' });
    $("#employment_end_date").datepicker({ dateFormat: 'dd-mm-yy' });

    $('#employment_end_date').change(function() {
        var start = $('#employment_start_date').datepicker('getDate');
        var end   = $('#employment_end_date').datepicker('getDate');

        if (start < end) {
            var days = (end - start)/1000/60/60/24;
            $('#employment_duration').val(days);
        }
        else {
          $('#employment_start_date').val("");
          $('#employment_end_date').val("");
          $('#employment_duration').val("");
        }
    });

    
    if ($('.personal-details').length) {
        var state_options = $("select[name='state_id']:enabled option:not(:first)");
        $('.personal-details').on('change', "select[name='country_id']", function () {
            var select = $("select[name='state_id']");
            state_options.detach();
            var displayed_state = state_options.filter("[data-country_id="+($(this).val() || 0)+"]");
            var nb = displayed_state.appendTo(select).show().length;
            if (nb == 0)
            {
                $(".state_province_data").hide();
            }
            else
            {
                $(".state_province_data").show();
            }
            select.parent().toggle(nb>=1);
        });
        $('.personal-details').find("select[name='country_id']").change();
    }

    $('#aadhar_number').keypress(function(){
         var rawNumbers = $(this).val().replace(/-/g,'');
         var cardLength = rawNumbers.length;
         if(cardLength !==0 && cardLength <=14 && cardLength % 4 == 0){
           $(this).val($(this).val()+'-');
         }
        });

    if ($('#add_education_details').length) {
        var state_options = $("select[name='state_id']:enabled option:not(:first)");
        $('#add_education_details').on('change', "select[name='country_id']", function () {
            var select = $("select[name='state_id']");
            state_options.detach();
            var displayed_state = state_options.filter("[data-country_id="+($(this).val() || 0)+"]");
            var nb = displayed_state.appendTo(select).show().length;
            if (nb == 0)
            {
                $(".state_province_data").hide();
            }
            else
            {
                $(".state_province_data").show();
            }
            select.parent().toggle(nb>=1);
        });
        $('#add_education_details').find("select[name='country_id']").change();
    }



    $('.tab-pane').click(function(){
        var active_tab=$(this).attr('id');
//        alert($("#my_file").val())
        if (active_tab != 'nav-home')
        {
            $.ajax({
            url: '/save/profile',
            data: {
                     'save_personal_details':true,
                     'applicant_name': $("#applicant_name").val(),
                     'email': $("#email").val(),
                     'birth_date' : $("#birth_date").val(),
                     'phone' : $("#phone").val(),
                     'aadhar_number' : $("#aadhar_number").val(),
                     'voter_id' : $("#voter_id").val(),
                     'source' : $("#source").val(),
                     'uploaded_by' : $("#uploaded_by").val(),
                     'visa_information' : $("#visa_information").val(),
                     'street' : $("#street").val(),
                     'street2' : $("#street2").val(),
                     'city' : $("#city").val(),
                     'zip' : $("#zip").val(),
                     'country_id' : $("#country_id").val(),
                     'state_id' : $("#state_id").val(),
                     'gender' : $("#gender").val(),
                     'nationality' : $("#nationality").val(),
                     'candidate_type' : $("#candidate_type").val(),
                     'category' : $("#category").val(),
                     'blood_group' : $("#blood_group").val(),
                     'social_twitter_acc' : $("#social_twitter_acc").val(),
                     'social_facebook_acc' : $("#social_facebook_acc").val(),
                     'social_github_acc' : $("#social_github_acc").val(),
                     'social_linkedin_acc' : $("#social_linkedin_acc").val(),
                     'social_youtube_acc' : $("#social_youtube_acc").val(),
                     'social_googleplus_acc' : $("#social_googleplus_acc").val(),
                     'social_instagram_acc' : $("#social_instagram_acc").val(),
//                     'myfile' : $("#my_file").val(),
            },
            success: function(data)
            {
                        var result = JSON.parse(data);
                        if(result)
                        {
                            console.log('DETAILS SAVED')
                        }
                    }
            });
        }
    });

    var d = new Date();
    var current_year = d.getFullYear()

    if ($('#applicant_name').length){

        for (var i = current_year; i > 1900; i--)
        {
            $('#degree_start_year').append($('<option />').val(i).html(i));
            $('#degree_end_year').append($('<option />').val(i).html(i));
            $('#update_degree_start_year').append($('<option />').val(i).html(i));
            $('#update_degree_end_year').append($('<option />').val(i).html(i));
            // $('#update_degree_start_month').append($('<option />').val(i).html(i));
            // $('#update_degree_end_month').append($('<option />').val(i).html(i));
            $('#award_year').append($('<option />').val(i).html(i));
            $('#update_award_year').append($('<option />').val(i).html(i));
        }
    }

    $(".aadhar_card_div").hide()
    $(".voter_id_div").hide()
    $(".other_name_div").hide()
    $(".degree_other_name_div").hide()
    $(".colleage_other_name_div").hide()
    $(".degree_other_name_div").hide()
    $(".other_company_name_div").hide()
    $(".div_degree_percentage").hide()
    $(".div_degree_cga").hide()

    $('#degree_end_year').click(function()
    {
        if (($('#degree_end_year').val()) < ($('#degree_start_year').val()))
        {
            swal('Warning', 'End Date should not be less than Start Date.');
            $('#degree_end_year').val('')
        }
    });

    $('#update_degree_end_year').click(function()
    {
        if (($('#update_degree_end_year').val()) < ($('#update_degree_start_year').val()))
        {
            swal('Warning', 'End Date should not be less than Start Date.');
            $('#update_degree_end_year').val('')
        }
    });

    $('#category').click(function()
    {
        var category = $("#category").val()
        if(category == 'aadharcard')
        {
            $(".aadhar_card_div").show()
            $(".voter_id_div").hide()
        }
        if(category == 'votterid')
        {
            $(".voter_id_div").show()
            $(".aadhar_card_div").hide()
        }
    });

    $('#score_type').click(function()
    {
        var score_type = $("#score_type").val()
        if(score_type == 'percentage')
        {
            $(".div_degree_percentage").show()
        }
        if(score_type == 'cgpa')
        {
            $(".div_degree_cga").show()
        }
    });

    $('#degree_type_id').click(function()
    {
        var degree_type_id = $("#degree_type_id").val()
        if(degree_type_id == 'other')
        {
            $(".other_name_div").show()
        }
        else{
            $(".other_name_div").hide()
        }
    });

    $('#degree').click(function()
    {
        var degree = $("#degree").val()
        if(degree == 'other')
        {
            $(".degree_other_name_div").show()
        }
        else{
            $(".degree_other_name_div").hide()
        }
    });

    $('#institute').click(function()
    {
        var institute = $("#institute").val()
        if(institute == 'other')
        {
            $(".colleage_other_name_div").show()
        }
        else{
            $(".colleage_other_name_div").hide()
        }
    });

    $('#company_name').click(function()
    {
        var company_name = $("#company_name").val()
        if(company_name == 'other')
        {
            $(".other_company_name_div").show()
        }
        else{
            $(".other_company_name_div").hide()
        }
    });

    $('#current_employer').click(function()
    {
        if ($('#current_employer').prop("checked") == true )
        {
            $('.employment_end_date').hide()
            $('.employment_duration').hide()
        }
        if ($('#current_employer').prop("checked") == false )
        {
            $('.employment_end_date').show()
            $('.employment_duration').show()
        }
    });

    $('#update_current_employer').click(function()
    {
        if ($('#update_current_employer').prop("checked") == true )
        {
            $('.update_employment_end_date').hide()
        }
        if ($('#update_current_employer').prop("checked") == false )
        {
            $('.update_employment_end_date').show()
        }
    });

    $('#candidate_type').click(function()
    {
        if($("#candidate_type").val() == 'fresh')
        {
            $(".candiate_experience").hide()
            $("#candidate_exp").val('')
        }
        if($("#candidate_type").val() != 'fresh')
        {
            $(".candiate_experience").show()
        }
    });

    $('#phone').keyup(function() {
          if (this.value.match(/[^0-9]/g)) {
         this.value = this.value.replace(/[^0-9]/g, '');
        }
    });

    // $('#aadhar_number').keyup(function() {
    //       if (this.value.match(/[^0-9]/g)) {
    //      this.value = this.value.replace(/[^0-9]/g, '');
    //     }
    // });

    $('#zip').keyup(function() {
          if (this.value.match(/[^0-9]/g)) {
         this.value = this.value.replace(/[^0-9]/g, '');
        }
    });


    $("#update_degree_percentage").change(function()
    {
        var num = $("#update_degree_percentage").val();
        if (num != '')
        {
            var n = parseFloat(num).toFixed(2);
            document.getElementById("update_degree_percentage").value = n;
        }
    });


    $("#degree_percentage").change(function()
    {
        var num = $("#degree_percentage").val();
        if (num != '')
        {
            var n = parseFloat(num).toFixed(2);
            document.getElementById("degree_percentage").value = n;
        }
    });

    $('.submit_update_applicant').click(function()
    {
        var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
        var email = $("#email").val();
        if (regex.test(email) == false)
        {
            swal('Warning', 'Please Enter a valid email id.');
            return false;
        }

        if(($("#social_instagram_acc").val() == '') && ($("#social_github_acc").val() == '') && ($("#social_linkedin_acc").val() == '') && ($("#social_youtube_acc").val() == '') && ($("#social_googleplus_acc").val() == '') && ($("#social_facebook_acc").val() == '') && ($("#social_twitter_acc").val() == ''))
        {
             swal('Warning', 'Please update any one of the social media account detail.');
            return false
        }
    });


    $('.delete_employment_record').click(function(event)
    {
        swal({
              title: "Warning",
              text: "Are you sure you want to delete this record?",
              icon: "warning",
              buttons: ["No", "Yes"],
              dangerMode: true,
            },(willDelete) => {
              if (willDelete)
              {
                var employment_id = event.currentTarget.attributes.custom_employment_id.value
                $.ajax({
                        url: '/delete_applicant_employment',
                        data: {'employment_id':employment_id},
                        success: function(data)
                        {
                            window.location.reload();
                        }
                });
              }
            })
    });


    $('.delete_assessment_record').click(function(event)
    {
        swal({
              title: "Warning",
              text: "Are you sure you want to delete this record?",
              icon: "warning",
              buttons: ["No", "Yes"],
              dangerMode: true,
            },(willDelete) => {
              if (willDelete)
              {
                var record_id = event.currentTarget.attributes.custom_assessment_id.value
                $.ajax({
                        url: '/delete_applicant_assessment',
                        data: {'record_id':record_id},
                        success: function(data)
                        {
                            window.location.reload();
                        }
                });
              }
            })
    });


    $('.delete_skill_record').click(function(event)
    {
        swal({
              title: "Warning",
              text: "Are you sure you want to delete this record?",
              icon: "warning",
              buttons: ["No", "Yes"],
              dangerMode: true,
            },(willDelete) => {
              if (willDelete)
              {
                var record_id = event.currentTarget.attributes.custom_skill_id.value
                $.ajax({
                        url: '/delete_applicant_skill',
                        data: {'record_id':record_id},
                        success: function(data)
                        {
                            window.location.reload();
                        }
                });
              }
            })
    });

    $('.delete_hobbies_record').click(function(event)
    {
        swal({
              title: "Warning",
              text: "Are you sure you want to delete this record?",
              icon: "warning",
              buttons: ["No", "Yes"],
              dangerMode: true,
            },(willDelete) => {
              if (willDelete)
              {
                var record_id = event.currentTarget.attributes.custom_hobbies_id.value
                $.ajax({
                        url: '/delete_applicant_hobbies',
                        data: {'record_id':record_id},
                        success: function(data)
                        {
                            window.location.reload();
                        }
                });
              }
            })
    });

    $('.delete_project_record').click(function(event)
    {
        swal({
              title: "Warning",
              text: "Are you sure you want to delete this record?",
              icon: "warning",
              buttons: ["No", "Yes"],
              dangerMode: true,
            },(willDelete) => {
              if (willDelete)
              {
                var record_id = event.currentTarget.attributes.custom_project_id.value
                $.ajax({
                        url: '/delete_applicant_project',
                        data: {'record_id':record_id},
                        success: function(data)
                        {
                            window.location.reload();
                        }
                });
              }
            })
    });


    $('.delete_shared_doc_record').click(function(event)
    {
        swal({
              title: "Warning",
              text: "Are you sure you want to delete this record?",
              icon: "warning",
              buttons: ["No", "Yes"],
              dangerMode: true,
            },(willDelete) => {
              if (willDelete)
              {
                var record_id = event.currentTarget.attributes.custom_shared_doc_id.value
                $.ajax({
                        url: '/delete_applicant_shared_doc',
                        data: {'record_id':record_id},
                        success: function(data)
                        {
                            window.location.reload();
                        }
                });
              }
            })
    });

    $('.delete_course_record').click(function(event)
    {
        swal({
              title: "Warning",
              text: "Are you sure you want to delete this record?",
              icon: "warning",
              buttons: ["No", "Yes"],
              dangerMode: true,
            },(willDelete) => {
              if (willDelete)
              {
                var record_id = event.currentTarget.attributes.custom_course_id.value
                $.ajax({
                        url: '/delete_applicant_course',
                        data: {'record_id':record_id},
                        success: function(data)
                        {
                            window.location.reload();
                        }
                });
              }
            })
    });


    $('.delete_certificate_record').click(function(event)
    {
        swal({
              title: "Warning",
              text: "Are you sure you want to delete this record?",
              icon: "warning",
              buttons: ["No", "Yes"],
              dangerMode: true,
            },(willDelete) => {
              if (willDelete)
              {
                var record_id = event.currentTarget.attributes.custom_certificate_id.value
                $.ajax({
                        url: '/delete_applicant_certificate',
                        data: {'record_id':record_id},
                        success: function(data)
                        {
                            window.location.reload();
                        }
                });
              }
            })
    });

    $('.delete_award_record').click(function(event)
    {
        swal({
              title: "Warning",
              text: "Are you sure you want to delete this record?",
              icon: "warning",
              buttons: ["No", "Yes"],
              dangerMode: true,
            },(willDelete) => {
              if (willDelete)
              {
                var record_id = event.currentTarget.attributes.custom_award_id.value
                $.ajax({
                        url: '/delete_applicant_award',
                        data: {'record_id':record_id},
                        success: function(data)
                        {
                            window.location.reload();
                        }
                });
              }
            })
    });

    $('.delete_education_record').click(function(event)
    {
        swal({
              title: "Warning",
              text: "Are you sure you want to delete this record?",
              icon: "warning",
              buttons: ["No", "Yes"],
              dangerMode: true,
            },(willDelete) => {
              if (willDelete)
              {
                var record_id = event.currentTarget.attributes.custom_education_id.value
                $.ajax({
                        url: '/delete_applicant_education',
                        data: {'record_id':record_id},
                        success: function(data)
                        {
                            window.location.reload();
                        }
                });
              }
            })
    });

    $('.view_employment_record').click(function(event)
    {
    var employment_id = event.currentTarget.attributes.custom_employment_id.value
    $.ajax({
                url: '/get_applicant_employment_details',
                data: {'employment_id':employment_id},
                success: function(data)
                {
                    var result = JSON.parse(data);
                    if(result)
                    {
                        $("#view_applicant_employment_id").val(employment_id)
                        $("#view_company_name").val(result['company_name'])
                        $("#view_designation_type_id").val(result['designation_type_id'])
                        $("#view_department_type_id").val(result['department_type_id'])
                        $("#view_employment_start_date").val(result['employment_start_date'])
                        $("#view_employment_end_date").val(result['employment_end_date'])
                        $("#view_deliverables").val(result['deliverables'])
                        $("#view_job_summary").val(result['job_summary'])
                        $("#view_job_accomplishments").val(result['job_accomplishments'])
                    }
                }
        })
    });
    
    $('.update_employment_record').click(function(event)
    {
		var employment_id = event.currentTarget.attributes.custom_employment_id.value
		$.ajax({
                url: '/get_applicant_employment_details',
                data: {'employment_id':employment_id},
                success: function(data)
                {
                    var result = JSON.parse(data);
                    if(result)
                    {
                        $("#applicant_employment_id").val(employment_id)
                        $("#update_company_name").val(result['company_name'])
                        $("#update_designation_type_id").val(result['designation_type_id'])
                        $("#update_department_type_id").val(result['department_type_id'])
                        $("#update_employment_start_date").val(result['employment_start_date'])
                        $("#update_employment_end_date").val(result['employment_end_date'])
                        $("#update_deliverables").val(result['deliverables'])
                        $("#update_job_summary").val(result['job_summary'])
                        $("#update_job_accomplishments").val(result['job_accomplishments'])
                    }
                }
        })
    });

    $('.update_hobbies_record').click(function(event)
    {
		var record_id = event.currentTarget.attributes.custom_hobbies_id.value
		$.ajax({
                url: '/get_applicant_hobbies_details',
                data: {'record_id':record_id},
                success: function(data)
                {
                    var result = JSON.parse(data);
                    if(result)
                    {
                        $("#applicant_hobbies_id").val(record_id)
                        $("#update_hobby_name").val(result['name'])
                        $("#update_hobbies_comments").val(result['hobbies_comments'])
                        $("#update_hobbies_achievements").val(result['hobbies_achievements'])
                    }
                }
        })
    });

    $('.update_shared_doc_record').click(function(event)
    {
		var record_id = event.currentTarget.attributes.custom_shared_doc_id.value
		$.ajax({
                url: '/get_applicant_shared_details',
                data: {'record_id':record_id},
                success: function(data)
                {
                    var result = JSON.parse(data);
                    if(result)
                    {
                        $("#applicant_shared_details_id").val(record_id)
                        $("#update_shared_company").val(result['shared_company'])
                        $("#update_stage_status").val(result['stage_status'])
                        $("#update_shared_date").val(result['shared_date'])
                    }
                }
        })
    });

    $('.update_project_record').click(function(event)
    {
		var record_id = event.currentTarget.attributes.custom_project_id.value
		$.ajax({
                url: '/get_applicant_project_details',
                data: {'record_id':record_id},
                success: function(data)
                {
                    var result = JSON.parse(data);
                    if(result)
                    {
                        $("#applicant_project_id").val(record_id)
                        $("#update_project_name").val(result['name'])
                        $("#update_industry").val(result['industry'])
                        $("#update_project_for").val(result['project_for'])
                        $("#update_impact").val(result['impact'])
                        $("#update_guided_by").val(result['guided_by'])
                        $("#update_project_summary").val(result['project_summary'])
                        $("#update_project_accomplishments").val(result['project_accomplishments'])
                        $("#update_team_size").val(result['team_size'])
                        $("#update_project_start_date").val(result['project_start_date'])
                        $("#update_project_end_date").val(result['project_end_date'])
                        $("#update_project_duration").val(result['project_duration'])
                        $("#update_project_link").val(result['project_link'])
                        $("#update_technology").val(result['technology'])
                    }
                }
        })
    });

    $('.update_education_record').click(function(event)
    {
		var record_id = event.currentTarget.attributes.custom_education_id.value
		$.ajax({
                url: '/get_applicant_education_details',
                data: {'record_id':record_id},
                success: function(data)
                {
                    var result = JSON.parse(data);
                    if(result)
                    {
                        $("#applicant_education_id").val(record_id)
                        $("#update_degree_type_id").val(result['degree_type_id'])
                        $("#update_degree").val(result['degree_type'])
                        $("#update_institute").val(result['institute'])
                        $("#update_degree_class").val(result['degree_class'])
                        $("#update_country_id").val(result['country_id'])
                        $("#update_state_id").val(result['state_id'])
                        $("#update_degree_start_year").val(result['degree_start_year'])
                        $("#update_degree_end_year").val(result['degree_end_year'])
                        $("#update_degree_score").val(result['degree_score'])
                        $("#update_degree_percentage").val(result['degree_percentage'])
                    }
                }
        })
    });

    $('.update_assessment_record').click(function(event)
    {
		var record_id = event.currentTarget.attributes.custom_assessment_id.value
		$.ajax({
                url: '/get_applicant_assessment_details',
                data: {'record_id':record_id},
                success: function(data)
                {
                    var result = JSON.parse(data);
                    if(result)
                    {
                        $("#applicant_assessment_id").val(record_id)
                        $("#update_assessment_name").val(result['assessment_name'])
                        $("#update_assessment_description").val(result['assessment_description'])
                        $("#update_assessment_scores").val(result['assessment_scores'])
                        $("#update_vendor").val(result['vendor'])
                        $("#update_link").val(result['link'])
                        $("#update_assessment_date").val(result['assessment_date'])
                    }
                }
        })
    });

    $('.update_award_record').click(function(event)
    {
		var record_id = event.currentTarget.attributes.custom_award_id.value
		$.ajax({
                url: '/get_applicant_award_details',
                data: {'record_id':record_id},
                success: function(data)
                {
                    var result = JSON.parse(data);
                    if(result)
                    {
                        $("#applicant_award_id").val(record_id)
                        $("#update_award_name").val(result['award_name'])
                        $("#update_present_by").val(result['present_by'])
                        $("#update_award_year").val(result['award_year'])
                    }
                }
        })
    });

    $('.update_certificate_record').click(function(event)
    {
		var record_id = event.currentTarget.attributes.custom_certificate_id.value
		$.ajax({
                url: '/get_applicant_certificate_details',
                data: {'record_id':record_id},
                success: function(data)
                {
                    var result = JSON.parse(data);
                    if(result)
                    {
                        $("#applicant_certificate_id").val(record_id)
                        $("#update_certificate_name").val(result['certificate_name'])
                        $("#update_certificate_vendor").val(result['certificate_vendor'])
                        $("#update_certificate_id").val(result['certificate_id'])
                        $("#update_certificate_technology").val(result['certificate_technology'])
                        $("#update_certificate_level").val(result['certificate_level'])
                    }
                }
        })
    });

    $('.update_course_record').click(function(event)
    {
		var record_id = event.currentTarget.attributes.custom_course_id.value
		$.ajax({
                url: '/get_applicant_course_details',
                data: {'record_id':record_id},
                success: function(data)
                {
                    var result = JSON.parse(data);
                    if(result)
                    {
                        $("#applicant_course_id").val(record_id)
                        $("#update_course").val(result['course'])
                        $("#update_course_vendor").val(result['course_vendor'])
                        $("#update_course_technology").val(result['course_technology'])
                        $("#update_course_status").val(result['course_status'])
                        $("#update_course_start").val(result['course_start'])
                        $("#update_course_end").val(result['course_end'])
                    }
                }
        })
    });






}





if ((window.location.href.indexOf('/website/profile') > 0)){

        window.onscroll = function() {myFunction()};

        var header = document.getElementById("fixedheader");
        var sticky = header.offsetTop;

        function myFunction() {
          if (window.pageYOffset > sticky) {
            header.classList.add("sticky");
          } else {
            header.classList.remove("sticky");
          }
        }


        // Cache selectors
        var lastId,
              topMenu = $("#customtop-menu"),
            topMenuHeight = topMenu.outerHeight()+170,
            // All list items
            menuItems = topMenu.find("a"),
            // Anchors corresponding to menu items
            scrollItems = menuItems.map(function(){
              var item = $($(this).attr("href"));
              if (item.length) { return item; }
            });

        // Bind click handler to menu items
        // so we can get a fancy scroll animation
        menuItems.click(function(e){
          var href = $(this).attr("href"),
              offsetTop = href === "#" ? 0 : $(href).offset().top-topMenuHeight+1;
          $('html, body').stop().animate({scrollTop: offsetTop}, 1200);
          e.preventDefault();
        });

        // Bind to scroll
        $(window).scroll(function(){
           // Get container scroll position
           var fromTop = $(this).scrollTop()+topMenuHeight;

           // Get id of current scroll item
           var cur = scrollItems.map(function(){
             if ($(this).offset().top < fromTop)
               return this;
           });
           // Get the id of the current element
           cur = cur[cur.length-1];
           var id = cur && cur.length ? cur[0].id : "";

           if (lastId !== id) {
               lastId = id;
               // Set/remove active class
               menuItems
                 .parent().removeClass("active")
                 .end().filter("[href='#"+id+"']").parent().addClass("active");
           }
        });


}



readURL = function(input){
           if (input.files && input.files[0]) {
               var reader = new FileReader();

               reader.onload = function (e) {
                   $('#blah')
                       .attr('src', e.target.result);
               };

               reader.readAsDataURL(input.files[0]);
           }
       }


//$("#txtEditor").Editor();





        $('#job_partner_phone').keyup(function() {
              if (this.value.match(/[^0-9]/g)) {
             this.value = this.value.replace(/[^0-9]/g, '');
            }
        });








        if (window.location.href.indexOf('/web/signup') > 0)
        {
            if ($('.login_details').length) {
                console.log("login_details ---------------> ",$('.login_details').length)
                var state_options = $("select[name='state_id']:enabled option:not(:first)");
                console.log("state_options--------------> ",state_options)
                $('.login_details').on('change', "select[name='country_id']", function () {
                    var select = $("select[name='state_id']");
                    state_options.detach();
                    var displayed_state = state_options.filter("[data-country_id="+($(this).val() || 0)+"]");
                    var nb = displayed_state.appendTo(select).show().length;
                    if (nb == 0)
                    {
                        $(".state_province").hide();
                    }
                    else
                    {
                        $(".state_province").show();
                    }
                    select.parent().toggle(nb>=1);
                });
                $('.login_details').find("select[name='country_id']").change();
            }


            $('#medium_password').hide()
            $('#weak_password').hide()
            $('#strong_password').hide()
            $('#password').keyup(function(password) {
                var password = $("#password").val();
                // Must have capital letter, numbers and lowercase letters
//                const strongRegex = new RegExp('^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$', 'g');
                var strongRegex = /^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$/;
                // Must have either capitals and lowercase letters or lowercase and numbers
//                const mediumRegex = new RegExp('^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}$', 'g');
                var mediumRegex = /^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}$/;
                // ((?=.*[A-Z])(?=.*[a-z]))|((?=.*[A-Z])(?=.*[0-9]))|
                // Must be at least 6 characters long
//                const okRegex = new RegExp('^(?=.*?[a-z]).{8,}$', 'g');
                var okRegex = /^(?=.*?[a-z]).{8,}$/;
                if (okRegex.test(password) === false) {
                  // If ok regex doesn't match the password
                  // console.log('If ok regex doesn\'t match the password111');
                  $('#medium_password').hide()
                  $('#weak_password').show()
                  $('#strong_password').hide()
                  return 'Weak';
                } else if (strongRegex.test(password)) {
                  // If reg ex matches strong password
                  $('#medium_password').hide()
                  $('#weak_password').hide()
                  $('#strong_password').show()
                  return 'Strong';
                } else if (mediumRegex.test(password)) {
                  // If medium password matches the reg ex
                  $('#medium_password').show()
                  $('#weak_password').hide()
                  $('#strong_password').hide()
                  return 'Medium';
                } else {
                  // console.log('If ok regex doesn\'t match the password');
                  // If password is ok
                  $('#medium_password').hide()
                  $('#weak_password').show()
                  $('#strong_password').hide()
                  return 'Weak';
                }
              });


$('.flexdatalist-json').flexdatalist({
     searchContain: false,
     textProperty: '{capital}, {name}, {continent}',
     valueProperty: 'iso2',
     minLength: 1,
     focusFirstResult: true,
     selectionRequired: true,
     groupBy: 'continent',
     visibleProperties: ["name","continent","capital","capital_timezone"],
     searchIn: ["name","continent","capital"],
     data: 'countries.json'
});
          

          $('.custom-user-signup-candidate').click(function() {
            {
              var email = $('#login').val();
              var username = $('#name').val();
              var partner_mobile = $('#mobile').val();
              var candidate_birth_date = $('#date_of_birth').val();
              var current_designation = $('#qualification').val();
              var app_yrs_of_exp = $('#experience').val();
              var app_gender = $('#gender').val();
              var nationality = $('#nationality').val();
              var aadhar_number = $('#aadhar_number').val();
              var street = $('#street').val();
              var street2 = $('#street2').val();
              var city = $('#city').val();
              var zipcode = $('#zip').val();
              var country_id = $('#country_id').val();
              var state_id = $('#state_id').val();
              return rpc.query({
                      model: 'hr.applicant',
                      method: 'create_hr_applicant',
                      args: [this.id, email, username, partner_mobile,
                            candidate_birth_date, current_designation,
                            app_yrs_of_exp, app_gender, nationality,
                            aadhar_number, street, street2, city, zipcode, country_id, state_id],
                  }).then(function (result) {
                      this.data = result
                  });

            }

          });


            $('.custom-user-signup').click(function() {
                var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
                var email = $("#login").val();
                if (regex.test(email) == false)
                {
                    swal('Warning', 'Please Enter Valid Email Id');
                    return false;
                }

                if (window.location.href.indexOf('/web/signup?user_type=college') > 0)
                {
                    var placement_officer_email = $("#placement_officer_email").val();
                    if (regex.test(placement_officer_email) == false)
                    {
                        swal('Warning', 'Please Enter Valid Email Id for Placement Officer');
                        return false;
                    }

                    var placement_head_email = $("#placement_head_email").val();
                    if (regex.test(placement_head_email) == false)
                    {
                        swal('Warning', 'Please Enter Valid Email Id for Placement Head');
                        return false;
                    }
                }


                var password = $("#password").val();
                var okRegex = /^(?=.*?[a-z]).{8,}$/;
                if (okRegex.test(password) === false) {
                  $('#medium_password').hide()
                  $('#weak_password').show()
                  $('#strong_password').hide()
                  swal('Warning', 'Password must contain at least 8 characters, including at least 1 uppercase, 1 lowercase, 1 number and 1 special character.');
                  return false;
                }



            });

            $('#mobile').keyup(function() {
                  if (this.value.match(/[^0-9]/g)) {
                 this.value = this.value.replace(/[^0-9]/g, '');
                }
            });

            // $('#aadhar_number').keyup(function() {
            //       if (this.value.match(/[^0-9]/g)) {
            //      this.value = this.value.replace(/[^0-9]/g, '');
            //     }
            // });

            $('#placement_officer_mobile').keyup(function() {
                  if (this.value.match(/[^0-9]/g)) {
                 this.value = this.value.replace(/[^0-9]/g, '');
                }
            });

            $('#placement_head_mobile').keyup(function() {
                  if (this.value.match(/[^0-9]/g)) {
                 this.value = this.value.replace(/[^0-9]/g, '');
                }
            });


        }

    });
});
