# Django Rave

## Project Description

This project provides Django integration for [Flutterwave](https://flutterwave.com/) Rave Card payments and subscriptions.

Current functionality:
- Allow users to make payments (once off and subscription)
- Create payment buttons which launch Rave payment modals
- Maintain a transaction history linked to users

# Requirements

- Python >= 3.6
- Django >= 2.0

# Installation

```bash
pip install djangorave
```

# Setup

Add `"djangorave"` to your `INSTALLED_APPS`

Run Django migrations:

```python
manage.py migrate
```

Add the following to your `settings.py`:

```python
RAVE_PRODUCTION_PUBLIC_KEY = "your key"
RAVE_PRODUCTION_SECRET_KEY = "your key"
RAVE_SANDBOX_PUBLIC_KEY = "your key"
RAVE_SANDBOX_SECRET_KEY = "your key"
RAVE_SANDBOX = True
```

The above config will ensure `djangorave` uses your Rave sandbox. Once you are
ready to go live, set `RAVE_SANDBOX = False`

Add `djangorave` to your `urls.py`:

```python
path("djangorave/", include("djangorave.urls", namespace="djangorave"))
```

Add the following url as a webhook in your Rave dashboard. This will be used by
Rave to `POST` payment transactions to your site:

```bash
http://yoursite.com/djangorave/transaction/
```

`Note:` while in development, a tool like ngrok (or similar) may prove useful.

# Usage

`djangorave` provides two models, namely:

- The `DRPaymentTypeModel` allows you to create `once off` or `recurring` payment types. When creating a `recurring` payment type, ensure the `payment_plan` field
corresponds to the Rave `Plan ID`.
- The `DRTransactionModel` creates transactions when Rave POSTS to the above mentioned webhook url. This provides a history of all transactions (once off or recurring), linked to the relevant `DRPaymentTypeModel` and `user`.

A payment button can be created as follows:

1. Create a new `PaymentType` using the django admin.
2. In the view where you wish the button to appear, add the above created `PaymentType` to your context, eg:

```python
from djangorave.models import DRPaymentTypeModel

class SignUpView(TemplateView):
    """Sign Up view"""

    template_name = "my_payment_template.html"

    def get_context_data(self, **kwargs):
        """Add payment type to context data"""
        kwargs = super().get_context_data(**kwargs)
        kwargs["pro_plan"] = DRPaymentTypeModel.objects.filter(
            description="Pro Plan"
        ).first()
        return kwargs
```

3. In your template, add your button wherever you wish for it to appear as follows:

```python
{% include 'djangorave/pay_button.html' with payment_model=pro_plan %}
```

`Note:` You can add multiple buttons to a single template by simply adding multiple
plans to your context data and then including each of them with their own `include`
tag as above.

4. Add the following script to your django base template (or anywhere in your template heirarchy that ensures it is loaded before your payment buttons):

```html
<script src="{% static 'djangorave/js/payment.js' %}"></script>
```

# Button Styling

The following css classes are available for styling your payment buttons:

- `rave-pay-btn` will apply to all buttons.
- `rave-subscription-btn` will apply to recurring payment types (ie: those with a `payment_plan`).
- `rave-onceoff-btn` will apply to once off payment types (ie: those without a `payment_plan`).

# Transaction Detail Page

Following a user payment, they will be redirected to the transaction detail page
located at `/djangorave/<str:reference>/`

A default transaction detail template is already available, however if you want
to override it, you may do so by creating a new template in your root
templates directory, ie: `/templates/djangorave/transaction.html`

You will have access to `{{ transaction }}` within that template.

# Development

If you wish to contribute to the project, there is an example app that demonstrates
general usage.

### Running the example:

```bash
git clone https://github.com/bdelate/django-rave.git
cd django-rave
make build
make migrate
make import
make dup
```

There is a section at the bottom of `django-rave/example/example/settings.py`. Ensure the values are set accordingly:

```python
RAVE_PRODUCTION_PUBLIC_KEY = "your key"
RAVE_PRODUCTION_SECRET_KEY = "your key"
RAVE_SANDBOX_PUBLIC_KEY = "your key"
RAVE_SANDBOX_SECRET_KEY = "your key"
RAVE_SANDBOX = True
```

Flutterwave Rave requires payments to be associated with users who have an email address.
Therefore, create and login with a new django user or use the existing user already
generated following the above import command:

```
username: testuser
password: secret
```

Navigate to http://localhost:8000/