# Django Flutterwave

## Project Description

This project provides Django integration for [Flutterwave](https://flutterwave.com/) payments and subscriptions.

Current functionality:

- Allow users to make payments (once off and subscription)
- Create payment buttons which launch inline payment modals
- Maintain a payment transaction history linked to users

# Requirements

- Python >= 3.6
- Django >= 2.0

# Installation

```bash
pip install djangoflutterwave
```

# Setup

Add `"djangoflutterwave"` to your `INSTALLED_APPS`

Run Django migrations:

```python
manage.py migrate
```

Add the following to your `settings.py`:

```python
FLW_PRODUCTION_PUBLIC_KEY = "your key"
FLW_PRODUCTION_SECRET_KEY = "your key"
FLW_SANDBOX_PUBLIC_KEY = "your key"
FLW_SANDBOX_SECRET_KEY = "your key"
FLW_SANDBOX = True
```

The above config will ensure `djangoflutterwave` uses your sandbox. Once you're ready to
go live, set `FLW_SANDBOX = False`

Add `djangoflutterwave` to your `urls.py`:

```python
path("djangoflutterwave/", include("djangoflutterwave.urls", namespace="djangoflutterwave"))
```

Add the following url as a webhook in your Flutterwave dashboard. This will be used by
Flutterwave to `POST` payment transactions to your site:

```bash
http://yoursite.com/djangoflutterwave/transaction/
```

`Note:` while in development, a tool like ngrok (or similar) may prove useful to ensure
your localhost is accessible to Flutterwave for the above webhook calls.

# Usage

`djangoflutterwave` provides two models, namely:

- The `FlwPlanModel` allows you to create `once off` or `subscription` plans. When creating a `subscription` plan, you will need to create the plan in Flutterwave first and then enter the corresonding information as a `FlwPlanModel` instance (ie: `flw_plan_id` field corresponds to the Flutterwave `Plan ID`).
- The `FlwTransactionModel` creates transactions when Flutterwave POSTS to the above mentioned webhook url. This provides a history of all transactions (once off or recurring), linked to the relevant `FlwPlanModel` and `user`.

A payment button can be created as follows:

1. Create a new plan (ie: `FlwPlanModel`) using the django admin.
2. In the view where you wish the button to appear, add the above created `FlwPlanModel` instance to your context, eg:

```python
from djangoflutterwave.models import FlwPlanModel

class SignUpView(TemplateView):
    """Sign Up view"""

    template_name = "my_payment_template.html"

    def get_context_data(self, **kwargs):
        """Add payment type to context data"""
        kwargs = super().get_context_data(**kwargs)
        kwargs["pro_plan"] = FlwPlanModel.objects.filter(
            name="Pro Plan"
        ).first()
        return kwargs
```

3. In your template, add the button wherever you wish for it to appear as follows:

```python
{% include 'djangoflutterwave/pay_button.html' with plan=pro_plan %}
```

`Note:` You can add multiple buttons to a single template by simply adding multiple
plans to your context data and then including each of them with their own `include`
tag as above.

4. Add the following to your django base template (or anywhere in your template heirarchy that ensures it is loaded before your payment buttons):

```html
<script
  type="text/javascript"
  src="https://checkout.flutterwave.com/v3.js"
></script>
<script src="{% static 'djangoflutterwave/js/payment.js' %}"></script>
```

# Button Styling

Use the `pay_button_css_classes` field on the `FlwPlanModel` model to add css classes to
buttons which will be rendered in your template.

# Transaction Detail Page

Following a user payment, they will be redirected to the transaction detail page
located at `/djangoflutterwave/<str:tx_ref>/`.

A default transaction detail template is already available, however if you want
to override it, you may do so by creating a new template in your root
templates directory, ie: `/templates/djangoflutterwave/transaction.html`

You will have access to `{{ transaction }}` within that template.

# API's and single page apps

As an alternative to rendering the above mentioned buttons in a django template, an API
end point is provided for retrieving payment params which can then be used in an API based app (eg: Vue, React).

End point: `djangoflutterwave/payment-params/?plan=nameofplanhere`

The above end point requires an authenticated user and will return the following:

```json
{
  "public_key": "flutterwave public key",
  "tx_ref": "transaction ref",
  "amount": 123.45,
  "currency": "USD",
  "payment_plan": 3453,
  "customer": {
    "email": "foo@bar.com",
    "name": "John Smith"
  },
  "customizations": {
    "title": "Pro Plan",
    "logo": "http://example.com/image.png"
  }
}
```

Below is a basic example of implementing Django Flutterwave into a Vue app:

```js
<template>
  <div>
    <button @click="makePayment">Sign up</button>
  </div>
</template>

<script>
import axios from "axios";
const token = localStorage.getItem("user-token") || "";
axios.defaults.headers.common["Authorization"] = `Token ${token}`;
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFToken";

export default {
  data() {
    return {
      params: {},
    };
  },
  mounted: function() {
    let flw = document.createElement("script");
    flw.setAttribute("src", "https://checkout.flutterwave.com/v3.js");
    flw.async = true;
    document.head.appendChild(flw);
  },
  created() {
    let params = axios.get("/djangoflutterwave/payment-params/?plan=proplan");
    this.params = params;
  },
  methods: {
    makePayment() {
      FlutterwaveCheckout({
        ...this.params,
        callback: function(data) {
          // This function is called after a successful payment. Add your code here.
        },
      });
    },
  },
};
</script>
```

The important points to note are:

- All initial setup is the same as per the above documentation.
- To call the end point, the user must be authenticated (ie: add their token).
- `https://checkout.flutterwave.com/v3.js` must be loaded as a script.
- A plan name is used to call the API end point which returns the payment params. Those payment params are then used in the `makePayment` method.
- There is a call back function which should be used to specify what to do after a
  payment has been completed.

# Development and contribution

If you wish to contribute to the project, there is an example app that demonstrates
general usage.

### Running the example:

```bash
git clone https://github.com/bdelate/django-flutterwave.git
cd django-flutterwave
```

Create file `example/env/dev.env` and populate it with the following:

```bash
FLW_SANDBOX_PUBLIC_KEY=your_sandbox_public_key
FLW_SANDBOX_SECRET_KEY=your_sandbox_secret_key
FLW_PRODUCTION_PUBLIC_KEY=test
FLW_PRODUCTION_SECRET_KEY=test
```

Run the following commands:

```bash
make build
make migrate
make import
make dup
```

Flutterwave requires payments to be associated with users who have an email address.
Therefore, create and login with a new django user or use the existing user which will
have been created by the above import command:

```
username: admin
password: adminadmin
```

Navigate to http://localhost:8000/
