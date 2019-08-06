const paymentParams = {};

function createPaymentParams(user, paymentModel, integrity_hash) {
  console.log(paymentModel.id);
}

function payWithRave(paymentParams) {
  let raveResponse = {};
  let x = getpaidSetup({
    PBFPubKey: paymentParams.PBFPubKey,
    amount: paymentParams.amount,
    currency: paymentParams.currency,
    custom_logo: paymentParams.custom_logo,
    custom_title: paymentParams.custom_title,
    customer_email: paymentParams.customer_email,
    customer_firstname: paymentParams.customer_firstname,
    customer_lastname: paymentParams.customer_lastname,
    pay_button_text: paymentParams.pay_button_text,
    payment_options: paymentParams.payment_options,
    payment_plan: paymentParams.payment_plan,
    txref: paymentParams.txref,
    redirect_url: paymentParams.redirect_url,
    integrity_hash: paymentParams.integrity_hash,
    onclose: function () {
      console.log(raveResponse);
      // window.location.href = 'http://localhost:8000/bla/'
    },
    callback: function (response) {
      let txref = response.tx.txRef; // collect txRef returned and pass to a server page to complete status check.
      raveResponse = response;
      console.log("This is the response returned after a charge", response);

      // send ajax post with response data to create transaction in db (regardless of
      // success or failure)
      // when ajax response is received (or when modal is closed):
      //    - redirect to paymentResponseReceivedView. If db transaction has already
      // been updated with response details, display template, else call rave verify
      // payment endpoint (using the txref that I add to the GET query params) and 
      // do a update_or_create db with response before displaying template
      // the template will include success.html or failure.html depending on 
      // transaction status. These templates are within django rave but can be
      // overriden by the user. The user will have access to the transaction object
      // in the template


      // if (
      //   response.tx.chargeResponseCode == "00" ||
      //   response.tx.chargeResponseCode == "0"
      // ) {
      //   // redirect to a success page
      //   console.log('here');
      //   // window.location.href = 'http://localhost:8000/bla/'
      // } else {
      //   // redirect to a failure page.
      //   console.log('there');
      // }

      // x.close(); // use this to close the modal immediately after payment.
    }
  });
}