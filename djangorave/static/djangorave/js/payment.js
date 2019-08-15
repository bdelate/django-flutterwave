const paymentParams = {};  // paymentParams for each pay button on page

function payWithRave(paymentParams) {
  let x = getpaidSetup({
    //
    // Rave params
    //
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
      //
      // navigate to redirect url when user closes modal
      //
      window.location.href = paymentParams.redirect_url;
    },

    callback: function (response) {
      //
      // Callback can optionally be used when response is received from Rave
      //
    }
  });
}