odoo.define('auth_signup_verify_email.auth_signup_verify', function (require) {
      "use strict";
      var ajax = require('web.ajax');

      $(document).on('click', "#validate", function () {
            const first = document.getElementById('first').value;
            const second = document.getElementById('second').value;
            const third = document.getElementById('third').value;
            const fourth = document.getElementById('fourth').value;
            const fifth = document.getElementById('fifth').value;
            const sixth = document.getElementById('sixth').value;
            const wrong = document.getElementById('wrong')
              const inputs = document.querySelector('#res');

            if (first === "" || second === "" || third === "" || fourth === "" || fifth === "" || sixth === "") {
                wrong.style.display = "block";
              }else{
                let sent_otp = first + second + third + fourth + fifth + sixth
                let email =$('#email');
                let emails= email[0].attributes['service'].value
                // console.log(emails)
                // console.log(sent_otp)
                            let wrongs = $("#wrongs")
                let ref ='ff'
                ajax.jsonRpc("/web/check_otp", 'call', {
                'email': emails,
                'otp': sent_otp,
                }).then(function (data) {
                    console.log("data", data)
                    if (data === "wrong"){
                    wrong.style.display = "block";

                    }else{
                        window.location.href = "/web";

                    }

                })

              }
          })
      $(document).on('click', "#resend", function () {
            const ok = document.getElementById('ok')
            ok.style.display = "block";
            let oks = $("#ok")
            ajax.jsonRpc("/web/send_otps", 'call', {
                }).then(function (data) {
                    console.log("send_otps", data)
                    oks.delay(2000).fadeOut(800)


                })
          //                           <span>omar adel omar moaed</span>
          // class="rounded-lg"

      })
})


