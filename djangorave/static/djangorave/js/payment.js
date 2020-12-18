const paymentParams = {};  // paymentParams for each pay button on page


function makePayment(paymentParams) {
  FlutterwaveCheckout({
    ...paymentParams,
    callback: function (data) {
      // not currently used
    },
    onclose: function () {  // redirect to redirect_url when modal is closed
      window.location.href = paymentParams.redirect_url;
    },
  });
}